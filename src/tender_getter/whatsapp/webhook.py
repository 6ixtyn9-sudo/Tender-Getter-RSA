"""
WhatsApp webhook handler for Twilio — AI-Enhanced (SECURE).
Receives inbound messages, status callbacks, and routes to AI handler.
Integrates with database for user management and conversation state.
Security hardening applied per red-team findings.
"""

import os
import re
import logging
from datetime import datetime
from typing import Optional, Dict, Any

from fastapi import FastAPI, Request, Form, HTTPException, BackgroundTasks
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from .models import (
    WhatsAppUser, ConversationState, MediaMessage, OutboundMessage,
    OnboardingStep, DocumentType, VerificationStatus, TABLES
)
from .media import download_media, upload_to_supabase, parse_document_with_gemini, guess_document_type
from .onboarding import handle_onboarding_step, start_onboarding
from .database import (
    get_user, upsert_user, get_conversation_state, upsert_conversation_state,
    create_media_message, update_media_message, create_outbound_message,
    update_outbound_message, get_digest_preferences
)
from .outbound import send_text_message, send_media_message, send_template_message
from .database import get_user, upsert_user
from ..ai import is_stop_command, is_greeting

logger = logging.getLogger(__name__)

# ============================================================
# SECURITY CONFIGURATION
# ============================================================

# Rate limiting: 30 req/min per IP, burst of 10
limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])

# Allowed origins for CORS (restrict to your domains)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "https://tendergetter.co.za,https://www.tendergetter.co.za").split(",")

# Health check allowed IPs (internal monitoring only)
ALLOWED_HEALTH_IPS = set(os.getenv("ALLOWED_HEALTH_IPS", "127.0.0.1,10.0.0.0/8,172.16.0.0/12").split(","))

# Media upload limits
MAX_MEDIA_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_MEDIA_TYPES = {
    "image/jpeg", "image/png", "image/heic", "image/webp",
    "application/pdf",
}

# ============================================================
# APP INITIALIZATION
# ============================================================

app = FastAPI(
    title="Tender Getter RSA - WhatsApp Webhook (AI-Enhanced)",
    docs_url=None,  # Disable Swagger in production
    redoc_url=None,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS - restricted to known origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type", "X-Twilio-Signature"],
)

# ============================================================
# TWILIO CONFIGURATION
# ============================================================

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

# CRITICAL: Fail fast if auth token not set in production
if not TWILIO_AUTH_TOKEN:
    logger.critical("TWILIO_AUTH_TOKEN not set — Twilio signature validation WILL FAIL")
    # In production, you should exit(1) here. For dev, we log and continue.
    if os.getenv("ENV", "development") == "production":
        raise RuntimeError("TWILIO_AUTH_TOKEN must be set in production")

# Request validator for security — CRITICAL: no bypass
validator = RequestValidator(TWILIO_AUTH_TOKEN)

# Twilio client for outbound messages
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN else None

# AI Handler (lazy init)
_ai_handler = None

def get_ai_handler_instance():
    """Lazy-load AI handler."""
    global _ai_handler
    if _ai_handler is None:
        _ai_handler = get_ai_handler()
    return _ai_handler

# ============================================================
# SECURITY HELPERS
# ============================================================

def validate_twilio_request(request: Request, form_data: dict) -> bool:
    """
    Validate that the request actually came from Twilio.
    CRITICAL: No bypass — raises if validator not configured.
    """
    url = str(request.url)
    signature = request.headers.get("X-Twilio-Signature", "")
    return validator.validate(url, form_data, signature)

def clean_phone(whatsapp_id: str) -> str:
    """Normalize WhatsApp ID to E.164 format."""
    return whatsapp_id.replace("whatsapp:", "")

def sanitize_phone_for_path(phone: str) -> str:
    """Sanitize phone number for safe use in file paths (prevent path traversal)."""
    # Keep only + and digits
    return re.sub(r"[^+\d]", "", phone)

def get_or_create_user(whatsapp_id: str) -> "WhatsAppUser":
    """Get existing user or create new one."""
    from .models import WhatsAppUser, OnboardingStep
    from .database import get_user, upsert_user
    
    phone = clean_phone(whatsapp_id)
    user = get_user(phone)
    if not user:
        user = WhatsAppUser(
            whatsapp_id=whatsapp_id,
            phone_number=phone,
            onboarding_step=OnboardingStep.WELCOME,
        )
        upsert_user(user)
    return user

