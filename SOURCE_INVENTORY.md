# Tender-Getter RSA – Complete Source List Audit
_Date of audit: 2026-07-08 (commit `dedd6f3`, "main" branch)_

This is a full inventory of every tender source the system knows about, **cross-referenced against the actual code in the repo**. I checked:
1. `src/tender_getter/sources.yaml` (the **declared** registry, 114 entries)
2. `src/tender_getter/sources/<dir>/*.py` plug-ins (the **implemented** scrapers, 112 classes + 2 sync functions)
3. `src/tender_getter/sources/__init__.py` (the **explicitly imported** classes, 108)
4. `tests/test_source_*.py` (the **test coverage**, 113 per-source test files)
5. `src/tender_getter/aggregator.py` (auto-discovery via `pkgutil`, so anything in a sources/ subpackage is picked up at runtime even if not explicitly imported)

---

## TL;DR — the numbers

| Layer | Count |
|---|---|
| Entries in `sources.yaml` | **114** |
| Plug-in modules on disk (`sources/**/*.py`) | 114 (incl. `common.py`) |
| Plug-in classes with `source_id` field | **112** |
| `TenderSource` subclasses explicitly imported in `__init__.py` | 108 |
| Sync functions (eTenders OCDS + CSV) called by the engine | 2 (`sync_live_tenders`, `sync_csv_tenders`) |
| Per-source test files (`tests/test_source_*.py`) | **113** |
| Non-source tests (aggregator, database, matcher, reporter, pipelines, list_tenders) | 6 |
| Total `tests/test_*.py` files | **119** |
| GitHub Actions daily workflow | ✅ (`/.github/workflows/sync.yml`) |
| Docs files reviewed | `README.md`, `PLANNING.md` (v1.3.0), `LICENSE` |

**Coverage verdict:** Every entry in `sources.yaml` has a corresponding plug-in module **and** a corresponding test file. The aggregator's `pkgutil`-based auto-discovery picks up the 8 research-council modules that aren't in the explicit `__init__.py` import list (`csir, geoscience, hsrc, mintek, nhls, sabs, sansa, wrc`), so they are still exercised at runtime. **No source is declared-but-unimplemented; no source is implemented-but-undeclared.**

---

## Repository layout (top level)

```
Tender-Getter-RSA/
├── .env.example              # GEMINI_API_KEY + SUPABASE_* keys
├── .github/workflows/sync.yml # Daily 05:00 SAST cron + pytest
├── .gitignore                # Excludes .env, caches, build/, etc.
├── LICENSE                   # (MIT-style, initial commit)
├── PLANNING.md               # v1.3.0 architectural spec, 304 lines
├── README.md                 # Hackathon landing page
├── requirements.txt          # pydantic, pdfplumber, pypdf, google-generativeai,
│                             # python-dotenv, pytest, psycopg2-binary, supabase, pyyaml
├── localdata/                # Generated outputs (sample TG_REPORT_*.md present)
├── scripts/
│   ├── doctor.py             # Health check (imports, key, sources.yaml, eTenders, DB)
│   ├── run_poc.py            # Mock-company POC runner (Sipho Electrical and Civils)
│   ├── run_ingestion_engine.py # Legacy ingestion runner (still present)
│   └── sync_all.py           # Unified ThreadPool CLI: --limit N --json
├── src/tender_getter/
│   ├── __init__.py
│   ├── schemas.py            # CompanyProfile, TenderOpportunity, MatchResult, CIDBGrading, Location
│   ├── matcher.py            # Gate 1 (CSD/Tax/Geo/CIDB) + Gate 2 (B-BBEE 80/20 + 90/10)
│   ├── database.py           # SQLite (default) + factory to Postgres/Supabase
│   ├── database_base.py      # Abstract TenderDatabaseBase
│   ├── database_postgres.py  # psycopg2 driver
│   ├── database_supabase.py  # PostgREST/Supabase REST driver
│   ├── aggregator.py         # pkgutil auto-discovery + ThreadPool + dedup + bulk upsert
│   ├── source_sync.py        # Backwards-compat re-export shim
│   ├── parser.py             # pdfplumber pre-screener → Gemini 1.5 Pro JSON sieve
│   ├── lead_harvester.py     # CSV → CompanyProfile importer (Phase 2 foundation)
│   ├── reporter.py           # Markdown TG_REPORT_*.md writer
│   ├── sources.yaml          # 114-entry metadata registry
│   └── sources/              # All plug-in modules (10 subpackages)
├── supabase/
│   ├── config.toml
│   ├── functions/match-tenders/index.ts # Deno edge fn (minimal – 15 lines, smoke-test only)
│   └── migrations/20260707_initial_schema.sql # 4 tables + indexes
└── tests/                    # 113 per-source + 6 core = 119 files
```

