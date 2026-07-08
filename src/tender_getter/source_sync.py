"""
source_sync.py - Live tender ingestion from the SA National Treasury OCDS API.

Connects to: https://ocds-api.etenders.gov.za
Parses OCDS-format release objects into TenderOpportunity schemas,
then persists them to the database.

Also supports CSV bulk import from https://data.etenders.gov.za/
and a sources.yaml registry loader.

Key responsibilities:
 - re_search_cidb(): regex extractor for CIDB codes in free text (e.g. "5GB", "3CE")
 - province_from_text(): maps common abbreviations/keywords to full province names
 - parse_ocds_release_to_tender(): converts a raw OCDS dict to TenderOpportunity
 - parse_csv_row_to_tender(): converts an eTenders CSV row to TenderOpportunity
 - sync_live_tenders(): hits the live OCDS API and persists results
 - sync_csv_tenders(): ingests a local/remote eTenders CSV file
 - load_sources(): loads src/tender_getter/sources.yaml
"""

import re
import logging
import csv
import io
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from urllib.request import urlopen, Request
from urllib.error import URLError
import json
from pathlib import Path

from .schemas import TenderOpportunity

# Accept any DB that implements upsert_tender – SQLite, Postgres, Supabase
# Import only for type checking to avoid circular imports at runtime
try:
    from .database_base import TenderDatabaseBase  # type: ignore
except ImportError:
    TenderDatabaseBase = Any  # type: ignore

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
# Sources registry loader
# ---------------------------------------------------------------------------

def load_sources() -> List[Dict[str, Any]]:
    """
    Load src/tender_getter/sources.yaml
    Returns [] if PyYAML is not installed or file is missing –
    keeps tests green in minimal environments.
    """
    try:
        import yaml  # type: ignore
    except ImportError:
        logger.warning("PyYAML not installed – load_sources() returning empty list")
        return []
    sources_path = Path(__file__).parent / "sources.yaml"
    if not sources_path.exists():
        return []
    with sources_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("sources", []) if isinstance(data, dict) else []


# ---------------------------------------------------------------------------
# Public helpers (also used by tests)
# ---------------------------------------------------------------------------

def re_search_cidb(text: str) -> Optional[tuple[str, str]]:
    """
    Searches free text for a CIDB grading code and returns (level, class_code)
    or None if no valid code is found.

    Examples:
    "Requires 3CE grading" -> ("3", "CE")
    "Level 4GB contractor only" -> ("4", "GB")
    "9EP substation works" -> ("9", "EP")
    "No CIDB grading required" -> None
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

def _parse_closing_date(s: Optional[str]) -> datetime:
    """Parse various eTenders date formats to timezone-aware datetime."""
    if not s:
        return datetime(2099, 12, 31, tzinfo=timezone.utc)
    s = s.strip()
    # Try ISO8601 first
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        pass
    # Try common SA formats: YYYY/MM/DD HH:MM:SS, DD-MM-YYYY, etc.
    for fmt in ("%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s[:19], fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return datetime(2099, 12, 31, tzinfo=timezone.utc)

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
        closing_date = _parse_closing_date(end_date_str)

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

# ---------------------------------------------------------------------------
# CSV bulk import – data.etenders.gov.za
# ---------------------------------------------------------------------------

def parse_csv_row_to_tender(row: dict) -> Optional[TenderOpportunity]:
    """
    Convert a single eTenders CSV row (OCDS flat export from data.etenders.gov.za)
    into a TenderOpportunity.

    Expected columns (case-insensitive, extra columns ignored):
      tender_id / tender/id
      tender_title / tender/title
      buyer_name
      tender_period_enddate
      tender_description
    """
    # Normalize keys to lower
    r = {str(k).lower(): v for k, v in row.items()}

    def get(*keys: str) -> str:
        for k in keys:
            if k in r and r[k]:
                return str(r[k]).strip()
        return ""

    tender_id = get("tender_id", "tender/id", "ocid", "id")
    title = get("tender_title", "tender/title", "title")
    issuer = get("buyer_name", "buyer/name", "issuing_entity", "department")
    description = get("tender_description", "tender/description", "description", "")
    closing_str = get("tender_period_enddate", "tender_period_enddate", "closing_date", "enddate")
    value_str = get("planning_budget_amount_amount", "tender_value_amount", "estimated_value", "value")

    if not tender_id or not title:
        return None

    closing_date = _parse_closing_date(closing_str)

    estimated_value: Optional[float] = None
    if value_str:
        try:
            estimated_value = float(str(value_str).replace(",", "").replace("R", "").strip())
        except (ValueError, TypeError):
            estimated_value = None

    combined_text = f"{title} {description}"
    cidb_hit = re_search_cidb(combined_text)
    required_cidb_level = int(cidb_hit[0]) if cidb_hit else None
    required_cidb_class = cidb_hit[1] if cidb_hit else None
    location_target = province_from_text(combined_text)

    try:
        return TenderOpportunity(
            tender_id=tender_id,
            title=title,
            issuing_entity=issuer or "Unknown Issuer",
            closing_date=closing_date,
            estimated_value=estimated_value,
            required_cidb_class=required_cidb_class,
            required_cidb_level=required_cidb_level,
            mandatory_csd=True,
            tax_compliance_required=True,
            location_target=location_target,
            raw_document_url=None,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to parse CSV row %s: %s", tender_id, exc)
        return None

def sync_csv_tenders(db, csv_path: str, limit: Optional[int] = None) -> int:
    """
    Ingest tenders from an eTenders CSV export.
    csv_path can be a local file path or an http(s) URL.
    Returns number of tenders saved.
    """
    saved = 0
    # Open local or remote
    if csv_path.startswith("http://") or csv_path.startswith("https://"):
        req = Request(csv_path, headers={"User-Agent": "Tender-Getter-RSA/1.1"})
        with urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        f = io.StringIO(text)
    else:
        f = open(csv_path, "r", encoding="utf-8", newline="")

    try:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if limit is not None and saved >= limit:
                break
            tender = parse_csv_row_to_tender(row)
            if tender:
                db.upsert_tender(tender)
                saved += 1
    finally:
        f.close()

    logger.info("sync_csv_tenders: saved %d tenders from %s", saved, csv_path)
    return saved

# ---------------------------------------------------------------------------
# Live OCDS sync
# ---------------------------------------------------------------------------

def sync_live_tenders(db, max_pages: int = 3) -> int:
    """
    Fetches live tender releases from the eTenders OCDS API and persists
    them to the database.

    db: any object with .upsert_tender(tender) – SQLite, Postgres, or Supabase
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
