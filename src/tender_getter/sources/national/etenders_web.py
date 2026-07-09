"""eTenders.gov.za Web API source – scrapes the paginated opportunities endpoint.

URL: https://www.etenders.gov.za/Home/PaginatedTenderOpportunities
This is the server-side DataTables endpoint that powers the eTenders portal.

Status codes:
  1 = Currently Advertised
  2 = Awarded
  3 = Closed
  4 = Cancelled

Rich structured data per tender:
  - tender_No, description, category, type, organ_of_State
  - closing_Date, date_Published
  - province, contactPerson, email, telephone
  - briefingSession, briefingCompulsory, briefingVenue
  - eSubmission, supportDocument (PDF downloads)
  - validity period, conditions

Complements the existing OCDS API source by providing:
  - Currently advertised tenders (OCDS API doesn't filter by status)
  - Contact person details
  - PDF document links
  - 1,883+ live tenders at any time
"""
from __future__ import annotations

import logging
import os
import json
import ssl
from datetime import datetime, timezone
from typing import Dict, List, Optional
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from ...schemas import TenderOpportunity
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

_BASE_URL = "https://www.etenders.gov.za"
_PAGINATED_ENDPOINT = f"{_BASE_URL}/Home/PaginatedTenderOpportunities"
_REFERER = f"{_BASE_URL}/Home/opportunities?id=1"

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
_FETCH_TIMEOUT = int(os.environ.get("TENDER_FETCH_TIMEOUT", "20"))
_PAGE_SIZE = int(os.environ.get("ETENDERS_WEB_PAGE_SIZE", "100"))
_MAX_PAGES = int(os.environ.get("ETENDERS_WEB_MAX_PAGES", "20"))

# Status codes for the eTenders portal
STATUS_ADVERTISED = 1
STATUS_AWARDED = 2
STATUS_CLOSED = 3
STATUS_CANCELLED = 4


def _get_ssl_ctx() -> Optional[ssl.SSLContext]:
    try:
        return ssl._create_unverified_context()
    except Exception:
        return None


def _fetch_page(
    status: int = STATUS_ADVERTISED,
    start: int = 0,
    length: int = 100,
    draw: int = 1,
) -> Optional[dict]:
    """Fetch one page of tender data from the eTenders paginated endpoint.

    Returns the raw JSON response dict, or None on failure.
    """
    params = {
        "draw": draw,
        "start": start,
        "length": length,
        "status": status,
    }
    url = f"{_PAGINATED_ENDPOINT}?{urlencode(params)}"
    req = Request(url, headers={
        "User-Agent": _USER_AGENT,
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": _REFERER,
    })
    kwargs: dict = {"timeout": _FETCH_TIMEOUT}
    ssl_ctx = _get_ssl_ctx()
    if ssl_ctx:
        kwargs["context"] = ssl_ctx

    try:
        with urlopen(req, **kwargs) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except (URLError, HTTPError, json.JSONDecodeError, TimeoutError) as exc:
        logger.warning("eTenders web fetch failed (status=%d, start=%d): %s", status, start, exc)
        return None


def _parse_tender_row(row: dict) -> Optional[TenderOpportunity]:
    """Parse one eTenders web API row into a TenderOpportunity."""
    tender_no = (row.get("tender_No") or "").strip()
    description = (row.get("description") or "").strip()
    department = (row.get("organ_of_State") or row.get("department") or "").strip()
    closing_str = row.get("closing_Date") or ""
    published_str = row.get("date_Published") or ""
    province = row.get("province") or ""
    category = row.get("category") or ""
    tender_type = row.get("type") or ""

    if not tender_no and not description:
        return None

    # Use tender_No as primary ref; fall back to row id
    ref = tender_no or f"ET-{row.get('id', 'unknown')}"

    # Build title: tender_No + description
    title = f"{ref}: {description}"[:500] if ref != tender_no else description[:500]
    if tender_no and description and tender_no != description:
        title = f"{tender_no}: {description}"[:500]

    # Closing date
    closing_date = parse_closing_date(closing_str)

    # Province
    location = province if province else None

    # CIDB
    combined_text = f"{ref} {description} {category}"
    cidb_hit = re_search_cidb(combined_text)
    cidb_level = int(cidb_hit[0]) if cidb_hit else None
    cidb_class = cidb_hit[1] if cidb_hit else None

    # Document URL – first support document
    doc_url: Optional[str] = None
    support_docs = row.get("supportDocument") or []
    if isinstance(support_docs, list) and support_docs:
        first_doc = support_docs[0] if support_docs else {}
        doc_guid = first_doc.get("supportDocumentID", "")
        if doc_guid:
            doc_url = f"{_BASE_URL}/Home/Download/?blobName={doc_guid}"

    return TenderOpportunity(
        tender_id=ref[:100],
        title=title,
        issuing_entity=department or "eTenders.gov.za",
        closing_date=closing_date,
        estimated_value=None,
        required_cidb_class=cidb_class,
        required_cidb_level=cidb_level,
        mandatory_csd=True,
        tax_compliance_required=True,
        location_target=location,
        raw_document_url=doc_url,
    )


def fetch_etenders_web(
    status: int = STATUS_ADVERTISED,
    limit: Optional[int] = None,
    max_pages: int = 0,
) -> List[TenderOpportunity]:
    """Fetch tenders from eTenders.gov.za web API.

    Args:
        status: 1=Advertised, 2=Awarded, 3=Closed, 4=Cancelled
        limit: Max tenders to return (None = no limit)
        max_pages: Max pages to fetch (0 = auto, uses _MAX_PAGES)
    """
    all_tenders: List[TenderOpportunity] = []
    seen_ids: set = set()
    page_size = _PAGE_SIZE
    max_p = max_pages if max_pages > 0 else _MAX_PAGES
    draw = 1

    for page in range(max_p):
        start = page * page_size
        if limit is not None and start >= limit:
            break

        data = _fetch_page(status=status, start=start, length=page_size, draw=draw)
        if not data:
            break

        records_total = data.get("recordsTotal", 0)
        rows = data.get("data", [])

        if not rows:
            break

        for row in rows:
            tender = _parse_tender_row(row)
            if tender and tender.tender_id not in seen_ids:
                seen_ids.add(tender.tender_id)
                all_tenders.append(tender)

        if page == 0:
            logger.info(
                "eTenders web: status=%d, recordsTotal=%d, first page=%d rows",
                status, records_total, len(rows),
            )

        # If we got fewer rows than page_size, we've reached the end
        if len(rows) < page_size:
            break

        draw += 1

    if limit is not None:
        all_tenders = all_tenders[:limit]

    logger.info(
        "eTenders web: status=%d → %d unique tenders (%d pages)",
        status, len(all_tenders), min(page + 1, max_p),
    )
    return all_tenders


class ETendersWebSource:
    """eTenders.gov.za web API source – currently advertised tenders.

    This source uses the paginated DataTables endpoint which provides
    rich structured data for all currently advertised tenders.

    Complements the existing OCDS API source (etenders_ocds.py) by providing:
      - Currently advertised tenders with status filter
      - Contact person details and document URLs
      - Fresh data from the live portal
    """

    source_id: str = "etenders_web"
    live: bool = True

    def __init__(self, status: int = STATUS_ADVERTISED):
        self.status = status
        self.source_id = f"etenders_web_status{status}"

    def fetch(self, limit: Optional[int] = None, **kw) -> List[TenderOpportunity]:
        """Fetch tenders from eTenders.gov.za web API."""
        return fetch_etenders_web(
            status=self.status,
            limit=limit,
            max_pages=0,  # auto
        )
