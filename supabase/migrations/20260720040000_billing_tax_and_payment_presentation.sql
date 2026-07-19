-- Tender Getter RSA — tax configuration and bank-neutral payment presentation.
-- Apply after 20260720030000_commercial_catalog.sql.

CREATE TABLE IF NOT EXISTS billing_tax_configuration (
  singleton BOOLEAN PRIMARY KEY DEFAULT TRUE CHECK (singleton),
  tax_mode TEXT NOT NULL CHECK (tax_mode IN ('not_registered','vat_inclusive','vat_exclusive')),
  vat_rate_percent NUMERIC(5,2) NOT NULL DEFAULT 15.00 CHECK (vat_rate_percent >= 0 AND vat_rate_percent <= 100),
  effective_from TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tender Getter is currently not VAT registered. Catalogue amounts are charged
-- exactly as displayed. Change only after formal VAT-registration decision.
INSERT INTO billing_tax_configuration(singleton, tax_mode, vat_rate_percent)
VALUES (TRUE, 'not_registered', 15.00)
ON CONFLICT (singleton) DO NOTHING;

ALTER TABLE checkout_sessions
  ADD COLUMN IF NOT EXISTS subtotal_amount_cents INTEGER,
  ADD COLUMN IF NOT EXISTS tax_amount_cents INTEGER NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS tax_mode TEXT NOT NULL DEFAULT 'not_registered';

ALTER TABLE billing_tax_configuration ENABLE ROW LEVEL SECURITY;
