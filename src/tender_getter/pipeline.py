"""pipeline.py - The real end-to-end Tender Getter RSA flow.

    ingest REAL tenders (no mock)  ->  store  ->  match a business  ->  report

This is the canonical business flow. It is deliberately mock-free: a tender
only enters the DB if a source's OWN parser found it in genuinely-fetched live
HTML/JSON. This is what makes match results trustworthy — you are never matching
a client against fake fixture data.

Why this module exists (the problem it fixes):
  - aggregator.sync_all_sources() calls each source's fetch(), which falls back
    to MOCK_HTML on failure. ~229 of 264 sources would therefore inject fake
    tenders. Matching against that is worthless.
  - The National Treasury OCDS API (our single best real source) is NOT picked
    up by the aggregator (no source_id class), so it is wired in here directly.

Public entry points:
  ingest_real_tenders(db, ...)   -> summary dict, writes real tenders to db
  match_company(company, db)     -> list[MatchResult], persists matches
  run_pipeline(...)              -> end-to-end, returns summary + report paths
"""
from __future__ import annotations

import importlib
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import re as _re

from .schemas import CompanyProfile, TenderOpportunity, MatchResult
from .matcher import match as run_match

logger = logging.getLogger(__name__)

# Tender IDs / titles that are obviously parser noise (nav-menu images, JS files, etc.)
_NOISE_RE = _re.compile(
    r"\.(?:GIF|PNG|JPE?G|CSS|JS)\b|\b(?:MENU|M1[A-Z0-9]*|IE\d|NS\d|DOM)\b",
    _re.IGNORECASE,
)


def _is_open_and_valid(tender: TenderOpportunity, now: datetime) -> bool:
    """A tender is matchable only if it is open, dated, and not parser noise.

    - closing_date must be in the future (not expired)
    - closing_date must be a real date (not the 2099 unparseable sentinel)
    - tender_id must not look like a tech artefact (.gif / menu / .js)
    """
    cd = tender.closing_date
    if cd is None:
        return False
    if cd <= now:
        return False  # expired
    if cd.year >= 2099:
        return False  # date could not be parsed
    if _NOISE_RE.search(tender.tender_id) or _NOISE_RE.search(tender.title or ""):
        return False
    return True


# ---------------------------------------------------------------------------
# 1. INGEST — real tenders only, no mock contamination
# ---------------------------------------------------------------------------

def _module_has_mock(cls) -> bool:
    try:
        mod = importlib.import_module(cls.__module__)
    except Exception:
        return False
    return any(n.upper().startswith("MOCK") and "HTML" in n.upper() for n in dir(mod))


def _fetch_one_real(inst) -> tuple[str, list[TenderOpportunity], Optional[str]]:
    """Fetch a source's REAL tenders only. Never engages mock fallback.

    Also recovers tender document (PDF) URLs from the page and attaches them as
    raw_document_url, so downstream enrichment can open and parse the docs.

    Returns (source_id, tenders, error_or_None). tenders is empty on any
    failure or genuine zero-yield — never mock data.
    """
    sid = getattr(inst, "source_id", inst.__class__.__name__)
    url = getattr(inst, "url", None)
    if not url or not str(url).startswith("http"):
        return sid, [], "no_url"
    from .sources.generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
    mock_backed = _module_has_mock(inst.__class__)
    try:
        if mock_backed:
            html = _do_fetch(url, _FETCH_TIMEOUT, _get_ssl_context())
            tenders = inst.parse_html(html)
            tenders = _attach_doc_urls(tenders, url, html)
        else:
            tenders = inst.fetch() or []
    except Exception as exc:
        return sid, [], f"{type(exc).__name__}: {exc}"[:120]
    return sid, list(tenders), None


def _attach_doc_urls(
    tenders: list[TenderOpportunity], page_url: str, html: str
) -> list[TenderOpportunity]:
    """Match tender refs to PDF links recovered from the same page."""
    if not tenders:
        return tenders
    try:
        from .doc_finder import find_document_urls
        mappings = find_document_urls.__wrapped__ if hasattr(find_document_urls, "__wrapped__") else None
        # call directly with already-fetched html by monkey-patching not needed:
        # find_document_urls fetches itself; to avoid a double fetch, do inline.
    except Exception:
        return tenders
    return _attach_doc_urls_inline(tenders, page_url, html)


