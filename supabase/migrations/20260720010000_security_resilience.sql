-- Tender Getter RSA — Security Resilience hardening after agentic billing rollout.
-- Apply after 20260720000000_agentic_billing.sql.

-- Durable inbound idempotency across Cloud Run instances and Twilio retries.
CREATE TABLE IF NOT EXISTS inbound_messages (
    message_sid TEXT PRIMARY KEY,
    sender_phone_number TEXT NOT NULL,
    message_type TEXT NOT NULL CHECK (message_type IN ('text','media','status')),
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Expand the durable work contract; long-running document parsing must be
-- queued rather than depend on a request-scoped background task.
ALTER TABLE agent_jobs DROP CONSTRAINT IF EXISTS agent_jobs_job_type_check;
ALTER TABLE agent_jobs ADD CONSTRAINT agent_jobs_job_type_check CHECK (
    job_type IN ('ingest','enrich','match','deliver_digest','build_bid_pack',
                 'payment_reconcile','process_document')
);

-- The function is SECURITY DEFINER, so its search path must not be inherited
-- from callers. Service-role workers bypass RLS; public/anon callers do not.
CREATE OR REPLACE FUNCTION claim_agent_job(worker_name TEXT)
RETURNS SETOF agent_jobs
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE claimed_id UUID;
BEGIN
  SELECT id INTO claimed_id FROM agent_jobs
  WHERE status IN ('queued', 'retry') AND run_after <= NOW()
  ORDER BY run_after, created_at FOR UPDATE SKIP LOCKED LIMIT 1;
  IF claimed_id IS NULL THEN RETURN; END IF;
  UPDATE agent_jobs SET status='running', locked_at=NOW(), locked_by=worker_name,
      attempts=attempts+1, updated_at=NOW() WHERE id=claimed_id;
  RETURN QUERY SELECT * FROM agent_jobs WHERE id=claimed_id;
END;
$$;

-- Customer data, message metadata, subscription state and agent reasoning are
-- not anonymously readable. Backend service-role access remains available.
ALTER TABLE whatsapp_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE media_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE outbound_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_digest_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE consent_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE opt_out_registry ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscription_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE company_subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE checkout_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE payment_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_actions ENABLE ROW LEVEL SECURITY;
ALTER TABLE natural_language_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE inbound_messages ENABLE ROW LEVEL SECURITY;

CREATE INDEX IF NOT EXISTS idx_inbound_messages_received_at ON inbound_messages(received_at);