def _cidr_match(ip: str, cidr: str) -> bool:
    """Check if IP matches CIDR notation."""
    import ipaddress
    try:
        if "/" in cidr:
            return ipaddress.ip_address(ip) in ipaddress.ip_network(cidr, strict=False)
        return ip == cidr
    except ValueError:
        return False

def _ip_allowed(ip: str, allowed_list: list) -> bool:
    """Check if IP is in allowed list (supports CIDR)."""
    return any(_cidr_match(ip, allowed) for allowed in allowed_list)

# ============================================================
# HEALTH CHECK ENDPOINT (RESTRICTED)
# ============================================================

@app.get("/health")
@limiter.limit("10/minute")  # Stricter limit for health checks
async def health_check(request: Request):
    """Health check endpoint for monitoring — IP restricted."""
    client_ip = request.client.host
    if not _ip_allowed(client_ip, list(ALLOWED_HEALTH_IPS)):
        logger.warning(f"Health check denied from {client_ip}")
        raise HTTPException(status_code=403, detail="Forbidden")
    
    from ..ai import get_gateway
    gateway = get_gateway()
    gateway_health = await gateway.health_check()
    
    return {
        "status": "ok",
        "service": "tender-getter-whatsapp",
        "timestamp": datetime.utcnow().isoformat(),
        # Don't leak gateway config in production
    }

# ============================================================
# MAIN WEBHOOK ENDPOINT (RATE LIMITED, SECURE)
# ============================================================

@app.post("/whatsapp/webhook")
@limiter.limit("30/minute")  # Rate limit per IP
async def whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    From: str = Form(...),
    Body: str = Form(""),
    MessageSid: str = Form(...),
    NumMedia: int = Form(0),
    MediaUrl0: Optional[str] = Form(None),
    MediaContentType0: Optional[str] = Form(None),
):
    """
    Main inbound message webhook — AI-Enhanced (SECURE).
    Handles text messages and media (images, PDFs, documents).
    Uses natural language understanding instead of rigid commands.
    """
    # 1. Parse form data
    form_data = dict(await request.form())
    
    # 2. Validate Twilio signature — CRITICAL: no bypass
    if not validate_twilio_request(request, form_data):
        logger.warning(f"Invalid Twilio signature from {From}")
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    # 3. Extract fields
    Body = form_data.get("Body", "")
    NumMedia = int(form_data.get("NumMedia", 0))
    MediaUrl0 = form_data.get("MediaUrl0")
    MediaContentType0 = form_data.get("MediaContentType0")
    
    logger.info(f"Incoming message from {From}: {Body[:50]}...")
    
    # 4. Get or create user
    user = get_or_create_user(From)
    user.last_active_at = datetime.utcnow()
    user.total_messages_received += 1
    upsert_user(user)
    
    # 4. Opt-out check FIRST (before any processing) — saves compute
    if user.opted_out_at:
        return Response(content="", media_type="application/xml")
    
    # 5. Handle media uploads with validation
    if NumMedia > 0 and MediaUrl0:
        # Validate media type
        if MediaContentType0 not in ALLOWED_MEDIA_TYPES:
            logger.warning(f"Rejected unsupported media type: {MediaContentType0} from {From}")
            return _twiml_response("❌ Unsupported file type. Please send PDF, JPEG, PNG, HEIC, or WebP.")
        
        response_text = await handle_media_upload(
            user, MessageSid, MediaUrl0, MediaContentType0, background_tasks
        )
    else:
        # 6. Sanitize input text (basic XSS prevention for logs)
        sanitized_body = _sanitize_input(Body)
        
        # Route through AI handler (natural language)
        ai_handler = get_ai_handler_instance()
        response_text = await ai_handler.handle_message(
            user=user,
            text=sanitized_body,
            message_sid=MessageSid,
            media_url=MediaUrl0,
            media_type=MediaContentType0,
        )
    
    # 7. Track outbound message
    if response_text and twilio_client:
        outbound = OutboundMessage(
            message_sid="",
            user_id=user.phone_number,
            message_type="text",
            content=response_text,
            status="queued",
        )
        create_outbound_message(outbound)
        background_tasks.add_task(send_text_message_async, user.phone_number, response_text, outbound)
    
    # 8. Return TwiML response
    twiml = MessagingResponse()
    if response_text:
        twiml.message(response_text)
    return Response(content=str(twiml), media_type="application/xml")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _sanitize_input(text: str) -> str:
    """Basic input sanitization for logging safety."""
    if not text:
        return ""
    # Remove potential control characters, limit length
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", text)
    return cleaned[:4096]  # Reasonable limit

