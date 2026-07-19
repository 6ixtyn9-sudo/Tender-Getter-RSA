"""Secure Twilio WhatsApp webhook.

Inbound replies are returned exactly once as TwiML.  Out-of-band messages
(digests, media-processing completion and reports) use the Twilio REST client.
This separation prevents duplicate delivery.
"""
from __future__ import annotations

import asyncio
import logging
import os
import time
from collections import defaultdict, deque
from datetime import datetime
from typing import Any, Optional

from fastapi import BackgroundTasks, FastAPI, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from .database import claim_inbound_message, create_media_message, update_media_message, upsert_user
from .media import download_media, guess_document_type, parse_document_with_gemini, upload_to_supabase, MediaTooLargeError
from .models import DocumentType, MediaMessage, VerificationStatus, WhatsAppUser
from .outbound import send_text_message

logger = logging.getLogger(__name__)
ENV = os.getenv("ENV", "development").lower()
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
validator = RequestValidator(TWILIO_AUTH_TOKEN) if TWILIO_AUTH_TOKEN else None
MAX_MEDIA_BYTES = int(os.getenv("TG_MAX_MEDIA_BYTES", str(15 * 1024 * 1024)))

app = FastAPI(title="Tender Getter RSA WhatsApp Webhook", docs_url=None if ENV == "production" else "/docs")
allowed_origins = [x.strip() for x in os.getenv("TG_CORS_ORIGINS", "").split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type", "X-Twilio-Signature"],
)

# A small process-local guard absorbs Twilio retries. Persistent message records
# are still the source of truth in production; retries across instances remain safe
# because inbound replies are TwiML, not a second REST send.
_seen_sids: dict[str, float] = {}
_rate_windows: dict[str, deque[float]] = defaultdict(deque)
_RATE_LIMIT = int(os.getenv("TG_WEBHOOK_RATE_PER_MINUTE", "30"))
# Hard cardinality bound for the in-process rate tracker so a flood of
# distinct sender numbers cannot grow memory without limit.
_MAX_TRACKED_SENDERS = int(os.getenv("TG_RATE_TRACKER_MAX_SENDERS", "10000"))


def clean_phone(value: str) -> str:
    return value.replace("whatsapp:", "").strip()


def _is_local_insecure_allowed() -> bool:
    return ENV in {"development", "test"} and os.getenv("TG_ALLOW_INSECURE_WEBHOOK", "0") == "1"


def validate_twilio_request(request: Request, form_data: dict[str, Any]) -> bool:
    """Fail closed in production; local unsigned requests require explicit opt-in."""
    if validator is None:
        if _is_local_insecure_allowed():
            logger.warning("Unsigned webhook accepted only because local development override is enabled")
            return True
        logger.error("Rejecting webhook: TWILIO_AUTH_TOKEN is not configured")
        return False
    return validator.validate(str(request.url), form_data, request.headers.get("X-Twilio-Signature", ""))


def _allow_request(phone: str) -> bool:
    now = time.monotonic()
    if len(_rate_windows) >= _MAX_TRACKED_SENDERS:
        # Memory bound: evict idle windows before admitting another sender.
        for sender, window in list(_rate_windows.items()):
            if not window or now - window[-1] > 60:
                _rate_windows.pop(sender, None)
        while len(_rate_windows) >= _MAX_TRACKED_SENDERS:
            _rate_windows.pop(next(iter(_rate_windows)), None)
    bucket = _rate_windows[phone]
    while bucket and now - bucket[0] > 60:
        bucket.popleft()
    if len(bucket) >= _RATE_LIMIT:
        return False
    bucket.append(now)
    return True


def _mark_seen(message_sid: str) -> bool:
    now = time.monotonic()
    for key, seen in list(_seen_sids.items()):
        if now - seen > 600:
            _seen_sids.pop(key, None)
    if message_sid in _seen_sids:
        return False
    _seen_sids[message_sid] = now
    return True