---

## The 114 sources — full inventory

> **Legend:** `YAML id` = registry id, `Module` = `sources/<subpkg>/<file>.py`, `Class` = the class imported and instantiated by the aggregator, `Test` = `tests/test_source_<slug>.py`.

### A. National — 3 sources

| # | YAML id | Module | Class | Test |
|---|---|---|---|---|
| 1 | `etenders_ocds` | `sources/national/etenders_ocds.py` | (sync fn `sync_live_tenders` + `parse_ocds_release_to_tender`) | covered by `test_pipelines.py` |
| 2 | `etenders_csv` | `sources/national/etenders_csv.py` | (sync fn `sync_csv_tenders` + `parse_csv_row_to_tender`) | `test_source_sync_csv.py` |
| 3 | `cidb_itender` | `sources/national/cidb.py` | `CIDBSource` | `test_source_cidb.py` |

### B. Provincial Treasuries — 9 sources (all 9 provinces)

| # | YAML id | Module | Class | Test |
|---|---|---|---|---|
| 4 | `gauteng_etenders` | `provincial/gauteng.py` | `GautengSource` | ✅ |
| 5 | `westerncape_tenders` | `provincial/westerncape.py` | `WesternCapeSource` | ✅ |
| 6 | `kzn_treasury` | `provincial/kzn.py` | `KZNSource` | ✅ |
| 7 | `easterncape_tenders` | `provincial/easterncape.py` | `EasternCapeSource` | ✅ |
| 8 | `freestate_tenders` | `provincial/freestate.py` | `FreeStateSource` | ✅ |
| 9 | `limpopo_tenders` | `provincial/limpopo.py` | `LimpopoSource` | ✅ |
| 10 | `mpumalanga_tenders` | `provincial/mpumalanga.py` | `MpumalangaSource` | ✅ |
| 11 | `northwest_tenders` | `provincial/northwest.py` | `NorthWestSource` | ✅ |
| 12 | `northerncape_tenders` | `provincial/northerncape.py` | `NorthernCapeSource` | ✅ |

### C. Metropolitan Municipalities — 8 sources ("Big 8")

| # | YAML id | Module | Class | Test |
|---|---|---|---|---|
| 13 | `capetown_tenders` | `metros/capetown.py` | `CapeTownSource` | ✅ |
| 14 | `johannesburg_tenders` | `metros/johannesburg.py` | `JohannesburgSource` | ✅ |
| 15 | `ethekwini_tenders` | `metros/ethekwini.py` | `EthekwiniSource` | ✅ |
| 16 | `tshwane_tenders` | `metros/tshwane.py` | `TshwaneSource` | ✅ |
| 17 | `ekurhuleni_tenders` | `metros/ekurhuleni.py` | `EkurhuleniSource` | ✅ |
| 18 | `nelsonmandelabay_tenders` | `metros/nelson_mandela_bay.py` | `NelsonMandelaBaySource` | ✅ |
| 19 | `buffalo_city_tenders` | `metros/buffalo_city.py` | `BuffaloCitySource` | ✅ |
| 20 | `mangaung_tenders` | `metros/mangaung.py` | `MangaungSource` | ✅ |

### D. State-Owned Enterprises (SOEs) — 15 sources

