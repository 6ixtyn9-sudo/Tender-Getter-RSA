# GUARDRAIL — Read This Before Making Any Changes

Every agent that touches this repo must read this file first.

## Rule 1: Never Claim Numbers You Haven't Verified
DO NOT say "X tenders from Y sources" unless you have run this command and it printed that number:

```bash
PYTHONPATH=src python3 -c "
import logging; logging.basicConfig(level=logging.WARNING)
from tender_getter.aggregator import sync_all_sources
s = sync_all_sources(limit_per_source=None, live_only=True, verbose=False)
print(f'Tenders: {s[\"tenders_fetched\"]} | Sources OK: {s[\"sources_ok\"]} | Failed: {s[\"sources_failed\"]}')
"
```
If you haven't run it, say "I haven't verified the live count yet." Do not estimate. Do not extrapolate. Do not count mock data as live tenders.

## Rule 2: Do Not Add Diagnostic/Tooling Scripts to the Repo Root
The repo root should contain zero standalone scripts. The root contains only standard project entry files. Operational scripts belong in `scripts/`, documentation in `docs/`, and static integration configuration in `config/`.

These files are bloat and should be deleted:

* `audit_sources.py` — one-time audit tool, results already in `audit_results.json`
* `check_table_content.py` — one-time diagnostic
* `find_real_urls.py` — one-time URL discovery
* `fix_sources_yaml.py` — one-time batch fix
* `scan_wp.py` — one-time WP scan
* `probe_playwright_bulk.py` — one-time Playwright probe
* `audit_results.json` — stale audit data (URLs change)
* `url_fixes.json` — one-time fix data
* `wp_candidates.json` — one-time scan results
* `NEXT_AGENT_PROMPT.md` — replaced by this file

If you need a diagnostic script, put it in `scripts/` and delete it before committing.

## Rule 3: Do Not Modify `generic.py` Unless You Understand Every Source
`generic.py` is imported by all 725 source files. Changes to `standard_fetch()`, `parse_html_table()`, `_do_fetch()`, or any public function can break every source silently.

Before modifying `generic.py`:

* Run `pytest tests/test_generic.py -v` — must pass
* Run `pytest tests/ -q --ignore=tests/test_aggregator.py -k "not e2e"` — all 2200+ tests must pass
* Run the live count command from Rule 1 — number must not decrease

The current `generic.py` pipeline (DO NOT simplify or remove layers):

* `_do_fetch()` — HTTPS → TLS 1.2 → HTTP fallback, SSL bypass by default
* `standard_fetch()` — calls `_do_fetch()`, falls back to mock HTML
* `parse_html_table()` — regex-based `<tr><td>` parser

Environment variables (do not add more):

* `TENDER_FETCH_TIMEOUT` — HTTP timeout in seconds (default 10)
* `TENDER_SSL_VERIFY` — set to "1" to enforce SSL (default: skip)
* `TENDER_AUTO_PLAYWRIGHT` — "0" disabled, "auto" conditional, "1" always

## Rule 4: Every Source File Must Follow This Pattern
```python
"""Entity Name tender source plug-in."""
import logging
import re
from typing import List, Optional

from ...schemas import TenderOpportunity
from ..generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT, standard_fetch
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

MOCK_HTML = """<html>...realistic mock with 2-3 tenders...</html>"""


class EntitySource:
    source_id: str = "entity_name"
    live: bool = True

    def __init__(self, url: str = "https://..."):
        self.url = url
        self.issuing_entity = "Entity Name"

    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]:
        """Fetch tenders. html_content parameter enables testing without network."""
        engaged_fallback = False
        if html_content is None:
            ssl_ctx = _get_ssl_context()
            try:
                html_content = _do_fetch(self.url, _FETCH_TIMEOUT, ssl_ctx)
            except Exception as exc:
                logger.warning("Failed to fetch %s (%s). Using fallback.", self.url, exc)
                html_content = MOCK_HTML
                engaged_fallback = True
        tenders = self.parse_html(html_content, limit)
        if not tenders and not engaged_fallback:
            tenders = self.parse_html(MOCK_HTML, limit)
        return tenders

    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]:
        """Parse HTML into tenders. Override for custom column layouts."""
        # Use standard_fetch for simple 3-column tables:
        return standard_fetch(self.url, MOCK_HTML, html, limit)
```
WordPress API sources use `wp_fetch_tenders()` from `wp_api.py` instead.

