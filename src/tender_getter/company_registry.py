"""company_registry.py — public-registry root-of-truth guard.

Before any uploaded document can flip a verification status, the guard asks the
question document parsing can never answer: *does this company exist and is it
active in a public South African register?* This protects onboarding time,
AI-extraction spend, and downstream matching from phantom companies.

Check states
------------
ACTIVE     – found in a public register with an active status → allow
INACTIVE   – found, but deregistered/in liquidation/inactive   → block
NOT_FOUND  – definitive search returned nothing                → block
UNKNOWN    – every reachable source was inconclusive/down      → hold (never bless,
             never brand as fraud; verification stays PENDING for review)

Policy mapping: ACTIVE → allow · UNKNOWN → hold · INACTIVE/NOT_FOUND → block.

Provider chain (first definitive answer wins)
---------------------------------------------
1. CSD   — National Treasury Central Supplier Database (all gov suppliers).
2. CIDB  — Construction Register of Contractors (name corroboration; the
           endpoint pattern is already proven in tender_getter.cidb_directory).
3. CIPC  — empty by default. CIPC moved public search behind login in 2024
           (POPI); wire an approved endpoint/account via TG_CIPC_SEARCH_URL.

All I/O is isolated behind `_fetch_json` so tests never touch the network, and
every provider fails soft to UNKNOWN — this module NEVER raises to its caller.
Endpoints are public but unofficial and may change; they are env-overridable.
"""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Protocol
from urllib.parse import quote

logger = logging.getLogger(__name__)

# CIPC company registration numbers look like 2019/123456/07.
_CIPC_FORMAT = None  # compiled lazily to keep import light


def _cipc_pattern():
    import re

    global _CIPC_FORMAT
    if _CIPC_FORMAT is None:
        _CIPC_FORMAT = re.compile(r"^\d{4}/\d{4,7}/\d{2}$")
    return _CIPC_FORMAT


def is_cipc_registration(value: str | None) -> bool:
    """True only for real CIPC numbers (never WA-… placeholders or MAAA… numbers)."""
    return bool(value) and bool(_cipc_pattern().match(value.strip()))


class RegistryStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    NOT_FOUND = "not_found"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class RegistryCheck:
    status: RegistryStatus
    source: str
    detail: str = ""


def registry_decision(check: RegistryCheck) -> str:
    """Map a check to enforcement: 'allow', 'hold' or 'block'."""
    if check.status == RegistryStatus.ACTIVE:
        return "allow"
    if check.status == RegistryStatus.UNKNOWN:
        return "hold"
    return "block"


# ---------------------------------------------------------------------------
# Transport (sync httpx wrapped for async use — mirrors media.py dependency)
# ---------------------------------------------------------------------------