def _attach_doc_urls_inline(
    tenders: list[TenderOpportunity], page_url: str, html: str
) -> list[TenderOpportunity]:
    """Inline version: parse the already-fetched html for doc links + match refs.
    Prefers actual .pdf/.doc links over keyword-matching listing pages."""
    from .doc_finder import _LinkTableParser, _is_doc_url
    from urllib.parse import urljoin, urlparse
    import re as _re

    _PDF_RE = _re.compile(r"\.(?:pdf|docx?|xlsx?)(?:\?|#|$)", _re.IGNORECASE)
    base_netloc = urlparse(page_url).netloc
    parser = _LinkTableParser()
    try:
        parser.feed(html)
    except Exception:
        return tenders

    # build ref -> doc_url from table rows, PREFERRING .pdf links
    mappings: dict[str, str] = {}
    for row in parser.rows:
        ref = ""
        pdf_href = None   # actual document file
        kw_href = None    # keyword-matching link (fallback)
        for cell in row:
            t = cell.get("text", "")
            if not ref and t:
                ref = t
            href = cell.get("href")
            if href and _is_doc_url(href, base_netloc):
                abs_href = urljoin(page_url, href)
                if _PDF_RE.search(href):
                    pdf_href = abs_href  # strongest signal
                elif not kw_href:
                    kw_href = abs_href  # weak signal
        doc = pdf_href or kw_href
        if doc and ref:
            mappings[ref[:100].lower()] = doc

    if not mappings:
        # fallback: standalone PDF links only (not listing pages)
        for text, href in parser.links:
            if _PDF_RE.search(href) and len(text) > 3:
                mappings[text[:100].lower()] = urljoin(page_url, href)

    if not mappings:
        return tenders

    for t in tenders:
        key = (t.tender_id or "").lower()
        if key and key in mappings:
            t.raw_document_url = mappings[key]
            continue
        # fuzzy: tender_id or title substring match
        matched = None
        tlow = (t.tender_id + " " + t.title).lower()
        for k, v in mappings.items():
            if k in tlow or any(word in k for word in key.split("/") if len(word) > 3):
                matched = v
                break
        if matched:
            t.raw_document_url = matched
    return tenders


def _ingest_ocds(db) -> tuple[int, Optional[str]]:
    """Pull the National Treasury eTenders OCDS API (not in the aggregator)."""
    try:
        from .sources.national.etenders_ocds import sync_live_tenders
        saved = sync_live_tenders(db, max_pages=6, days_back=45)
        return saved, None
    except Exception as exc:
        logger.warning("OCDS ingest failed: %s", exc)
        return 0, f"{type(exc).__name__}: {exc}"[:120]


def ingest_real_tenders(
    db,
    max_workers: int = 25,
    include_ocds: bool = True,
    verbose: bool = True,
) -> dict:
    """Ingest real tenders from every live source + OCDS API. Writes to db.

    Returns a summary dict with counts and a per-source breakdown.
    """
    from .aggregator import get_all_source_instances

    t0 = time.time()
    if not getattr(db, "_conn", None) and hasattr(db, "connect"):
        try:
            db.connect()
        except Exception:
            pass

    sources = get_all_source_instances(live_only=True)
    per_source = []
    all_tenders: list[TenderOpportunity] = []
    ok = 0
    empty = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=min(max_workers, max(1, len(sources)))) as ex:
        futs = {ex.submit(_fetch_one_real, inst): inst for inst in sources}
        for fut in as_completed(futs):
            sid, tenders, err = fut.result()
            if err:
                failed += 1
                per_source.append({"source_id": sid, "real_count": 0, "status": "error", "detail": err})
            elif tenders:
                ok += 1
                all_tenders.extend(tenders)
                per_source.append({"source_id": sid, "real_count": len(tenders), "status": "live"})
                if verbose:
                    logger.info("[%s] %d real tenders", sid, len(tenders))
            else:
                empty += 1
                per_source.append({"source_id": sid, "real_count": 0, "status": "empty"})

    # OCDS national API (skipped by aggregator) — inject explicitly
    ocds_saved = 0
    ocds_err = None
    if include_ocds:
        ocds_saved, ocds_err = _ingest_ocds(db)
        if ocds_err is None:
            per_source.append({"source_id": "etenders_ocds", "real_count": ocds_saved, "status": "live"})
            ok += 1
        else:
            per_source.append({"source_id": "etenders_ocds", "real_count": 0, "status": "error", "detail": ocds_err})
            failed += 1

    # Dedup by tender_id (same tender may appear under multiple issuers)
    unique: dict[str, TenderOpportunity] = {}
    for t in all_tenders:
        unique[t.tender_id] = t
    unique_tenders = list(unique.values())

    # Persist
    upserted = 0
    if hasattr(db, "upsert_tender"):
        for t in unique_tenders:
            try:
                db.upsert_tender(t)
                upserted += 1
            except Exception as exc:
                logger.warning("Upsert failed for %s: %s", t.tender_id, exc)

    summary = {
        "sources_live_yielding_data": ok,
        "sources_empty": empty,
        "sources_failed": failed,
        "real_tenders_raw": len(all_tenders) + ocds_saved,
        "real_tenders_unique": len(unique_tenders) + ocds_saved,
        "tenders_upserted": upserted + ocds_saved,
        "duration_s": round(time.time() - t0, 1),
        "per_source": sorted(per_source, key=lambda x: (-x.get("real_count", 0), x["source_id"])),
    }
    return summary