| # | YAML id | Module | Class | Test |
|---|---|---|---|---|
| 21 | `eskom` | `soes/eskom.py` | `EskomSource` | ✅ |
| 22 | `transnet` | `soes/transnet.py` | `TransnetSource` | ✅ |
| 23 | `sanral` | `soes/sanral.py` | `SANRALSource` | ✅ |
| 24 | `prasa_tenders` | `soes/prasa.py` | `PRASASource` | ✅ |
| 25 | `landbank_tenders` | `soes/landbank.py` | `LandbankSource` | ✅ |
| 26 | `sabc_tenders` | `soes/sabc.py` | `SABCSource` | ✅ |
| 27 | `acsa_tenders` | `soes/acsa.py` | `ACSASource` | ✅ |
| 28 | `denel_tenders` | `soes/denel.py` | `DenelSource` | ✅ |
| 29 | `sentech_tenders` | `soes/sentech.py` | `SentechSource` | ✅ |
| 30 | `safcol_tenders` | `soes/safcol.py` | `SAFCOLSource` | ✅ |
| 31 | `necsa_tenders` | `soes/necsa.py` | `NECSASource` | ✅ |
| 32 | `petrosa_tenders` | `soes/petrosa.py` | `PetroSASource` | ✅ |
| 33 | `infraco_tenders` | `soes/infraco.py` | `BroadbandInfracoSource` | ✅ |
| 34 | `atns_tenders` | `soes/atns.py` | `ATNSSource` | ✅ |
| 35 | `alexkor_tenders` | `soes/alexkor.py` | `AlexkorSource` | ✅ |

### E. Research & Scientific Councils — 9 sources

| # | YAML id | Module | Class | Test |
|---|---|---|---|---|
| 36 | `sita_tenders` | `research/sita.py` | `SITASource` | ✅ |
| 37 | `csir_tenders` | `research/csir.py` | `CSIRSource` | ✅ |
| 38 | `nhls_tenders` | `research/nhls.py` | `NHLSSource` | ✅ |
| 39 | `sansa_tenders` | `research/sansa.py` | `SANSASource` | ✅ |
| 40 | `geoscience_tenders` | `research/geoscience.py` | `GeoscienceSource` | ✅ |
| 41 | `mintek_tenders` | `research/mintek.py` | `MintekSource` | ✅ |
| 42 | `hsrc_tenders` | `research/hsrc.py` | `HSRCSource` | ✅ |
| 43 | `wrc_tenders` | `research/wrc.py` | `WRCSource` | ✅ |
| 44 | `sabs_tenders` | `research/sabs.py` | `SABSSource` | ✅ |

> ⚠️ **Implementation note:** only `SITASource` is explicitly imported in `sources/__init__.py`. The other 8 research-council classes (CSIR/NHLS/SANSA/Geoscience/Mintek/HSRC/WRC/SABS) are auto-discovered at runtime by `aggregator.py`'s `pkgutil.iter_modules` walk, **not** via the explicit import list. Same for `CSIRSource` / `NHLSSource` / `SANSASource` / `GeoscienceSource` / `MintekSource` / `HSRCSource` / `WRCSource` / `SABSSource` — they ARE in the `__all__` list at the bottom of `__init__.py`, but not actually imported at the top of the file. **They still work** because of the walk, but this is worth knowing — Phase 2 may want to clean this up.

### F. Water Boards — 10 sources (all 10)

| # | YAML id | Module | Class | Test |
|---|---|---|---|---|
| 45 | `rand_water_tenders` | `water/rand_water.py` | `RandWaterSource` | ✅ |
| 46 | `umgeni_water_tenders` | `water/umgeni_water.py` | `UmgeniWaterSource` | ✅ |
| 47 | `mhlathuze_water_tenders` | `water/mhlathuze_water.py` | `MhlathuzeWaterSource` | ✅ |
| 48 | `overberg_water_tenders` | `water/overberg_water.py` | `OverbergWaterSource` | ✅ |
| 49 | `amatola_water_tenders` | `water/amatola_water.py` | `AmatolaWaterSource` | ✅ |
| 50 | `lepelle_water_tenders` | `water/lepelle_water.py` | `LepelleWaterSource` | ✅ |
| 51 | `magalies_water_tenders` | `water/magalies_water.py` | `MagaliesWaterSource` | ✅ |
| 52 | `bloem_water_tenders` | `water/bloem_water.py` | `BloemWaterSource` | ✅ |
| 53 | `sedibeng_water_tenders` | `water/sedibeng_water.py` | `SedibengWaterSource` | ✅ |
| 54 | `tcta_tenders` | `water/tcta.py` | `TCTASource` | ✅ |

