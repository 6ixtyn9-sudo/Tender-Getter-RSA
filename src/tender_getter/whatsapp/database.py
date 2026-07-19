"""
WhatsApp database operations using Supabase/PostgreSQL.
Falls back to in-memory for development.
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from threading import Lock

from .models import (
    WhatsAppUser, ConversationState, MediaMessage, OutboundMessage,
    DailyDigestPreferences, TABLES, OnboardingStep, VerificationStatus, DocumentType
)

logger = logging.getLogger(__name__)

# In-memory fallback for development
_memory_store: Dict[str, Dict[str, Any]] = {
    "whatsapp_users": {},
    "conversation_states": {},
    "media_messages": {},
    "outbound_messages": {},
    "daily_digest_preferences": {},
}
_memory_lock = Lock()

# Try to initialize Supabase client
_supabase = None
_use_supabase = False

try:
    from supabase import create_client, Client
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if SUPABASE_URL and SUPABASE_SERVICE_KEY:
        _supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        _use_supabase = True
        logger.info("Supabase client initialized for WhatsApp module")
    else:
        logger.warning("Supabase credentials not set — using in-memory store")
except ImportError:
    logger.warning("Supabase package not available — using in-memory store")
except Exception as e:
    logger.warning(f"Supabase initialization failed: {e} — using in-memory store")


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def _get_table(table_name: str):
    """Get Supabase table or return None."""
    if _use_supabase and _supabase:
        return _supabase.table(TABLES[table_name])
    return None


def _memory_get(table: str, key: str) -> Optional[Dict]:
    with _memory_lock:
        return _memory_store[table].get(key)


def _memory_set(table: str, key: str, value: Dict):
    with _memory_lock:
        _memory_store[table][key] = value


def _memory_upsert(table: str, key_field: str, value: Dict):
    """Upsert in memory store."""
    key = value.get(key_field)
    if key:
        _memory_set(table, key, value)


def _model_to_dict(model) -> Dict:
    """Convert Pydantic model to dict with datetime serialization."""
    data = model.model_dump()
    for k, v in data.items():
        if isinstance(v, datetime):
            data[k] = v.isoformat()
        elif hasattr(v, 'value'):  # Enum
            data[k] = v.value
    return data


def _dict_to_model(data: Dict, model_class):
    """Convert dict to Pydantic model with datetime parsing."""
    if not data:
        return None
    parsed = {}
    for k, v in data.items():
        if k.endswith('_at') and isinstance(v, str):
            try:
                parsed[k] = datetime.fromisoformat(v.replace('Z', '+00:00'))
            except Exception:
                parsed[k] = v
        else:
            parsed[k] = v
    return model_class(**parsed)


# ---------------------------------------------------------------------------
# WhatsApp User Operations
# ---------------------------------------------------------------------------

def get_user(phone_number: str) -> Optional[WhatsAppUser]:
    """Get user by phone number (E.164 format)."""
    table = _get_table("whatsapp_users")
    if table:
        try:
            result = table.select("*").eq("phone_number", phone_number).execute()
            if result.data:
                return _dict_to_model(result.data[0], WhatsAppUser)
        except Exception as e:
            logger.error(f"Supabase get_user error: {e}")
    
    # Fallback to memory
    return _dict_to_model(_memory_get("whatsapp_users", phone_number), WhatsAppUser)


def upsert_user(user: WhatsAppUser) -> bool:
    """Insert or update user."""
    user.updated_at = datetime.utcnow()
    data = _model_to_dict(user)
    
    table = _get_table("whatsapp_users")
    if table:
        try:
            table.upsert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Supabase upsert_user error: {e}")
    
    _memory_upsert("whatsapp_users", "phone_number", data)
    return True


def get_users_by_step(step: OnboardingStep) -> List[WhatsAppUser]:
    """Get all users at a specific onboarding step."""
    table = _get_table("whatsapp_users")
    users = []
    if table:
        try:
            result = table.select("*").eq("onboarding_step", step.value).execute()
            users = [_dict_to_model(row, WhatsAppUser) for row in result.data]
        except Exception as e:
            logger.error(f"Supabase get_users_by_step error: {e}")
    
    if not users:
        with _memory_lock:
            for data in _memory_store["whatsapp_users"].values():
                if data.get("onboarding_step") == step.value:
                    users.append(_dict_to_model(data, WhatsAppUser))
    return users


# ---------------------------------------------------------------------------
# Conversation State Operations
# ---------------------------------------------------------------------------

def get_conversation_state(user_id: str) -> Optional[ConversationState]:
    """Get conversation state for user."""
    table = _get_table("conversation_states")
    if table:
        try:
            result = table.select("*").eq("user_id", user_id).execute()
            if result.data:
                return _dict_to_model(result.data[0], ConversationState)
        except Exception as e:
            logger.error(f"Supabase get_conversation_state error: {e}")
    
    return _dict_to_model(_memory_get("conversation_states", user_id), ConversationState)


def upsert_conversation_state(state: ConversationState) -> bool:
    """Insert or update conversation state."""
    state.updated_at = datetime.utcnow()
    data = _model_to_dict(state)
    
    table = _get_table("conversation_states")
    if table:
        try:
            table.upsert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Supabase upsert_conversation_state error: {e}")
    
    _memory_upsert("conversation_states", "user_id", data)
    return True


def delete_conversation_state(user_id: str) -> bool:
    """Delete conversation state."""
    table = _get_table("conversation_states")
    if table:
        try:
            table.delete().eq("user_id", user_id).execute()
            return True
        except Exception as e:
            logger.error(f"Supabase delete_conversation_state error: {e}")
    
    with _memory_lock:
        _memory_store["conversation_states"].pop(user_id, None)
    return True


# ---------------------------------------------------------------------------
# Media Message Operations
# ---------------------------------------------------------------------------

def create_media_message(msg: MediaMessage) -> bool:
    """Create media message record."""
    data = _model_to_dict(msg)
    
    table = _get_table("media_messages")
    if table:
        try:
            table.insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Supabase create_media_message error: {e}")
    
    key = f"{msg.user_id}_{msg.message_sid}"
    _memory_upsert("media_messages", "message_sid", data)
    return True


def update_media_message(msg: MediaMessage) -> bool:
    """Update media message record."""
    data = _model_to_dict(msg)
    
    table = _get_table("media_messages")
    if table:
        try:
            table.update(data).eq("message_sid", msg.message_sid).execute()
            return True
        except Exception as e:
            logger.error(f"Supabase update_media_message error: {e}")
    
    key = f"{msg.user_id}_{msg.message_sid}"
    _memory_upsert("media_messages", "message_sid", data)
    return True


def get_media_message(user_id: str, message_sid: str) -> Optional[MediaMessage]:
    """Get media message by user and message SID."""
    table = _get_table("media_messages")
    if table:
        try:
            result = table.select("*").eq("user_id", user_id).eq("message_sid", message_sid).execute()
            if result.data:
                return _dict_to_model(result.data[0], MediaMessage)
        except Exception as e:
            logger.error(f"Supabase get_media_message error: {e}")
    
    key = f"{user_id}_{message_sid}"
    return _dict_to_model(_memory_get("media_messages", key), MediaMessage)


# ---------------------------------------------------------------------------
# Outbound Message Operations
# ---------------------------------------------------------------------------

def create_outbound_message(msg: OutboundMessage) -> bool:
    """Create outbound message record."""
    data = _model_to_dict(msg)
    
    table = _get_table("outbound_messages")
    if table:
        try:
            table.insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Supabase create_outbound_message error: {e}")
    
    key = msg.message_sid or f"{msg.user_id}_{datetime.utcnow().timestamp()}"
    _memory_upsert("outbound_messages", "message_sid", data)
    return True


def update_outbound_message(msg: OutboundMessage) -> bool:
    """Update outbound message record."""
    data = _model_to_dict(msg)
    
    table = _get_table("outbound_messages")
    if table:
        try:
            table.update(data).eq("message_sid", msg.message_sid).execute()
            return True
        except Exception as e:
            logger.error(f"Supabase update_outbound_message error: {e}")
    
    _memory_upsert("outbound_messages", "message_sid", data)
    return True


# ---------------------------------------------------------------------------
# Digest Preferences
# ---------------------------------------------------------------------------

def get_digest_preferences(user_id: str) -> Optional[DailyDigestPreferences]:
    """Get daily digest preferences for user."""
    table = _get_table("digest_preferences")
    if table:
        try:
            result = table.select("*").eq("user_id", user_id).execute()
            if result.data:
                return _dict_to_model(result.data[0], DailyDigestPreferences)
        except Exception as e:
            logger.error(f"Supabase get_digest_preferences error: {e}")
    
    return _dict_to_model(_memory_get("daily_digest_preferences", user_id), DailyDigestPreferences)


def upsert_digest_preferences(prefs: DailyDigestPreferences) -> bool:
    """Insert or update digest preferences."""
    prefs.updated_at = datetime.utcnow()
    data = _model_to_dict(prefs)
    
    table = _get_table("digest_preferences")
    if table:
        try:
            table.upsert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Supabase upsert_digest_preferences error: {e}")
    
    _memory_upsert("daily_digest_preferences", "user_id", data)
    return True


# ---------------------------------------------------------------------------
# Schema Initialization (run once on startup)
# ---------------------------------------------------------------------------

def init_whatsapp_tables():
    """Create WhatsApp tables in Supabase if they don't exist.
    Run this once during application startup.
    """
    if not _use_supabase:
        logger.info("Skipping table creation — using in-memory store")
        return
    
    # DDL is versioned and deployed with Supabase migrations, not executed by
    # the application service role. See 20260719000000_whatsapp_and_privacy.sql.
    logger.info("WhatsApp schema is managed by Supabase migration 20260719000000_whatsapp_and_privacy.sql")


# SQL for manual table creation (run in Supabase SQL editor)
CREATE_TABLES_SQL = """
-- WhatsApp Users
CREATE TABLE IF NOT EXISTS whatsapp_users (
    whatsapp_id TEXT PRIMARY KEY,
    phone_number TEXT UNIQUE NOT NULL,
    registration_number TEXT,
    onboarding_step TEXT NOT NULL DEFAULT 'welcome',
    onboarding_data JSONB DEFAULT '{}',
    onboarding_started_at TIMESTAMPTZ,
    onboarding_completed_at TIMESTAMPTZ,
    csd_status TEXT NOT NULL DEFAULT 'not_provided',
    bbbee_status TEXT NOT NULL DEFAULT 'not_provided',
    tax_status TEXT NOT NULL DEFAULT 'not_provided',
    cidb_status TEXT NOT NULL DEFAULT 'not_provided',
    documents JSONB DEFAULT '{}',
    sectors TEXT[] DEFAULT '{}',
    province TEXT,
    language TEXT DEFAULT 'en',
    timezone TEXT DEFAULT 'Africa/Johannesburg',
    popia_consent BOOLEAN DEFAULT FALSE,
    popia_consent_at TIMESTAMPTZ,
    popia_consent_version TEXT DEFAULT '1.0',
    marketing_opt_in BOOLEAN DEFAULT FALSE,
    last_active_at TIMESTAMPTZ,
    total_messages_sent INTEGER DEFAULT 0,
    total_messages_received INTEGER DEFAULT 0,
    opted_out_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Conversation States
CREATE TABLE IF NOT EXISTS conversation_states (
    user_id TEXT PRIMARY KEY,
    current_flow TEXT,
    current_step TEXT,
    context_data JSONB DEFAULT '{}',
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Media Messages
CREATE TABLE IF NOT EXISTS media_messages (
    message_sid TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    media_url TEXT NOT NULL,
    media_content_type TEXT NOT NULL,
    media_size INTEGER,
    guessed_type TEXT,
    downloaded BOOLEAN DEFAULT FALSE,
    supabase_path TEXT,
    parsed_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Outbound Messages
CREATE TABLE IF NOT EXISTS outbound_messages (
    message_sid TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    message_type TEXT NOT NULL,
    template_sid TEXT,
    content TEXT,
    media_url TEXT,
    status TEXT NOT NULL DEFAULT 'queued',
    sent_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    read_at TIMESTAMPTZ,
    error_code TEXT,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Daily Digest Preferences
CREATE TABLE IF NOT EXISTS daily_digest_preferences (
    user_id TEXT PRIMARY KEY,
    enabled BOOLEAN DEFAULT TRUE,
    delivery_time TEXT DEFAULT '07:00',
    timezone TEXT DEFAULT 'Africa/Johannesburg',
    max_tenders INTEGER DEFAULT 5,
    min_match_score REAL DEFAULT 70.0,
    include_report_links BOOLEAN DEFAULT TRUE,
    language TEXT DEFAULT 'en',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_whatsapp_users_phone ON whatsapp_users(phone_number);
CREATE INDEX IF NOT EXISTS idx_whatsapp_users_step ON whatsapp_users(onboarding_step);
CREATE INDEX IF NOT EXISTS idx_media_messages_user ON media_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_outbound_messages_user ON outbound_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_outbound_messages_status ON outbound_messages(status);
"""