def get_or_create_user(whatsapp_id: str) -> WhatsAppUser:
    from .database import get_user
    phone = clean_phone(whatsapp_id)
    user = get_user(phone)
    if user is None:
        user = WhatsAppUser(whatsapp_id=whatsapp_id, phone_number=phone)
        upsert_user(user)
    return user


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


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
    form_data = dict(await request.form())
    if not validate_twilio_request(request, form_data):
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")
    phone = clean_phone(From)
    if not _allow_request(phone):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    message_type = "media" if NumMedia > 0 else "text"
    if not claim_inbound_message(MessageSid, phone, message_type) or not _mark_seen(MessageSid):
        return Response(content="<Response/>", media_type="application/xml")

    user = get_or_create_user(From)
    user.last_active_at = datetime.utcnow()
    user.total_messages_received += 1
    upsert_user(user)
    if user.opted_out_at:
        return Response(content="<Response/>", media_type="application/xml")

    if NumMedia > 0 and MediaUrl0:
        response_text = await handle_media_upload(user, MessageSid, MediaUrl0, MediaContentType0 or "application/octet-stream", background_tasks)
    else:
        from ..ai import get_ai_handler
        response_text = await get_ai_handler().handle_message(user, Body, MessageSid)

    # One delivery mechanism for the immediate reply: TwiML only.
    twiml = MessagingResponse()
    if response_text:
        twiml.message(response_text)
    return Response(content=str(twiml), media_type="application/xml")


@app.post("/billing/paystack/webhook")
async def paystack_billing_webhook(request: Request):
    """Idempotently activate a paid entitlement after verified hosted checkout."""
    body = await request.body()
    if len(body) > 512_000:
        raise HTTPException(status_code=413, detail="Payment payload too large")
    from ..billing.service import BillingService
    service = BillingService()
    if not service.provider.verify_webhook(body, request.headers.get("x-paystack-signature", "")):
        raise HTTPException(status_code=403, detail="Invalid payment signature")
    import json
    event = json.loads(body.decode("utf-8")); event_id = event.get("data", {}).get("id") or event.get("data", {}).get("reference")
    if not event_id or not service.client:
        return Response(status_code=204)
    # Insert is the durable idempotency boundary. Duplicate provider retries do
    # not create another subscription or change entitlement state.
    existing = service.client.table("payment_events").select("id").eq("provider", "paystack").eq("provider_event_id", str(event_id)).execute().data
    if existing: return Response(status_code=204)
    try:
        service.client.table("payment_events").insert({"provider": "paystack", "provider_event_id": str(event_id), "event_type": event.get("event", "unknown"), "payload": event, "processed_at": datetime.utcnow().isoformat()}).execute()
    except Exception as exc:
        # The UNIQUE(provider, provider_event_id) constraint is the final race
        # barrier when two provider retries arrive at different instances.
        if "duplicate" in str(exc).lower() or "23505" in str(exc): return Response(status_code=204)
        raise
    if event.get("event") == "charge.success":
        payment = event.get("data", {}) or {}
        reference = str(payment.get("reference", ""))
        sessions = service.client.table("checkout_sessions").select("*").eq("provider", "paystack").eq("provider_reference", reference).execute().data
        if not sessions:
            logger.error("Verified payment has no matching checkout session: %s", reference)
            return Response(status_code=204)
        session = sessions[0]
        if int(payment.get("amount", -1)) != int(session["amount_cents"]) or payment.get("currency", "ZAR") != session["currency"]:
            logger.error("Payment amount/currency mismatch for checkout %s", reference)
            return Response(status_code=204)
        service.client.table("checkout_sessions").update({"status": "paid"}).eq("id", session["id"]).execute()
        service.client.table("company_subscriptions").upsert({"registration_number": session["registration_number"], "owner_phone_number": session["owner_phone_number"], "plan_code": session["plan_code"], "status": "active", "billing_provider": "paystack", "provider_customer_id": str(payment.get("customer", {}).get("customer_code", "")), "provider_subscription_id": reference, "billing_interval": session["billing_interval"], "last_payment_at": datetime.utcnow().isoformat()}, on_conflict="registration_number").execute()
        try:
            confirmation_sid = send_text_message(session["owner_phone_number"], f"✅ Payment confirmed. Your *{session['plan_code'].title()}* plan is active. Your payment reference is *{session['customer_reference']}*.")
            service.client.table("company_subscriptions").update({"payment_confirmation_message_sid": confirmation_sid}).eq("registration_number", session["registration_number"]).execute()
        except Exception:
            logger.exception("Payment was activated but WhatsApp confirmation could not be sent")
    return Response(status_code=204)