### G. DFIs / Regulators — 10 sources

| # | YAML id | Module | Class | Test |
|---|---|---|---|---|
| 55 | `dbsa_tenders` | `dfi/dbsa.py` | `DBSASource` | ✅ |
| 56 | `idc_tenders` | `dfi/idc.py` | `IDCSource` | ✅ |
| 57 | `sars_tenders` | `dfi/sars.py` | `SARSSource` | ✅ |
| 58 | `samsa_tenders` | `dfi/samsa.py` | `SAMSASource` | ✅ |
| 59 | `sanparks_tenders` | `dfi/sanparks.py` | `SANParksSource` | ✅ |
| 60 | `seda_tenders` | `dfi/seda.py` | `SEDASource` | ✅ |
| 61 | `sefa_tenders` | `dfi/sefa.py` | `SefaSource` | ✅ |
| 62 | `raf_tenders` | `dfi/raf.py` | `RAFSource` | ✅ |
| 63 | `compensation_fund_tenders` | `dfi/compensation_fund.py` | `CompensationFundSource` | ✅ |
| 64 | `uif_tenders` | `dfi/uif.py` | `UIFSource` | ✅ |

### H. District Municipalities — 9 sources

| # | YAML id | Module | Class | Test |
|---|---|---|---|---|
| 65 | `west_rand_tenders` | `districts/west_rand.py` | `WestRandSource` | ✅ |
| 66 | `sedibeng_dm_tenders` | `districts/sedibeng_dm.py` | `SedibengDMSource` | ✅ |
| 67 | `cape_winelands_tenders` | `districts/cape_winelands.py` | `CapeWinelandsSource` | ✅ |
| 68 | `garden_route_tenders` | `districts/garden_route.py` | `GardenRouteSource` | ✅ |
| 69 | `king_cetshwayo_tenders` | `districts/king_cetshwayo.py` | `KingCetshwayoSource` | ✅ |
| 70 | `ilembe_tenders` | `districts/ilembe.py` | `ILembeSource` | ✅ |
| 71 | `or_tambo_tenders` | `districts/or_tambo.py` | `ORTamboSource` | ✅ |
| 72 | `capricorn_tenders` | `districts/capricorn.py` | `CapricornSource` | ✅ |
| 73 | `ehlanzeni_tenders` | `districts/ehlanzeni.py` | `EhlanzeniSource` | ✅ |

### I. Provincial Infrastructure / SCM Departments — 15 sources

