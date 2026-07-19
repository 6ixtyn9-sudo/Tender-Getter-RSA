"""Single source of truth for turning a WhatsApp profile into matchable data."""
from __future__ import annotations
from typing import Iterable

from ..schemas import CIDBGrading, CompanyProfile, Location, MatchResult, TenderOpportunity
from ..matcher import match
from .models import WhatsAppUser


def company_from_user(user: WhatsAppUser) -> CompanyProfile | None:
    """Build a conservative profile: unverified items never become true claims."""
    if not user.registration_number:
        return None
    data = user.onboarding_data or {}
    gradings = []
    for value in data.get("cidb_gradings", []):
        try:
            gradings.append(CIDBGrading(class_code=str(value["class_code"]).upper(), level=int(value["level"])))
        except (KeyError, TypeError, ValueError):
            continue
    return CompanyProfile(
        registration_number=user.registration_number,
        company_name=data.get("company_name") or "Tender Getter customer",
        csd_number=data.get("csd_number") if str(user.csd_status) == "verified" else None,
        bbbee_level=int(data.get("bbbee_level", 9) or 9) if str(user.bbbee_status) == "verified" else 9,
        cidb_gradings=gradings,
        location=Location(province=user.province or "National", city=data.get("city") or "Unknown"),
        sectors=user.sectors,
        has_tax_pin=str(user.tax_status) == "verified",
        has_coida=bool(data.get("has_coida", False)),
    )


def match_user_tenders(user: WhatsAppUser, tenders: Iterable[TenderOpportunity]) -> list[tuple[TenderOpportunity, MatchResult]]:
    company = company_from_user(user)
    if company is None:
        return []
    outcomes = [(tender, match(company, tender)) for tender in tenders]
    return sorted(outcomes, key=lambda pair: (not pair[1].is_eligible, -pair[1].match_score))