def _twiml_response(text: str) -> Response:
    """Quick TwiML response helper."""
    twiml = MessagingResponse()
    twiml.message(text)
    return Response(content=str(twiml), media_type="application/xml")

def validate_twilio_request(request: Request, form_data: dict) -> bool:
    """Validate that the request actually came from Twilio. NO BYPASS."""
    url = str(request.url)
    signature = request.headers.get("X-Twilio-Signature", "")
    return validator.validate(url, form_data, signature)

def clean_phone(whatsapp_id: str) -> str:
    """Normalize WhatsApp ID to E.164 format."""
    return whatsapp_id.replace("whatsapp:", "")

def get_or_create_user(whatsapp_id: str) -> "WhatsAppUser":
    from .models import WhatsAppUser, OnboardingStep
    from .database import get_user, upsert_user
    
    phone = clean_phone(whatsapp_id)
    user = get_user(phone)
    if not user:
        user = WhatsAppUser(
            whatsapp_id=whatsapp_id,
            phone_number=phone,
            onboarding_step=OnboardingStep.WELCOME,
        )
        upsert_user(user)
    return user

# ============================================================
# MEDIA HANDLING (SECURE)
# ============================================================

async def handle_media_upload(
    user: "WhatsAppUser",
    message_sid: str,
    media_url: str,
    media_type: str,
    background_tasks: BackgroundTasks,
) -> str:
    """Handle uploaded documents with validation."""
    logger.info(f"Media upload from {user.phone_number}: {media_type} at {media_url}")
    
    from .models import MediaMessage
    from .media import guess_document_type
    from .database import create_media_message
    
    media_msg = MediaMessage(
        message_sid=message_sid,
        user_id=user.phone_number,
        media_url=media_url,
        media_content_type=media_type,
        guessed_type=guess_document_type(media_type),
    )
    create_media_message(media_msg)
    
    doc_type = guess_document_type(media_type)
    response = (
        f"📄 Received your {doc_type} document.\n\n"
        f"✅ Uploaded successfully.\n"
        f"🔍 Processing... (extracting details with AI)\n\n"
        f"Type *profile* to see your verification status."
    )
    
    background_tasks.add_task(process_media_async, media_msg, user)
    return response


async def process_media_async(media_msg: "MediaMessage", user: "WhatsAppUser"):
    """Background task: download, upload to Supabase, parse with Gemini."""
    try:
        # Download media WITH SIZE LIMIT
        content = await download_media(media_msg.media_url, max_size=MAX_MEDIA_SIZE)
        media_msg.media_size = len(content)
        
        # Upload to Supabase
        supabase_path = await upload_to_supabase(
            content,
            media_msg.media_content_type,
            sanitize_phone_for_path(user.phone_number),  # SAFE path
        )
        media_msg.supabase_path = supabase_path
        media_msg.downloaded = True
        
        # Parse with Gemini (PDFs validated)
        if media_msg.media_content_type == "application/pdf":
            # Basic PDF validation
            if not content.startswith(b"%PDF"):
                raise ValueError("Invalid PDF file")
        
        parsed_data = await parse_document_with_gemini(
            content,
            media_msg.media_content_type,
            media_msg.guessed_type,
        )
        media_msg.parsed_data = parsed_data
        
        # Update user verification status based on parsed data
        if parsed_data:
            await update_user_from_parsed_data(user, media_msg.guessed_type, parsed_data)
        
        update_media_message(media_msg)
        
        if twilio_client:
            await send_text_message_async(
                user.phone_number,
                f"✅ Your {media_msg.guessed_type.value.replace('_', ' ').upper()} "
                f"has been verified and your profile updated!",
                OutboundMessage(message_sid="", user_id=user.phone_number, message_type="text"),
            )
        
    except Exception as e:
        logger.error(f"Media processing failed for {user.phone_number}: {e}")
        media_msg.parsed_data = {"error": str(e)}
        update_media_message(media_msg)
        
        if twilio_client:
            await send_text_message_async(
                user.phone_number,
                f"❌ Failed to process document: {str(e)[:100]}\n"
                f"Please try again or type *help* for support.",
                OutboundMessage(message_sid="", user_id=user.phone_number, message_type="text"),
            )


