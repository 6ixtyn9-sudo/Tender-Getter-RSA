"""TenderBulletins.co.za aggregator – scrapes the consolidated SA tender database.

URL pattern: https://tenderbulletins.co.za/department-company/{slug}/
Pagination:  .../page/{n}/
Table format: Tender Title | Tender Number | Briefing Date | Closing Date

This is a high-reliability fallback for sources whose own websites are:
  - 403/404/DNS_FAIL (Tshwane, DWS, DPWI, many municipalities)
  - JS-rendered with no static data
  - Temporarily down

Rate-limited to ~1 req/s to be respectful of the free service.
"""
from __future__ import annotations

import logging
import re
import ssl
import time
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
from urllib.parse import urljoin
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from ...schemas import TenderOpportunity
from ..common import re_search_cidb, province_from_text, parse_closing_date

logger = logging.getLogger(__name__)

_BASE = "https://tenderbulletins.co.za"
_DEPT_PATH = "/department-company/{slug}/"
_PAGE_PATH = "/department-company/{slug}/page/{n}/"

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
_FETCH_TIMEOUT = int(os.environ.get("TENDER_FETCH_TIMEOUT", "15"))
_MAX_PAGES = int(os.environ.get("TB_MAX_PAGES", "5"))  # pages per department
_MIN_DELAY = 0.6  # seconds between requests (rate limit)

# ── Source ID → TenderBulletins slug mapping ──────────────────────────
# Covers all priority-1/2 stubborn sources plus common departments.
# Key = source_id from sources.yaml, Value = TenderBulletins URL slug.