## Rule 5: Every Test File Must Follow This Pattern
```python
"""Tests for Entity source plug-in."""
import pytest
from tender_getter.sources.category.entity import EntitySource, MOCK_HTML


def test_init():
    src = EntitySource()
    assert src.source_id == "entity_name"
    assert "domain.co.za" in src.url

def test_parse_mock():
    src = EntitySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2
    t = tenders[0]
    assert len(t.tender_id) > 0
    assert t.closing_date.year >= 2025
    assert len(t.issuing_entity) > 0

def test_fallback():
    src = EntitySource()
    tenders = src.fetch(html_content="<html></html>")
    assert len(tenders) >= 2
```
DO NOT assert exact tender IDs, exact dates, or exact counts from mock data. Assert structure and reasonable values.

## Rule 6: Verified Working Sources (Do Not Break These)
These sources return real live tenders as of the last verified run. If your changes break any of these, revert and try again.

| Source | Type | Verified Tenders |
|---|---|---|
| DFFE | HTML table | 699 |
| UKZN | HTML table | 1148 |
| Legal Aid SA | HTML table | 786 |
| DOH | HTML table | 298 |
| Bela-Bela LM | HTML table | 300 |
| Mkhondo LM | HTML table | 311 |
| Armscor | HTML table | 133 |
| Umgeni Water | HTML table | 134 |
| CSIR | HTML table | 50 |
| CEF | HTML table | 87 |
| Merafong LM | HTML table | 100 |
| AgriSETA | HTML table | 72 |
| Joburg | HTML table | 33 |
| Services SETA | HTML table | 24 |
| Ekurhuleni | Div-based | 7 |
| SABC | HTML table | 10 |
| Swartland LM | HTML table | 8 |
| Bitou LM | HTML table | 4 |
| DBSA | HTML table | 7 |
| UP | HTML table | 3 |
| SACAA | HTML table | 2 |
| DSBD | HTML table | 2 |
| NECSA | Key-value | 3 |
| ECSA | HTML table | 7 |
| PSETA | HTML table | 1 |
| George LM | WP API | 20 |
| False Bay TVET | WP API | 20 |
| HSRC | WP API | 20 |
| SANSA | WP API | 20 |
| SAQA | WP API | 20 |
| Rail Safety | WP API | 20 |
| SARS | WP API | 20 |
| TCTA | WP API | 10 |
| UGU DM | WP API | 10 |
| OCDS API | JSON API | 62 |

To verify a specific source still works:

```bash
PYTHONPATH=src python3 -c "
import logging; logging.basicConfig(level=logging.WARNING)
from tender_getter.sources.category.module import SourceClass
src = SourceClass()
t = src.fetch()
print(f'{src.source_id}: {len(t)} tenders')
assert len(t) > 0, 'BROKEN: returns 0 tenders'
"
```

## Rule 7: Do Not Add New Dependencies Without Justification
Current dependencies: `pydantic`, `pyyaml`, `pytest`. That's it.

Playwright is the one acceptable addition. It must be:

* Optional (import guarded with try/except)
* Disabled by default (`TENDER_AUTO_PLAYWRIGHT=0`)
* Only used as a last resort (layer 3, after static + subpage)

Do NOT add: `selenium`, `requests`, `scrapy`, `beautifulsoup4`, `httpx`, `aiohttp`, or any other HTTP/HTML library. The stdlib `urllib` + `re` is sufficient.