async def _fetch_json(url: str, timeout: float = 8.0) -> Any:
    """GET a URL and parse JSON. Raises on any failure (callers fail soft)."""
    import asyncio

    import certifi
    import httpx

    def _get() -> Any:
        with httpx.Client(timeout=timeout, verify=certifi.where(), follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()

    return await asyncio.to_thread(_get)


def _norm_digits(text: str) -> str:
    """Digits-only comparison key so 2019/123456/07 matches '201912345607'."""
    return "".join(ch for ch in text if ch.isdigit())


# ---------------------------------------------------------------------------
# Providers
# ---------------------------------------------------------------------------


class RegistryProvider(Protocol):
    source: str

    async def check(self, registration_number: str, company_name: Optional[str]) -> Optional[RegistryCheck]:
        """Return a definitive check, None when this provider cannot answer."""
        ...


class CSDSupplierProvider:
    """National Treasury CSD: the widest public register of SA gov suppliers."""

    source = "csd.gov.za"

    def _url(self) -> Optional[str]:
        # Public supplier search; override if Treasury documents a newer route
        # or issues an access key (TG_CSD_API_KEY is passed as query param).
        return os.getenv(
            "TG_CSD_SEARCH_URL",
            "https://www.csd.gov.za/api/suppliers/search",
        )

    async def check(self, registration_number: str, company_name: Optional[str]) -> Optional[RegistryCheck]:
        base = self._url()
        if not base:
            return None
        try:
            api_key = os.getenv("TG_CSD_API_KEY", "")
            query = f"?registrationNumber={quote(registration_number)}"
            if api_key:
                query += f"&apiKey={quote(api_key)}"
            payload = await _fetch_json(base + query)
        except Exception as exc:
            logger.info("CSD registry check failed for %s: %s", registration_number, exc)
            return RegistryCheck(RegistryStatus.UNKNOWN, self.source, str(exc))

        text = json.dumps(payload, default=str)
        if _norm_digits(registration_number) not in _norm_digits(text):
            return RegistryCheck(RegistryStatus.NOT_FOUND, self.source, "registration not present in CSD results")

        low = text.lower()
        inactive_hit = any(k in low for k in ("inactive", "de-registered", "deregistered", "suspended", "liquidation"))
        active_hit = "active" in low and not inactive_hit
        if inactive_hit:
            return RegistryCheck(RegistryStatus.INACTIVE, self.source, "supplier flagged inactive in CSD")
        if active_hit or "true" in low:  # e.g. IsActive: true
            return RegistryCheck(RegistryStatus.ACTIVE, self.source, "supplier active in CSD")
        return RegistryCheck(RegistryStatus.UNKNOWN, self.source, "CSD status could not be determined")


class CIDBRegisterProvider:
    """CIDB Register of Contractors — name corroboration for construction firms.

    A MISSING row is NOT a NOT_FOUND verdict (only construction companies are
    registered), so this provider declines instead of condemning.
    """

    source = "registers.cidb.org.za"
    SEARCH_URL = "https://registers.cidb.org.za/PublicContractors/ContractorSearch"

    async def check(self, registration_number: str, company_name: Optional[str]) -> Optional[RegistryCheck]:
        if not company_name or len(company_name.strip()) < 3:
            return None
        try:
            url = f"{self.SEARCH_URL}?PageSize=10&PageNo=1&CName={quote(company_name.strip())}"
            payload = await _fetch_json(url)
        except Exception as exc:
            logger.info("CIDB registry check failed for %r: %s", company_name, exc)
            return RegistryCheck(RegistryStatus.UNKNOWN, self.source, str(exc))

        rows = payload.get("table", []) if isinstance(payload, dict) else []
        if not rows:
            return None  # not a construction company verdict — decline
        needle = company_name.strip().lower()
        matched = [
            row for row in rows
            if isinstance(row, dict)
            and (needle in str(row.get("Contractor Name", "")).lower()
                 or str(row.get("Contractor Name", "")).lower() in needle)
        ]
        if not matched:
            return None
        if any(str(row.get("Status", "")).strip().lower() == "active" for row in matched):
            return RegistryCheck(RegistryStatus.ACTIVE, self.source, "active CIDB contractor record")
        return RegistryCheck(RegistryStatus.INACTIVE, self.source, "CIDB record exists but not active")


class CIPCEndpointProvider:
    """Opt-in CIPC lookup. Disabled until TG_CIPC_SEARCH_URL is configured with
    an approved endpoint containing the literal placeholder {registration}."""

    source = "cipc"

    def _url(self, registration_number: str) -> Optional[str]:
        template = os.getenv("TG_CIPC_SEARCH_URL", "")
        if "{registration}" not in template:
            return None
        return template.replace("{registration}", quote(registration_number))

    async def check(self, registration_number: str, company_name: Optional[str]) -> Optional[RegistryCheck]:
        url = self._url(registration_number)
        if not url:
            return None
        try:
            payload = await _fetch_json(url)
        except Exception as exc:
            logger.info("CIPC registry check failed for %s: %s", registration_number, exc)
            return RegistryCheck(RegistryStatus.UNKNOWN, self.source, str(exc))

        if _norm_digits(registration_number) not in _norm_digits(json.dumps(payload, default=str)):
            return RegistryCheck(RegistryStatus.NOT_FOUND, self.source, "registration not found by CIPC endpoint")
        low = json.dumps(payload, default=str).lower()
        if "in business" in low or '"active"' in low:
            return RegistryCheck(RegistryStatus.ACTIVE, self.source, "CIPC status 'In Business'")
        if any(k in low for k in ("deregistration", "liquidation", "business rescue", "inactive")):
            return RegistryCheck(RegistryStatus.INACTIVE, self.source, "CIPC status not active")
        return RegistryCheck(RegistryStatus.UNKNOWN, self.source, "CIPC status could not be determined")


# ---------------------------------------------------------------------------
# Chain + TTL cache
# ---------------------------------------------------------------------------

_DEFAULT_PROVIDERS: tuple = (CSDSupplierProvider(), CIDBRegisterProvider(), CIPCEndpointProvider())

_TTL_SECONDS = {
    RegistryStatus.ACTIVE: 24 * 3600,
    RegistryStatus.INACTIVE: 24 * 3600,
    RegistryStatus.NOT_FOUND: 6 * 3600,
    RegistryStatus.UNKNOWN: 15 * 60,  # retry outages quickly
}


@dataclass
class _Cache:
    entries: dict = field(default_factory=dict)  # reg -> (stored_at, check)


_CACHE = _Cache()


async def check_company_active(
    registration_number: str,
    company_name: Optional[str] = None,
    *,
    providers: Optional[tuple] = None,
) -> RegistryCheck:
    """
    Answer 'is this CIPC-registered company active in a public register?'

    Non-CIPC inputs (WA-… placeholders, MAAA… CSD numbers) short-circuit to
    UNKNOWN: callers must skip enforcement rather than block legitimate users.
    Never raises.
    """
    registration_number = (registration_number or "").strip()
    if not is_cipc_registration(registration_number):
        return RegistryCheck(RegistryStatus.UNKNOWN, "skip", "not a CIPC-format registration number")

    now = time.monotonic()
    cached_at, cached = _CACHE.entries.get(registration_number, (0.0, None))
    if cached and (now - cached_at) < _TTL_SECONDS[cached.status]:
        return cached

    chain = providers if providers is not None else _DEFAULT_PROVIDERS
    verdict = RegistryCheck(RegistryStatus.UNKNOWN, "chain", "no provider returned a definitive answer")
    for provider in chain:
        try:
            result = await provider.check(registration_number, company_name)
        except Exception as exc:  # providers fail soft already; belt-and-braces
            logger.warning("Registry provider %s crashed: %s", getattr(provider, "source", provider), exc)
            continue
        if result is None:
            continue
        if result.status != RegistryStatus.UNKNOWN:
            verdict = result
            break

    _CACHE.entries[registration_number] = (now, verdict)
    return verdict


def _reset_cache() -> None:
    """Test hook: clear the TTL cache."""
    _CACHE.entries.clear()
