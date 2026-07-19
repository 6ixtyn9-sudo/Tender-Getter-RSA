-- Tender Getter RSA — autonomous agents, natural-language feedback and billing.
-- Applied after 20260719000000_20260719000000_whatsapp_and_privacy.sql.

CREATE TABLE IF NOT EXISTS subscription_plans (
    plan_code TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    monthly_amount_cents INTEGER NOT NULL CHECK (monthly_amount_cents > 0),
    annual_amount_cents INTEGER NOT NULL CHECK (annual_amount_cents > 0),
    currency TEXT NOT NULL DEFAULT 'ZAR',
    capabilities JSONB NOT NULL DEFAULT '{}'::jsonb,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- One paying owner and one subscription per registered company. Beta access is
-- represented as an explicit complimentary subscription, never a hidden bypass.
CREATE TABLE IF NOT EXISTS company_subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    registration_number TEXT NOT NULL REFERENCES company_profiles(registration_number) ON DELETE CASCADE,
    owner_phone_number TEXT NOT NULL REFERENCES whatsapp_users(phone_number) ON DELETE RESTRICT,
    plan_code TEXT NOT NULL REFERENCES subscription_plans(plan_code),
    status TEXT NOT NULL CHECK (status IN ('beta','trial','active','past_due','cancelled','expired')),
    billing_provider TEXT,
    provider_customer_id TEXT,
    provider_subscription_id TEXT UNIQUE,
    billing_interval TEXT NOT NULL CHECK (billing_interval IN ('monthly','annual')),
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    cancel_at_period_end BOOLEAN NOT NULL DEFAULT FALSE,
    beta_expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(registration_number),
    UNIQUE(owner_phone_number)
);

CREATE TABLE IF NOT EXISTS checkout_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    registration_number TEXT NOT NULL REFERENCES company_profiles(registration_number) ON DELETE CASCADE,
    owner_phone_number TEXT NOT NULL REFERENCES whatsapp_users(phone_number) ON DELETE CASCADE,
    plan_code TEXT NOT NULL REFERENCES subscription_plans(plan_code),
    billing_interval TEXT NOT NULL CHECK (billing_interval IN ('monthly','annual')),
    provider TEXT NOT NULL,
    provider_reference TEXT NOT NULL UNIQUE,
    checkout_url TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'created' CHECK (status IN ('created','opened','paid','expired','cancelled','failed')),
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS payment_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider TEXT NOT NULL,
    provider_event_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload JSONB NOT NULL,
    processed_at TIMESTAMPTZ,
    processing_error TEXT,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(provider, provider_event_id)
);

-- Durable, idempotent autonomous work. A worker claims one queued job at a
-- time; no user-facing workflow depends on an in-memory background task.
CREATE TABLE IF NOT EXISTS agent_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    idempotency_key TEXT NOT NULL UNIQUE,
    job_type TEXT NOT NULL CHECK (job_type IN ('ingest','enrich','match','deliver_digest','build_bid_pack','payment_reconcile')),
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    status TEXT NOT NULL DEFAULT 'queued' CHECK (status IN ('queued','running','succeeded','retry','failed','dead_letter')),
    attempts INTEGER NOT NULL DEFAULT 0,
    run_after TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    locked_at TIMESTAMPTZ,
    locked_by TEXT,
    last_error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS agent_actions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_name TEXT NOT NULL,
    registration_number TEXT REFERENCES company_profiles(registration_number) ON DELETE SET NULL,
    tender_id TEXT REFERENCES tenders(tender_id) ON DELETE SET NULL,
    decision TEXT NOT NULL CHECK (decision IN ('alert','suppress','enrich','retry','bid_pack','payment_link')),
    confidence REAL NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    rationale JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS natural_language_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_phone_number TEXT NOT NULL REFERENCES whatsapp_users(phone_number) ON DELETE CASCADE,
    tender_id TEXT REFERENCES tenders(tender_id) ON DELETE SET NULL,
    raw_text TEXT NOT NULL,
    sentiment TEXT CHECK (sentiment IN ('positive','negative','neutral','action_requested')),
    intent TEXT,
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    extracted_signals JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agent_jobs_claim ON agent_jobs(status, run_after) WHERE status IN ('queued','retry');
CREATE INDEX IF NOT EXISTS idx_agent_actions_company ON agent_actions(registration_number, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_feedback_owner ON natural_language_feedback(owner_phone_number, created_at DESC);

-- Atomic claim avoids two Cloud Run workers processing the same task.
CREATE OR REPLACE FUNCTION claim_agent_job(worker_name TEXT)
RETURNS SETOF agent_jobs
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE claimed_id UUID;
BEGIN
  SELECT id INTO claimed_id
  FROM agent_jobs
  WHERE status IN ('queued', 'retry') AND run_after <= NOW()
  ORDER BY run_after, created_at
  FOR UPDATE SKIP LOCKED
  LIMIT 1;
  IF claimed_id IS NULL THEN RETURN; END IF;
  UPDATE agent_jobs
  SET status = 'running', locked_at = NOW(), locked_by = worker_name,
      attempts = attempts + 1, updated_at = NOW()
  WHERE id = claimed_id;
  RETURN QUERY SELECT * FROM agent_jobs WHERE id = claimed_id;
END;
$$;