## Rule 8: `sources.yaml` Is the Source of Truth for Metadata
* `live: true` means the URL returns HTTP 200 AND has parseable content
* `live: false` means the URL is dead, 404, DNS failure, or has no parseable content
* `url:` must be the actual working URL (not a guess)
* `priority:` 1 = national/SOE, 2 = provincial/metro, 3 = municipal/other

To batch-update live flags after a URL audit:

```bash
python3 fix_sources_yaml.py  # reads audit_results.json
```

## Rule 9: The Playwright Decision Tree
```text
Is the source returning 0 tenders from static HTML?
  └─ YES: Does the page have <table> tags but 0 <tr> rows?
       └─ YES: Page is JS-rendered. Try Playwright.
       └─ NO: Does the page have tender keywords in the text?
            └─ YES: Content is in divs/non-table. Try regex extraction.
            └─ NO: Page is a landing page. Follow links to subpages.
  └─ NO: Source works. Don't touch it.
```

## Rule 10: Before You Commit, Run These 3 Commands
```bash
# 1. All tests pass
pytest tests/ -q --ignore=tests/test_aggregator.py -k "not e2e"

# 2. No import errors
PYTHONPATH=src python3 -c "from tender_getter.aggregator import discover_source_classes; print(f'{len(discover_source_classes())} sources')"

# 3. Live count hasn't decreased
PYTHONPATH=src python3 -c "
import logging; logging.basicConfig(level=logging.WARNING)
from tender_getter.aggregator import sync_all_sources
s = sync_all_sources(limit_per_source=None, live_only=True, verbose=False)
print(f'Tenders: {s[\"tenders_fetched\"]} | OK: {s[\"sources_ok\"]} | Failed: {s[\"sources_failed\"]}')
"
```
If any of these fail or show a decrease, do not commit. Revert and investigate.

## What The Next Agent Should Actually Do
* Delete the bloat — remove all standalone scripts from repo root (move to `scripts/` or delete)
* Run the 3 verification commands — establish baseline numbers
* Focus on Playwright — the ~80 JS-rendered sources are the only remaining high-value target
* Do NOT re-audit URLs — the audit was done, URLs were fixed, move on
* Do NOT re-scan for WP APIs — it was done across all 723 sources, no more exist
* Do NOT modify working source files — if it returns tenders, leave it alone
* Report actual numbers — run the verification commands, paste the output

## Known Branch Divergence (Critical)
There are two parallel branches that diverged from `f269f0b`:

**Branch A (this branch — `dc6b11f`)**: 15 commits focused on real data
* Fixed 35 source parsers with custom column mapping
* Fixed 108 broken URLs in `sources.yaml` (404 → working alternative)
* Flipped 108 sources from `live: false` to `live: true`
* Result: 4,470 tenders, 253 live sources, 2,271 tests

**Branch B (GitHub main — `2784208`)**: 4 commits focused on infrastructure
* Standardized test imports across all files
* Added Playwright + subpage discovery to `generic.py`
* Added TLS retry logic
* Result: 2,144 tenders, 145 live sources, 2,243 tests

Why Branch B has fewer tenders:
* 108 sources marked `live: false` that Branch A fixed. The aggregator skips these entirely. This is the primary cause (~2,000 missing tenders).
* Test count difference (2,243 vs 2,271) is from test standardization removing some assertions.

To merge Branch A's fixes into Branch B:

```bash
# Cherry-pick the sources.yaml URL fixes
git show dc6b11f:src/tender_getter/sources.yaml > src/tender_getter/sources.yaml

# Or merge the full branch
git merge dc6b11f
```


## Rule 11: Every Agent Must Report the Same 2 Numbers
To prevent confusion from different agents reporting different counts, NEVER report capped numbers. Always report these two:

* Uncapped (`limit_per_source=None`): Tenders: X | OK: Y | Failed: Z
* Sources with real data (not mock fallback): count sources where `len(fetch()) > 0` and tenders have valid dates

The uncapped count is the real capacity. The "real data" count is what actually matters.
