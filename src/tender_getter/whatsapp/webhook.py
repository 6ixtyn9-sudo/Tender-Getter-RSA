"""
WhatsApp webhook handler for Twilio — AI-Enhanced.
Receives inbound messages, status callbacks, and routes to AI handler.
Integrates with database for user management and conversation state.
"""

import os
import logging
from datetime import datetime
from typing import Optional, Dict, Any

from fastapi import FastAPI, Request, Form, HTTPException, BackgroundTasks
from fastapi.responses import Response
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

app = FastAPI(title="Tender Getter RSA - WhatsApp Webhook (AI-Enhanced)")

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

# Request validator for security
validator = RequestValidator(TWILIO_AUTH_TOKEN) if TWILIO_AUTH_TOKEN else None

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


def validate_twilio_request(request: Request, form_data: dict) -> bool:
    """Validate that the request actually came from Twilio."""
    if not validator:
        logger.warning("TWILIO_AUTH_TOKEN not set — skipping request validation")
        return True
    
    url = str(request.url)
    signature = request.headers.get("X-Twilio-Signature", "")
    return validator.validate(url, form_data, signature)


def clean_phone(whatsapp_id: str) -> str:
    """Normalize WhatsApp ID to E.164 format."""
    return whatsapp_id.replace("whatsapp:", "")


def get_or_create_user(whatsapp_id: str) -> WhatsAppUser:
    """Get existing user or create new one."""
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


@app.post("/whatsapp/webhook")
async def whatsapp_webhook(
    background_tasks: BackgroundTasks,
    request: Request,
    From: str = Form(...),
    Body: str = Form(""),
    MessageSid: str = Form(...),
    NumMedia: int = Form(0),
    MediaUrl0: Optional[str] = Form(None),
    MediaContentType0: Optional[str] = Form(None),
):
    """
    Main inbound message webhook — AI-Enhanced.
    Handles text messages and media (images, PDFs, documents).
    Uses natural language understanding instead of rigid commands.
    """
    form_data = dict(await request.form())
    
    if not validate_twilio_request(request, form_data):
        logger.warning(f"Invalid Twilio signature from {From}")
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    logger.info(f"Incoming message from {From}: {Body[:50]}...")
    
    # Get or create user
    user = get_or_create_user(From)
    user.last_active_at = datetime.utcnow()
    user.total_messages_received += 1
    upsert_user(user)
    
    # Handle opt-out first
    if user.opted_out_at:
        return Response(content="", media_type="application/xml")
    
    # Handle media uploads
    if NumMedia > 0 and MediaUrl0:
        response_text = await handle_media_upload(
            user, MessageSid, MediaUrl0, MediaContentType0, background_tasks
        )
    else:
        # Route through AI handler (natural language)
        ai_handler = get_ai_handler_instance()
        response_text = await ai_handler.handle_message(
            user=user,
            text=Body,
            message_sid=MessageSid,
            media_url=MediaUrl0,
            media_type=MediaContentType0,
        )
    
    # Track outbound message
    if response_text and twilio_client:
        outbound = OutboundMessage(
            message_sid="",  # Will be filled after send
            user_id=user.phone_number,
            message_type="text",
            content=response_text,
            status="queued",
        )
        create_outbound_message(outbound)
        
        # Send in background
        background_tasks.add_task(send_text_message_async, user.phone_number, response_text, outbound)
    
    # Return TwiML response
    twiml = MessagingResponse()
    if response_text:
        twiml.message(response_text)
    return Response(content=str(twiml), media_type="application/xml")


async def send_text_message_async(to: str, body: str, outbound: OutboundMessage):
    """Send text message asynchronously and update status."""
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


@app.post("/whatsapp/status")
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
    
    # Update outbound message status
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


# ---------------------------------------------------------------------------
# Media Handling (unchanged from original)
# ---------------------------------------------------------------------------

async def handle_media_upload(
    user: WhatsAppUser,
    message_sid: str,
    media_url: str,
    media_type: str,
    background_tasks: BackgroundTasks,
) -> str:
    """Handle uploaded documents (CSD, B-BBEE, CIDB cert, Tax PIN)."""
    logger.info(f"Media upload from {user.phone_number}: {media_type} at {media_url}")
    
    # Create media message record
    media_msg = MediaMessage(
        message_sid=message_sid,
        user_id=user.phone_number,
        media_url=media_url,
        media_content_type=media_type,
        guessed_type=guess_document_type(media_type),
    )
    create_media_message(media_msg)
    
    # Acknowledge receipt immediately
    doc_type = guess_document_type(media_type)
    response = (
        f"📄 Received your {doc_type} document.\n\n"
        f"✅ Uploaded successfully.\n"
        f"🔍 Processing... (extracting details with AI)\n\n"
        f"Type *profile* to see your verification status."
    )
    
    # Process in background
    background_tasks.add_task(
        process_media_async,
        media_msg,
        user,
    )
    
    return response


async def process_media_async(media_msg: MediaMessage, user: WhatsAppUser):
    """Background task: download, upload to Supabase, parse with Gemini."""
    try:
        # Download media
        content = await download_media(media_msg.media_url)
        media_msg.media_size = len(content)
        
        # Upload to Supabase
        supabase_path = await upload_to_supabase(
            content,
            media_msg.media_content_type,
            user.phone_number,
        )
        media_msg.supabase_path = supabase_path
        media_msg.downloaded = True
        
        # Parse with Gemini
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
        
        # Send confirmation
        if twilio_client:
            await send_text_message_async(
                user.phone_number,
                f"✅ Your {media_msg.guessed_type.value.replace('_', ' ').upper()} "
                f"has been verified and your profile updated!",
                OutboundMessage(message_sid="", user_id=user.phone_number, message_type="text"),
            )
        
    except Exception as e:
        logger.error(f"Media processing failed: {e}")
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
    user: WhatsAppUser,
    doc_type: Optional[DocumentType],
    parsed_data: Dict[str, Any],
):
    """Update user verification status based on parsed document data."""
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
    
    # Store document reference
    if doc_type:
        user.documents[doc_type] = media_msg.supabase_path if 'media_msg' in dir() else ""
    
    upsert_user(user)


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def clean_phone(whatsapp_id: str) -> str:
    """Normalize WhatsApp ID to E.164 format."""
    return whatsapp_id.replace("whatsapp:", "")


# ---------------------------------------------------------------------------
# Outbound Message Helpers
# ---------------------------------------------------------------------------

async def send_text_message_async(to: str, body: str, outbound: OutboundMessage):
    """Send text message asynchronously and update status."""
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
    """Send a free-form text message (session must be open)."""
    if not twilio_client:
        raise RuntimeError("Twilio client not configured")
    message = twilio_client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=f"whatsapp:{to}",
        body=body,
    )
    return message.sid


def send_media_message(to: str, media_url: str, caption: str = "") -> str:
    """Send a media message (PDF report, image)."""
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
    """Send a pre-approved template message. Returns message SID."""
    if not twilio_client:
        raise RuntimeError("Twilio client not configured")
    message = twilio_client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=f"whatsapp:{to}",
        content_sid=template_sid,
        content_variables=str(variables).replace("'", '"'),
    )
    return message.sid


# ---------------------------------------------------------------------------
# Health Check Endpoint
# ---------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    from ..ai import get_gateway
    gateway = get_gateway()
    gateway_health = await gateway.health_check()
    
    return {
        "status": "ok",
        "service": "tender-getter-whatsapp",
        "gateway": gateway_health,
        "timestamp": datetime.utcnow().isoformat(),
    }


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)