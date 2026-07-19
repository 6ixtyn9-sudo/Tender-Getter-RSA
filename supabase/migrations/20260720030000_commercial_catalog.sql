-- Tender Getter RSA — approved commercial catalogue and VIP Bid-Craft metering.
-- All customer plans are paid. Beta is a temporary entitlement, not a plan.

INSERT INTO subscription_plans (
  plan_code, display_name, monthly_amount_cents, annual_amount_cents,
  currency, capabilities, active
) VALUES
(
  'starter', 'Starter', 24900, 249000, 'ZAR',
  '{"tender_alerts":true,"compliance_report":true,"bid_craft":false}', true
),
(
  'pro', 'Pro', 54900, 549000, 'ZAR',
  '{"tender_alerts":true,"compliance_report":true,"document_analysis":true,"bid_craft":false}', true
),
(
  'vip', 'VIP Bid-Craft', 149000, 1490000, 'ZAR',
  '{"tender_alerts":true,"compliance_report":true,"document_analysis":true,"bid_craft":true,"bid_craft_packs_per_month":2,"additional_bid_craft_pack_amount_cents":65000}', true
)
ON CONFLICT (plan_code) DO UPDATE SET
  display_name = EXCLUDED.display_name,
  monthly_amount_cents = EXCLUDED.monthly_amount_cents,
  annual_amount_cents = EXCLUDED.annual_amount_cents,
  currency = EXCLUDED.currency,
  capabilities = EXCLUDED.capabilities,
  active = EXCLUDED.active,
  updated_at = NOW();

ALTER TABLE checkout_sessions
  ADD COLUMN IF NOT EXISTS requested_payment_method TEXT NOT NULL DEFAULT 'hosted_checkout';

CREATE TABLE IF NOT EXISTS billing_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  registration_number TEXT REFERENCES company_profiles(registration_number) ON DELETE CASCADE,
  owner_phone_number TEXT NOT NULL REFERENCES whatsapp_users(phone_number) ON DELETE CASCADE,
  requested_method TEXT NOT NULL CHECK (requested_method IN ('card','pay_by_bank','debit_order','debitcheck','annual_invoice')),
  status TEXT NOT NULL DEFAULT 'requested' CHECK (status IN ('requested','mandate_pending','configured','cancelled','failed')),
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bid_craft_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  registration_number TEXT NOT NULL REFERENCES company_profiles(registration_number) ON DELETE CASCADE,
  tender_id TEXT NOT NULL REFERENCES tenders(tender_id) ON DELETE CASCADE,
  used_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(registration_number, tender_id)
);

-- Atomically reserve a monthly VIP Bid-Craft allowance. The system must reserve
-- before invoking an expensive proposal generation job; duplicate tender asks
-- are idempotent and do not consume another pack.
CREATE OR REPLACE FUNCTION reserve_bid_craft_pack(company_reg TEXT, bid_tender_id TEXT)
RETURNS BOOLEAN
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public AS $$
DECLARE limit_per_month INTEGER;
DECLARE used_this_month INTEGER;
DECLARE current_status TEXT;
DECLARE current_plan TEXT;
BEGIN
  SELECT status, plan_code INTO current_status, current_plan
  FROM company_subscriptions WHERE registration_number = company_reg FOR UPDATE;
  IF current_status NOT IN ('active','beta','trial') OR current_plan <> 'vip' THEN RETURN FALSE; END IF;
  SELECT COALESCE((capabilities->>'bid_craft_packs_per_month')::INTEGER, 0)
  INTO limit_per_month FROM subscription_plans WHERE plan_code = current_plan AND active = TRUE;
  IF limit_per_month <= 0 THEN RETURN FALSE; END IF;
  IF EXISTS (SELECT 1 FROM bid_craft_usage WHERE registration_number=company_reg AND tender_id=bid_tender_id) THEN RETURN TRUE; END IF;
  SELECT COUNT(*) INTO used_this_month FROM bid_craft_usage
  WHERE registration_number=company_reg AND used_at >= date_trunc('month', NOW());
  IF used_this_month >= limit_per_month THEN RETURN FALSE; END IF;
  INSERT INTO bid_craft_usage(registration_number,tender_id) VALUES(company_reg,bid_tender_id);
  RETURN TRUE;
END;
$$;

ALTER TABLE billing_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE bid_craft_usage ENABLE ROW LEVEL SECURITY;
CREATE INDEX IF NOT EXISTS idx_bid_craft_usage_month ON bid_craft_usage(registration_number, used_at DESC);
CREATE INDEX IF NOT EXISTS idx_billing_requests_owner ON billing_requests(owner_phone_number, created_at DESC);

CREATE TABLE IF NOT EXISTS bid_packs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  registration_number TEXT NOT NULL REFERENCES company_profiles(registration_number) ON DELETE CASCADE,
  tender_id TEXT NOT NULL REFERENCES tenders(tender_id) ON DELETE CASCADE,
  status TEXT NOT NULL DEFAULT 'queued' CHECK (status IN ('queued','drafting','ready','failed')),
  draft_content TEXT,
  storage_path TEXT,
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(registration_number, tender_id)
);
ALTER TABLE bid_packs ENABLE ROW LEVEL SECURITY;
CREATE INDEX IF NOT EXISTS idx_bid_packs_company ON bid_packs(registration_number, created_at DESC);
