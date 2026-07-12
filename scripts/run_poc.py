"""
Tender Getter RSA — Proof of Concept / full flow runner.

  ingest REAL tenders -> [enrich: open tender PDFs] -> match REAL companies -> report

This is the canonical entry point. It delegates to tender_getter.pipeline so the
logic lives in the library, not in a script.

Defaults to REAL CIDB-sourced companies (Register of Contractors) instead of a
hard-coded phantom. Use --company <profile.json> to match a single custom client.

Usage:
  PYTHONPATH=src python scripts/run_poc.py                       # full flow, real CIDB companies
  PYTHONPATH=src python scripts/run_poc.py --match-only          # reuse DB, match only
  PYTHONPATH=src python scripts/run_poc.py --enrich              # open tender PDFs + extract fields
  PYTHONPATH=src python scripts/run_poc.py --company client.json # single custom company
  PYTHONPATH=src python scripts/run_poc.py --list-companies      # show real CIDB companies
"""
import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass


def main():
    ap = argparse.ArgumentParser(description="Tender Getter RSA — POC / flow runner")
    ap.add_argument("--limit", type=int, default=None, help="Max tenders per source during ingest")
    ap.add_argument("--match-only", action="store_true", help="Skip ingestion, match on existing DB")
    ap.add_argument("--enrich", action="store_true",
                    help="Open tender PDFs and extract CIDB/value/date (Gemini for scanned)")
    ap.add_argument("--enrich-limit", type=int, default=60, help="Max tenders to enrich")
    ap.add_argument("--company", help="Path to a single company profile JSON")
    ap.add_argument("--strict", action="store_true",
                    help="Strict full matcher (hard-disqualify on unknown CSD/tax) "
                         "instead of CIDB screening mode")
    ap.add_argument("--no-reports", action="store_true", help="Skip writing .md reports")
    ap.add_argument("--match-limit", type=int, default=500)
    ap.add_argument("--workers", type=int, default=25)
    ap.add_argument("--list-companies", action="store_true",
                    help="List real CIDB companies available for matching, then exit")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )

    from tender_getter.pipeline import (
        ingest_real_tenders, enrich_open_tenders, run_pipeline_match,
        load_company, load_companies,
    )
    from tender_getter.database import get_database_client

    if args.list_companies:
        companies = load_companies()
        print(f"\n{len(companies)} REAL companies available (CIDB Register of Contractors):\n")
        for c in sorted(companies, key=lambda c: -max((g.level for g in c.cidb_gradings), default=0)):
            grades = " ".join(f"{g.class_code}{g.level}" for g in c.cidb_gradings)
            print(f"  {grades:10} {c.registration_number:14} {c.company_name}")
        return 0

    db = get_database_client()
    if hasattr(db, "connect"):
        db.connect()

    sep = "=" * 64

    # --- 1. INGEST ---
    ing = None
    if not args.match_only:
        print("\n[1/3] Ingesting REAL tenders (mock-free, capturing document URLs)…")
        ing = ingest_real_tenders(db, max_workers=args.workers)
        print(f"      → {ing['real_tenders_unique']} real tenders from "
              f"{ing['sources_live_yielding_data']} live sources")
        try:
            import sqlite3
            _c = sqlite3.connect(str(getattr(db, "db_path", "localdata/tender_getter.db")))
            n = _c.execute(
                "SELECT COUNT(*) FROM tenders WHERE raw_document_url IS NOT NULL").fetchone()[0]
            _c.close()
            print(f"      → tenders with a document URL: {n}")
        except Exception:
            pass
    else:
        print("\n[1/3] --match-only: skipping ingestion")

    # --- 2. ENRICH ---
    enr = None
    if args.enrich:
        print(f"\n[2/3] Opening & parsing tender documents (limit {args.enrich_limit})…")
        enr = enrich_open_tenders(db, limit=args.enrich_limit, use_gemini=True)
        m = enr["methods"]
        print(f"      → enriched {enr['tenders_enriched']}/{enr['tenders_considered']} tenders, "
              f"{enr['fields_extracted']} fields extracted")
        print(f"      → methods: local_regex={m.get('local_regex', 0)} "
              f"gemini_vision={m.get('gemini_vision', 0)} no_doc={m.get('no_doc', 0)} "
              f"failed={m.get('failed', 0)}")
    else:
        print("\n[2/3] Skipping enrichment (use --enrich to open tender PDFs)")

    # --- 3. MATCH real companies ---
    if args.company:
        companies = [load_company(Path(args.company))]
    else:
        companies = load_companies()
    print(f"\n[3/3] Matching {len(companies)} real CIDB companies against open tenders…")

    summary = run_pipeline_match(
        companies=companies, db=db,
        match_limit=args.match_limit, write_reports=not args.no_reports,
        partial_compliance=not args.strict,
    )

    print("\n" + sep)
    print("  TENDER GETTER RSA — RESULT")
    print(sep)
    print(f"  Companies matched : {summary['companies_matched']}")
    print(f"  Tenders evaluated : {summary['tenders_evaluated']}")
    print(f"  ✅ Screened-in    : {summary['screened_in']}")
    print(f"  ❌ Blocked (CIDB) : {summary['blocked']}")
    print(f"  Reports written   : {summary['reports_written']}")
    if ing:
        print("-" * 64)
        print(f"  Ingest : {ing['real_tenders_unique']} real tenders / "
              f"{ing['sources_live_yielding_data']} live sources")
    if enr:
        print(f"  Enrich : {enr['fields_extracted']} fields from {enr['tenders_enriched']} documents")
    print("-" * 64)
    for top in summary["top_matches"][:6]:
        print(f"  • [{top['grades']}] {top['company'][:28]:28} → {top['tender'][:28]:28} "
              f"({top['score']:.0f}%)")
    print(sep)

    if hasattr(db, "close"):
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
