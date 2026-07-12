#!/usr/bin/env python3
"""
doctor.py – Tender Getter RSA health check
Exits 0 if all checks pass, 1 otherwise. No secrets are printed.
"""
import sys
import os

# Load .env automatically if python-dotenv is installed
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

def check(label: str, fn):
    try:
        ok, msg = fn()
    except Exception as e:
        ok, msg = False, str(e)
    icon = "✅" if ok else "❌"
    print(f"{icon} {label}" + (f": {msg}" if msg else ""))
    return ok

def check_imports():
    try:
        import pydantic  # noqa
        from tender_getter import schemas, matcher  # noqa
        return True, ""
    except Exception as e:
        return False, str(e)

def check_gemini_key():
    key = os.environ.get("GEMINI_API_KEY", "")
    if key and len(key) > 20:
        return True, "present"
    return False, "missing – set GEMINI_API_KEY in .env"

def check_sources():
    try:
        from tender_getter.source_sync import load_sources
        srcs = load_sources()
        if not srcs:
            return False, "sources.yaml empty or PyYAML missing – pip install pyyaml"
        ids = [s.get("id") for s in srcs]
        if "etenders_ocds" not in ids:
            return False, f"etenders_ocds not found in {ids}"
        return True, f"{len(srcs)} sources loaded"
    except Exception as e:
        return False, str(e)

def check_etenders_api():
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
    from datetime import datetime, timezone, timedelta
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=30)
    params = f"PageNumber=1&PageSize=1&dateFrom={start.strftime('%Y-%m-%dT%H:%M:%SZ')}&dateTo={end.strftime('%Y-%m-%dT%H:%M:%SZ')}"
    urls = [
        f"https://ocds-api.etenders.gov.za/api/OCDSReleases?{params}",
        "https://data.etenders.gov.za/",
    ]
    for url in urls:
        try:
            req = Request(url, headers={"User-Agent": "Tender-Getter-RSA/doctor", "Accept": "application/json"})
            with urlopen(req, timeout=8) as r:
                if 200 <= r.status < 400:
                    host = url.split("/")[2]
                    return True, f"OK via {host}"
        except (URLError, HTTPError, Exception):
            continue
    return False, "eTenders OCDS API and data portal both unreachable"

def check_database():
    try:
        from tender_getter.database import get_database_client
        db = get_database_client()
        db.connect()
        name = type(db).__name__
        try:
            if hasattr(db, "list_open_tenders"):
                _ = db.list_open_tenders(limit=1)
        except Exception:
            pass
        db.close()
        return True, name
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Tender Getter RSA – health check")
    ap.add_argument("--probe", action="store_true",
                    help="Probe every live source to see which return REAL data vs mock/dead")
    ap.add_argument("--all", action="store_true", help="With --probe, include live:false sources too")
    args = ap.parse_args()

    if args.probe:
        from tender_getter.pipeline import probe_live_sources
        s = probe_live_sources(all_sources=args.all)
        print(f"Tender Getter RSA – source probe ({s['probed']} sources)")
        print("-" * 50)
        for st, n in sorted(s["status_counts"].items(), key=lambda x: -x[1]):
            print(f"  {st:12}: {n}")
        print(f"\n  REAL sources: {s['live_sources']} | REAL tenders: {s['total_live_tenders']}")
        print("-" * 50)
        for r in s["live"][:20]:
            print(f"  {r['count']:>5}  {r['source_id']}")
        sys.exit(0)

    print("Tender Getter RSA – doctor")
    print("-" * 40)
    results = [
        check("Python imports", check_imports),
        check("GEMINI_API_KEY", check_gemini_key),
        check("sources.yaml", check_sources),
        check("eTenders portal", check_etenders_api),
        check("Database", check_database),
    ]
    print("-" * 40)
    if all(results):
        print("All checks passed ✅")
        sys.exit(0)
    else:
        print(f"{sum(1 for r in results if not r)} check(s) failed ❌")
        sys.exit(1)
