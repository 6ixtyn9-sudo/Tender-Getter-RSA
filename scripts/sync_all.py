#!/usr/bin/env python3
"""
Tender-Getter RSA – Full Source Sync CLI

Usage:
  PYTHONPATH=src:. python scripts/sync_all.py [--limit N] [--json]
"""
import argparse
import json
import logging
import sys

def main():
    ap = argparse.ArgumentParser(description="Sync all Tender-Getter RSA sources")
    ap.add_argument("--limit", type=int, default=None, help="Max tenders per source (default: all)")
    ap.add_argument("--json", action="store_true", help="Output JSON summary")
    ap.add_argument("-v", "--verbose", action="count", default=1)
    args = ap.parse_args()

    level = logging.WARNING if args.verbose == 0 else logging.INFO if args.verbose == 1 else logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")

    from tender_getter.aggregator import sync_all_sources
    summary = sync_all_sources(limit_per_source=args.limit, verbose=True)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"Tender-Getter RSA – Sync Summary")
        print(f"{'='*60}")
        print(f"Sources OK:      {summary['sources_ok']}/{summary['sources_total']}")
        print(f"Sources failed:  {summary['sources_failed']}")
        print(f"Tenders fetched: {summary['tenders_fetched']}")
        print(f"Tenders unique:  {summary['tenders_unique']}")
        print(f"Tenders upserted:{summary['tenders_upserted']}")
        print(f"Duration:        {summary['duration_s']}s")
        print()
        print(f"{'Source':<35} {'Status':<8} {'Count':>5}  {'Time'}")
        print("-"*60)
        for r in summary["per_source"]:
            print(f"{r['source_id']:<35} {r['status']:<8} {r['count']:>5}  {r['elapsed_s']}s")
        print()

    # exit non-zero if any source failed and we got zero tenders
    if summary["tenders_unique"] == 0:
        sys.exit(2)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
