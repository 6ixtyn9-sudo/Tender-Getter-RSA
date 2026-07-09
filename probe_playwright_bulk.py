#!/usr/bin/env python3
"""Bulk Playwright probe for JS-rendered sources.

Scans live sources that return 0 tenders via static HTML and tries:
  1. Subpage discovery (already in generic.py standard_fetch)
  2. Playwright headless render
  3. Reports recovery rate

Usage:
  # Install Playwright first:
  pip install playwright && playwright install chromium

  # Run probe:
  PYTHONPATH=src python3 probe_playwright_bulk.py --limit 10 --timeout-ms 20000

  # With filter on specific sources:
  PYTHONPATH=src python3 probe_playwright_bulk.py --sources namakwa_dm,newcastle_lm,garden_route
"""
from __future__ import annotations

import argparse
import json
import ssl
import sys
import time
from pathlib import Path
from typing import Optional

# Allow running from repo root without install
sys.path.insert(0, str(Path(__file__).parent / "src"))

import yaml
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from tender_getter.sources.generic import (
    _do_fetch, _get_ssl_context, _discover_tender_subpages, parse_html_table
)

_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"


def static_yield(url: str, timeout: int = 10) -> tuple[int, int]:
    """Return (n_rows, n_tenders) from a static fetch."""
    ssl_ctx = _get_ssl_context()
    try:
        html = _do_fetch(url, timeout, ssl_ctx)
        tenders = parse_html_table(html)
        return len(tenders), len(html)
    except Exception:
        return 0, 0


def playwright_yield(url: str, timeout_ms: int = 20000) -> tuple[int, str]:
    """Return (n_tenders, html) via Playwright."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page(user_agent=_UA)
            page.goto(url, timeout=timeout_ms, wait_until="networkidle")
            html = page.content()
            browser.close()
        tenders = parse_html_table(html)
        return len(tenders), html
    except ImportError:
        print("  ❌ Playwright not installed. Run: pip install playwright && playwright install chromium")
        return -1, ""
    except Exception as e:
        return 0, str(e)


def load_sources(yaml_path: str = "src/tender_getter/sources.yaml") -> list:
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    return data.get("sources", data) if isinstance(data, dict) else data


def main():
    parser = argparse.ArgumentParser(description="Bulk Playwright probe for zero-yield sources")
    parser.add_argument("--limit", type=int, default=20, help="Max sources to probe")
    parser.add_argument("--timeout-ms", type=int, default=20000, help="Playwright timeout in ms")
    parser.add_argument("--sources", type=str, default="", help="Comma-separated source IDs to probe")
    parser.add_argument("--output", type=str, default="pw_probe_results.json", help="Output JSON file")
    args = parser.parse_args()

    sources = load_sources()
    if args.sources:
        filter_ids = set(args.sources.split(","))
        sources = [s for s in sources if s["id"] in filter_ids]
    else:
        # Only probe live sources
        sources = [s for s in sources if s.get("live", True)][:args.limit]

    print(f"Probing {len(sources)} sources...\n")
    results = []

    for src in sources:
        sid = src["id"]
        url = src.get("url", "")
        if not url.startswith("http"):
            continue

        # Quick static check
        static_n, html_size = static_yield(url)
        print(f"{'✅' if static_n > 0 else '⚠️ '} {sid:30s} static={static_n} ({html_size // 1024}KB)", end="")

        pw_n = None
        subpage_n = 0

        if static_n == 0:
            # Try subpage discovery first
            try:
                html = _do_fetch(url, 10, _get_ssl_context())
                subpages = _discover_tender_subpages(url, html)
                for sub in subpages[:3]:
                    try:
                        sub_html = _do_fetch(sub, 10, _get_ssl_context())
                        sub_tenders = parse_html_table(sub_html)
                        if sub_tenders:
                            subpage_n = len(sub_tenders)
                            print(f" | subpage={subpage_n}@{sub}", end="")
                            break
                    except Exception:
                        pass
            except Exception:
                pass

            if subpage_n == 0:
                # Try Playwright
                print(" | trying PW...", end="", flush=True)
                t0 = time.time()
                pw_n, _ = playwright_yield(url, args.timeout_ms)
                elapsed = time.time() - t0
                if pw_n == -1:
                    print(f"\n  Playwright unavailable – stopping PW probes.")
                    break
                print(f" PW={pw_n} ({elapsed:.1f}s)", end="")

        print()
        results.append({
            "id": sid,
            "url": url,
            "static": static_n,
            "subpage": subpage_n,
            "playwright": pw_n,
            "recovered": max(static_n, subpage_n, pw_n or 0) > 0,
        })

    # Summary
    recovered = [r for r in results if r["recovered"]]
    zero = [r for r in results if not r["recovered"]]
    print(f"\n{'='*60}")
    print(f"Recovered via any method: {len(recovered)}/{len(results)}")
    print(f"Still zero:               {len(zero)}")
    if zero:
        print(f"\nZero-yield sources (need Playwright or manual fix):")
        for r in zero[:20]:
            print(f"  - {r['id']:30s} {r['url']}")

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
