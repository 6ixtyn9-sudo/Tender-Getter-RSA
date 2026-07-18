"""
WhatsApp integration for Tender Getter RSA.
Provides webhook handling, outbound messaging, media handling,
onboarding flows, and daily digest delivery.
"""

from .webhook import app
from .models import (
    WhatsAppUser, OnboardingStep, DocumentType, VerificationStatus,
    ConversationState, MediaMessage, OutboundMessage, DailyDigestPreferences, TABLES
)
from .outbound import send_text_message, send_media_message, send_template_message
from .media import download_media, upload_to_supabase, parse_document_with_gemini, guess_document_type
from .onboarding import start_onboarding, handle_onboarding_step
from .digest import send_daily_digest, build_digest_message, TenderMatch, run_daily_digest_job
from .flows import get_onboarding_flow_json, get_flow_templates, get_all_flows, get_flow_templates as get_templates
from .database import (
    get_user, upsert_user, get_conversation_state, upsert_conversation_state,
    create_media_message, update_media_message, create_outbound_message,
    update_outbound_message, get_digest_preferences
)

__all__ = [
    "app",
    "send_text_message",
    "send_media_message",
    "send_template_message",
    "WhatsAppUser",
    "OnboardingStep",
    "DocumentType",
    "VerificationStatus",
    "ConversationState",
    "MediaMessage",
    "OutboundMessage",
    "DailyDigestPreferences",
    "TABLES",
    "download_media",
    "upload_to_supabase",
    "parse_document_with_gemini",
    "guess_document_type",
    "start_onboarding",
    "handle_onboarding_step",
    "send_daily_digest",
    "build_digest_message",
    "TenderMatch",
    "run_daily_digest_job",
    "get_onboarding_flow_json",
    "get_flow_templates",
    "get_all_flows",
    "get_user",
    "upsert_user",
    "get_conversation_state",
    "upsert_conversation_state",
    "create_media_message",
    "update_media_message",
    "create_outbound_message",
    "update_outbound_message",
    "get_digest_preferences",
]