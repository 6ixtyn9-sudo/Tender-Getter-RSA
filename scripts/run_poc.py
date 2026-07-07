"""
run_poc.py - Tender Getter RSA: Proof of Concept CLI Runner

Usage:
    PYTHONPATH=. python scripts/run_poc.py

This script:
  1. Initialises the local SQLite database.
  2. Creates a mock company profile (Sipho Electrical and Civils).
  3. Caches 3 mock tenders with different disqualification scenarios.
  4. Runs the matching engine against each tender.
  5. Prints a formatted terminal scorecard.
"""

import sys
from pathlib import Path
from datetime import datetime, timezone

# Ensure project root is on the path when running directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.tender_getter.schemas import (
    CIDBGrading, Location, CompanyProfile, TenderOpportunity,
)
from src.tender_getter.matcher import match
from src.tender_getter.database import TenderDatabase


# ---------------------------------------------------------------------------
# Mock data
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
    print("      TENDER GETTER RSA - PROOF OF CONCEPT        ")
    print("=" * 50)

    # Step 1: Database
    db = TenderDatabase()
    db.connect()
    print("[1/4] Local SQLite database initialized successfully.")

    # Step 2: Save company
    db.upsert_company(MOCK_COMPANY)
    cidb_str = ", ".join(
        f"{g.class_code}{g.level}" for g in MOCK_COMPANY.cidb_gradings
    )
    print(
        f"[2/4] Mock Client Profile Saved: {MOCK_COMPANY.company_name} "
        f"(CIDB: {cidb_str})"
    )

    # Step 3: Cache tenders
    for tender in MOCK_TENDERS:
        db.upsert_tender(tender)
    print(f"[3/4] {len(MOCK_TENDERS)} Live Tenders Cached in Database.")

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

    for tender in MOCK_TENDERS:
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
    print("\nAll results persisted to localdata/tender_getter.db")
    print("Day 2 milestone: COMPLETE ✅\n")


if __name__ == "__main__":
    run_poc()
