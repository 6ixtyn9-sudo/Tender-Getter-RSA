import os
import pytest
from datetime import datetime, timezone
from src.tender_getter.source_sync import parse_ocds_release_to_tender, re_search_cidb
from src.tender_getter.lead_harvester import import_suppliers_from_csv
from src.tender_getter.database import TenderDatabase

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
