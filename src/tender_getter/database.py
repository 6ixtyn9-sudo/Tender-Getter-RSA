"""
database.py - Local-first SQLite persistence layer for Tender Getter RSA.

Tables:
  - company_profiles   : Registered client bidders.
  - cidb_gradings      : CIDB class/level records linked to companies.
  - tenders            : Cached raw tender opportunities.
  - matches            : Historic match results and audit records.

Factory:
  - get_database_client() : Returns TenderDatabase (SQLite) when SUPABASE_DB_URL
                            is unset, or PostgresDatabase (Supabase) when it is set.
"""

import os
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from .database_base import TenderDatabaseBase
from .schemas import CompanyProfile, TenderOpportunity, MatchResult

DEFAULT_DB_PATH = Path(__file__).resolve().parents[3] / "localdata" / "tender_getter.db"


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------

_CREATE_COMPANY_PROFILES = """
CREATE TABLE IF NOT EXISTS company_profiles (
    registration_number TEXT PRIMARY KEY,
    company_name        TEXT NOT NULL,
    csd_number          TEXT,
    bbbee_level         INTEGER NOT NULL DEFAULT 9,
    black_ownership_pct REAL    NOT NULL DEFAULT 0.0,
    youth_ownership_pct REAL    NOT NULL DEFAULT 0.0,
    women_ownership_pct REAL    NOT NULL DEFAULT 0.0,
    province            TEXT    NOT NULL,
    city                TEXT    NOT NULL,
    municipality        TEXT,
    sectors             TEXT    NOT NULL DEFAULT '[]',   -- JSON array
    has_tax_pin         INTEGER NOT NULL DEFAULT 0,      -- boolean
    has_coida           INTEGER NOT NULL DEFAULT 0,      -- boolean
    is_active           INTEGER NOT NULL DEFAULT 1,      -- boolean
    created_at          TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at          TEXT    NOT NULL DEFAULT (datetime('now'))
);
"""

_CREATE_CIDB_GRADINGS = """
CREATE TABLE IF NOT EXISTS cidb_gradings (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_number TEXT    NOT NULL REFERENCES company_profiles(registration_number),
    class_code          TEXT    NOT NULL,
    level               INTEGER NOT NULL,
    UNIQUE(registration_number, class_code)
);
"""

