"""National Treasury eTenders OCDS API – https://ocds-api.etenders.gov.za"""
import logging
import json
from typing import Optional
from urllib.request import urlopen, Request
from urllib.error import URLError

from ..schemas import TenderOpportunity
from .common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

OCDS_API_BASE = "https://ocds-api.etenders.gov.za"
OCDS_RELEASES_ENDPOINT = f"{OCDS_API_BASE}/api/v1/releases"

def parse_ocds_release_to_tender(release: dict) -> Optional[TenderOpportunity]:
    try:
        ocid = release.get("ocid", "")
        buyer = release.get("buyer", {})
        tender_block = release.get("tender", {})
        title = tender_block.get("title", "").strip()
        description = tender_block.get("description", "")
        issuer = buyer.get("name", "Unknown Issuer")
        end_date_str = tender_block.get("tenderPeriod", {}).get("endDate")
        closing_date = parse_closing_date(end_date_str)
        value_block = tender_block.get("value", {})
        estimated_value: Optional[float] = value_block.get("amount")
        combined_text = f"{title} {description}"
        cidb_hit = re_search_cidb(combined_text)
        required_cidb_level = int(cidb_hit[0]) if cidb_hit else None
        required_cidb_class = cidb_hit[1] if cidb_hit else None
        location_target = province_from_text(combined_text)
        if not ocid or not title:
            return None
        return TenderOpportunity(
            tender_id=ocid,
            title=title,
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

def sync_live_tenders(db, max_pages: int = 3) -> int:
    saved = 0
    page = 1
    while page <= max_pages:
        url = f"{OCDS_RELEASES_ENDPOINT}?page={page}&pageSize=50"
        try:
            req = Request(url, headers={"Accept": "application/json"})
            with urlopen(req, timeout=15) as resp:
                payload = json.loads(resp.read().decode())
        except (URLError, json.JSONDecodeError) as exc:
            logger.error("Failed to fetch page %d from OCDS API: %s", page, exc)
            break
        releases = payload.get("releases", payload.get("data", []))
        if not releases:
            break
        for release in releases:
            tender = parse_ocds_release_to_tender(release)
            if tender:
                db.upsert_tender(tender)
                saved += 1
        page += 1
    logger.info("sync_live_tenders: saved %d tenders from %d pages.", saved, page - 1)
    return saved
