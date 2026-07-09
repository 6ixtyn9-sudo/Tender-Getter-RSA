"""WordPress REST API source – fetches tenders from WP sites with custom post types.

Replaces Playwright/Selenium for sites that expose tender data via wp-json.
Each WP source specifies its base URL and custom post type slug.
"""
from __future__ import annotations

import json
import logging
import re
import ssl
from typing import List, Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from ..schemas import TenderOpportunity
from .common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

_USER_AGENT = "Tender-Getter-RSA/2.0"
_FETCH_TIMEOUT = 15
_TAG_STRIP = re.compile(r"<[^>]+>")
_RFP_REF = re.compile(r"\b(RFP|RFQ|Bid|SCM|TEND)[\s:/-]*([\w][\w\s/-]+\d{2,})\b", re.IGNORECASE)
_NUM_REF = re.compile(r"\b([A-Z]{2,}[\s/]*\d{2,}[\s/]*\d{2,4})\b")


def _ssl_ctx():
    try:
        return ssl._create_unverified_context()
    except Exception:
        return None


def wp_fetch_tenders(
    source_id: str,
    url: str,
    post_type: str = "tenders",
    issuing_entity: str = "",
    default_location: str = "National",
    limit: Optional[int] = None,
) -> List[TenderOpportunity]:
    """Fetch tenders from a WordPress REST API endpoint.

    Args:
        source_id: Source identifier (e.g. "george_lm")
        url: Base site URL (e.g. "https://www.george.gov.za")
        post_type: WP custom post type slug (e.g. "supply-chain-categor")
        issuing_entity: Human-readable entity name
        default_location: Default province/location
        limit: Max items to return

    Returns:
        List of parsed TenderOpportunity instances
    """
    api_url = f"{url.rstrip('/')}/wp-json/wp/v2/{post_type}?per_page={min(limit or 20, 100)}"
    ctx = _ssl_ctx()
    try:
        req = Request(api_url, headers={
            "User-Agent": _USER_AGENT,
            "Accept": "application/json",
        })
        kwargs = {"timeout": _FETCH_TIMEOUT}
        if ctx:
            kwargs["context"] = ctx
        with urlopen(req, **kwargs) as resp:
            items = json.loads(resp.read())
    except Exception as exc:
        logger.warning("WP API failed for %s: %s", source_id, exc)
        return []

    if not isinstance(items, list):
        return []

    return _parse_wp_items(items, source_id, issuing_entity, default_location, limit)


def _parse_wp_items(
    items: list,
    source_id: str,
    issuing_entity: str,
    default_location: str,
    limit: Optional[int] = None,
) -> List[TenderOpportunity]:
    tenders: List[TenderOpportunity] = []
    for item in items:
        raw_title = item.get("title", {}).get("rendered", "")
        title = _TAG_STRIP.sub("", raw_title).strip()
        title = title.replace("&#8211;", "–").replace("&#8217;", "'").replace("&amp;", "&")

        if not title or len(title) < 5:
            continue

        # Extract ref
        ref_match = _RFP_REF.search(title) or _NUM_REF.search(title)
        if ref_match:
            ref = ref_match.group(0).strip()[:80]
        else:
            slug = item.get("slug", "")[:40]
            ref = f"{source_id}/{slug}"

        # Date
        closing_str = item.get("date", "")

        combined = f"{ref} {title}"
        cidb_hit = re_search_cidb(combined)
        location = province_from_text(combined) or default_location

        tenders.append(
            TenderOpportunity(
                tender_id=ref[:100],
                title=title[:500],
                issuing_entity=issuing_entity,
                closing_date=parse_closing_date(closing_str),
                estimated_value=None,
                required_cidb_class=cidb_hit[1] if cidb_hit else None,
                required_cidb_level=int(cidb_hit[0]) if cidb_hit else None,
                mandatory_csd=True,
                tax_compliance_required=True,
                location_target=location,
                raw_document_url=None,
            )
        )
        if limit is not None and len(tenders) >= limit:
            break
    return tenders