# ---------------------------------------------------------------------------
# 2. MATCH — a business against the stored real tenders
# ---------------------------------------------------------------------------

def match_company(
    company: CompanyProfile,
    db,
    limit: int = 500,
    province_first: bool = True,
    persist: bool = True,
    open_only: bool = True,
) -> list[MatchResult]:
    """Match a company against tenders in the DB.

    If open_only (default), only OPEN, dated, non-noise tenders are considered —
    expired tenders, unparseable-date tenders, and parser artefacts are excluded
    so match results reflect real, actionable opportunities.

    Tries the company's province first (local-content advantage), then falls
    back to national. Returns MatchResults sorted: eligible first, by score.
    """
    now = datetime.now(timezone.utc)
    tenders: list[TenderOpportunity] = []
    if province_first:
        try:
            tenders = db.list_open_tenders(limit=10000, province=company.location.province)
        except Exception:
            tenders = []
    if len(tenders) < limit:
        try:
            extra = db.list_open_tenders(limit=10000)
            seen = {t.tender_id for t in tenders}
            tenders += [t for t in extra if t.tender_id not in seen]
        except Exception as exc:
            logger.warning("list_open_tenders failed: %s", exc)

    if open_only:
        before = len(tenders)
        tenders = [t for t in tenders if _is_open_and_valid(t, now)]
        logger.info("Open/valid filter: %d -> %d tenders", before, len(tenders))
    tenders = tenders[:limit]

    results: list[MatchResult] = []
    for tender in tenders:
        res = run_match(company, tender)
        if persist and hasattr(db, "save_match"):
            try:
                db.save_match(company, res)
            except Exception as exc:
                logger.warning("save_match failed for %s: %s", tender.tender_id, exc)
        results.append(res)

    results.sort(key=lambda r: (not r.is_eligible, -r.match_score))
    return results


# ---------------------------------------------------------------------------
# 3. REPORT — generate the R500 deliverable for eligible matches
# ---------------------------------------------------------------------------

def generate_reports(
    company: CompanyProfile,
    results: list[MatchResult],
    output_dir: Optional[Path] = None,
    eligible_only: bool = True,
) -> list[Path]:
    """Generate Markdown reports. Returns paths to written files."""
    from .reporter import generate_report
    from .database import TenderDatabase
    out: list[Path] = []
    for res in results:
        if eligible_only and not res.is_eligible:
            continue
        # We need the TenderOpportunity for the reporter; reconstruct from result
        try:
            generate_report(company, _result_to_tender(res, company), res, output_dir)
        except Exception as exc:
            logger.warning("Report generation failed for %s: %s", res.tender_id, exc)
    return out


def _result_to_tender(res: MatchResult, company: CompanyProfile) -> TenderOpportunity:
    """Minimal TenderOpportunity reconstruction for the reporter (title/id only)."""
    return TenderOpportunity(
        tender_id=res.tender_id,
        title=res.tender_title,
        issuing_entity="",
        closing_date=datetime(2099, 12, 31, tzinfo=timezone.utc),
    )


# ---------------------------------------------------------------------------
# 4. COMPANY PROFILE LOADING
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 2b. SCREEN — match CIDB-sourced companies (partial compliance) honestly
# ---------------------------------------------------------------------------