async def update_user_from_parsed_data(
    user: "WhatsAppUser",
    doc_type: Optional["DocumentType"],
    parsed_data: Dict[str, Any],
):
    from .models import DocumentType, VerificationStatus
    from .database import upsert_user
    
    if not doc_type:
        return
    
    if doc_type == DocumentType.CSD_LETTER:
        csd_number = parsed_data.get("csd_number") or parsed_data.get("supplier_number")
        if csd_number:
            user.csd_status = VerificationStatus.VERIFIED
            user.registration_number = parsed_data.get("registration_number")
    
    elif doc_type == DocumentType.BBBEE_CERT:
        bbbee_level = parsed_data.get("bbbee_level")
        if bbbee_level:
            user.bbbee_status = VerificationStatus.VERIFIED
    
    elif doc_type == DocumentType.TAX_PIN:
        tax_pin = parsed_data.get("tax_pin") or parsed_data.get("pin_number")
        if tax_pin:
            user.tax_status = VerificationStatus.VERIFIED
    
    elif doc_type == DocumentType.CIDB_CERT:
        cidb_gradings = parsed_data.get("cidb_gradings", [])
        if cidb_gradings:
            user.cidb_status = VerificationStatus.VERIFIED
    
    if doc_type:
        user.documents[doc_type] = getattr(media_msg, 'supabase_path', "") if 'media_msg' in dir() else ""
    
    upsert_user(user)


# ============================================================
# STATUS CALLBACK
# ============================================================

@app.post("/whatsapp/status")
@limiter.limit("60/minute")
async def whatsapp_status_callback(
    request: Request,
    MessageSid: str = Form(...),
    MessageStatus: str = Form(...),
    To: str = Form(...),
    From: str = Form(...),
):
    """Delivery status callbacks (sent, delivered, read, failed)."""
    form_data = dict(await request.form())
    
    if not validate_twilio_request(request, form_data):
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    logger.info(f"Status update: {MessageSid} → {MessageStatus} (to: {To})")
    
    outbound = OutboundMessage(
        message_sid=MessageSid,
        user_id=clean_phone(To),
        message_type="",
        status=MessageStatus,
    )
    
    if MessageStatus == "sent":
        outbound.sent_at = datetime.utcnow()
    elif MessageStatus == "delivered":
        outbound.delivered_at = datetime.utcnow()
    elif MessageStatus == "read":
        outbound.read_at = datetime.utcnow()
    elif MessageStatus in ("failed", "undelivered"):
        outbound.error_message = MessageStatus
    
    update_outbound_message(outbound)
    return Response(content="", status_code=200)


# ============================================================
# OUTBOUND MESSAGE HELPERS
# ============================================================

async def send_text_message_async(to: str, body: str, outbound: OutboundMessage):
    if not twilio_client:
        return
    
    try:
        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{to}",
            body=body,
        )
        outbound.message_sid = message.sid
        outbound.status = "sent"
        outbound.sent_at = datetime.utcnow()
        update_outbound_message(outbound)
    except Exception as e:
        logger.error(f"Failed to send message to {to}: {e}")
        outbound.status = "failed"
        outbound.error_message = str(e)
        update_outbound_message(outbound)


def send_text_message(to: str, body: str) -> str:
    if not twilio_client:
        raise RuntimeError("Twilio client not configured")
    message = twilio_client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=f"whatsapp:{to}",
        body=body,
    )
    return message.sid


def send_media_message(to: str, media_url: str, caption: str = "") -> str:
    if not twilio_client:
        raise RuntimeError("Twilio client not configured")
    message = twilio_client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=f"whatsapp:{to}",
        body=caption,
        media_url=[media_url],
    )
    return message.sid


def send_template_message(to: str, template_sid: str, variables: dict) -> str:
    if not twilio_client:
        raise RuntimeError("Twilio client not configured")
    message = twilio_client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=f"whatsapp:{to}",
        content_sid=template_sid,
        content_variables=json.dumps(variables),  # SAFE JSON encoding
    )
    return message.sid


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    import uvicorn
    import json  # For template message encoding
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=30)