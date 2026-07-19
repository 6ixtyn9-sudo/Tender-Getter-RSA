-- Tender Getter RSA — WhatsApp, POPIA and delivery persistence
-- Apply after 20260707000000_initial_schema.sql. All statements are idempotent.

CREATE TABLE IF NOT EXISTS whatsapp_users (
    whatsapp_id TEXT PRIMARY KEY,
    phone_number TEXT UNIQUE NOT NULL,
    registration_number TEXT REFERENCES company_profiles(registration_number) ON DELETE SET NULL,
    onboarding_step TEXT NOT NULL DEFAULT 'welcome',
    onboarding_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    onboarding_started_at TIMESTAMPTZ,
    onboarding_completed_at TIMESTAMPTZ,
    csd_status TEXT NOT NULL DEFAULT 'not_provided',
    bbbee_status TEXT NOT NULL DEFAULT 'not_provided',
    tax_status TEXT NOT NULL DEFAULT 'not_provided',
    cidb_status TEXT NOT NULL DEFAULT 'not_provided',
    documents JSONB NOT NULL DEFAULT '{}'::jsonb,
    sectors TEXT[] NOT NULL DEFAULT '{}',
    province TEXT,
    language TEXT NOT NULL DEFAULT 'en',
    timezone TEXT NOT NULL DEFAULT 'Africa/Johannesburg',
    popia_consent BOOLEAN NOT NULL DEFAULT FALSE,
    popia_consent_at TIMESTAMPTZ,
    popia_consent_version TEXT NOT NULL DEFAULT '1.0',
    marketing_opt_in BOOLEAN NOT NULL DEFAULT FALSE,
    last_active_at TIMESTAMPTZ,
    total_messages_sent INTEGER NOT NULL DEFAULT 0,
    total_messages_received INTEGER NOT NULL DEFAULT 0,
    opted_out_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS conversation_states (
    user_id TEXT PRIMARY KEY REFERENCES whatsapp_users(phone_number) ON DELETE CASCADE,
    current_flow TEXT,
    current_step TEXT,
    context_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS media_messages (
    message_sid TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES whatsapp_users(phone_number) ON DELETE CASCADE,
    media_url TEXT NOT NULL,
    media_content_type TEXT NOT NULL,
    media_size INTEGER,
    guessed_type TEXT,
    downloaded BOOLEAN NOT NULL DEFAULT FALSE,
    supabase_path TEXT,
    parsed_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS outbound_messages (
    message_sid TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES whatsapp_users(phone_number) ON DELETE CASCADE,
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
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS daily_digest_preferences (
    user_id TEXT PRIMARY KEY REFERENCES whatsapp_users(phone_number) ON DELETE CASCADE,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    delivery_time TEXT NOT NULL DEFAULT '07:00',
    timezone TEXT NOT NULL DEFAULT 'Africa/Johannesburg',
    max_tenders INTEGER NOT NULL DEFAULT 5 CHECK (max_tenders BETWEEN 1 AND 20),
    min_match_score REAL NOT NULL DEFAULT 70.0 CHECK (min_match_score BETWEEN 0 AND 100),
    include_report_links BOOLEAN NOT NULL DEFAULT TRUE,
    language TEXT NOT NULL DEFAULT 'en',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Immutable POPIA audit records and a suppression registry are intentionally
-- separate from the mutable user record.
CREATE TABLE IF NOT EXISTS consent_log (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    consent_type TEXT NOT NULL,
    granted BOOLEAN NOT NULL,
    consent_version TEXT,
    captured_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source TEXT NOT NULL DEFAULT 'whatsapp'
);
CREATE TABLE IF NOT EXISTS opt_out_registry (
    phone_number TEXT PRIMARY KEY,
    opted_out_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    reason TEXT NOT NULL DEFAULT 'user_request'
);

CREATE INDEX IF NOT EXISTS idx_whatsapp_users_registration ON whatsapp_users(registration_number);
CREATE INDEX IF NOT EXISTS idx_whatsapp_users_step ON whatsapp_users(onboarding_step);
CREATE INDEX IF NOT EXISTS idx_media_messages_user ON media_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_outbound_messages_user_status ON outbound_messages(user_id, status);
CREATE INDEX IF NOT EXISTS idx_consent_log_user ON consent_log(user_id, captured_at DESC);
