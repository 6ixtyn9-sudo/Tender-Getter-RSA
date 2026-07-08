#!/usr/bin/env python3
"""
doctor.py – Tender Getter RSA health check
Exits 0 if all checks pass, 1 otherwise. No secrets are printed.

Checks:
  1. Python / package imports
  2. GEMINI_API_KEY present
  3. sources.yaml loads and contains etenders_ocds
  4. eTenders OCDS API reachable
  5. Database client connects (Supabase / Postgres / SQLite fallback)

Usage:
  PYTHONPATH=src:. python scripts/doctor.py
"""
import sys
import os

# Load .env if available – do not fail if missing
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
        import pydantic, pytest  # noqa
        from tender_getter import schemas, matcher  # noqa
        return True, ""
    except Exception as e:
        return False, str(e)

def check_gemini_key():
    key = os.environ.get("GEMINI_API_KEY", "")
    if key and len(key) > 20:
        return True, "present"
    return False, "missing or too short – set GEMINI_API_KEY in .env"

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
    from urllib.error import URLError
    url = "https://ocds-api.etenders.gov.za/api/v1/releases?page=1&pageSize=1"
    try:
        req = Request(url, headers={"User-Agent": "Tender-Getter-RSA/doctor", "Accept": "application/json"})
        with urlopen(req, timeout=5) as r:
            ok = 200 <= r.status < 300
            return ok, f"HTTP {r.status}"
    except URLError as e:
        return False, f"unreachable: {e}"

def check_database():
    try:
        from tender_getter.database import get_database_client
        db = get_database_client()
        db.connect()
        name = type(db).__name__
        db.close()
        return True, name
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    print("Tender Getter RSA – doctor")
    print("-" * 40)
    results = [
        check("Python imports", check_imports),
        check("GEMINI_API_KEY", check_gemini_key),
        check("sources.yaml", check_sources),
        check("eTenders OCDS API", check_etenders_api),
        check("Database", check_database),
    ]
    print("-" * 40)
    if all(results):
        print("All checks passed ✅")
        sys.exit(0)
    else:
        print(f"{sum(1 for r in results if not r)} check(s) failed ❌")
        sys.exit(1)
