-- Tender Getter RSA — payment identity, customer confirmation and distributed abuse protection.
-- Apply after 20260720010000_security_resilience.sql.

ALTER TABLE company_subscriptions
  ADD COLUMN IF NOT EXISTS trial_expires_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS last_payment_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS payment_confirmation_message_sid TEXT;

ALTER TABLE checkout_sessions
  ADD COLUMN IF NOT EXISTS amount_cents INTEGER,
  ADD COLUMN IF NOT EXISTS currency TEXT NOT NULL DEFAULT 'ZAR',
  ADD COLUMN IF NOT EXISTS customer_reference TEXT UNIQUE;

-- One atomic database operation handles both replay rejection and distributed
-- per-phone throttling. A rejected SID remains recorded so retries cannot
-- amplify traffic against the WhatsApp agent.
CREATE OR REPLACE FUNCTION accept_inbound_message(
  incoming_sid TEXT,
  incoming_phone TEXT,
  incoming_type TEXT,
  max_per_minute INTEGER DEFAULT 30
) RETURNS BOOLEAN
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public AS $$
DECLARE inserted_count INTEGER;
DECLARE recent_count INTEGER;
BEGIN
  INSERT INTO inbound_messages(message_sid, sender_phone_number, message_type)
  VALUES (incoming_sid, incoming_phone, incoming_type)
  ON CONFLICT (message_sid) DO NOTHING;
  GET DIAGNOSTICS inserted_count = ROW_COUNT;
  IF inserted_count = 0 THEN RETURN FALSE; END IF;

  SELECT COUNT(*) INTO recent_count FROM inbound_messages
  WHERE sender_phone_number = incoming_phone
    AND received_at >= NOW() - INTERVAL '1 minute';
  RETURN recent_count <= max_per_minute;
END;
$$;
