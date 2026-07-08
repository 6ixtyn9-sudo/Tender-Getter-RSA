"""
DEPRECATED: scripts/run_poc.py is superseded by scripts/sync_all.py.

As of v2.0.0, the Proof-of-Concept runner no longer hard-codes 11 sources.
It now delegates the ingestion step to the unified aggregator (which
discovers all 731 wired sources via pkgutil), then runs the matching
demo against the mock company.

To replicate the v1.x behaviour:
  PYTHONPATH=src:. python scripts/sync_all.py --live-only
  PYTHONPATH=src:. python scripts/run_poc.py   # this file

This file remains for backward compatibility with existing developer
workflows but is no longer the recommended entry point.
"""
import sys
import logging
from pathlib import Path

# Ensure src is on path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# Load .env if present
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

import argparse


# -----------------------------------------------------------------------------
# Mock company and demo tenders (kept from v1.0; used by the matching demo)
# -----------------------------------------------------------------------------

MOCK_COMPANY = None  # lazy import to avoid top-level Pydantic cost


def _build_mock_company():
    from tender_getter.schemas import CIDBGrading, Location, CompanyProfile
    return CompanyProfile(
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


# Demo tenders – kept as fallback if the DB yields nothing.
def _build_demo_tenders():
    from datetime import datetime, timezone
    from tender_getter.schemas import TenderOpportunity
    return [
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


# -----------------------------------------------------------------------------
# Main: delegate ingestion to aggregator, then run the match demo
# -----------------------------------------------------------------------------

def print_separator(char: str = "-", width: int = 80):
    print(char * width)


def main():
    parser = argparse.ArgumentParser(
        description="Tender-Getter RSA – Proof of Concept (delegates to aggregator)"
    )
    parser.add_argument("--limit", type=int, default=None, help="Max tenders per source")
    parser.add_argument("--live-only", action="store_true", help="Skip sources flagged live:false")
    parser.add_argument("--match-only", action="store_true", help="Skip ingestion, run match demo only")
    args = parser.parse_args()

    print()
    print("=" * 50)
    print("      TENDER GETTER RSA - PROOF OF CONCEPT")
    print("=" * 50)
    print("  (deprecated – delegates to scripts/sync_all.py)")
    print()

    # Step 1-3: Sync via aggregator (replaces v1.x hard-coded 11 sources).
    if not args.match_only:
        from tender_getter.aggregator import sync_all_sources
        from tender_getter.database import get_database_client
        logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
        print("[1/4] Running unified aggregator (all 731 sources, threaded)…")
        summary = sync_all_sources(limit_per_source=args.limit, live_only=args.live_only)
        print(f"        → {summary['tenders_unique']} unique tenders from "
              f"{summary['sources_ok']}/{summary['sources_total']} sources in "
              f"{summary['duration_s']}s "
              f"({summary['sources_skipped_live_false']} skipped via live:false)")
    else:
        summary = None
        print("[1/4] --match-only – skipping ingestion")

    # Step 2: Save the mock company.
    from tender_getter.database import get_database_client
    db = get_database_client()
    try:
        db.connect()
    except Exception as e:
        print(f"Database connect failed: {e}")
        return 1
    print(f"[2/4] Database connected: {type(db).__name__}")

    company = _build_mock_company()
    db.upsert_company(company)
    cidb_str = ", ".join(f"{g.class_code}{g.level}" for g in company.cidb_gradings)
    print(f"[3/4] Client Profile Saved: {company.company_name} (CIDB: {cidb_str})")

    # Step 3: Pull tenders from DB (or fall back to mocks).
    tenders_to_match = []
    used_mocks = False
    try:
        tenders_to_match = db.list_open_tenders(limit=25, province=company.location.province)
        if not tenders_to_match:
            tenders_to_match = db.list_open_tenders(limit=25)
    except Exception as e:
        print(f"  list_open_tenders failed: {e}")

    if not tenders_to_match:
        tenders_to_match = _build_demo_tenders()
        used_mocks = True
        print(f"[4/4] {len(tenders_to_match)} demo tenders cached (live sources yielded 0).")
    else:
        print(f"[4/4] {len(tenders_to_match)} open tenders loaded from DB")

    # Step 4: Run matching.
    from tender_getter.matcher import match
    print_separator()
    print(f"MATCH REPORT FOR: {company.company_name}")
    bbbee_label = "Non-Compliant" if company.bbbee_level == 9 else f"Level {company.bbbee_level}"
    print(f"Province: {company.location.province} | B-BBEE: {bbbee_label}")
    print_separator()

    eligible_count = 0
    for tender in tenders_to_match[:25]:
        result = match(company, tender)
        db.save_match(company, result)
        if result.is_eligible:
            eligible_count += 1
        status_icon = "✅ ELIGIBLE" if result.is_eligible else "❌ DISQUALIFIED"
        print(f"Tender ID : {result.tender_id}")
        print(f"Title     : {result.tender_title}")
        print(f"Status    : {status_icon} (Match Score: {result.match_score}%)")
        print(f"Feedback  : {result.feedback}")
        print_separator()

    db.close()
    print(f"\nEvaluated {len(tenders_to_match[:25])} tenders – {eligible_count} eligible")
    print(f"DB driver: {type(db).__name__}")
    print(f"Results persisted to matches table")
    if used_mocks:
        print("Note: using demo tenders (live sources yielded 0 rows this run).")
    print("Day 2 milestone: COMPLETE ✅ (deprecated entry point)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
