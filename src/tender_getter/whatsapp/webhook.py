"""
WhatsApp webhook handler for Twilio.
Receives inbound messages, status callbacks, and routes to handlers.
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import Response
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

app = FastAPI(title="Tender Getter RSA - WhatsApp Webhook")

# Twilio credentials
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

# Request validator for security
validator = RequestValidator(TWILIO_AUTH_TOKEN) if TWILIO_AUTH_TOKEN else None


def validate_twilio_request(request: Request, form_data: dict) -> bool:
    """Validate that the request actually came from Twilio."""
    if not validator:
        logger.warning("TWILIO_AUTH_TOKEN not set — skipping request validation")
        return True
    
    url = str(request.url)
    signature = request.headers.get("X-Twilio-Signature", "")
    return validator.validate(url, form_data, signature)


@app.post("/whatsapp/webhook")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(""),
    MessageSid: str = Form(...),
    NumMedia: int = Form(0),
    MediaUrl0: Optional[str] = Form(None),
    MediaContentType0: Optional[str] = Form(None),
):
    """
    Main inbound message webhook.
    Handles text messages and media (images, PDFs, documents).
    """
    form_data = dict(await request.form())
    
    if not validate_twilio_request(request, form_data):
        logger.warning(f"Invalid Twilio signature from {From}")
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    logger.info(f"Incoming message from {From}: {Body[:50]}...")
    
    # Clean phone number (remove whatsapp: prefix)
    user_id = From.replace("whatsapp:", "")
    
    # Route to handler
    response_text = await handle_inbound_message(
        user_id=user_id,
        body=Body,
        message_sid=MessageSid,
        num_media=NumMedia,
        media_url=MediaUrl0,
        media_type=MediaContentType0,
    )
    
    # Return TwiML response
    twiml = MessagingResponse()
    if response_text:
        twiml.message(response_text)
    return Response(content=str(twiml), media_type="application/xml")


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
    
    # TODO: Update message status in database
    # await update_message_status(MessageSid, MessageStatus)
    
    return Response(content="", status_code=200)


# ---------------------------------------------------------------------------
# Message Handlers
# ---------------------------------------------------------------------------

async def handle_inbound_message(
    user_id: str,
    body: str,
    message_sid: str,
    num_media: int,
    media_url: Optional[str],
    media_type: Optional[str],
) -> str:
    """
    Route inbound messages to appropriate handler based on user state.
    Returns response text (empty string = no reply).
    """
    body_lower = body.strip().lower()
    
    # Handle media uploads (documents, images)
    if num_media > 0 and media_url:
        return await handle_media_upload(user_id, media_url, media_type, message_sid)
    
    # Command routing
    if body_lower in ("hi", "hello", "start", "menu", "help"):
        return get_welcome_message()
    
    if body_lower in ("tenders", "matches", "my tenders", "show tenders"):
        return await handle_show_tenders(user_id)
    
    if body_lower.startswith("verify "):
        return await handle_verification_command(user_id, body)
    
    if body_lower in ("profile", "my profile", "settings"):
        return await handle_show_profile(user_id)
    
    if body_lower in ("stop", "unsubscribe", "opt out"):
        return await handle_opt_out(user_id)
    
    if body_lower in ("onboard", "register", "sign up"):
        return await handle_onboarding_start(user_id)
    
    # Default: show help
    return get_help_message()


async def handle_media_upload(
    user_id: str,
    media_url: str,
    media_type: str,
    message_sid: str,
) -> str:
    """Handle uploaded documents (CSD, B-BBEE, CIDB cert, Tax PIN)."""
    logger.info(f"Media upload from {user_id}: {media_type} at {media_url}")
    
    # TODO: Download media, upload to Supabase, parse with Gemini
    # For now, acknowledge receipt
    doc_type = guess_document_type(media_type)
    
    return (
        f"📄 Received your {doc_type} document.\n\n"
        f"✅ Uploaded successfully.\n"
        f"🔍 Processing... (this feature coming soon)\n\n"
        f"Type *profile* to see your current verification status."
    )


async def handle_show_tenders(user_id: str) -> str:
    """Show matched tenders for this user."""
    # TODO: Query database for matches
    return (
        "📋 *Your Matched Tenders*\n\n"
        "No active matches yet. The system runs matching daily.\n\n"
        "Run: `python scripts/run_poc.py --match-only` to refresh.\n\n"
        "Type *menu* for options."
    )


async def handle_verification_command(user_id: str, body: str) -> str:
    """Handle 'verify csd', 'verify tax', 'verify bbbee', etc."""
    parts = body.lower().split()
    if len(parts) < 2:
        return "Usage: `verify csd` | `verify tax` | `verify bbbee` | `verify cidb`"
    
    doc_type = parts[1]
    return (
        f"🔍 *Verification Request: {doc_type.upper()}*\n\n"
        f"Please upload your {doc_type.upper()} document (PDF or photo).\n"
        f"I'll extract the details and update your profile.\n\n"
        f"Or type *menu* for other options."
    )


async def handle_show_profile(user_id: str) -> str:
    """Show user's current profile and verification status."""
    # TODO: Load from database
    return (
        "👤 *Your Profile*\n\n"
        "Company: Not set\n"
        "CIDB: Not verified\n"
        "CSD: Not verified\n"
        "Tax PIN: Not verified\n"
        "B-BBEE: Not verified\n\n"
        "Type *onboard* to set up your profile."
    )