| # | YAML id | Module | Class | Test |
|---|---|---|---|---|
| 74 | `gdid_tenders` | `provincial_depts/gdid.py` | `GDIDSource` | ✅ |
| 75 | `gdrt_tenders` | `provincial_depts/gdrt.py` | `GDRTSource` | ✅ |
| 76 | `gde_tenders` | `provincial_depts/gde.py` | `GDESource` | ✅ |
| 77 | `gdh_tenders` | `provincial_depts/gdh.py` | `GDHSource` | ✅ |
| 78 | `wcdi_tenders` | `provincial_depts/wcdi.py` | `WCDISource` | ✅ |
| 79 | `wc_health_tenders` | `provincial_depts/wc_health.py` | `WCHealthSource` | ✅ |
| 80 | `kzn_dot_tenders` | `provincial_depts/kzn_dot.py` | `KZNDoTSource` | ✅ |
| 81 | `kzn_human_settlements_tenders` | `provincial_depts/kzn_human_settlements.py` | `KZNHumanSettlementsSource` | ✅ |
| 82 | `ec_public_works_tenders` | `provincial_depts/ec_public_works.py` | `ECPublicWorksSource` | ✅ |
| 83 | `ec_education_tenders` | `provincial_depts/ec_education.py` | `ECEducationSource` | ✅ |
| 84 | `fs_police_roads_tenders` | `provincial_depts/fs_police_roads.py` | `FSPoliceRoadsSource` | ✅ |
| 85 | `limpopo_pwri_tenders` | `provincial_depts/limpopo_pwri.py` | `LimpopoPWRISource` | ✅ |
| 86 | `mpumalanga_education_tenders` | `provincial_depts/mpumalanga_education.py` | `MpumalangaEducationSource` | ✅ |
| 87 | `nw_public_works_tenders` | `provincial_depts/nw_public_works.py` | `NWPublicWorksSource` | ✅ |
| 88 | `nc_roads_tenders` | `provincial_depts/nc_roads.py` | `NCRoadsSource` | ✅ |

### J. National Government Departments — 26 sources (all major ministries)

| # | YAML id | Module | Class | Test |
|---|---|---|---|---|
| 89 | `saps_tenders` | `national_depts/saps.py` | `SAPSSource` | ✅ |
| 90 | `doel_tenders` | `national_depts/doel.py` | `DoELSource` | ✅ |
| 91 | `dpwi_tenders` | `national_depts/dpwi.py` | `DPWISource` | ✅ |
| 92 | `dws_tenders` | `national_depts/dws.py` | `DWSSource` | ✅ |
| 93 | `dod_tenders` | `national_depts/dod.py` | `DoDSource` | ✅ |
| 94 | `doh_tenders` | `national_depts/doh.py` | `DoHSource` | ✅ |
| 95 | `dbe_tenders` | `national_depts/dbe.py` | `DBESource` | ✅ |
| 96 | `dhet_tenders` | `national_depts/dhet.py` | `DHETSource` | ✅ |
| 97 | `dha_tenders` | `national_depts/dha.py` | `DHASource` | ✅ |
| 98 | `dmre_tenders` | `national_depts/dmre.py` | `DMRESource` | ✅ |
| 99 | `dalrrd_tenders` | `national_depts/dalrrd.py` | `DALRRDSource` | ✅ |
| 100 | `dffe_tenders` | `national_depts/dffe.py` | `DFFESource` | ✅ |
| 101 | `dot_tenders` | `national_depts/dot.py` | `DoTSource` | ✅ |
| 102 | `national_treasury_tenders` | `national_depts/national_treasury.py` | `NationalTreasurySource` | ✅ |
| 103 | `dcs_tenders` | `national_depts/dcs.py` | `DCSSource` | ✅ |
| 104 | `tourism_tenders` | `national_depts/tourism.py` | `TourismSource` | ✅ |
| 105 | `dsac_tenders` | `national_depts/dsac.py` | `DSACSource` | ✅ |
| 106 | `dsi_tenders` | `national_depts/dsi.py` | `DSISource` | ✅ |
| 107 | `dcdt_tenders` | `national_depts/dcdt.py` | `DCDTSource` | ✅ |
| 108 | `dsbd_tenders` | `national_depts/dsbd.py` | `DSBDSource` | ✅ |
| 109 | `dhs_tenders` | `national_depts/dhs.py` | `DHSSource` | ✅ |
| 110 | `cogta_tenders` | `national_depts/cogta.py` | `COGTASource` | ✅ |
| 111 | `dpsa_tenders` | `national_depts/dpsa.py` | `DPSASource` | ✅ |
| 112 | `dtic_tenders` | `national_depts/dtic.py` | `DTICSource` | ✅ |
| 113 | `dpme_tenders` | `national_depts/dpme.py` | `DPMESource` | ✅ |
| 114 | `presidency_tenders` | `national_depts/presidency.py` | `PresidencySource` | ✅ |

---

## What "implemented" actually means — plug-in anatomy