SLUG_MAP: Dict[str, str] = {
    # ── Metros ──
    "tshwane": "city-of-tshwane",
    "johannesburg": "city-council-of-johannesburg",
    "capetown": "city-of-cape-town",
    "ekurhuleni": "city-of-ekurhuleni",
    "ethekwini": "ethekwini-metropolitan-municipality",
    "buffalo_city": "buffalo-city-metropolitan-municipality",
    "mangaung": "mangaung-metropolitan-municipality",
    "nelson_mandela_bay": "nelson-mandela-bay-municipality",

    # ── National departments ──
    "dws": "water-and-sanitation",
    "dpwi": "public-works",
    "dbsa": "development-bank-of-southern-africa",
    "dbe": "basic-education",
    "dhet": "higher-education-training",
    "dcs": "correctional-services",
    "dod": "defence",
    "doh": "health",
    "dsd": "social-development",
    "dha": "home-affairs",
    "dpe": "public-enterprises",
    "dtic": "trade-industry",
    "dffe": "environmental-affairs",
    "dsbd": "small-business-development",
    "dtps": "transport",
    "dmgd": "mineral-resources",
    "nt": "national-treasury",
    "sars": "south-african-revenue-service",
    "saps": "south-african-police-service",

    # ── SOEs ──
    "eskom": "eskom",
    "transnet": "transnet-soc-ltd",
    "armscor": "armscor",
    "sanral": "south-african-national-roads-agency-soc-limited-sanral",
    "prasa": "passenger-rail-agency-of-south-africa",

    # ── District municipalities ──
    "capricorn_dm": "capricorn-district-municipality",
    "ehlanzeni_dm": "ehlanzeni-district-municipality",
    "bojanala_dm": "bojanala-district-municipality",
    "fezile_dabi_dm": "fezile-dabi-district-municipality",
    "sedibeng_dm": "sedibeng-district-municipality",
    "west_rand_dm": "west-rand-district-municipality",
    "gert_sibande_dm": "gert-sibande-district-municipality",
    "nkangala_dm": "nkangala-district-municipality",
    "waterberg_dm": "waterberg-district-municipality",
    "sekhukhune_dm": "sekhukhune-district-municipality",
    "cape_winelands_dm": "cape-winelands-district-municipality",
    "garden_route_dm": "garden-route-district-municipality",
    "central_karoo_dm": "central-karoo-district-municipality",
    "overberg_dm": "overberg-district-municipality",
    "west_coast_dm": "west-coast-district-municipality",
    "alfred_nzo_dm": "alfred-nzo-district-municipality",
    "amajuba_dm": "amajuba-district-municipality",
    "amathole_dm": "amathole-district-municipality",
    "buffalo_city_dm": "buffalo-city-metropolitan-municipality",
    "chris_hani_dm": "chris-hani-district-municipality",
    "joe_gqabi_dm": "joe-gqabi-district-municipality",
    "sarah_baartman_dm": "sarah-baartman-district-municipality",
    "harry_gwala_dm": "harry-gwala-district-municipality",
    "umgungundlovu_dm": "umgungundlovu-district-municipality",
    "umkhanyakude_dm": "umkhanyakude-district-municipality",
    "umzinyathi_dm": "umzinyathi-district-municipality",
    "uthukela_dm": "uthukela-district-municipality",
    "zululand_dm": "zululand-district-municipality",
    "mopani_dm": "mopani-district-municipality",
    "vhembe_dm": "vhembe-district-municipality",
    "thabo_mofutsanyana_dm": "thabo-mofutsanyana-district-municipality",
    "lejweleputswa_dm": "lejweleputswa-district-municipality",
    "xhariep_dm": "xhariep-district-municipality",
    "francis_baard_dm": "francis-baard-district-municipality",
    "john_taolo_gaetsewe_dm": "john-taolo-gaetsewe-district-municipality",
    "namakwa_dm": "namakwa-district-municipality",
    "pixley_ka_seme_dm": "pixley-ka-seme-district-municipality",
    "ngaka_modiri_molema_dm": "ngaka-modiri-molema-district-municipality",
    "dr_kaunda_dm": "dr-kenneth-kaunda-district-municipality",

    # ── Local municipalities (sample – high priority ones) ──
    "ba_phalaborwa_lm": "ba-phalaborwa-local-municipality",
    "emalahleni_lm": "emalahleni-local-municipality",
    "govan_mbeki_lm": "govan-mbeki-local-municipality",
    "stellenbosch_lm": "stellenbosch-municipality",
    "drakenstein_lm": "drakenstein-municipality",
    "george_lm": "george-municipality",
    "bitou_lm": "bitou-municipality",
    "breede_valley_lm": "breede-valley-municipality",
    "beaufort_west_lm": "beaufort-west-municipality",
    "bela_bela_lm": "bela-bela-local-municipality",
    "blouberg_lm": "blouberg-municipality",

    # ── DFI / Chapter 9 / Water ──
    "dbsa": "development-bank-of-southern-africa",
    "raf": "road-accident-fund",
    "sars": "south-african-revenue-service",
    "seda": "small-enterprise-development-agency",
    "sefa": "small-enterprise-finance-agency",
    "sanparks": "south-african-national-parks",
    "sahrc": "south-african-human-rights-commission",
    "agsa": "auditor-general-of-south-africa",
    "public_protector": "public-protector-south-africa",
    "ffc": "financial-and-fiscal-commission",
    "psc": "public-service-commission",
    "uif": "unemployment-insurance-fund",
    "rand_water": "rand-water",
    "umgeni_water": "umgeni-water",
    "amatola_water": "amatola-water-board",
    "bloem_water": "bloem-water",
    "magalies_water": "magalies-water",
    "overberg_water": "overberg-water",
    "lepelle_water": "lepelle-northern-water",

    # ── Universities ──
    "up": "university-of-pretoria",
    "uj": "university-of-johannesburg",
    "uct": "university-of-cape-town",
    "ukzn": "university-of-kwazulu-natal",
    "stellenbosch": "stellenbosch-university",
    "ufs": "university-of-the-free-state",
    "nmu": "nelson-mandela-university",
    "nwu": "north-west-university",
    "unisa": "university-of-south-africa",
    "cput": "cape-peninsula-university-of-technology",
    "dut": "durban-university-of-technology",
    "tut": "tshwane-university-of-technology",
    "cut": "central-university-of-technology-free-state",

    # ── TVET Colleges ──
    "boland_tvet": "boland-tvet-college",
    "capricorn_tvet": "capricorn-tvet-college",
    "central_johannesburg_tvet": "central-johannesburg-tvet-college",
    "ekurhuleni_east_tvet": "ekurhuleni-east-tvet-college",
    "ekurhuleni_west_tvet": "ekurhuleni-west-tvet-college",
    "south_west_gauteng_tvet": "south-west-gauteng-tvet-college",
}

# ── Entity name → slug lookup (for sources without a SLUG_MAP entry) ──
_NAME_KEYWORDS_TO_SLUG: Dict[str, str] = {
    "tshwane": "city-of-tshwane",
    "johannesburg": "city-council-of-johannesburg",
    "cape town": "city-of-cape-town",
    "ekurhuleni": "city-of-ekurhuleni",
    "ethekwini": "ethekwini-metropolitan-municipality",
    "buffalo city": "buffalo-city-metropolitan-municipality",
    "mangaung": "mangaung-metropolitan-municipality",
    "nelson mandela bay": "nelson-mandela-bay-metropolitan-municipality",
    "water and sanitation": "water-and-sanitation",
    "public works": "public-works",
    "eskom": "eskom",
    "transnet": "transnet-soc-ltd",
    "sanral": "south-african-national-roads-agency-soc-limited-sanral",
    "prasa": "passenger-rail-agency-of-south-africa",
}