@app.post("/whatsapp/status")
async def whatsapp_status_callback(request: Request, MessageSid: str = Form(...), MessageStatus: str = Form(...), To: str = Form(""), From: str = Form("")):
    form_data = dict(await request.form())
    if not validate_twilio_request(request, form_data):
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")
    from .database import update_outbound_message
    from .models import OutboundMessage
    update_outbound_message(OutboundMessage(message_sid=MessageSid, user_id=clean_phone(To), message_type="text", status=MessageStatus))
    return Response(content="", status_code=200)


async def handle_media_upload(user: WhatsAppUser, message_sid: str, media_url: str, media_type: str, background_tasks: BackgroundTasks) -> str:
    allowed = {"application/pdf", "image/jpeg", "image/png", "image/webp"}
    if media_type.lower().split(";")[0] not in allowed:
        return "Please upload a PDF, JPG, PNG, or WEBP document only."
    guessed = guess_document_type(media_type)
    media = MediaMessage(message_sid=message_sid, user_id=user.phone_number, media_url=media_url, media_content_type=media_type, guessed_type=guessed)
    create_media_message(media)
    # Production processing is durable and picked up by agent_worker. Local
    # development keeps a fast in-process path for a simple smoke-test loop.
    from ..agents.store import AgentStore
    AgentStore().enqueue("process_document", {"message_sid": message_sid, "owner_phone": user.phone_number}, f"process_document:{message_sid}")
    if ENV != "production":
        background_tasks.add_task(process_media_async, media, user)
    label = guessed.value.replace("_", " ") if guessed else "document"
    return f"📄 Received your {label}. I’m securely checking it now. Type *profile* shortly for the updated verification status."


async def process_media_async(media: MediaMessage, user: WhatsAppUser) -> None:
    try:
        content = await download_media(media.media_url, max_bytes=MAX_MEDIA_BYTES)
        media.media_size = len(content)
        media.supabase_path = await upload_to_supabase(content, media.media_content_type, user.phone_number)
        media.downloaded = True
        media.parsed_data = await parse_document_with_gemini(content, media.media_content_type, media.guessed_type)
        if media.parsed_data:
            await update_user_from_parsed_data(user, media.guessed_type, media.parsed_data, media.supabase_path)
        update_media_message(media)
        send_text_message(user.phone_number, "✅ Your document was processed. Type *profile* to review its verification status.")
    except MediaTooLargeError as exc:
        logger.info("Media too large for %s: %s", media.message_sid, exc)
        media.parsed_data = {"error": "too_large"}
        update_media_message(media)
        try:
            send_text_message(
                user.phone_number,
                f"📄 That file is too large — {exc}. Please send a smaller PDF or a clear photo instead.",
            )
        except Exception:
            logger.exception("Could not send media-size notice")
    except Exception:
        logger.exception("Media processing failed for %s", media.message_sid)
        media.parsed_data = {"error": "processing_failed"}
        update_media_message(media)
        try:
            send_text_message(user.phone_number, "❌ I could not process that document. Please send a clear PDF or image, or contact support.")
        except Exception:
            logger.exception("Could not send media-processing failure notice")


async def update_user_from_parsed_data(user: WhatsAppUser, doc_type: Optional[DocumentType], parsed: dict[str, Any], storage_path: Optional[str]) -> None:
    if doc_type is None:
        return
    if doc_type == DocumentType.CSD_LETTER and (parsed.get("csd_number") or parsed.get("supplier_number")):
        user.csd_status = VerificationStatus.VERIFIED
        user.registration_number = parsed.get("registration_number") or user.registration_number
    elif doc_type == DocumentType.BBBEE_CERT and parsed.get("bbbee_level"):
        user.bbbee_status = VerificationStatus.VERIFIED
    elif doc_type == DocumentType.TAX_PIN and (parsed.get("tax_pin") or parsed.get("pin_number")):
        user.tax_status = VerificationStatus.VERIFIED
    elif doc_type == DocumentType.CIDB_CERT and parsed.get("cidb_gradings"):
        user.cidb_status = VerificationStatus.VERIFIED
    if storage_path:
        user.documents[doc_type.value] = storage_path
    upsert_user(user)


@app.get("/health")
async def health_check():
    from ..ai import get_gateway
    return {"status": "ok", "service": "tender-getter-whatsapp", "environment": ENV, "gateway": await get_gateway().health_check(), "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
