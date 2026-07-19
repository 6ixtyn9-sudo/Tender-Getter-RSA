"""
Outbound message helpers for WhatsApp — shared between webhook, digest, and AI handler.
Breaks circular import between webhook.py and digest.py.
"""

import json
import os
from typing import Optional

from twilio.rest import Client

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

# Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN else None


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
        # Proper JSON — user-controlled values (company names, quotes) must
        # never be able to corrupt the payload the way str().replace() did.
        content_variables=json.dumps(variables),
    )
    return message.sid