"""
matcher.py - Mathematical matching & regulatory gating engine.

Implements the two-gate matching pipeline:
  Gate 1: Binary hard disqualification filters (CSD, Tax, CIDB, Geofencing)
  Gate 2: Preferential procurement scoring (B-BBEE / PPPFA 80/20 & 90/10)
"""

from typing import Optional
from .schemas import CompanyProfile, TenderOpportunity, MatchResult

# ---------------------------------------------------------------------------
# Statutory lookup tables (South African law / PPPFA regulations)
# ---------------------------------------------------------------------------

# CIDB financial upper limits per grade (ZAR). Grade 9 is unlimited.
CIDB_LIMITS: dict[int, float] = {
    1: 200_000,
    2: 1_000_000,
    3: 3_000_000,
    4: 6_000_000,
    5: 10_000_000,
    6: 20_000_000,
    7: 60_000_000,
    8: 200_000_000,
    9: float("inf"),
}

# B-BBEE preference points per system per level.
# Level 9 is used internally to represent Non-Compliant.
BBBEE_POINTS: dict[str, dict[int, float]] = {
    "80/20": {
        1: 20, 2: 18, 3: 14, 4: 12, 5: 8, 6: 6, 7: 4, 8: 2, 9: 0
    },
    "90/10": {
        1: 10, 2: 9, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1, 9: 0
    },
}

# Threshold that determines which preference point system applies.
BBBEE_THRESHOLD_ZAR = 50_000_000


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def get_bbbee_system(estimated_value: Optional[float]) -> str:
    """
    Returns the applicable preference point system ('80/20' or '90/10')
    based on the tender's estimated value.
    Falls back to '80/20' when the value is unknown.
    """
    if estimated_value is None or estimated_value < BBBEE_THRESHOLD_ZAR:
        return "80/20"
    return "90/10"


def get_bbbee_points(bbbee_level: int, system: str) -> float:
    """Returns preference points for a given B-BBEE level under the chosen system."""
    table = BBBEE_POINTS.get(system, BBBEE_POINTS["80/20"])
    # Level 9 represents Non-Compliant in our schema
    return table.get(bbbee_level, 0.0)