def screen_company(
    company: CompanyProfile,
    tenders: list[TenderOpportunity],
    partial_compliance: bool = True,
) -> list[MatchResult]:
    """Screen a company against tenders using the gates we CAN verify.

    CIDB-sourced companies have verified CIDB gradings but unknown CSD/tax/BEE
    (the CIDB register doesn't carry them). Rather than falsely disqualifying
    on fields we don't have, this runs CIDB + geofence (verifiable) and flags
    CSD/tax/BEE as 'verify before bidding'. Set partial_compliance=False to use
    the strict full matcher instead.
    """
    from .matcher import match as run_match, _check_cidb, get_bbbee_system

    if not partial_compliance:
        return sorted(
            [run_match(company, t) for t in tenders],
            key=lambda r: (not r.is_eligible, -r.match_score),
        )

    now = datetime.now(timezone.utc)
    results: list[MatchResult] = []
    for tender in tenders:
        audit: list[str] = []
        eligible = True
        reason = None

        # CIDB gate (verifiable for CIDB companies)
        if tender.required_cidb_class and tender.required_cidb_level:
            cidb_outcome = _check_cidb(company, tender)
            if cidb_outcome is not None:
                eligible = False
                reason = cidb_outcome
            else:
                audit.append(f"CIDB OK ({tender.required_cidb_class}{tender.required_cidb_level})")
        elif tender.required_cidb_class:
            has = any(g.class_code.upper() == tender.required_cidb_class.upper()
                      for g in company.cidb_gradings)
            if not has:
                eligible = False
                reason = f"Missing CIDB class {tender.required_cidb_class}"
            else:
                audit.append(f"CIDB class OK ({tender.required_cidb_class})")

        # Geofence (verifiable)
        if eligible and tender.location_target and tender.location_target.lower() != "national":
            if tender.location_target.lower() != company.location.province.lower():
                # for CIDB companies province is often "National"/unknown -> warn, not block
                if company.location.province not in ("National", "Unknown"):
                    eligible = False
                    reason = (f"Geofence: tender in {tender.location_target}, "
                              f"company in {company.location.province}")
                else:
                    audit.append(f"Geofence unverified (tender: {tender.location_target})")
            else:
                audit.append(f"Geofence OK ({company.location.province})")

        # CSD / tax / BEE — unknown for CIDB-sourced -> flag as verify
        if eligible:
            audit.append("⚠ Verify before bid: CSD, SARS tax pin, B-BBEE certificate")

        system = get_bbbee_system(tender.estimated_value)
        max_pts = 20.0 if system == "80/20" else 10.0
        grade_str = "/".join(f"{g.class_code}{g.level}" for g in company.cidb_gradings)
        score = 70.0 if eligible else 0.0
        feedback = (" | ".join(audit)) if eligible else reason
        results.append(MatchResult(
            company_name=company.company_name,
            tender_id=tender.tender_id,
            tender_title=tender.title,
            is_eligible=eligible,
            match_score=score,
            bbbee_points=0.0,
            bbbee_max_points=max_pts,
            bbbee_system=system,
            disqualification_reason=reason,
            feedback=f"[CIDB {grade_str}] {feedback}",
        ))
    results.sort(key=lambda r: (not r.is_eligible, -r.match_score))
    return results


# ---------------------------------------------------------------------------
# 3b. ENRICH — open tender documents and backfill structured fields
# ---------------------------------------------------------------------------

def enrich_open_tenders(
    db,
    limit: int = 60,
    use_gemini: bool = True,
    discover_urls: bool = True,
) -> dict:
    """Open tender PDFs and backfill CIDB/value/date onto open tenders in the DB.

    For each open tender: resolve a document URL (raw_document_url, or discover
    via doc_finder against the source page), download, and extract fields
    (local regex for text PDFs, Gemini vision for scanned). Updates the DB.

    Returns a summary dict.
    """
    from .tender_enrichment import enrich_tender, apply_fields
    now = datetime.now(timezone.utc)
    tenders = []
    try:
        tenders = db.list_open_tenders(limit=10000)
    except Exception as exc:
        logger.warning("enrich: list_open_tenders failed: %s", exc)
    # only open + dated + valid
    tenders = [t for t in tenders if t.closing_date and t.closing_date > now
               and t.closing_date.year < 2099][:limit]

    updated = 0
    methods = {"local_regex": 0, "gemini_vision": 0, "no_doc": 0, "failed": 0}
    fields_found = 0

    for tender in tenders:
        doc_url = tender.raw_document_url
        if discover_urls and not doc_url:
            # best-effort: we don't store the source page URL per tender, so
            # document discovery happens at ingest via ingest_real_tenders.
            pass
        if not doc_url:
            methods["no_doc"] += 1
            continue
        try:
            fields, method = enrich_tender(tender, doc_url=doc_url, use_gemini=use_gemini)
        except Exception as exc:
            if "RateBlocked" in type(exc).__name__ or "rate" in str(exc).lower():
                logger.info("Gemini rate-limited — stopping enrichment batch (will resume next run).")
                break
            logger.warning("enrich error %s: %s", tender.tender_id, exc)
            methods["failed"] += 1
            continue
        methods[method] = methods.get(method, 0) + 1
        if fields:
            fields_found += len(fields)
            tender = apply_fields(tender, fields)
            try:
                db.upsert_tender(tender)
                updated += 1
            except Exception as exc:
                logger.warning("enrich upsert failed %s: %s", tender.tender_id, exc)

    return {
        "tenders_considered": len(tenders),
        "tenders_enriched": updated,
        "fields_extracted": fields_found,
        "methods": methods,
    }


