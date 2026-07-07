"""
source_sync.py - Live tender ingestion from the SA National Treasury OCDS API.

Connects to: https://ocds-api.etenders.gov.za
Parses OCDS-format release objects into TenderOpportunity schemas,
then persists them to the local SQLite database.

Key responsibilities:
  - re_search_cidb(): regex extractor for CIDB codes in free text (e.g. "5GB", "3CE")
  - province_from_text(): maps common abbreviations/keywords to full province names
  - parse_ocds_release_to_tender(): converts a raw OCDS dict to TenderOpportunity
  - sync_live_tenders(): hits the live API and persists results to the database
"""

import re
import logging
from datetime import datetime, timezone
from typing import Optional
from urllib.request import urlopen, Request
from urllib.error import URLError
import json

from .schemas import TenderOpportunity
from .database import TenderDatabase

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OCDS_API_BASE = "https://ocds-api.etenders.gov.za"
OCDS_RELEASES_ENDPOINT = f"{OCDS_API_BASE}/api/v1/releases"

# Regex: matches patterns like "3CE", "5 GB", "Level 4GB", "9EP"
# Captures (level_digit, class_code) e.g. ("3", "CE")
_CIDB_PATTERN = re.compile(
    r"(?:level\s*)?(\d)\s*([A-Z]{2})\b",
    re.IGNORECASE,
)

# Province name normalisation map
_PROVINCE_MAP: dict[str, str] = {
    "gauteng": "Gauteng",
    "gp": "Gauteng",
    "gt": "Gauteng",
    "western cape": "Western Cape",
    "wc": "Western Cape",
    "eastern cape": "Eastern Cape",
    "ec": "Eastern Cape",
    "kwazulu-natal": "KwaZulu-Natal",
    "kwazulu natal": "KwaZulu-Natal",
    "kzn": "KwaZulu-Natal",
    "limpopo": "Limpopo",
    "lp": "Limpopo",
    "mpumalanga": "Mpumalanga",
    "mp": "Mpumalanga",
    "north west": "North West",
    "nw": "North West",
    "northern cape": "Northern Cape",
    "nc": "Northern Cape",
    "free state": "Free State",
    "fs": "Free State",
}

# Known CIDB valid class codes
_VALID_CIDB_CLASSES = {
    "CE", "GB", "EE", "ME", "SB", "PE", "PS", "EP", "SF", "SI", "SO", "SP", "SW",
}


# ---------------------------------------------------------------------------
# Public helpers (also used by tests)
# ---------------------------------------------------------------------------

def re_search_cidb(text: str) -> Optional[tuple[str, str]]:
    """
    Searches free text for a CIDB grading code and returns (level, class_code)
    or None if no valid code is found.

    Examples:
      "Requires 3CE grading"          -> ("3", "CE")
      "Level 4GB contractor only"     -> ("4", "GB")
      "9EP substation works"          -> ("9", "EP")
      "No CIDB grading required"      -> None
    """
    for match in _CIDB_PATTERN.finditer(text):
        level_str = match.group(1)
        class_code = match.group(2).upper()
        if class_code in _VALID_CIDB_CLASSES and 1 <= int(level_str) <= 9:
            return (level_str, class_code)
    return None


def province_from_text(text: str) -> Optional[str]:
    """
    Attempts to extract a South African province name from arbitrary text.
    Returns the normalised full province name, or None.
    """
    if not text:
        return None
    text_lower = text.lower()
    for key, province in _PROVINCE_MAP.items():
        if re.search(r"\b" + re.escape(key) + r"\b", text_lower):
            return province
    return None


def parse_ocds_release_to_tender(release: dict) -> Optional[TenderOpportunity]:
    """
    Converts a raw OCDS release dict (from the eTenders API) into a
    TenderOpportunity, or returns None if mandatory fields are missing.

    CIDB and geofencing are extracted by scanning title + description text.
    """
    try:
        ocid = release.get("ocid", "")
        buyer = release.get("buyer", {})
        tender_block = release.get("tender", {})

        title = tender_block.get("title", "").strip()
        description = tender_block.get("description", "")
        issuer = buyer.get("name", "Unknown Issuer")

        # Closing date
        end_date_str = (
            tender_block.get("tenderPeriod", {}).get("endDate")
        )
        if end_date_str:
            closing_date = datetime.fromisoformat(
                end_date_str.replace("Z", "+00:00")
            )
        else:
            closing_date = datetime(2099, 12, 31, tzinfo=timezone.utc)

        # Estimated value
        value_block = tender_block.get("value", {})
        estimated_value: Optional[float] = value_block.get("amount")

        # CIDB extraction from title + description
        combined_text = f"{title} {description}"
        cidb_hit = re_search_cidb(combined_text)
        required_cidb_level: Optional[int] = None
        required_cidb_class: Optional[str] = None
        if cidb_hit:
            required_cidb_level = int(cidb_hit[0])
            required_cidb_class = cidb_hit[1]

        # Province / geofencing
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
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to parse OCDS release %s: %s", release.get("ocid"), exc)
        return None


def sync_live_tenders(db: TenderDatabase, max_pages: int = 3) -> int:
    """
    Fetches live tender releases from the eTenders OCDS API and persists
    them to the database.

    Returns the number of tenders successfully saved.
    """
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
