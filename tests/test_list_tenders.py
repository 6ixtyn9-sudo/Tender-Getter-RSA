import pytest
from datetime import datetime, timezone, timedelta

from tender_getter.schemas import TenderOpportunity
from tender_getter.database import TenderDatabase

def _make_tender(tid: str, days_offset: int, province: str = "Gauteng") -> TenderOpportunity:
    return TenderOpportunity(
        tender_id=tid,
        title=f"Test {tid}",
        issuing_entity="Test Org",
        closing_date=datetime.now(timezone.utc) + timedelta(days=days_offset),
        estimated_value=100000.0,
        required_cidb_class="GB",
        required_cidb_level=1,
        mandatory_csd=True,
        tax_compliance_required=True,
        location_target=province,
    )

def test_list_open_tenders_returns_in_date_order(tmp_path):
    db_path = tmp_path / "test.db"
    db = TenderDatabase(db_path).connect()
    try:
        db.upsert_tender(_make_tender("C", 30))
        db.upsert_tender(_make_tender("A", 5))
        db.upsert_tender(_make_tender("B", 15))
        results = db.list_open_tenders(limit=10)
        assert [t.tender_id for t in results] == ["A", "B", "C"]
    finally:
        db.close()

def test_list_open_tenders_filters_by_province(tmp_path):
    db_path = tmp_path / "test2.db"
    db = TenderDatabase(db_path).connect()
    try:
        db.upsert_tender(_make_tender("GP1", 5, "Gauteng"))
        db.upsert_tender(_make_tender("WC1", 5, "Western Cape"))
        db.upsert_tender(_make_tender("NAT1", 5, "National"))
        t = _make_tender("NONE1", 6, "Gauteng")
        t.location_target = None  # type: ignore
        db.upsert_tender(t)

        gp = db.list_open_tenders(limit=10, province="Gauteng")
        ids = {t.tender_id for t in gp}
        assert "GP1" in ids
        assert "NAT1" in ids
        assert "NONE1" in ids
        assert "WC1" not in ids
    finally:
        db.close()
