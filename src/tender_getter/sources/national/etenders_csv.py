"""National Treasury eTenders CSV bulk – https://data.etenders.gov.za/"""
import logging
import csv
import io
from typing import Optional
from urllib.request import urlopen, Request

from ...schemas import TenderOpportunity
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

def parse_csv_row_to_tender(row: dict) -> Optional[TenderOpportunity]:
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
    closing_date = parse_closing_date(closing_str)
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
    except Exception as exc:
        logger.warning("Failed to parse CSV row %s: %s", tender_id, exc)
        return None

def sync_csv(db, csv_path: str, limit: Optional[int] = None) -> int:
    saved = 0
    if csv_path.startswith("http://") or csv_path.startswith("https://"):
        req = Request(csv_path, headers={"User-Agent": "Tender-Getter-RSA/1.1"})
        with urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        f = io.StringIO(text)
    else:
        f = open(csv_path, "r", encoding="utf-8", newline="")
    try:
        reader = csv.DictReader(f)
        for row in reader:
            if limit is not None and saved >= limit:
                break
            tender = parse_csv_row_to_tender(row)
            if tender:
                db.upsert_tender(tender)
                saved += 1
    finally:
        f.close()
    logger.info("sync_csv: saved %d tenders from %s", saved, csv_path)
    return saved