def resolve_slug(source_id: str, entity_name: str = "") -> Optional[str]:
    """Resolve a source_id or entity name to a TenderBulletins URL slug.

    Tries:
      1. Direct lookup in SLUG_MAP by source_id
      2. Fuzzy keyword match on entity_name
    """
    if source_id in SLUG_MAP:
        return SLUG_MAP[source_id]
    # Try entity name keywords
    name_lower = (entity_name or "").lower()
    for keyword, slug in _NAME_KEYWORDS_TO_SLUG.items():
        if keyword in name_lower:
            return slug
    return None


# ── HTML fetching ─────────────────────────────────────────────────────

def _get_ssl_ctx() -> Optional[ssl.SSLContext]:
    try:
        ctx = ssl._create_unverified_context()
        return ctx
    except Exception:
        return None


def _fetch_page(url: str) -> Optional[str]:
    """Fetch a single page from TenderBulletins. Returns HTML or None."""
    try:
        req = Request(url, headers={
            "User-Agent": _USER_AGENT,
                    "Accept-Language": "en-ZA,en;q=0.9",
        })
        kwargs: dict = {"timeout": _FETCH_TIMEOUT}
        ssl_ctx = _get_ssl_ctx()
        if ssl_ctx:
            kwargs["context"] = ssl_ctx
        with urlopen(req, **kwargs) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as exc:
        logger.warning("TenderBulletins fetch failed for %s: %s", url, exc)
        return None


# ── Parsing ───────────────────────────────────────────────────────────

_TR_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
_TD_RE = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)
_TAG_RE = re.compile(r"<[^>]+>")
_HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
_TOTAL_RE = re.compile(r"Total\s+Posts:\s*(\d+)", re.IGNORECASE)


def _parse_tenderbulletins_page(
    html: str,
    issuing_entity: str = "",
    base_url: str = "",
    limit: Optional[int] = None,
) -> List[TenderOpportunity]:
    """Parse a single TenderBulletins department page.

    Expected table columns: Tender Title | Tender Number | Briefing Date | Closing Date
    The title column contains a link to the detail page.
    """
    tenders: List[TenderOpportunity] = []
    rows = _TR_RE.findall(html or "")

    for row_html in rows:
        tds = [_TAG_RE.sub("", td).strip() for td in _TD_RE.findall(row_html)]
        if len(tds) < 3:
            continue

        # Typical column order: Title | Tender Number | Briefing Date | Closing Date
        # Sometimes: Title | Tender Number | Closing Date (3 cols)
        title_text = tds[0]
        tender_number = tds[1] if len(tds) > 1 else ""

        # Find closing date — scan from the end backwards
        closing_str = ""
        for td_val in reversed(tds[2:]):
            if any(ch.isdigit() for ch in td_val) and len(td_val) > 6:
                closing_str = td_val
                break
        # Also check tds[2] if not found in reversed scan
        if not closing_str and len(tds) > 2:
            if any(ch.isdigit() for ch in tds[2]) and len(tds[2]) > 6:
                closing_str = tds[2]

        # Extract doc URL from the title column's link
        href_match = _HREF_RE.search(row_html)
        doc_url = None
        if href_match:
            raw_href = href_match.group(1)
            # Only take links to tender detail pages
            if "/tender-bulletin/" in raw_href or "/custom-tender/" in raw_href:
                doc_url = urljoin(base_url, raw_href) if base_url else raw_href

        # Skip header/noise rows
        if not title_text or not tender_number:
            continue
        if len(title_text) < 10:
            continue
        # Header rows: "Tender Title", "Tender Number", etc.
        if title_text.lower() in ("tender title", "tender number"):
            continue

        # Use tender_number as the primary reference
        ref = tender_number.strip()
        if not ref:
            # Fallback: extract from title
            ref = f"TB-{abs(hash(title_text[:60])) % 100000:05d}"

        combined = f"{ref} {title_text}"
        cidb_hit = re_search_cidb(combined)
        cidb_level = int(cidb_hit[0]) if cidb_hit else None
        cidb_class = cidb_hit[1] if cidb_hit else None
        location = province_from_text(combined)

        try:
            tender = TenderOpportunity(
                tender_id=ref[:100],
                title=title_text[:500],
                issuing_entity=issuing_entity or "TenderBulletins.co.za",
                closing_date=parse_closing_date(closing_str),
                estimated_value=None,
                required_cidb_class=cidb_class,
                required_cidb_level=cidb_level,
                mandatory_csd=True,
                tax_compliance_required=True,
                location_target=location,
                raw_document_url=doc_url,
            )
            tenders.append(tender)
        except Exception as exc:
            logger.debug("Failed to create TenderOpportunity from row: %s", exc)

        if limit is not None and len(tenders) >= limit:
            break

    return tenders