_CREATE_TENDERS = """
CREATE TABLE IF NOT EXISTS tenders (
    tender_id             TEXT PRIMARY KEY,
    title                 TEXT NOT NULL,
    issuing_entity        TEXT NOT NULL,
    closing_date          TEXT NOT NULL,
    estimated_value       REAL,
    required_cidb_class   TEXT,
    required_cidb_level   INTEGER,
    mandatory_csd         INTEGER NOT NULL DEFAULT 1,
    tax_compliance_required INTEGER NOT NULL DEFAULT 1,
    location_target       TEXT,
    raw_document_url      TEXT,
    created_at            TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

_CREATE_MATCHES = """
CREATE TABLE IF NOT EXISTS matches (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    company_reg_number    TEXT    NOT NULL REFERENCES company_profiles(registration_number),
    tender_id             TEXT    NOT NULL REFERENCES tenders(tender_id),
    is_eligible           INTEGER NOT NULL,
    match_score           REAL    NOT NULL,
    bbbee_points          REAL    NOT NULL DEFAULT 0.0,
    bbbee_system          TEXT,
    disqualification_reason TEXT,
    feedback              TEXT,
    evaluated_at          TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE(company_reg_number, tender_id)
);
"""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class TenderDatabase(TenderDatabaseBase):
    """Local-first SQLite driver implementing TenderDatabaseBase."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None

    # -- Connection lifecycle ------------------------------------------------

    def connect(self) -> "TenderDatabase":
        self._conn = sqlite3.connect(str(self.db_path))
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._create_tables()
        return self

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "TenderDatabase":
        return self.connect()

    def __exit__(self, *_):
        self.close()

    # -- Company profiles ----------------------------------------------------

    def upsert_company(self, company: CompanyProfile) -> None:
        """Insert or update a company profile and its CIDB gradings."""
        assert self._conn, "Call connect() first."
        with self._conn:
            self._conn.execute(
                """
                INSERT INTO company_profiles (
                    registration_number, company_name, csd_number, bbbee_level,
                    black_ownership_pct, youth_ownership_pct, women_ownership_pct,
                    province, city, municipality, sectors,
                    has_tax_pin, has_coida, is_active, updated_at
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now'))
                ON CONFLICT(registration_number) DO UPDATE SET
                    company_name        = excluded.company_name,
                    csd_number          = excluded.csd_number,
                    bbbee_level         = excluded.bbbee_level,
                    black_ownership_pct = excluded.black_ownership_pct,
                    youth_ownership_pct = excluded.youth_ownership_pct,
                    women_ownership_pct = excluded.women_ownership_pct,
                    province            = excluded.province,
                    city                = excluded.city,
                    municipality        = excluded.municipality,
                    sectors             = excluded.sectors,
                    has_tax_pin         = excluded.has_tax_pin,
                    has_coida           = excluded.has_coida,
                    is_active           = excluded.is_active,
                    updated_at          = datetime('now')
                """,
                (
                    company.registration_number, company.company_name,
                    company.csd_number, company.bbbee_level,
                    company.black_ownership_pct, company.youth_ownership_pct,
                    company.women_ownership_pct,
                    company.location.province, company.location.city,
                    company.location.municipality,
                    json.dumps(company.sectors),
                    int(company.has_tax_pin), int(company.has_coida),
                    int(company.is_active),
                ),
            )
            # Replace CIDB gradings for this company
            self._conn.execute(
                "DELETE FROM cidb_gradings WHERE registration_number = ?",
                (company.registration_number,),
            )
            for grading in company.cidb_gradings:
                self._conn.execute(
                    """
                    INSERT INTO cidb_gradings (registration_number, class_code, level)
                    VALUES (?, ?, ?)
                    ON CONFLICT(registration_number, class_code) DO UPDATE SET
                        level = excluded.level
                    """,
                    (company.registration_number, grading.class_code, grading.level),
                )

    # -- Tenders -------------------------------------------------------------

    def upsert_tender(self, tender: TenderOpportunity) -> None:
        """Insert or update a tender opportunity."""
        assert self._conn, "Call connect() first."
        with self._conn:
            self._conn.execute(
                """
                INSERT INTO tenders (
                    tender_id, title, issuing_entity, closing_date,
                    estimated_value, required_cidb_class, required_cidb_level,
                    mandatory_csd, tax_compliance_required, location_target,
                    raw_document_url
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(tender_id) DO UPDATE SET
                    title                   = excluded.title,
                    issuing_entity          = excluded.issuing_entity,
                    closing_date            = excluded.closing_date,
                    estimated_value         = excluded.estimated_value,
                    required_cidb_class     = excluded.required_cidb_class,
                    required_cidb_level     = excluded.required_cidb_level,
                    mandatory_csd           = excluded.mandatory_csd,
                    tax_compliance_required = excluded.tax_compliance_required,
                    location_target         = excluded.location_target,
                    raw_document_url        = excluded.raw_document_url
                """,
                (
                    tender.tender_id, tender.title, tender.issuing_entity,
                    tender.closing_date.isoformat(),
                    tender.estimated_value,
                    tender.required_cidb_class, tender.required_cidb_level,
                    int(tender.mandatory_csd), int(tender.tax_compliance_required),
                    tender.location_target, tender.raw_document_url,
                ),
            )

    # -- Match results -------------------------------------------------------

    def save_match(self, company: CompanyProfile, result: MatchResult) -> None:
        """Persist a MatchResult to the matches table."""
        assert self._conn, "Call connect() first."
        with self._conn:
            self._conn.execute(
                """
                INSERT INTO matches (
                    company_reg_number, tender_id, is_eligible,
                    match_score, bbbee_points, bbbee_system,
                    disqualification_reason, feedback, evaluated_at
                ) VALUES (?,?,?,?,?,?,?,?,datetime('now'))
                ON CONFLICT(company_reg_number, tender_id) DO UPDATE SET
                    is_eligible             = excluded.is_eligible,
                    match_score             = excluded.match_score,
                    bbbee_points            = excluded.bbbee_points,
                    bbbee_system            = excluded.bbbee_system,
                    disqualification_reason = excluded.disqualification_reason,
                    feedback                = excluded.feedback,
                    evaluated_at            = datetime('now')
                """,
                (
                    company.registration_number, result.tender_id,
                    int(result.is_eligible), result.match_score,
                    result.bbbee_points, result.bbbee_system,
                    result.disqualification_reason, result.feedback,
                ),
            )

    # -- Private helpers -----------------------------------------------------

    def _create_tables(self):
        assert self._conn
        with self._conn:
            for stmt in [
                _CREATE_COMPANY_PROFILES,
                _CREATE_CIDB_GRADINGS,
                _CREATE_TENDERS,
                _CREATE_MATCHES,
            ]:
                self._conn.execute(stmt)


# ---------------------------------------------------------------------------
# Public factory — runtime driver selection
# ---------------------------------------------------------------------------

def get_database_client() -> TenderDatabaseBase:
    """
    Priority:
    1. SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY -> SupabaseDatabase (PostgREST, recommended)
    2. SUPABASE_DB_URL                          -> PostgresDatabase (psycopg2)
    3. fallback                                 -> TenderDatabase (SQLite)
    """
    import os
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_ANON_KEY")
    if supabase_url and supabase_key:
        from .database_supabase import SupabaseDatabase
        return SupabaseDatabase(supabase_url, supabase_key)
    postgres_url = os.environ.get("SUPABASE_DB_URL")
    if postgres_url:
        from .database_postgres import PostgresDatabase
        return PostgresDatabase(postgres_url)
    return TenderDatabase()

