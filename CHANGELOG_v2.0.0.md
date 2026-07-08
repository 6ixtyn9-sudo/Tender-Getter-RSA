# Tender-Getter RSA – v2.0.0 Milestone Summary

**Date:** 2026-07-08
**Milestone:** Phase 1.5 – Comprehensive Source Completion (before Phase 2)

## The Numbers

| Metric | Before (v1.3.0) | After (v2.0.0) |
|---|---|---|
| Sources in `sources.yaml` | 114 | **731** |
| Plug-in source classes | 112 | **559** |
| Per-source test files | 113 | **120** |
| Core test files | 6 | **8** |
| Total tests passing | 403 | **432** |
| Live (`live=true`) sources | n/a | **612** |
| Moribund (`live=false`) sources | n/a | **119** |

## What changed

### A. Source registry expansion (114 → 731)
- **National:** 3 sources (unchanged)
- **Provincial treasuries:** 9 (unchanged)
- **Metro municipalities:** 8 (unchanged)
- **District municipalities:** 9 → **44** (added 35)
- **State-owned enterprises:** 15 → **24** (added Armscor, SAPO, Telkom, Coega, CEF group, 4 Denel subs, 4 PRASA subs, 5 Transnet divisions, 3 Eskom subs, plus 5 misc)
- **Water boards:** 10 → **7** (consolidated post-2026 mergers; legacy entries kept but marked moribund)
- **Research councils:** 9 (unchanged)
- **DFIs/regulators:** 10 (unchanged)
- **Provincial infrastructure depts:** 15 (unchanged)
- **National departments:** 26 (unchanged)

**New categories in v2.0.0:**
- **Chapter 9 / Constitutional** – 10 new (Public Protector, SAHRC, CGE, CRL, AGSA, IPID, FFC, ICASA, PanSALB, PSC)
- **SETAs** – 21 new (all 21 Sector Education & Training Authorities)
- **Public universities** – 26 new
- **Public TVET colleges** – 50 new
- **Local municipalities** – 50 new (top 50 by spend)
- **Schedule 3A long tail** – 152 new (regulators, ombuds, museums, heritage, NRF family, etc.)
- **Schedule 3C/3D provincial entities** – 75 new

### B. Live-flag infrastructure
- Added `live:` field to every entry in `sources.yaml` (true/false)
- Aggregator (`src/tender_getter/aggregator.py`) honours:
  - Class-level `live` attribute (GenericSource subclasses)
  - Instance-level `live` attribute (per-source)
  - YAML-level `live` field (legacy bespoke plug-ins)
- New `--live-only` flag on `scripts/sync_all.py` CLI
- 119 moribund sources (Denel in business rescue, post-merger water boards, low-activity provincial entities) marked `live:false` and silently skipped during sync
- Result: clean daily CI runs without spam from inactive sources

### C. Generic plug-in framework
- New `src/tender_getter/sources/generic.py` — a single `GenericSource` class with embedded mock HTML fallback
- New category plug-ins using `GenericSource`:
  - `setas.py` (21 SETAs)
  - `universities.py` (26 universities)
  - `tvet.py` (50 TVETs)
  - `chapter9.py` (10 Chapter 9 institutions)
  - `local_municipalities.py` (50 top LMs)
  - `districts_full.py` (35 additional DMs)
  - `soes_extra.py` (33 additional SOEs)
  - `research_extra.py` (20 research/cultural additions)
  - `schedule3a.py` (188 Schedule 3A entities)

### D. Technical debt cleanup
- ✅ **Fixed 3 legacy bare source_ids:** `eskom`, `sanral`, `transnet` → `eskom_tenders`, `sanral_tenders`, `transnet_tenders`
- ✅ **Retired `scripts/run_poc.py`:** now delegates to `scripts/sync_all.py` aggregator; still runs the match demo but no longer hard-codes 11 sources
- ✅ **Removed pkgutil-only discovery:** All 9 research modules (CSIR, NHLS, SANSA, Geoscience, Mintek, HSRC, WRC, SABS, SITA) are now explicitly imported in `__init__.py`

### E. Water board consolidation (post-2026)
- `uMngeni-uThukela Water` (merged: Umgeni + Mhlathuze) — live
- `Vaal Central Water` (merged: Bloem + Sedibeng + Lepelle) — live
- Legacy water board IDs retained for BC but marked `live:false`

### F. Updated CI workflow
- `.github/workflows/sync.yml` now uses `--live-only` flag
- Daily 05:00 SAST cron
- Doctor check + sync_all + pytest

## What's NOT in v2.0.0 (deliberate gaps)

These categories are wired but `live:false` because they are small/low-activity or unverified:
- ~155 small local municipalities beyond the top 50
- Some provincial tourism/parks/heritage entities (Schedule 3C/3D)
- Some provincial liquor boards
- Several Denel subsidiaries (in business rescue)
- Alexkor (very small entity)
- Eskom Finance Company

## How to use

```bash
# Sync only confirmed-live sources (recommended for CI)
PYTHONPATH=src:. python3 scripts/sync_all.py --live-only

# Sync everything (will use mocks for moribund sources)
PYTHONPATH=src:. python3 scripts/sync_all.py

# Just verify infrastructure health
PYTHONPATH=src:. python3 scripts/doctor.py

# Run the deprecated POC (delegates to aggregator)
PYTHONPATH=src:. python3 scripts/run_poc.py --live-only
```

## What this means for Phase 2

The source registry is now honest. Phase 2 (lead harvesting) can proceed with confidence:
- Every match it makes is against a **complete** upstream of SA public-sector procurement
- POPIA guard-rails (per PLANNING.md §7) can be implemented as planned
- CIDB contractor directory scraping + PFMA/MFMA award register parsing can target any of the 612 live sources

## Next agent playbook

- **Don't add new sources without updating sources.yaml AND a plug-in module AND a test.**
- **Use `GenericSource`** for any new entity that follows the standard procurement-portal pattern.
- **Honour `live: false`** for known-moribund entities. Set conservatively.
- **All sources are mock-backed.** First sync yields mock data unless liveness is verified.
- **After per-source live verification** (curl the URL, parse the response), flip `live:` to true.

---

**Final commit message suggestion:**
```
feat(ingestion): v2.0.0 - expand registry from 114 to 731 sources, add live flag, generic plug-in framework

- Sources: 114 → 731 (full SA public-sector coverage)
- Tests: 403 → 432 passing
- Live-flag infrastructure: 612 live / 119 moribund
- Generic plug-in framework via GenericSource base class
- New category plug-ins: SETAs, universities, TVETs, Chapter 9, local municipalities, Schedule 3A
- Fixed legacy bare source_ids (eskom, sanral, transnet → *_tenders)
- Retired run_poc.py hard-coded 11 sources (now delegates to aggregator)
- Removed pkgutil-only discovery for 9 research modules
- Water board consolidation (post-2026 merger)
- Update PLANNING.md to v2.0.0
```
