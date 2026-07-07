-- =============================================================================
-- Tender Getter RSA — Supabase Production Schema Migration
-- Version: 1.1.0
-- Date:    2026-07-07
--
-- Run this script once in the Supabase SQL Editor (or via psql) before
-- pointing SUPABASE_DB_URL at your project.  All statements are idempotent.
-- =============================================================================

-- 1. Enable UUID extension (Supabase enables this by default, kept for safety)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- -----------------------------------------------------------------------------
-- 2. Company Profiles Table
--    Central store for all registered client bidders.
--    sectors stored as JSONB for efficient indexing of the string array.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS company_profiles (
    registration_number TEXT        PRIMARY KEY,
    company_name        TEXT        NOT NULL,
    csd_number          TEXT,
    bbbee_level         INTEGER     NOT NULL DEFAULT 9,
    black_ownership_pct REAL        NOT NULL DEFAULT 0.0,
    youth_ownership_pct REAL        NOT NULL DEFAULT 0.0,
    women_ownership_pct REAL        NOT NULL DEFAULT 0.0,
    province            TEXT        NOT NULL,
    city                TEXT        NOT NULL,
    municipality        TEXT,
    sectors             JSONB       NOT NULL DEFAULT '[]'::jsonb,
    has_tax_pin         BOOLEAN     NOT NULL DEFAULT FALSE,
    has_coida           BOOLEAN     NOT NULL DEFAULT FALSE,
    is_active           BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE  company_profiles                      IS 'Registered client bidders and their regulatory profiles.';
COMMENT ON COLUMN company_profiles.registration_number  IS 'CIPC company registration number, e.g. 2019/123456/07';
COMMENT ON COLUMN company_profiles.csd_number           IS 'CSD Central Supplier Database MAAA supplier number.';
COMMENT ON COLUMN company_profiles.bbbee_level          IS 'B-BBEE Level 1-8. Value 9 indicates Non-Compliant.';
COMMENT ON COLUMN company_profiles.sectors              IS 'JSONB array of industry tags, e.g. ["Electrical","Civil"]';

-- -----------------------------------------------------------------------------
-- 3. CIDB Gradings Table
--    One-to-many child of company_profiles.  Cascades on parent delete.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cidb_gradings (
    id                  BIGSERIAL   PRIMARY KEY,
    registration_number TEXT        NOT NULL
                                    REFERENCES company_profiles(registration_number)
                                    ON DELETE CASCADE,
    class_code          TEXT        NOT NULL,
    level               INTEGER     NOT NULL,
    UNIQUE(registration_number, class_code)
);

COMMENT ON TABLE  cidb_gradings            IS 'CIDB class/level registrations for each company (one row per class code).';
COMMENT ON COLUMN cidb_gradings.class_code IS 'CIDB class code, e.g. CE, GB, EE, ME, EP, SB.';
COMMENT ON COLUMN cidb_gradings.level      IS 'CIDB grading level 1 (smallest) to 9 (unlimited).';

-- Index for fast company lookups
CREATE INDEX IF NOT EXISTS idx_cidb_gradings_reg
    ON cidb_gradings(registration_number);

-- -----------------------------------------------------------------------------
-- 4. Tenders Table
--    Cached raw tender opportunities parsed from public platforms.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tenders (
    tender_id               TEXT        PRIMARY KEY,
    title                   TEXT        NOT NULL,
    issuing_entity          TEXT        NOT NULL,
    closing_date            TIMESTAMPTZ NOT NULL,
    estimated_value         REAL,
    required_cidb_class     TEXT,
    required_cidb_level     INTEGER,
    mandatory_csd           BOOLEAN     NOT NULL DEFAULT TRUE,
    tax_compliance_required BOOLEAN     NOT NULL DEFAULT TRUE,
    location_target         TEXT,
    raw_document_url        TEXT,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE  tenders                          IS 'Cached tender opportunities sourced from public procurement portals.';
COMMENT ON COLUMN tenders.tender_id                IS 'Official bid reference number, e.g. COJ/EE/2026/012.';
COMMENT ON COLUMN tenders.estimated_value          IS 'Estimated contract value in South African Rand (ZAR).';
COMMENT ON COLUMN tenders.required_cidb_class      IS 'Minimum CIDB class code required to bid, e.g. CE, GB, EE.';
COMMENT ON COLUMN tenders.location_target          IS 'Province name for localized tenders or "National" for open bids.';

-- Index for fast closing-date range scans (most common query pattern)
CREATE INDEX IF NOT EXISTS idx_tenders_closing_date
    ON tenders(closing_date);

-- -----------------------------------------------------------------------------
-- 5. Matches & Audits Table
--    Historic match results keyed on (company, tender) composite unique constraint.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS matches (
    id                      BIGSERIAL   PRIMARY KEY,
    company_reg_number      TEXT        NOT NULL
                                        REFERENCES company_profiles(registration_number)
                                        ON DELETE CASCADE,
    tender_id               TEXT        NOT NULL
                                        REFERENCES tenders(tender_id)
                                        ON DELETE CASCADE,
    is_eligible             BOOLEAN     NOT NULL,
    match_score             REAL        NOT NULL,
    bbbee_points            REAL        NOT NULL DEFAULT 0.0,
    bbbee_system            TEXT,
    disqualification_reason TEXT,
    feedback                TEXT,
    evaluated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(company_reg_number, tender_id)
);

COMMENT ON TABLE  matches                          IS 'Audit trail of all match evaluations between companies and tenders.';
COMMENT ON COLUMN matches.match_score              IS 'Composite eligibility score as a percentage (0.0 to 100.0).';
COMMENT ON COLUMN matches.bbbee_points             IS 'B-BBEE preference points awarded under PPPFA.';
COMMENT ON COLUMN matches.bbbee_system             IS 'Preferential procurement system applied: "80/20" or "90/10".';
COMMENT ON COLUMN matches.disqualification_reason  IS 'Gate-failure reason if is_eligible is FALSE.';

-- Indexes for company-centric and tender-centric audit queries
CREATE INDEX IF NOT EXISTS idx_matches_company
    ON matches(company_reg_number);

CREATE INDEX IF NOT EXISTS idx_matches_tender
    ON matches(tender_id);

CREATE INDEX IF NOT EXISTS idx_matches_evaluated_at
    ON matches(evaluated_at DESC);

-- =============================================================================
-- End of migration
-- =============================================================================