async def handle_opt_out(user_id: str) -> str:
    """Handle POPIA opt-out."""
    # TODO: Log opt-out in database
    return (
        "✅ You've been unsubscribed from all Tender Getter messages.\n\n"
        "Your data will be deleted per POPIA requirements.\n"
        "To rejoin, just send *start*."
    )


async def handle_onboarding_start(user_id: str) -> str:
    """Start the onboarding flow."""
    return (
        "🚀 *Welcome to Tender Getter RSA Onboarding!*\n\n"
        "I'll help you set up your company profile in 5 steps:\n\n"
        "1️⃣ Company name & CIDB lookup\n"
        "2️⃣ CIDB grading confirmation\n"
        "3️⃣ Document upload (CSD, B-BBEE, Tax PIN, CIDB cert)\n"
        "4️⃣ Sector & province selection\n"
        "5️⃣ POPIA consent\n\n"
        "Let's start — what's your *company name*?\n\n"
        "(Type *cancel* anytime to exit)"
    )


def guess_document_type(media_type: str) -> str:
    """Guess document type from MIME type."""
    if "pdf" in media_type:
        return "PDF document"
    if "image" in media_type:
        return "photo"
    return "document"


def get_welcome_message() -> str:
    return (
        "👋 *Welcome to Tender Getter RSA!*\n\n"
        "I find tenders you can actually win — checking your CIDB, CSD, "
        "Tax PIN, and B-BBEE automatically.\n\n"
        "*Commands:*\n"
        "• *tenders* — View your matched tenders\n"
        "• *profile* — View verification status\n"
        "• *verify csd/tax/bbbee/cidb* — Upload documents\n"
        "• *onboard* — Set up your profile\n"
        "• *stop* — Unsubscribe (POPIA)\n\n"
        "Type *onboard* to get started!"
    )


def get_help_message() -> str:
    return (
        "🤔 Not sure what you meant. Try:\n\n"
        "• *tenders* — View matches\n"
        "• *profile* — Your status\n"
        "• *onboard* — Set up profile\n"
        "• *verify csd* — Upload CSD letter\n"
        "• *menu* — This help\n"
        "• *stop* — Unsubscribe"
    )


# ---------------------------------------------------------------------------
# Outbound Message Helpers (for daily digests, reports, etc.)
# ---------------------------------------------------------------------------

def send_template_message(to: str, template_sid: str, variables: dict) -> str:
    """Send a pre-approved template message. Returns message SID."""
    from twilio.rest import Client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=f"whatsapp:{to}",
        content_sid=template_sid,
        content_variables=str(variables).replace("'", '"'),
    )
    return message.sid


def send_text_message(to: str, body: str) -> str:
    """Send a free-form text message (session must be open)."""
    from twilio.rest import Client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=f"whatsapp:{to}",
        body=body,
    )
    return message.sid


def send_media_message(to: str, media_url: str, caption: str = "") -> str:
    """Send a media message (PDF report, image)."""
    from twilio.rest import Client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=f"whatsapp:{to}",
        body=caption,
        media_url=[media_url],
    )
    return message.sid


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)