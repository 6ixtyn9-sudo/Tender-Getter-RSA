import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Load .env automatically if python-dotenv is installed
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

# Ensure src is on path when running directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tender_getter.schemas import (
    CIDBGrading, Location, CompanyProfile, TenderOpportunity,
)
from tender_getter.matcher import match
from tender_getter.database import get_database_client
from tender_getter.source_sync import sync_live_tenders, sync_csv_tenders

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

# Fallback mock tenders – used if live sources yield 0
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
    cidb_str = ", ".join(f"{g.class_code}{g.level}" for g in MOCK_COMPANY.cidb_gradings)
    print(f"[2/4] Client Profile Saved: {MOCK_COMPANY.company_name} (CIDB: {cidb_str})")

    # Step 3: Sync live tenders
    ocds_count = 0
    csv_count = 0

    # 3a – OCDS API first (usually most current)
    try:
        ocds_count = sync_live_tenders(db, max_pages=2)
        if ocds_count > 0:
            print(f"[3/4] OCDS API: {ocds_count} tenders synced")
    except Exception as e:
        print(f"  OCDS sync failed: {e}")

    # 3b – CSV bulk fallback / supplement – eTenders CSV dumps are typically monthly
    # Try: last 90 days weekly, plus first-of-month for last 6 months
    if ocds_count == 0:
        today = datetime.now(timezone.utc)
        tried = set()
        dates_to_try = []
        # weekly backoff, 90 days
        for days_back in range(0, 90, 7):
            dates_to_try.append(today - timedelta(days=days_back))
        # first-of-month, last 6 months
        for m in range(0, 6):
            year = today.year
            month = today.month - m
            while month < 1:
                month += 12
                year -= 1
            dates_to_try.append(datetime(year, month, 1, tzinfo=timezone.utc))
        
        for d in dates_to_try:
            csv_url = f"https://data.etenders.gov.za/Home/DownloadFile/?fileName={d.strftime('%d%m%Y')}.csv"
            if csv_url in tried:
                continue
            tried.add(csv_url)
            try:
                n = sync_csv_tenders(db, csv_url)
                csv_count += n
                if n > 0:
                    print(f"  CSV hit: {d.strftime('%Y-%m-%d')} → {n} tenders")
                    # keep going – collect from multiple files, but stop after 3 successful hits to avoid API burn
                    if csv_count >= 50:
                        break
            except Exception:
                continue
        
        if csv_count > 0:
            print(f"[3/4] CSV bulk: {csv_count} total tenders synced from {len(tried)} URLs probed")
    
    # 3c – SANRAL Scraping Ingestion Vector (New in Patch G!)
    sanral_count = 0
    try:
        from tender_getter.sources import SANRALSource
        sanral_src = SANRALSource()
        sanral_tenders = sanral_src.fetch()
        for tender in sanral_tenders:
            db.upsert_tender(tender)
            sanral_count += 1
        if sanral_count > 0:
            print(f"[3/4] SANRAL Scraper: {sanral_count} high-value civil engineering tenders synced")
    except Exception as e:
        print(f"  SANRAL sync failed: {e}")

    # 3d – Eskom Scraping Ingestion Vector (New!)
    eskom_count = 0
    try:
        from tender_getter.sources import EskomSource
        eskom_src = EskomSource()
        eskom_tenders = eskom_src.fetch()
        for tender in eskom_tenders:
            db.upsert_tender(tender)
            eskom_count += 1
        if eskom_count > 0:
            print(f"[3/4] Eskom Scraper: {eskom_count} high-value energy & engineering tenders synced")
    except Exception as e:
        print(f"  Eskom sync failed: {e}")

    # 3e – Gauteng eTenders Scraping Ingestion Vector (New!)
    gauteng_count = 0
    try:
        from tender_getter.sources import GautengSource
        gauteng_src = GautengSource()
        gauteng_tenders = gauteng_src.fetch()
        for tender in gauteng_tenders:
            db.upsert_tender(tender)
            gauteng_count += 1
        if gauteng_count > 0:
            print(f"[3/4] Gauteng eTenders: {gauteng_count} provincial tenders synced")
    except Exception as e:
        print(f"  Gauteng eTenders sync failed: {e}")

    # 3f – CIDB i-Tender Scraping Ingestion Vector (New!)
    cidb_count = 0
    try:
        from tender_getter.sources import CIDBSource
        cidb_src = CIDBSource()
        cidb_tenders = cidb_src.fetch()
        for tender in cidb_tenders:
            db.upsert_tender(tender)
            cidb_count += 1
        if cidb_count > 0:
            print(f"[3/4] CIDB i-Tenders: {cidb_count} national construction tenders synced")
    except Exception as e:
        print(f"  CIDB sync failed: {e}")

    # 3g – Western Cape eTenders Scraping Ingestion Vector (New!)
    westerncape_count = 0
    try:
        from tender_getter.sources import WesternCapeSource
        wc_src = WesternCapeSource()
        wc_tenders = wc_src.fetch()
        for tender in wc_tenders:
            db.upsert_tender(tender)
            westerncape_count += 1
        if westerncape_count > 0:
            print(f"[3/4] Western Cape eTenders: {westerncape_count} provincial tenders synced")
    except Exception as e:
        print(f"  Western Cape sync failed: {e}")

    # 3h – SITA Scraping Ingestion Vector (New!)
    sita_count = 0
    try:
        from tender_getter.sources import SITASource
        sita_src = SITASource()
        sita_tenders = sita_src.fetch()
        for tender in sita_tenders:
            db.upsert_tender(tender)
            sita_count += 1
        if sita_count > 0:
            print(f"[3/4] SITA Scraper: {sita_count} high-value government ICT tenders synced")
    except Exception as e:
        print(f"  SITA sync failed: {e}")

    # 3i – Transnet Scraping Ingestion Vector (New!)
    transnet_count = 0
    try:
        from tender_getter.sources import TransnetSource
        transnet_src = TransnetSource()
        transnet_tenders = transnet_src.fetch()
        for tender in transnet_tenders:
            db.upsert_tender(tender)
            transnet_count += 1
        if transnet_count > 0:
            print(f"[3/4] Transnet Scraper: {transnet_count} high-value freight & transport tenders synced")
    except Exception as e:
        print(f"  Transnet sync failed: {e}")

    # 3j – City of Cape Town Scraping Ingestion Vector (New!)
    capetown_count = 0
    try:
        from tender_getter.sources import CapeTownSource
        coct_src = CapeTownSource()
        coct_tenders = coct_src.fetch()
        for tender in coct_tenders:
            db.upsert_tender(tender)
            capetown_count += 1
        if capetown_count > 0:
            print(f"[3/4] City of Cape Town Scraper: {capetown_count} municipal tenders synced")
    except Exception as e:
        print(f"  Cape Town sync failed: {e}")

    # 3k – KZN Treasury Scraping Ingestion Vector (New!)
    kzn_count = 0
    try:
        from tender_getter.sources import KZNSource
        kzn_src = KZNSource()
        kzn_tenders = kzn_src.fetch()
        for tender in kzn_tenders:
            db.upsert_tender(tender)
            kzn_count += 1
        if kzn_count > 0:
            print(f"[3/4] KZN Treasury Scraper: {kzn_count} provincial tenders synced")
    except Exception as e:
        print(f"  KZN Treasury sync failed: {e}")

    total_synced = ocds_count + csv_count + sanral_count + eskom_count + gauteng_count + cidb_count + westerncape_count + sita_count + transnet_count + capetown_count + kzn_count

    # Pull open tenders from DB – real data path
    try:
        # Try province-filtered first, fall back to national
        tenders_to_match = db.list_open_tenders(limit=25, province=MOCK_COMPANY.location.province)
        if not tenders_to_match:
            tenders_to_match = db.list_open_tenders(limit=25)
    except Exception as e:
        print(f"  list_open_tenders failed: {e}")
        tenders_to_match = []

    # Fallback to mocks if DB is empty
    used_mocks = False
    if not tenders_to_match:
        for tender in MOCK_TENDERS:
            db.upsert_tender(tender)
        tenders_to_match = MOCK_TENDERS
        used_mocks = True
        print(f"[3/4] {len(MOCK_TENDERS)} mock tenders cached (live sources yielded 0).")
    else:
        src = f"OCDS:{ocds_count} CSV:{csv_count} SANRAL:{sanral_count} ESKOM:{eskom_count} GAUTENG:{gauteng_count} CIDB:{cidb_count} WC:{westerncape_count} SITA:{sita_count} TRANSNET:{transnet_count} COCT:{capetown_count} KZN:{kzn_count}" if total_synced > 0 else "DB cache"
        print(f"[3/4] {len(tenders_to_match)} open tenders loaded from DB [{src}]")

    # Step 4: Match
    print("\n[4/4] Running Automated Matching Core...\n")

    print_separator()
    print(f"MATCH REPORT FOR: {MOCK_COMPANY.company_name}")
    bbbee_label = "Non-Compliant" if MOCK_COMPANY.bbbee_level == 9 else f"Level {MOCK_COMPANY.bbbee_level}"
    print(f"Province: {MOCK_COMPANY.location.province} | B-BBEE: {bbbee_label}")
    if not used_mocks and total_synced > 0:
        print(f"Source: Live – {total_synced} tenders ingested this run")
    print_separator()

    eligible_count = 0
    for tender in tenders_to_match[:25]:  # cap output at 25 for readability
        result = match(MOCK_COMPANY, tender)
        db.save_match(MOCK_COMPANY, result)
        if result.is_eligible:
            eligible_count += 1

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
    print(f"\nEvaluated {len(tenders_to_match[:25])} tenders – {eligible_count} eligible")
    print(f"DB driver: {type(db).__name__}")
    print(f"Results persisted to matches table")
    print("Day 2 milestone: COMPLETE ✅\n")

if __name__ == "__main__":
    run_poc()
