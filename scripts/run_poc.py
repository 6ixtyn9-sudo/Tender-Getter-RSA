"""
run_poc.py - Tender Getter RSA: Proof of Concept CLI Runner

Usage:
 PYTHONPATH=src:. python scripts/run_poc.py
 Set SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY in .env to write to Supabase,
 otherwise falls back to local SQLite.

This script:
 1. Initialises the database via get_database_client() (Supabase/Postgres/SQLite).
 2. Creates a mock company profile (Sipho Electrical and Civils).
 3. Tries to sync live tenders from data.etenders.gov.za CSV,
    falls back to 3 mock tenders if offline.
 4. Runs the matching engine.
 5. Prints a formatted terminal scorecard.
"""

import sys
from pathlib import Path
from datetime import datetime, timezone

# Load .env automatically if python-dotenv is installed
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

# Ensure project root is on the path when running directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tender_getter.schemas import (
    CIDBGrading, Location, CompanyProfile, TenderOpportunity,
)
from tender_getter.matcher import match
from tender_getter.database import get_database_client
from tender_getter.source_sync import sync_csv_tenders

# ---------------------------------------------------------------------------
# Mock company
# ---------------------------------------------------------------------------

MOCK_COMPANY = CompanyProfile(
    registration_number="2019/112233/07",
    company_name="Sipho Electrical and Civils (Pty) Ltd",
    csd_number="MAAA0554433",
    bbbee_level=1,
    black_ownership_pct=75.0,
    youth_ownership_pct=30.0,
    women_ownership_pct=25.0,
    cidb_gradings=[
        CIDBGrading(class_code="EE", level=3),
        CIDBGrading(class_code="CE", level=2),
    ],
    location=Location(
        province="Gauteng",
        city="Johannesburg",
        municipality="City of Johannesburg Metropolitan Municipality",
    ),
    sectors=["Electrical Engineering", "Civil Engineering"],
    has_tax_pin=True,
    has_coida=True,
    is_active=True,
)

# Fallback mock tenders – used if live CSV sync fails / returns 0
MOCK_TENDERS = [
    TenderOpportunity(
        tender_id="COJ/EE/2026/012",
        title="Soweto Substation Transformer Maintenance",
        issuing_entity="City of Johannesburg",
        closing_date=datetime(2026, 8, 15, tzinfo=timezone.utc),
        estimated_value=1_500_000,
        required_cidb_class="EE",
        required_cidb_level=3,
        mandatory_csd=True,
        tax_compliance_required=True,
        location_target="Gauteng",
    ),
    TenderOpportunity(
        tender_id="SANRAL/CE/2026/045",
        title="N1 Bridge Joint Structural Repair",
        issuing_entity="SANRAL",
        closing_date=datetime(2026, 8, 20, tzinfo=timezone.utc),
        estimated_value=2_500_000,
        required_cidb_class="CE",
        required_cidb_level=3,
        mandatory_csd=True,
        tax_compliance_required=True,
        location_target="Gauteng",
    ),
    TenderOpportunity(
        tender_id="CPT/EE/2026/089",
        title="Cape Town Harbour Electrical Reticulation",
        issuing_entity="City of Cape Town",
        closing_date=datetime(2026, 9, 1, tzinfo=timezone.utc),
        estimated_value=800_000,
        required_cidb_class="EE",
        required_cidb_level=2,
        mandatory_csd=True,
        tax_compliance_required=True,
        location_target="Western Cape",
    ),
]

# ---------------------------------------------------------------------------
# CLI runner
# ---------------------------------------------------------------------------

def print_separator(char: str = "-", width: int = 80):
    print(char * width)

def run_poc():
    print()
    print("=" * 50)
    print("      TENDER GETTER RSA - PROOF OF CONCEPT")
    print("=" * 50)

    # Step 1: Database – Supabase / Postgres / SQLite auto-selected
    db = get_database_client()
    try:
        db.connect()
    except Exception as e:
        print(f"Database connect failed: {e}")
        return
    print(f"[1/4] Database connected: {type(db).__name__}")

    # Step 2: Save company
    db.upsert_company(MOCK_COMPANY)
    cidb_str = ", ".join(
        f"{g.class_code}{g.level}" for g in MOCK_COMPANY.cidb_gradings
    )
    print(f"[2/4] Client Profile Saved: {MOCK_COMPANY.company_name} (CIDB: {cidb_str})")

    # Step 3: Sync live tenders – try CSV bulk first
    # data.etenders.gov.za publishes daily OCDS CSVs – try recent dates
    # Fall back to mock data if offline
    live_count = 0
    try:
        # Try latest daily CSV – eTenders uses DDMMYYYY.csv
        # Try a few recent dates to find a non-empty file
        from datetime import timedelta
        today = datetime.now(timezone.utc)
        for days_back in range(0, 7):
            d = today - timedelta(days=days_back)
            csv_url = f"https://data.etenders.gov.za/Home/DownloadFile/?fileName={d.strftime('%d%m%Y')}.csv"
            try:
                live_count = sync_csv_tenders(db, csv_url)
                if live_count > 0:
                    print(f"[3/4] {live_count} live tenders synced from eTenders CSV: {csv_url}")
                    break
            except Exception:
                continue
    except Exception as e:
        print(f"Live CSV sync failed: {e}")

    # Fallback to mock tenders if live sync yielded nothing
    if live_count == 0:
        for tender in MOCK_TENDERS:
            db.upsert_tender(tender)
        print(f"[3/4] {len(MOCK_TENDERS)} mock tenders cached (live source offline).")
        tenders_to_match = MOCK_TENDERS
    else:
        # Pull back the tenders we just saved – for POC, re-match the mock company
        # against whatever came in from the CSV. Simplest: query via DB if available,
        # otherwise just use the mock list for display.
        # Here we keep it simple: if we got live data, we can't easily list it without
        # a list_tenders() method, so fall back to matching the mock set for a stable demo.
        # TODO: add list_open_tenders() to TenderDatabaseBase
        tenders_to_match = MOCK_TENDERS
        print(f"[3/4] Live tenders saved to DB – running matcher against demo set for stable output.")

    # Step 4: Match
    print("\n[4/4] Running Automated Matching Core...\n")

    print_separator()
    print(f"MATCH REPORT FOR: {MOCK_COMPANY.company_name}")
    bbbee_label = (
        "Non-Compliant" if MOCK_COMPANY.bbbee_level == 9
        else f"Level {MOCK_COMPANY.bbbee_level}"
    )
    print(
        f"Province: {MOCK_COMPANY.location.province} | "
        f"B-BBEE: {bbbee_label}"
    )
    print_separator()

    for tender in tenders_to_match:
        result = match(MOCK_COMPANY, tender)
        db.save_match(MOCK_COMPANY, result)

        status_icon = "✅ ELIGIBLE" if result.is_eligible else "❌ DISQUALIFIED"
        print(f"Tender ID : {result.tender_id}")
        print(f"Title     : {result.tender_title}")
        print(f"Issuer    : {tender.issuing_entity}")
        if tender.required_cidb_class and tender.required_cidb_level:
            print(f"Required  : CIDB Class {tender.required_cidb_class}{tender.required_cidb_level}")
        print(f"Status    : {status_icon} (Match Score: {result.match_score}%)")
        print(f"Feedback  : {result.feedback}")
        print_separator()

    db.close()
    print("\nAll results persisted.")
    print(f"DB driver: {type(db).__name__}")
    print("Day 2 milestone: COMPLETE ✅\n")

if __name__ == "__main__":
    run_poc()
