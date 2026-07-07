"""
database_postgres.py - Supabase / PostgreSQL production driver for Tender Getter RSA.

Implements TenderDatabaseBase using psycopg2 for direct PostgreSQL wire-protocol
access. Designed for Supabase connection strings (postgresql://...) but works with
any standards-compliant PostgreSQL instance.

Environment variable consumed by get_database_client() (in database.py):
    SUPABASE_DB_URL  — full connection string, e.g.:
        postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres

Schema (DDL) lives in scripts/migrate_supabase.sql and is run once against
Supabase. This driver assumes the tables already exist.
"""

import json
from typing import Optional

from .database_base import TenderDatabaseBase
from .schemas import CompanyProfile, TenderOpportunity, MatchResult


class PostgresDatabase(TenderDatabaseBase):
    """
    Production PostgreSQL driver.  Uses psycopg2 (psycopg2-binary) which is
    lazily imported so that machines without Supabase configured never need the
    package installed.
    """

    def __init__(self, dsn: str):
        """
        Args:
            dsn: A libpq-compatible connection string, e.g.
                 'postgresql://user:pass@host:5432/dbname'
        """
        self._dsn = dsn
        self._conn = None  # psycopg2.connection, set in connect()

    # -- Connection lifecycle ------------------------------------------------

    def connect(self) -> "PostgresDatabase":
        """Open the psycopg2 connection. Returns self for chaining."""
        import psycopg2
        import psycopg2.extras  # for RealDictCursor (future queries)

        self._conn = psycopg2.connect(self._dsn)
        self._conn.autocommit = False
        return self

    def close(self) -> None:
        """Commit any pending transaction and release the connection."""
        if self._conn and not self._conn.closed:
            self._conn.commit()
            self._conn.close()
            self._conn = None

    # -- Helpers -------------------------------------------------------------

    def _cursor(self):
        """Return a standard psycopg2 cursor. Asserts connection is open."""
        assert self._conn is not None and not self._conn.closed, (
            "PostgresDatabase: call connect() before issuing queries."
        )
        return self._conn.cursor()

    # -- Company profiles ----------------------------------------------------

    def upsert_company(self, company: CompanyProfile) -> None:
        """
        Upsert a company profile row and atomically refresh its CIDB gradings.

        CIDB gradings are handled with a DELETE + batch INSERT inside a single
        transaction so that stale gradings can never linger.
        """
        cur = self._cursor()
        try:
            # 1. Upsert the parent company_profiles row
            cur.execute(
                """
                INSERT INTO company_profiles (
                    registration_number, company_name, csd_number, bbbee_level,
                    black_ownership_pct, youth_ownership_pct, women_ownership_pct,
                    province, city, municipality, sectors,
                    has_tax_pin, has_coida, is_active, updated_at
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s,%s,%s,NOW())
                ON CONFLICT (registration_number) DO UPDATE SET
                    company_name        = EXCLUDED.company_name,
                    csd_number          = EXCLUDED.csd_number,
                    bbbee_level         = EXCLUDED.bbbee_level,
                    black_ownership_pct = EXCLUDED.black_ownership_pct,
                    youth_ownership_pct = EXCLUDED.youth_ownership_pct,
                    women_ownership_pct = EXCLUDED.women_ownership_pct,
                    province            = EXCLUDED.province,
                    city                = EXCLUDED.city,
                    municipality        = EXCLUDED.municipality,
                    sectors             = EXCLUDED.sectors,
                    has_tax_pin         = EXCLUDED.has_tax_pin,
                    has_coida           = EXCLUDED.has_coida,
                    is_active           = EXCLUDED.is_active,
                    updated_at          = NOW()
                """,
                (
                    company.registration_number,
                    company.company_name,
                    company.csd_number,
                    company.bbbee_level,
                    company.black_ownership_pct,
                    company.youth_ownership_pct,
                    company.women_ownership_pct,
                    company.location.province,
                    company.location.city,
                    company.location.municipality,
                    json.dumps(company.sectors),   # cast to ::jsonb in SQL
                    company.has_tax_pin,           # native Python bool → BOOLEAN
                    company.has_coida,
                    company.is_active,
                ),
            )

            # 2. Atomically replace CIDB gradings for this company
            cur.execute(
                "DELETE FROM cidb_gradings WHERE registration_number = %s",
                (company.registration_number,),
            )
            for grading in company.cidb_gradings:
                cur.execute(
                    """
                    INSERT INTO cidb_gradings (registration_number, class_code, level)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (registration_number, class_code) DO UPDATE SET
                        level = EXCLUDED.level
                    """,
                    (company.registration_number, grading.class_code, grading.level),
                )

            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
        finally:
            cur.close()

    # -- Tenders -------------------------------------------------------------

    def upsert_tender(self, tender: TenderOpportunity) -> None:
        """
        Upsert a tender opportunity row.

        closing_date is stored as TIMESTAMPTZ — psycopg2 automatically adapts
        Python datetime objects (timezone-aware) to the correct wire format.
        """
        cur = self._cursor()
        try:
            cur.execute(
                """
                INSERT INTO tenders (
                    tender_id, title, issuing_entity, closing_date,
                    estimated_value, required_cidb_class, required_cidb_level,
                    mandatory_csd, tax_compliance_required,
                    location_target, raw_document_url
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (tender_id) DO UPDATE SET
                    title                   = EXCLUDED.title,
                    issuing_entity          = EXCLUDED.issuing_entity,
                    closing_date            = EXCLUDED.closing_date,
                    estimated_value         = EXCLUDED.estimated_value,
                    required_cidb_class     = EXCLUDED.required_cidb_class,
                    required_cidb_level     = EXCLUDED.required_cidb_level,
                    mandatory_csd           = EXCLUDED.mandatory_csd,
                    tax_compliance_required = EXCLUDED.tax_compliance_required,
                    location_target         = EXCLUDED.location_target,
                    raw_document_url        = EXCLUDED.raw_document_url
                """,
                (
                    tender.tender_id,
                    tender.title,
                    tender.issuing_entity,
                    tender.closing_date,           # datetime → TIMESTAMPTZ via psycopg2
                    tender.estimated_value,
                    tender.required_cidb_class,
                    tender.required_cidb_level,
                    tender.mandatory_csd,          # native bool → BOOLEAN
                    tender.tax_compliance_required,
                    tender.location_target,
                    tender.raw_document_url,
                ),
            )
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
        finally:
            cur.close()

    # -- Match results -------------------------------------------------------

    def save_match(self, company: CompanyProfile, result: MatchResult) -> None:
        """
        Persist (or update) a MatchResult row keyed on (company_reg_number, tender_id).
        """
        cur = self._cursor()
        try:
            cur.execute(
                """
                INSERT INTO matches (
                    company_reg_number, tender_id, is_eligible,
                    match_score, bbbee_points, bbbee_system,
                    disqualification_reason, feedback, evaluated_at
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())
                ON CONFLICT (company_reg_number, tender_id) DO UPDATE SET
                    is_eligible             = EXCLUDED.is_eligible,
                    match_score             = EXCLUDED.match_score,
                    bbbee_points            = EXCLUDED.bbbee_points,
                    bbbee_system            = EXCLUDED.bbbee_system,
                    disqualification_reason = EXCLUDED.disqualification_reason,
                    feedback                = EXCLUDED.feedback,
                    evaluated_at            = NOW()
                """,
                (
                    company.registration_number,
                    result.tender_id,
                    result.is_eligible,            # native bool → BOOLEAN
                    result.match_score,
                    result.bbbee_points,
                    result.bbbee_system,
                    result.disqualification_reason,
                    result.feedback,
                ),
            )
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
        finally:
            cur.close()
