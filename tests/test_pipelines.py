import os
import pytest
from datetime import datetime, timezone
from tender_getter.source_sync import parse_ocds_release_to_tender, re_search_cidb
from tender_getter.lead_harvester import import_suppliers_from_csv
from tender_getter.database import TenderDatabase
from tender_getter.sources.common import parse_closing_date, parse_html_table

@pytest.fixture(autouse=True)
def clean_db():
    db = TenderDatabase()
    # Safely clear tables using context
    with db:
        db._conn.execute("DELETE FROM tenders")
        db._conn.execute("DELETE FROM company_profiles")
        db._conn.execute("DELETE FROM cidb_gradings")
    yield

def test_re_search_cidb():
    assert re_search_cidb("Requires 3CE grading and local labor") == ("3", "CE")
    assert re_search_cidb("Renovation of block Level 4GB contractor only") == ("4", "GB")
    assert re_search_cidb("9EP substation works") == ("9", "EP")
    assert re_search_cidb("No CIDB grading required") is None

def test_parse_ocds_release_to_tender():
    mock_release = {
        "ocid": "ocds-tender-12345",
        "buyer": {"name": "Gauteng Department of Infrastructure Development"},
        "tender": {
            "title": "Design and Construct of Johannesburg North Clinic (Required CIDB: 5GB)",
            "description": "Localized project in GP",
            "tenderPeriod": {
                "endDate": "2026-08-30T11:00:00Z"
            },
            "value": {
                "amount": 9500000.0
            }
        }
    }
    
    tender = parse_ocds_release_to_tender(mock_release)
    assert tender is not None
    assert tender.tender_id == "ocds-tender-12345"
    assert tender.issuing_entity == "Gauteng Department of Infrastructure Development"
    assert tender.required_cidb_class == "GB"
    assert tender.required_cidb_level == 5
    assert tender.location_target == "Gauteng"
    assert tender.estimated_value == 9500000.0

def test_import_suppliers_from_csv():
    csv_data = """company_name,registration_number,csd_number,bbbee_level,black_ownership_pct,province,city,sectors,cidb_codes,has_tax_pin
Sipho Electrics,2024/111111/07,MAAA0111111,1,100.0,Gauteng,Johannesburg,Electrical;Construction,3EE;2CE,true
Khumalo Cleaners,2023/222222/07,MAAA0222222,2,51.0,KwaZulu-Natal,Durban,Cleaning,None,true
"""
    count = import_suppliers_from_csv(csv_data)
    assert count == 2
    
    with TenderDatabase() as db:
        comp = db._conn.execute("SELECT * FROM company_profiles WHERE registration_number = '2024/111111/07'").fetchone()
        assert comp is not None
        assert comp["company_name"] == "Sipho Electrics"


# ---------------------------------------------------------------------------
# Red Team & Stress-Test Pipeline Resilience Unit Tests
# ---------------------------------------------------------------------------

def test_verbal_and_numeric_date_resilience():
    # Verbal format parsing
    d1 = parse_closing_date("30 August 2026")
    assert d1.year == 2026
    assert d1.month == 8
    assert d1.day == 30

    d2 = parse_closing_date("15 Sep 2026")
    assert d2.year == 2026
    assert d2.month == 9
    assert d2.day == 15

    # Numeric slash/dash format parsing
    d3 = parse_closing_date("10/12/2026")
    assert d3.year == 2026
    assert d3.month == 12
    assert d3.day == 10

    d4 = parse_closing_date("01-05-2026")
    assert d4.year == 2026
    assert d4.month == 5
    assert d4.day == 1

    # Safe fallback on invalid dates
    d5 = parse_closing_date("invalid-date-completely")
    assert d5.year == 2099
    assert d5.month == 12
    assert d5.day == 31


def test_cidb_false_positive_memory_filtering():
    # SITA / IT tenders mentioning computer memory must not be misidentified as CIDB construction grades
    t1 = re_search_cidb("SITA requires 8 GB RAM and 256 GB SSD storage")
    assert t1 is None  # "8 GB" and "256 GB" are memory descriptions, not CIDB Grade 8 / Grade 2 General Building

    # True CIDB descriptions must still parse perfectly
    t2 = re_search_cidb("Construction of School Clinic (Gauteng, Grade 5GB)")
    assert t2 == ("5", "GB")

    t3 = re_search_cidb("Routine Road Maintenance (Grade 7CE)")
    assert t3 == ("7", "CE")


def test_html_table_parser_resilience_to_nested_tags():
    # Simple regex row parsing breaks when tags are nested or unclosed. Our HTML table parser must survive this perfectly.
    nested_html = """
    <table>
        <tr>
            <td><strong>NRA R.003-020</strong></td>
            <td>Routine Road Maintenance with <span class="badge">Grade 7CE</span></td>
            <td>30 August 2026</td>
        </tr>
        <tr>
            <td>CIDB/2026/001</td>
            <td>Upgrade of pipelines in Limpopo</td>
            <td>15/09/2026</td>
        </tr>
    </table>
    """
    rows = parse_html_table(nested_html)
    assert len(rows) == 2
    
    # First row check
    r1 = rows[0]
    assert r1[0] == "NRA R.003-020"
    assert "Routine Road Maintenance with Grade 7CE" in r1[1]
    assert r1[2] == "30 August 2026"

    # Second row check
    r2 = rows[1]
    assert r2[0] == "CIDB/2026/001"
    assert r2[1] == "Upgrade of pipelines in Limpopo"
    assert r2[2] == "15/09/2026"