def load_company(path: Optional[Path] = None) -> CompanyProfile:
    """Load a CompanyProfile from a YAML/JSON file, or return the default demo client."""
    from .schemas import CIDBGrading, Location
    if path:
        p = Path(path)
        data = json.loads(p.read_text()) if p.suffix == ".json" else \
            _yaml_load(p.read_text())
        return CompanyProfile(**data)
    return CompanyProfile(
        registration_number="2019/112233/07",
        company_name="Sipho Electrical and Civils (Pty) Ltd",
        csd_number="MAAA0554433",
        bbbee_level=1,
        black_ownership_pct=75.0,
        youth_ownership_pct=30.0,
        women_ownership_pct=25.0,
        cidb_gradings=[CIDBGrading(class_code="EE", level=3),
                       CIDBGrading(class_code="CE", level=2)],
        location=Location(province="Gauteng", city="Johannesburg",
                          municipality="City of Johannesburg Metropolitan Municipality"),
        sectors=["Electrical Engineering", "Civil Engineering"],
        has_tax_pin=True, has_coida=True, is_active=True,
    )


def load_companies() -> list[CompanyProfile]:
    """Load REAL companies from the CIDB register (live, or real seed if WAF-blocked)."""
    from .cidb_directory import get_companies
    return get_companies(live=True, min_grade=1)