Every `TenderSource` class follows the same shape (verified by spot-checking `sources/research/sita.py`, `sources/metros/johannesburg.py`, and reading `sources/common.py`):

```python
class XxxSource:
    source_id: str = "xxx_tenders"          # class-level, used by aggregator dedup
    def __init__(self, url: str = "https://..."): ...
    def fetch(self, limit: int | None = None,
              html_content: str | None = None) -> list[TenderOpportunity]:
        # 1. Try live HTTP GET (urllib, 8-second timeout, Chrome UA)
        # 2. On URLError/HTTPError/Exception → fall back to embedded MOCK_X_HTML
        # 3. parse_html(html) → list[TenderOpportunity]
        # 4. If parsing yielded 0 → fall back to mock
    def parse_html(self, html: str, limit: int | None = None) -> list[TenderOpportunity]:
        # Generic <tr><td>… regex scraper, common across all sources
        # → re_search_cidb() for class/level
        # → province_from_text() for location_target
        # → parse_closing_date() with 4-format fallback
```

**Important reality check:** all 112 plug-ins are **stubs with high-fidelity mock HTML**. They:
- Always ship a `MOCK_<SOURCE>_HTML` constant (3 fake tender rows in a `<table>`)
- Hit the real URL with `urllib.request.urlopen(timeout=8)` and fall back to the mock on failure
- The mock HTML deliberately includes realistic SA tender refs (e.g. `COJ/EE001/25-26`, `RFB 2026/012`) so the parsers exercise the full path

So Phase 1 is "wired end-to-end with mocks", not "live-fetched 114 portals". The doctor script confirms this on every CI run: `check_etenders_api()` is the only source actually poked live, and it has a graceful failure path.

---

## Phase 1 architectural components (verified working)

| Component | File | Status |
|---|---|---|
| Pydantic V2 data contracts | `schemas.py` (137 lines) | ✅ CompanyProfile / TenderOpportunity / MatchResult / CIDBGrading / Location |
| Matching engine | `matcher.py` (254 lines) | ✅ Gate 1 (CSD/Tax/Geofence/CIDB-class+level+financial-cap fallback) + Gate 2 (B-BBEE 80/20 & 90/10 via PPPFA thresholds) |
| SQLite persistence | `database.py` (323 lines) | ✅ 4 tables (company_profiles, cidb_gradings, tenders, matches) with idempotent upserts |
| Postgres driver | `database_postgres.py` | ✅ psycopg2-based |
| Supabase REST driver | `database_supabase.py` | ✅ PostgREST API |
| Aggregator (ThreadPool) | `aggregator.py` (227 lines) | ✅ pkgutil auto-discovery, 20-worker ThreadPoolExecutor, dedup by tender_id, per-source error isolation |
| Sync CLI | `scripts/sync_all.py` | ✅ `--limit N --json` flags, exit code 2 if 0 tenders |
| Daily CI cron | `.github/workflows/sync.yml` | ✅ 03:00 UTC = 05:00 SAST, runs doctor + sync_all + pytest |
| Schema migration | `supabase/migrations/20260707_initial_schema.sql` | ✅ 4 tables + 3 indexes, idempotent |
| Supabase edge fn | `supabase/functions/match-tenders/index.ts` | ⚠️ Minimal smoke-test (15 lines, just counts tenders) — **not** a full match worker |
| Gemini PDF parser | `parser.py` (186 lines) | ✅ pdfplumber pre-screener → Gemini 1.5 Pro JSON extraction |
| Lead harvester (Phase 2 foundation) | `lead_harvester.py` (130 lines) | ✅ CSV → CompanyProfile with CIDB code parser ("3EE;2CE" notation) |
| Reporter | `reporter.py` (259 lines) | ✅ Markdown TG_REPORT_*.md with ASCII score bar, SBD checklist, gate summary |

---

## Phase 1 → Phase 2 gap analysis (PLANNING.md §7 vs. actual code)

