"""
test_database.py - Unit tests for the Tender Getter RSA dual-database adapter layer.

Coverage:
  - TenderDatabaseBase: abstract contract enforced at class instantiation.
  - get_database_client(): returns correct driver based on SUPABASE_DB_URL env var.
  - TenderDatabase (SQLite): full upsert round-trips for company, tender, and match.
  - PostgresDatabase: correct driver type returned when env var is set (no live connection).
  - Both drivers satisfy TenderDatabaseBase (isinstance check).
"""

import os
import json
import pytest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock

from tender_getter.database_base import TenderDatabaseBase
from tender_getter.database import TenderDatabase, get_database_client
from tender_getter.schemas import (
    CIDBGrading, Location, CompanyProfile, TenderOpportunity, MatchResult,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tmp_db(tmp_path) -> TenderDatabase:
    """
    Provides a fresh, isolated SQLite TenderDatabase for each test.
    Uses pytest's tmp_path to avoid touching localdata/tender_getter.db.
    """
    db = TenderDatabase(db_path=tmp_path / "test_tender_getter.db")
    with db:
        yield db


@pytest.fixture
def sample_company() -> CompanyProfile:
    return CompanyProfile(
        registration_number="2019/TEST001/07",
        company_name="Mthembu Civil Works (Pty) Ltd",
        csd_number="MAAA9900001",
        bbbee_level=2,
        black_ownership_pct=51.0,
        youth_ownership_pct=30.0,
        women_ownership_pct=25.0,
        cidb_gradings=[
            CIDBGrading(class_code="CE", level=4),
            CIDBGrading(class_code="GB", level=3),
        ],
        location=Location(
            province="KwaZulu-Natal",
            city="Durban",
            municipality="eThekwini Metropolitan Municipality",
        ),
        sectors=["Civil", "Building"],
        has_tax_pin=True,
        has_coida=True,
    )


@pytest.fixture
def sample_tender() -> TenderOpportunity:
    return TenderOpportunity(
        tender_id="KZN/CE/2026/099",
        title="Construction of Umlazi Community Hall",
        issuing_entity="eThekwini Municipality",
        closing_date=datetime(2026, 9, 15, 11, 0, tzinfo=timezone.utc),
        estimated_value=5_500_000.0,
        required_cidb_class="CE",
        required_cidb_level=4,
        mandatory_csd=True,
        tax_compliance_required=True,
        location_target="KwaZulu-Natal",
    )


@pytest.fixture
def sample_match(sample_company, sample_tender) -> MatchResult:
    return MatchResult(
        company_name=sample_company.company_name,
        tender_id=sample_tender.tender_id,
        tender_title=sample_tender.title,
        is_eligible=True,
        match_score=98.0,
        bbbee_points=18.0,
        bbbee_max_points=20.0,
        bbbee_system="80/20",
        disqualification_reason=None,
        feedback="All gates passed. B-BBEE Level 2 awarded 18/20 preference points.",
    )


# ---------------------------------------------------------------------------
# 1. Abstract base class: interface contract
# ---------------------------------------------------------------------------

class TestAbstractBaseContract:
    """TenderDatabaseBase must raise TypeError for any incomplete subclass."""

    def test_cannot_instantiate_base_directly(self):
        with pytest.raises(TypeError):
            TenderDatabaseBase()  # type: ignore[abstract]

    def test_concrete_missing_one_method_raises(self):
        """A subclass that skips save_match must not be instantiable."""
        class Incomplete(TenderDatabaseBase):
            def connect(self): ...
            def close(self): ...
            def upsert_company(self, c): ...
            def upsert_tender(self, t): ...
            # save_match intentionally omitted

        with pytest.raises(TypeError):
            Incomplete()

    def test_sqlite_driver_satisfies_base(self):
        """TenderDatabase must be a proper subclass of TenderDatabaseBase."""
        assert issubclass(TenderDatabase, TenderDatabaseBase)


# ---------------------------------------------------------------------------
# 2. Factory: get_database_client()
# ---------------------------------------------------------------------------

class TestGetDatabaseClient:
    """Driver selection based on SUPABASE_DB_URL environment variable."""

    def test_returns_sqlite_when_env_unset(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("SUPABASE_DB_URL", None)
            client = get_database_client()
        assert isinstance(client, TenderDatabase)

    def test_returns_sqlite_when_env_empty_string(self):
        with patch.dict(os.environ, {"SUPABASE_DB_URL": ""}, clear=False):
            client = get_database_client()
        # Empty string is falsy — should still fall back to SQLite
        assert isinstance(client, TenderDatabase)

    def test_returns_postgres_when_env_set(self):
        """PostgresDatabase is returned when SUPABASE_DB_URL is non-empty."""
        from tender_getter.database_postgres import PostgresDatabase

        fake_dsn = "postgresql://postgres:secret@db.example.supabase.co:5432/postgres"
        with patch.dict(os.environ, {"SUPABASE_DB_URL": fake_dsn}):
            client = get_database_client()

        assert isinstance(client, PostgresDatabase)

    def test_postgres_client_satisfies_base(self):
        """PostgresDatabase must satisfy the TenderDatabaseBase interface."""
        from tender_getter.database_postgres import PostgresDatabase
        assert issubclass(PostgresDatabase, TenderDatabaseBase)

    def test_postgres_not_connected_without_calling_connect(self):
        """Calling upsert before connect() must raise AssertionError."""
        from tender_getter.database_postgres import PostgresDatabase

        pg = PostgresDatabase("postgresql://fake:fake@localhost:5432/fake")
        with pytest.raises(AssertionError, match="connect\\(\\)"):
            pg.upsert_company(MagicMock())


# ---------------------------------------------------------------------------
# 3. TenderDatabase (SQLite): company upsert round-trip
# ---------------------------------------------------------------------------

class TestSQLiteCompanyUpsert:

    def test_insert_new_company(self, tmp_db, sample_company):
        tmp_db.upsert_company(sample_company)
        row = tmp_db._conn.execute(
            "SELECT * FROM company_profiles WHERE registration_number = ?",
            (sample_company.registration_number,),
        ).fetchone()
        assert row is not None
        assert row["company_name"] == "Mthembu Civil Works (Pty) Ltd"

    def test_sectors_stored_as_json(self, tmp_db, sample_company):
        tmp_db.upsert_company(sample_company)
        row = tmp_db._conn.execute(
            "SELECT sectors FROM company_profiles WHERE registration_number = ?",
            (sample_company.registration_number,),
        ).fetchone()
        stored = json.loads(row["sectors"])
        assert stored == ["Civil", "Building"]

    def test_cidb_gradings_stored(self, tmp_db, sample_company):
        tmp_db.upsert_company(sample_company)
        rows = tmp_db._conn.execute(
            "SELECT class_code, level FROM cidb_gradings WHERE registration_number = ?",
            (sample_company.registration_number,),
        ).fetchall()
        codes = {r["class_code"]: r["level"] for r in rows}
        assert codes == {"CE": 4, "GB": 3}

    def test_update_existing_company(self, tmp_db, sample_company):
        tmp_db.upsert_company(sample_company)
        sample_company.bbbee_level = 1
        sample_company.company_name = "Mthembu Civil Works Updated"
        tmp_db.upsert_company(sample_company)

        row = tmp_db._conn.execute(
            "SELECT bbbee_level, company_name FROM company_profiles WHERE registration_number = ?",
            (sample_company.registration_number,),
        ).fetchone()
        assert row["bbbee_level"] == 1
        assert row["company_name"] == "Mthembu Civil Works Updated"

    def test_cidb_gradings_replaced_on_update(self, tmp_db, sample_company):
        """After an update, stale CIDB gradings must not linger."""
        tmp_db.upsert_company(sample_company)
        # Remove GB grading, add ME grading
        sample_company.cidb_gradings = [
            CIDBGrading(class_code="CE", level=5),
            CIDBGrading(class_code="ME", level=2),
        ]
        tmp_db.upsert_company(sample_company)

        rows = tmp_db._conn.execute(
            "SELECT class_code FROM cidb_gradings WHERE registration_number = ?",
            (sample_company.registration_number,),
        ).fetchall()
        codes = {r["class_code"] for r in rows}
        assert codes == {"CE", "ME"}
        assert "GB" not in codes

    def test_boolean_fields_stored_correctly(self, tmp_db, sample_company):
        tmp_db.upsert_company(sample_company)
        row = tmp_db._conn.execute(
            "SELECT has_tax_pin, has_coida, is_active FROM company_profiles WHERE registration_number = ?",
            (sample_company.registration_number,),
        ).fetchone()
        # SQLite stores booleans as integers (1/0)
        assert row["has_tax_pin"] == 1
        assert row["has_coida"] == 1
        assert row["is_active"] == 1

    def test_optional_municipality_stored(self, tmp_db, sample_company):
        tmp_db.upsert_company(sample_company)
        row = tmp_db._conn.execute(
            "SELECT municipality FROM company_profiles WHERE registration_number = ?",
            (sample_company.registration_number,),
        ).fetchone()
        assert row["municipality"] == "eThekwini Metropolitan Municipality"

    def test_company_with_no_municipality(self, tmp_db):
        company = CompanyProfile(
            registration_number="2020/NOMUNIC/07",
            company_name="No Municipality Co",
            bbbee_level=5,
            black_ownership_pct=0.0,
            location=Location(province="Western Cape", city="Cape Town"),
            sectors=[],
            has_tax_pin=False,
            has_coida=False,
        )
        tmp_db.upsert_company(company)
        row = tmp_db._conn.execute(
            "SELECT municipality FROM company_profiles WHERE registration_number = ?",
            (company.registration_number,),
        ).fetchone()
        assert row["municipality"] is None


# ---------------------------------------------------------------------------
# 4. TenderDatabase (SQLite): tender upsert round-trip
# ---------------------------------------------------------------------------

class TestSQLiteTenderUpsert:

    def test_insert_new_tender(self, tmp_db, sample_tender):
        tmp_db.upsert_tender(sample_tender)
        row = tmp_db._conn.execute(
            "SELECT * FROM tenders WHERE tender_id = ?",
            (sample_tender.tender_id,),
        ).fetchone()
        assert row is not None
        assert row["title"] == "Construction of Umlazi Community Hall"
        assert row["estimated_value"] == pytest.approx(5_500_000.0)

    def test_closing_date_stored_as_iso_string(self, tmp_db, sample_tender):
        tmp_db.upsert_tender(sample_tender)
        row = tmp_db._conn.execute(
            "SELECT closing_date FROM tenders WHERE tender_id = ?",
            (sample_tender.tender_id,),
        ).fetchone()
        assert "2026-09-15" in row["closing_date"]

    def test_update_existing_tender(self, tmp_db, sample_tender):
        tmp_db.upsert_tender(sample_tender)
        sample_tender.estimated_value = 7_000_000.0
        tmp_db.upsert_tender(sample_tender)
        row = tmp_db._conn.execute(
            "SELECT estimated_value FROM tenders WHERE tender_id = ?",
            (sample_tender.tender_id,),
        ).fetchone()
        assert row["estimated_value"] == pytest.approx(7_000_000.0)

    def test_optional_fields_null_by_default(self, tmp_db):
        tender = TenderOpportunity(
            tender_id="NATIONAL/2026/001",
            title="General Works",
            issuing_entity="National Treasury",
            closing_date=datetime(2026, 12, 31, tzinfo=timezone.utc),
        )
        tmp_db.upsert_tender(tender)
        row = tmp_db._conn.execute(
            "SELECT estimated_value, required_cidb_class, raw_document_url "
            "FROM tenders WHERE tender_id = ?",
            (tender.tender_id,),
        ).fetchone()
        assert row["estimated_value"] is None
        assert row["required_cidb_class"] is None
        assert row["raw_document_url"] is None


# ---------------------------------------------------------------------------
# 5. TenderDatabase (SQLite): match/audit round-trip
# ---------------------------------------------------------------------------

class TestSQLiteMatchSave:

    def _setup(self, db, company, tender):
        """Insert required FK rows before testing matches."""
        db.upsert_company(company)
        db.upsert_tender(tender)

    def test_save_match_creates_row(self, tmp_db, sample_company, sample_tender, sample_match):
        self._setup(tmp_db, sample_company, sample_tender)
        tmp_db.save_match(sample_company, sample_match)

        row = tmp_db._conn.execute(
            "SELECT * FROM matches WHERE company_reg_number = ? AND tender_id = ?",
            (sample_company.registration_number, sample_tender.tender_id),
        ).fetchone()
        assert row is not None
        assert row["is_eligible"] == 1
        assert row["match_score"] == pytest.approx(98.0)
        assert row["bbbee_system"] == "80/20"

    def test_save_match_updates_on_conflict(self, tmp_db, sample_company, sample_tender, sample_match):
        self._setup(tmp_db, sample_company, sample_tender)
        tmp_db.save_match(sample_company, sample_match)

        # Re-evaluate with different score
        sample_match.match_score = 85.0
        sample_match.bbbee_points = 14.0
        tmp_db.save_match(sample_company, sample_match)

        rows = tmp_db._conn.execute(
            "SELECT match_score, bbbee_points FROM matches "
            "WHERE company_reg_number = ? AND tender_id = ?",
            (sample_company.registration_number, sample_tender.tender_id),
        ).fetchall()
        # Must be exactly one row (upsert, not duplicate)
        assert len(rows) == 1
        assert rows[0]["match_score"] == pytest.approx(85.0)
        assert rows[0]["bbbee_points"] == pytest.approx(14.0)

    def test_ineligible_match_stored_correctly(
        self, tmp_db, sample_company, sample_tender
    ):
        self._setup(tmp_db, sample_company, sample_tender)
        disqualified = MatchResult(
            company_name=sample_company.company_name,
            tender_id=sample_tender.tender_id,
            tender_title=sample_tender.title,
            is_eligible=False,
            match_score=0.0,
            bbbee_points=0.0,
            bbbee_max_points=20.0,
            bbbee_system="80/20",
            disqualification_reason="CSD number missing.",
            feedback="GATE 1 FAILED: CSD number missing.",
        )
        tmp_db.save_match(sample_company, disqualified)

        row = tmp_db._conn.execute(
            "SELECT is_eligible, disqualification_reason FROM matches "
            "WHERE company_reg_number = ?",
            (sample_company.registration_number,),
        ).fetchone()
        assert row["is_eligible"] == 0
        assert row["disqualification_reason"] == "CSD number missing."