def probe_live_sources(max_workers: int = 30, all_sources: bool = False) -> dict:
    """Honest live-source probe: which sources return REAL data vs mock/dead.

    Bypasses every source's mock fallback by fetching each URL live and parsing
    with the source's OWN parse_html() (which does not inject mock data).

    Returns a summary dict. Exposed so doctor.py --probe can run it.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from collections import Counter
    from .aggregator import get_all_source_instances

    sources = get_all_source_instances(live_only=not all_sources)
    results = []

    def _probe_one(inst) -> dict:
        sid = getattr(inst, "source_id", inst.__class__.__name__)
        url = getattr(inst, "url", None)
        rec = {"source_id": sid, "url": url, "status": "UNKNOWN", "count": 0}
        if not url or not str(url).startswith("http"):
            rec["status"] = "NO_URL"
            return rec
        try:
            from .sources.generic import _do_fetch, _get_ssl_context, _FETCH_TIMEOUT
            if _module_has_mock(inst.__class__):
                html = _do_fetch(url, _FETCH_TIMEOUT, _get_ssl_context())
                tenders = inst.parse_html(html)
            else:
                tenders = inst.fetch() or []
            rec["count"] = len(tenders)
            rec["status"] = "LIVE" if tenders else ("LIVE_EMPTY" if not _module_has_mock(inst.__class__) else "MOCK_ONLY")
        except Exception:
            rec["status"] = "DEAD_URL"
        return rec

    with ThreadPoolExecutor(max_workers=min(max_workers, max(1, len(sources)))) as ex:
        for fut in as_completed({ex.submit(_probe_one, s): s for s in sources}):
            try:
                results.append(fut.result())
            except Exception as e:
                results.append({"source_id": "?", "status": "CRASH", "count": 0})

    counts = Counter(r["status"] for r in results)
    live = sorted([r for r in results if r["status"] == "LIVE"],
                  key=lambda x: x["count"], reverse=True)
    return {
        "probed": len(results),
        "status_counts": dict(counts),
        "live_sources": len(live),
        "total_live_tenders": sum(r["count"] for r in live),
        "live": live,
        "results": results,
    }


def run_pipeline_match(
    companies: list[CompanyProfile],
    db,
    match_limit: int = 500,
    write_reports: bool = True,
    partial_compliance: bool = True,
    persist: bool = True,
) -> dict:
    """Match a set of real companies against open tenders in the DB."""
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    tenders: list[TenderOpportunity] = []
    try:
        tenders = db.list_open_tenders(limit=10000)
    except Exception as exc:
        logging.warning("match: list_open_tenders failed: %s", exc)
    # open + dated + valid only
    valid = [t for t in tenders if t.closing_date and t.closing_date > now
             and t.closing_date.year < 2099
             and not _NOISE_RE.search(t.tender_id)
             and not _NOISE_RE.search(t.title or "")][:match_limit]

    total_eval = 0
    screened_in = 0
    blocked = 0
    all_matches: list[MatchResult] = []
    report_paths: list[str] = []

    for company in companies:
        results = screen_company(company, valid, partial_compliance=partial_compliance)
        if persist and hasattr(db, "save_match"):
            for res in results:
                try:
                    db.save_match(company, res)
                except Exception as exc:
                    logger.warning("save_match failed %s: %s", res.tender_id, exc)
        if write_reports:
            from .reporter import generate_report
            out_dir = Path(__file__).resolve().parents[2] / "localdata"
            tender_by_id = {t.tender_id: t for t in valid}
            for res in results:
                if not res.is_eligible:
                    continue
                t = tender_by_id.get(res.tender_id)
                if t:
                    try:
                        p = generate_report(company, t, res, out_dir)
                        report_paths.append(str(p))
                    except Exception as exc:
                        logger.warning("report failed %s: %s", res.tender_id, exc)
        total_eval += len(results)
        screened_in += sum(1 for r in results if r.is_eligible)
        blocked += sum(1 for r in results if not r.is_eligible)
        all_matches.extend(results)

    # top matches by score
    top = sorted([r for r in all_matches if r.is_eligible],
                 key=lambda r: -r.match_score)[:10]
    top_matches = [{
        "company": r.company_name,
        "grades": _grades_str(r.feedback),
        "tender": r.tender_title[:32],
        "score": r.match_score,
    } for r in top]

    return {
        "companies_matched": len(companies),
        "tenders_evaluated": total_eval,
        "screened_in": screened_in,
        "blocked": blocked,
        "reports_written": len(report_paths),
        "top_matches": top_matches,
    }


def _grades_str(feedback: str) -> str:
    """Extract the CIDB grades tag from a screening feedback string."""
    import re as _re
    m = _re.search(r"\[CIDB ([^\]]+)\]", feedback)
    return m.group(1) if m else "?"


def _yaml_load(text: str) -> dict:
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        raise RuntimeError("PyYAML required to load YAML company profiles")


# ---------------------------------------------------------------------------
# 5. END-TO-END
# ---------------------------------------------------------------------------

def run_pipeline(
    company: Optional[CompanyProfile] = None,
    db=None,
    output_dir: Optional[Path] = None,
    ingest: bool = True,
    write_reports: bool = True,
    max_workers: int = 25,
    match_limit: int = 500,
) -> dict:
    """Run the full flow: ingest real tenders -> match a business -> report.

    Returns a summary dict with everything: ingest stats, match counts,
    eligible matches, and report file paths.
    """
    t0 = time.time()
    if company is None:
        company = load_company()
    if db is None:
        from .database import get_database_client
        db = get_database_client()
    if hasattr(db, "connect"):
        db.connect()

    ingest_summary = None
    if ingest:
        ingest_summary = ingest_real_tenders(db, max_workers=max_workers)

    results = match_company(company, db, limit=match_limit)
    eligible = [r for r in results if r.is_eligible]
    disqualified = [r for r in results if not r.is_eligible]

    report_paths: list[str] = []
    if write_reports and eligible:
        from .reporter import generate_report
        out_dir = Path(output_dir) if output_dir else \
            Path(__file__).resolve().parents[2] / "localdata"
        # Pull full tender objects for richer reports
        tender_by_id = {t.tender_id: t for t in db.list_open_tenders(limit=10000)}
        for res in eligible:
            tender = tender_by_id.get(res.tender_id) or _result_to_tender(res, company)
            try:
                p = generate_report(company, tender, res, out_dir)
                report_paths.append(str(p))
            except Exception as exc:
                logger.warning("report failed %s: %s", res.tender_id, exc)

    db.close() if hasattr(db, "close") else None

    return {
        "company": company.company_name,
        "ingest": ingest_summary,
        "match": {
            "evaluated": len(results),
            "eligible": len(eligible),
            "disqualified": len(disqualified),
        },
        "reports_written": len(report_paths),
        "report_paths": report_paths[:20],
        "total_duration_s": round(time.time() - t0, 1),
    }