def match(company: CompanyProfile, tender: TenderOpportunity) -> MatchResult:
    """
    Evaluate whether a company qualifies for a tender and compute its
    preference score.

    Returns a MatchResult with full audit feedback.
    """
    audit_parts: list[str] = []

    # ------------------------------------------------------------------
    # GATE 1 — Binary hard disqualifications
    # ------------------------------------------------------------------

    # 1a. CSD (Central Supplier Database) check
    if tender.mandatory_csd and not company.csd_number:
        return _disqualify(
            company, tender,
            "Disqualified: Tender requires a valid CSD supplier number (MAAA...), "
            "but this company has no CSD registration on file."
        )
    if company.csd_number:
        audit_parts.append(f"CSD Verified ({company.csd_number})")

    # 1b. Tax compliance (SARS Tax PIN) check
    if tender.tax_compliance_required and not company.has_tax_pin:
        return _disqualify(
            company, tender,
            "Disqualified: Tender requires an active SARS tax compliance PIN, "
            "but this company does not have one on record."
        )
    if company.has_tax_pin:
        audit_parts.append("Tax Compliance PIN Active")

    # 1c. Geofencing — province-level locality check
    if (
        tender.location_target
        and tender.location_target.lower() != "national"
        and tender.location_target.lower() != company.location.province.lower()
    ):
        return _disqualify(
            company, tender,
            f"Disqualified: Tender is localized to '{tender.location_target}'. "
            f"Client is based in '{company.location.province}'."
        )
    audit_parts.append(f"Geographically Aligned ({company.location.province})")

    # 1d. CIDB grading check (class + financial capacity)
    if tender.required_cidb_class and tender.required_cidb_level:
        cidb_outcome = _check_cidb(company, tender)
        if cidb_outcome is not None:
            return _disqualify(company, tender, cidb_outcome)
        audit_parts.append(
            f"CIDB Gradings Aligned "
            f"({tender.required_cidb_class}{tender.required_cidb_level})"
        )
    elif tender.required_cidb_class and not tender.required_cidb_level:
        # Class required but no level specified — check class existence only
        has_class = any(
            g.class_code.upper() == tender.required_cidb_class.upper()
            for g in company.cidb_gradings
        )
        if not has_class:
            return _disqualify(
                company, tender,
                f"Disqualified: Tender requires CIDB class "
                f"'{tender.required_cidb_class}', which this company does not hold."
            )
        audit_parts.append(f"CIDB Class Aligned ({tender.required_cidb_class})")

    # ------------------------------------------------------------------
    # GATE 2 — B-BBEE preferential procurement scoring
    # ------------------------------------------------------------------
    system = get_bbbee_system(tender.estimated_value)
    max_pts = 20.0 if system == "80/20" else 10.0
    awarded_pts = get_bbbee_points(company.bbbee_level, system)

    bbbee_label = (
        "Non-Compliant" if company.bbbee_level == 9
        else f"B-BBEE Level {company.bbbee_level}"
    )
    audit_parts.append(
        f"Preference Score: {awarded_pts:.0f}/{max_pts:.0f} pts "
        f"({bbbee_label} under {system} system)"
    )

    # ------------------------------------------------------------------
    # Calculate overall match score
    # Base eligibility = 80 pts. B-BBEE preference = up to 20 pts.
    # Score is expressed as a percentage (0–100).
    # ------------------------------------------------------------------
    base = 80.0
    bbbee_contribution = (awarded_pts / max_pts) * 20.0 if max_pts > 0 else 0.0
    raw_score = base + bbbee_contribution  # max 100.0

    feedback = "Eligible match found! Detailed audit: " + " | ".join(audit_parts)

    return MatchResult(
        company_name=company.company_name,
        tender_id=tender.tender_id,
        tender_title=tender.title,
        is_eligible=True,
        match_score=round(raw_score, 1),
        bbbee_points=awarded_pts,
        bbbee_max_points=max_pts,
        bbbee_system=system,
        disqualification_reason=None,
        feedback=feedback,
    )


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _check_cidb(
    company: CompanyProfile, tender: TenderOpportunity
) -> Optional[str]:
    """
    Validates CIDB eligibility.
    Returns a disqualification string if the company fails, or None if it passes.

    Logic:
      1. The company must hold the required class code.
      2. If company level >= required level → automatic pass.
      3. If company level < required level → check financial capacity gate:
         the tender estimated_value must be <= CIDB_LIMITS[company_level].
    """
    required_class = tender.required_cidb_class.upper()  # type: ignore[union-attr]
    required_level = tender.required_cidb_level          # type: ignore[assignment]

    # Find the company's highest registered level for the required class
    matching_gradings = [
        g for g in company.cidb_gradings
        if g.class_code.upper() == required_class
    ]

    if not matching_gradings:
        return (
            f"Disqualified: Client has no CIDB '{required_class}' class registration. "
            f"Required: {required_class}{required_level}."
        )

    company_level = max(g.level for g in matching_gradings)
    company_cap = CIDB_LIMITS[company_level]

    if company_level >= required_level:
        return None  # Pass — grade level is sufficient

    # Under-graded: apply financial capacity fallback
    tender_value = tender.estimated_value
    if tender_value is None:
        # No value declared — block on principle (grade level shortfall)
        return (
            f"Disqualified: Client's CIDB Level {company_level} "
            f"is below the required Level {required_level} and no tender "
            f"value is available to apply the financial capacity gate."
        )

    if tender_value <= company_cap:
        return None  # Pass — tender value is within company's financial cap

    return (
        f"Disqualified: Client's CIDB Level {company_level} "
        f"(limit R{company_cap:,.2f}) is too low for the required "
        f"Level {required_level} (value R{tender_value:,.2f})."
    )


def _disqualify(
    company: CompanyProfile,
    tender: TenderOpportunity,
    reason: str,
) -> MatchResult:
    """Constructs a zero-score disqualification MatchResult."""
    system = get_bbbee_system(tender.estimated_value)
    max_pts = 20.0 if system == "80/20" else 10.0
    return MatchResult(
        company_name=company.company_name,
        tender_id=tender.tender_id,
        tender_title=tender.title,
        is_eligible=False,
        match_score=0.0,
        bbbee_points=0.0,
        bbbee_max_points=max_pts,
        bbbee_system=system,
        disqualification_reason=reason,
        feedback=reason,
    )
