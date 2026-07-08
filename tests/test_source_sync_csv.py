import io
import tempfile
import os
from datetime import timezone

import pytest

from tender_getter.source_sync import parse_csv_row_to_tender, sync_csv_tenders, load_sources
from tender_getter.database import TenderDatabase


def test_parse_csv_row_minimal():
    row = {
        "tender_id": "TEST/2026/001",
        "tender_title": "Soweto Electrical Maintenance EE3 Gauteng",
        "buyer_name": "City of Johannesburg",
        "tender_period_enddate": "2026-08-15 11:00:00",
        "tender_description": "CIDB 3EE required",
    }
    t = parse_csv_row_to_tender(row)
    assert t is not None
    assert t.tender_id == "TEST/2026/001"
    assert t.required_cidb_class == "EE"
    assert t.required_cidb_level == 3
    assert t.location_target == "Gauteng"


def test_sync_csv_tenders_sqlite(tmp_path):
    csv_content = """tender_id,tender_title,buyer_name,tender_period_enddate,tender_description
COJ/EE/2026/012,Soweto Substation Transformer Maintenance,City of Johannesburg,2026-09-01 11:00:00,EE3 Gauteng
CPT/EE/2026/089,Cape Town Harbour Electrical Reticulation,City of Cape Town,2026-09-15 11:00:00,EE2 Western Cape
"""
    csv_file = tmp_path / "tenders.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    db_path = tmp_path / "test.db"
    db = TenderDatabase(db_path).connect()
    try:
        n = sync_csv_tenders(db, str(csv_file))
        assert n == 2
    finally:
        db.close()


def test_load_sources_returns_list():
    srcs = load_sources()
    assert isinstance(srcs, list)
    if srcs:
        # If yaml is installed, check structure (alphabetically sorted)
        ids = [s["id"] for s in srcs]
        assert "etenders_ocds" in ids
        assert "etenders_csv" in ids
        assert "cidb_itender" in ids
        # Every entry has the required fields
        for s in srcs:
            assert "id" in s
            assert "name" in s
            assert "url" in s
            assert "live" in s
