"""
test_matcher.py - Unit tests for the Tender Getter RSA matching engine.

Tests cover:
  - B-BBEE point allocation (80/20 & 90/10 systems)
  - CIDB system selection thresholds
  - CSD hard disqualification
  - Tax PIN hard disqualification
  - Geofencing (province-level)
  - CIDB class mismatch
  - CIDB level shortfall with financial capacity fallback (PASS & FAIL)
  - Full eligible match with score calculation
"""

import pytest
from datetime import datetime, timezone

from tender_getter.schemas import CIDBGrading, Location, CompanyProfile, TenderOpportunity
from tender_getter.matcher import (
    match, get_bbbee_system, get_bbbee_points, BBBEE_THRESHOLD_ZAR
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def base_company():
    """A fully compliant Level 1 B-BBEE company in Gauteng with EE3 + CE3."""
    return CompanyProfile(
        registration_number="2019/000001/07",
        company_name="Test Co (Pty) Ltd",
        csd_number="MAAA1234567",
        bbbee_level=1,
        black_ownership_pct=75.0,
        cidb_gradings=[
            CIDBGrading(class_code="EE", level=3),
            CIDBGrading(class_code="CE", level=3),
        ],
        location=Location(province="Gauteng", city="Johannesburg"),
        sectors=["Electrical"],
        has_tax_pin=True,
        has_coida=True,
    )


@pytest.fixture
def base_tender():
    """A standard localized EE3 Gauteng tender valued at R1.5m (80/20 system)."""
    return TenderOpportunity(
        tender_id="TEST/001",
        title="Test Tender",
        issuing_entity="Test Municipality",
        closing_date=datetime(2026, 12, 31, tzinfo=timezone.utc),
        estimated_value=1_500_000,
        required_cidb_class="EE",
        required_cidb_level=3,
        mandatory_csd=True,
        tax_compliance_required=True,
        location_target="Gauteng",
    )


# ---------------------------------------------------------------------------
# B-BBEE system selection
# ---------------------------------------------------------------------------

def test_bbbee_system_below_threshold():
    assert get_bbbee_system(10_000_000) == "80/20"

def test_bbbee_system_at_threshold():
    assert get_bbbee_system(BBBEE_THRESHOLD_ZAR) == "80/20"

def test_bbbee_system_above_threshold():
    assert get_bbbee_system(100_000_000) == "90/10"

def test_bbbee_system_no_value():
    assert get_bbbee_system(None) == "80/20"


# ---------------------------------------------------------------------------
# B-BBEE point allocation
# ---------------------------------------------------------------------------

def test_bbbee_points_level1_8020():
    assert get_bbbee_points(1, "80/20") == 20

def test_bbbee_points_level1_9010():
    assert get_bbbee_points(1, "90/10") == 10

def test_bbbee_points_level4_8020():
    assert get_bbbee_points(4, "80/20") == 12

def test_bbbee_points_noncompliant_8020():
    assert get_bbbee_points(9, "80/20") == 0

def test_bbbee_points_level8_9010():
    assert get_bbbee_points(8, "90/10") == 1


# ---------------------------------------------------------------------------
# Gate 1: CSD disqualification
# ---------------------------------------------------------------------------

def test_disqualify_missing_csd(base_company, base_tender):
    base_company.csd_number = None
    result = match(base_company, base_tender)
    assert not result.is_eligible
    assert result.match_score == 0.0
    assert "CSD" in result.feedback


# ---------------------------------------------------------------------------
# Gate 1: Tax PIN disqualification
# ---------------------------------------------------------------------------

def test_disqualify_missing_tax_pin(base_company, base_tender):
    base_company.has_tax_pin = False
    result = match(base_company, base_tender)
    assert not result.is_eligible
    assert "tax" in result.feedback.lower()


# ---------------------------------------------------------------------------
# Gate 1: Geofencing
# ---------------------------------------------------------------------------

def test_disqualify_wrong_province(base_company, base_tender):
    base_tender.location_target = "Western Cape"
    result = match(base_company, base_tender)
    assert not result.is_eligible
    assert "Western Cape" in result.feedback


def test_national_tender_passes_geofence(base_company, base_tender):
    base_tender.location_target = "National"
    result = match(base_company, base_tender)
    assert result.is_eligible


# ---------------------------------------------------------------------------
# Gate 1: CIDB class mismatch
# ---------------------------------------------------------------------------

def test_disqualify_wrong_cidb_class(base_company, base_tender):
    base_tender.required_cidb_class = "GB"
    base_tender.required_cidb_level = 3
    result = match(base_company, base_tender)
    assert not result.is_eligible
    assert "GB" in result.feedback


# ---------------------------------------------------------------------------
# Gate 1: CIDB level & financial capacity
# ---------------------------------------------------------------------------

def test_disqualify_cidb_level_shortfall_exceeds_cap(base_company, base_tender):
    """Company is CE2 (cap R1m), tender requires CE3, value R2.5m -> FAIL."""
    base_company.cidb_gradings = [CIDBGrading(class_code="CE", level=2)]
    base_tender.required_cidb_class = "CE"
    base_tender.required_cidb_level = 3
    base_tender.estimated_value = 2_500_000
    result = match(base_company, base_tender)
    assert not result.is_eligible
    assert "1,000,000.00" in result.feedback


def test_cidb_level_shortfall_within_cap_passes(base_company, base_tender):
    """Company is CE2 (cap R1m), tender requires CE3, value R700k -> PASS."""
    base_company.cidb_gradings = [CIDBGrading(class_code="CE", level=2)]
    base_tender.required_cidb_class = "CE"
    base_tender.required_cidb_level = 3
    base_tender.estimated_value = 700_000
    result = match(base_company, base_tender)
    assert result.is_eligible


# ---------------------------------------------------------------------------
# Full eligible match & score calculation
# ---------------------------------------------------------------------------

def test_full_eligible_match_score(base_company, base_tender):
    """Level 1 company, 80/20 system: base 80 + (20/20)*20 = 100.0%"""
    result = match(base_company, base_tender)
    assert result.is_eligible
    assert result.match_score == 100.0
    assert result.bbbee_points == 20.0
    assert result.bbbee_system == "80/20"


def test_level4_match_score(base_company, base_tender):
    """Level 4 company, 80/20 system: base 80 + (12/20)*20 = 92.0%"""
    base_company.bbbee_level = 4
    result = match(base_company, base_tender)
    assert result.is_eligible
    assert result.match_score == 92.0
    assert result.bbbee_points == 12.0


def test_noncompliant_match_score(base_company, base_tender):
    """Non-compliant company (level 9), 80/20: base 80 + 0 = 80.0%"""
    base_company.bbbee_level = 9
    result = match(base_company, base_tender)
    assert result.is_eligible
    assert result.match_score == 80.0
    assert result.bbbee_points == 0.0