**What PLANNING.md promises for Phase 2 (Lead Harvesting):**
1. **Method 1 — Public Bid Award Registers:** PFMA/MFMA-mandated awarded-bids PDFs and web tables → parse winning bidders + losing bidders. **Code: ❌ NOT YET BUILT.** `lead_harvester.py` only handles CSV, not PDF/HTML bid-award registers.
2. **Method 2 — Public Professional Registries (CIDB):** Scrape CIDB active contractor directory. **Code: ❌ NOT YET BUILT.** No CIDB directory scraper exists; only `cidb_itender` source (for tenders, not contractors).
3. **Method 3 — Chamber / SCM partnerships:** No code required (it's an outreach play, not a scraper).

**Foundation code that exists for Phase 2:**
- `CompanyProfile` schema with all required fields (CIPC reg, CSD MAAA, B-BBEE level, CIDB gradings, location, sectors, tax pin, COIDA)
- `lead_harvester.import_suppliers_from_csv(csv_text)` ready to receive any CSV feed (handles `3EE;2CE` CIDB code notation, `true/false/1/0` booleans, `;`-delimited sectors)
- `database.upsert_company()` and `database.list_open_tenders(province=…)` for storage and retrieval
- `matcher.match()` already wired to CompanyProfile × TenderOpportunity

**What's missing for safe Phase 2:**
1. **Bid award register scraper** (PDF + HTML) → `sources/awards/` package
2. **CIDB contractor directory scraper** → `sources/cidb_directory.py`
3. **POPIA-compliant dedup & opt-out pipeline** (the plan says opt-in/out is required; nothing exists yet)
4. **CIPC company-search scraper** (only mentioned implicitly; CIPC public records need a separate scraper)
5. **A simple outreach queue table** to track who has been contacted + when (new DB table, new migration)
6. **Edge function for match-tenders** is currently just a smoke test — Phase 2 should flesh it out into a proper matcher Edge Function

---

## Things I'd flag before signing off on Phase 2

1. **All 112 plug-ins are mock-backed.** Production deployment needs a real network reachability matrix per source (some portals require JS, cookies, CAPTCHAs, or login). Suggest a per-source `live=True/False` flag and a "skip-and-keep-mock" runtime mode for the first few weeks.
2. **Auto-discovery vs explicit imports** — 8 research modules (CSIR/NHLS/SANSA/Geoscience/Mintek/HSRC/WRC/SABS) rely on `pkgutil` walk rather than explicit imports in `__init__.py`. Works today, fragile for refactoring.
3. **Three legacy bare source_ids** kept for BC: `eskom`, `sanral`, `transnet` (no `_tenders` suffix). Intentional per CHANGELOG 1.3.0 but worth a heads-up — anything filtering by suffix will miss them.
4. **`scripts/run_poc.py` is duplicative** — it hard-codes 11 sources to fetch, while `scripts/sync_all.py` already does all 114. Phase 2 should retire `run_poc.py` and point everything at `sync_all.py`.
5. **`supabase/functions/match-tenders/index.ts` is a stub** (15 lines). Either build it out or delete it.
6. **No integration test that actually fetches from a real portal** — all `test_source_*.py` tests pass `html_content=<MOCK>` directly. The end-to-end "live fetch → parse → upsert" path is only exercised in CI by the `doctor.py` eTenders portal probe.
7. **Phase 2 deliverables (lead harvesting) need their own DB migration** — there's currently no `outreach_queue`, `opt_out`, or `consent_log` table.

---

## Bottom line

✅ **Phase 1 ingestion is complete and honest:** 114 sources declared, 112 plug-ins implemented with full unit-test coverage, 1 super-set aggregator that auto-discovers everything, daily CI cron, Supabase migration, multi-driver DB, and a working POC against a realistic mock client. **There is no phantom or unimplemented source.**

⚠️ **Phase 2 has zero code written yet.** Only the *foundation* (CompanyProfile schema + CSV harvester) exists. The three promised lead-harvesting methods (PFMA award registers, CIDB directory, chamber outreach) all need to be built from scratch — and POPIA guard-rails (opt-in/out + consent log) need to be designed before a single email goes out.