def _get_total_posts(html: str) -> int:
    """Extract 'Total Posts: NNN' from page HTML."""
    m = _TOTAL_RE.search(html)
    return int(m.group(1)) if m else 0


# ── Public API ────────────────────────────────────────────────────────

def fetch_tenderbulletins(
    slug: str,
    issuing_entity: str = "",
    limit: Optional[int] = None,
    max_pages: int = 0,
    recent_only: bool = True,
) -> List[TenderOpportunity]:
    """Fetch tenders from TenderBulletins.co.za for a specific department.

    Args:
        slug: TenderBulletins URL slug, e.g. 'city-of-tshwane'
        issuing_entity: Override issuing_entity name on returned tenders
        limit: Max tenders to return (None = no limit)
        max_pages: Max pages to scrape (0 = auto from first page total)
        recent_only: If True, stop after finding a page with no future closing dates
    """
    all_tenders: List[TenderOpportunity] = []
    first_url = _BASE + _DEPT_PATH.format(slug=slug)
    last_request_time = 0.0

    # Fetch first page to determine total posts / pages
    html = _fetch_page(first_url)
    if not html:
        logger.warning("TenderBulletins: no data for slug '%s'", slug)
        return []

    total_posts = _get_total_posts(html)
    logger.info("TenderBulletins: slug='%s' total_posts=%d", slug, total_posts)

    tenders = _parse_tenderbulletins_page(html, issuing_entity, _BASE, limit)
    all_tenders.extend(tenders)

    # Determine page count (posts per page ≈ 15)
    if max_pages == 0:
        posts_per_page = max(len(tenders), 15)
        max_pages = min((total_posts + posts_per_page - 1) // posts_per_page, _MAX_PAGES)

    # Paginate
    for page_num in range(2, max_pages + 1):
        if limit is not None and len(all_tenders) >= limit:
            break

        # Rate limiting
        elapsed = time.time() - last_request_time
        if elapsed < _MIN_DELAY:
            time.sleep(_MIN_DELAY - elapsed)

        page_url = _BASE + _PAGE_PATH.format(slug=slug, n=page_num)
        last_request_time = time.time()
        page_html = _fetch_page(page_url)
        if not page_html:
            break

        page_tenders = _parse_tenderbulletins_page(page_html, issuing_entity, _BASE, limit)
        if not page_tenders:
            break

        # If recent_only, check if all tenders on this page have already closed
        if recent_only and page_tenders:
            now = datetime.now(timezone.utc)
            all_closed = all(
                t.closing_date < now - timedelta(days=90) for t in page_tenders
            )
            if all_closed:
                # Still add them but stop paginating further
                all_tenders.extend(page_tenders)
                break

        all_tenders.extend(page_tenders)

    # Deduplicate by tender_id
    seen: Dict[str, TenderOpportunity] = {}
    for t in all_tenders:
        seen[t.tender_id] = t

    result = list(seen.values())
    if limit is not None:
        result = result[:limit]

    logger.info(
        "TenderBulletins: slug='%s' → %d tenders (%d pages)",
        slug, len(result), min(max_pages, _MAX_PAGES),
    )
    return result


class TenderBulletinsSource:
    """Generic TenderBulletins aggregator source.

    Usage as a TenderSource plug-in:
        # In a per-source file (e.g. tshwane.py):
        class TshwaneSource:
            def fetch(self, limit=None, **kw):
                from .aggregators import TenderBulletinsSource
                tb = TenderBulletinsSource("tshwane", "City of Tshwane Metropolitan Municipality")
                return tb.fetch(limit=limit)

    Usage as a standalone fallback:
        from .aggregators import fetch_tenderbulletins
        tenders = fetch_tenderbulletins("city-of-tshwane", "City of Tshwane", limit=50)
    """

    source_id: str = "tenderbulletins"
    live: bool = True

    def __init__(
        self,
        source_id: str = "",
        issuing_entity: str = "",
        slug: str = "",
    ):
        """Initialize with a source_id (looked up in SLUG_MAP) or explicit slug."""
        self.source_id = source_id or "tenderbulletins"
        self.issuing_entity = issuing_entity
        self.slug = slug or resolve_slug(source_id, issuing_entity) or ""
        if not self.slug:
            logger.warning(
                "TenderBulletinsSource: no slug for source_id='%s' entity='%s'",
                source_id, issuing_entity,
            )

    def fetch(self, limit: Optional[int] = None, **kw) -> List[TenderOpportunity]:
        """Fetch tenders from TenderBulletins for this source's slug."""
        if not self.slug:
            return []
        return fetch_tenderbulletins(
            self.slug,
            issuing_entity=self.issuing_entity,
            limit=limit,
        )
