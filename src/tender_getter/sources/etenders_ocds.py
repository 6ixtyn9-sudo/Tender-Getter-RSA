# src/tender_getter/sources/etenders_ocds.py
"""National Treasury eTenders OCDS API – https://ocds-api.etenders.gov.za"""
import logging
import json
from datetime import datetime, timezone, timedelta
from typing import Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode

from ..schemas import TenderOpportunity
from .common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

OCDS_API_BASE = "https://ocds-api.etenders.gov.za"
OCDS_RELEASES_ENDPOINT = f"{OCDS_API_BASE}/api/OCDSReleases"

def _normalize_province(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    p = province_from_text(raw)
    return p or raw.strip().title()

def _pick_title(tender_number: str, description: str) -> str:
    """
    eTenders OCDS API v1 (2024+): tender.title is often the tender reference
    number (e.g. "SCM/1337/S/2025-2026"), tender.description is the real title.
    Old test fixtures / older API: tender.title is already descriptive.
    
    Heuristic: if title looks like a ref (contains '/' and is < 60 chars)
    and description is substantially longer, use description as title,
    prefixed with the ref for traceability.
    Otherwise keep title as-is (backwards compatible with tests).
    """
    tn = (tender_number or "").strip()
    desc = (description or "").strip()
    if not tn:
        return desc or "Untitled Tender"
    if not desc:
        return tn
    # Is tn likely a reference number? contains / and is relatively short
    is_ref = "/" in tn and len(tn) < 60
    # Is description substantially more descriptive?
    desc_is_better = len(desc) > 30 and len(desc) > len(tn)
    if is_ref and desc_is_better:
        return f"{tn}: {desc}"[:500]
    # Default – keep original title, append description if it's different and useful
    if desc.lower() not in tn.lower() and len(desc) > 10:
        # For old-style records where title is already descriptive,
        # don't duplicate – just use title
        # Only append if description adds meaningful content and isn't already included
        return tn
    return tn

def parse_ocds_release_to_tender(release: dict) -> Optional[TenderOpportunity]:
    try:
        ocid = release.get("ocid", "")
        buyer = release.get("buyer", {})
        tender_block = release.get("tender", {})

        tender_number = tender_block.get("title", "").strip()
        description = tender_block.get("description", "")
        title = _pick_title(tender_number, description)
        issuer = buyer.get("name", "Unknown Issuer")

        end_date_str = tender_block.get("tenderPeriod", {}).get("endDate")
        closing_date = parse_closing_date(end_date_str)

        value_block = tender_block.get("value", {})
        estimated_value: Optional[float] = value_block.get("amount")
        if estimated_value == 0:
            estimated_value = None

        combined_text = f"{tender_number} {title} {description}"
        cidb_hit = re_search_cidb(combined_text)
        required_cidb_level = int(cidb_hit[0]) if cidb_hit else None
        required_cidb_class = cidb_hit[1] if cidb_hit else None

        # Province – use structured field first (new API), fallback to text scan
        location_target = (
            _normalize_province(tender_block.get("province"))
            or province_from_text(combined_text)
        )

        if not ocid or not title:
            return None

        return TenderOpportunity(
            tender_id=ocid,
            title=title[:500],
            issuing_entity=issuer,
            closing_date=closing_date,
            estimated_value=estimated_value,
            required_cidb_class=required_cidb_class,
            required_cidb_level=required_cidb_level,
            mandatory_csd=True,
            tax_compliance_required=True,
            location_target=location_target,
        )
    except Exception as exc:
        logger.warning("Failed to parse OCDS release %s: %s", release.get("ocid"), exc)
        return None

def sync_live_tenders(db, max_pages: int = 3, days_back: int = 30) -> int:
    """
    Fetches live tender releases from the eTenders OCDS API and persists them.

    db: any object with .upsert_tender(tender)
    Returns number of tenders successfully saved.
    """
    saved = 0
    page = 1
    end_dt = datetime.now(timezone.utc)
    start_dt = end_dt - timedelta(days=days_back)
    date_from = start_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    date_to = end_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    while page <= max_pages:
        params = {
            "PageNumber": page,
            "PageSize": 100,
            "dateFrom": date_from,
            "dateTo": date_to,
        }
        url = f"{OCDS_RELEASES_ENDPOINT}?{urlencode(params)}"
        try:
            req = Request(url, headers={
                "Accept": "application/json",
                "User-Agent": "Tender-Getter-RSA/1.3"
            })
            with urlopen(req, timeout=20) as resp:
                payload = json.loads(resp.read().decode())
        except (URLError, HTTPError, json.JSONDecodeError) as exc:
            logger.error("Failed to fetch page %d from OCDS API: %s", page, exc)
            break

        releases = payload.get("releases", [])
        if not releases:
            break

        for release in releases:
            tender = parse_ocds_release_to_tender(release)
            if tender:
                db.upsert_tender(tender)
                saved += 1

        if len(releases) < 100:
            break
        page += 1

    logger.info("sync_live_tenders: saved %d tenders from %d pages (window %s to %s)",
                saved, page, date_from[:10], date_to[:10])
    return saved
