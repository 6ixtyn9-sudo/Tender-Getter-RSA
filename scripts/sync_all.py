#!/usr/bin/env python3
"""
Tender-Getter RSA – Full Source Sync CLI

Usage:
  PYTHONPATH=src:. python scripts/sync_all.py [--limit N] [--json] [--live-only] [--sequential]

Flags:
  --limit N        Max tenders per source (default: all)
  --json           Output JSON summary instead of table
  --live-only      Skip sources flagged `live: false` in sources.yaml (or
                   in their plug-in's live attribute). Recommended for
                   daily CI runs to avoid noise from moribund entities.
  --sequential     Run sources one-at-a-time instead of ThreadPool.
  -v, --verbose    Increase logging verbosity (repeatable).
"""
import argparse
import json
import logging
import sys


def main():
    ap = argparse.ArgumentParser(description="Sync all Tender-Getter RSA sources")
    ap.add_argument("--limit", type=int, default=None, help="Max tenders per source (default: all)")
    ap.add_argument("--json", action="store_true", help="Output JSON summary")
    ap.add_argument("--live-only", action="store_true", help="Skip sources flagged live:false")
    ap.add_argument("--sequential", action="store_true", help="Run sequentially instead of ThreadPool")
    ap.add_argument("--allow-mock-fallback", action="store_true", help="DIAGNOSTIC ONLY: permit fixture fallback data")
    ap.add_argument("-v", "--verbose", action="count", default=1)
    args = ap.parse_args()

    level = logging.WARNING if args.verbose == 0 else logging.INFO if args.verbose == 1 else logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")

    from tender_getter.aggregator import sync_all_sources
    summary = sync_all_sources(
        limit_per_source=args.limit,
        verbose=True,
        use_threads=not args.sequential,
        live_only=args.live_only,
        allow_mock_fallback=args.allow_mock_fallback,
    )

    if args.json:
        print(json.dumps(summary, indent=2, default=str))
    else:
        print(f"\n{'='*60}")
        print(f"Tender-Getter RSA – Sync Summary")
        print(f"{'='*60}")
        print(f"Data mode          : {summary['data_mode']}")
        print(f"Sources candidates : {summary['class_total']}")
        print(f"Sources skipped     : {summary['sources_skipped_live_false']} (live:false)")
        print(f"Sources OK          : {summary['sources_ok']}/{summary['sources_total']}")
        print(f"Sources failed      : {summary['sources_failed']}")
        print(f"Tenders fetched     : {summary['tenders_fetched']}")
        print(f"Tenders unique      : {summary['tenders_unique']}")
        print(f"Tenders upserted    : {summary['tenders_upserted']}")
        print(f"Duration            : {summary['duration_s']}s")
        print()
        print(f"{'Source':<40} {'Status':<8} {'Count':>5}  {'Time'}")
        print("-"*70)
        for r in summary["per_source"]:
            print(f"{r['source_id']:<40} {r['status']:<8} {r['count']:>5}  {r['elapsed_s']}s")
        print()

    # exit non-zero if any source failed AND we got zero tenders
    if summary["tenders_unique"] == 0:
        sys.exit(2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
