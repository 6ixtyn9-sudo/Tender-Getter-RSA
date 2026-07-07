"""
test_reporter.py - Unit tests for the Tender Getter RSA report generator.

Tests cover:
  - Report file is created and named correctly
  - Eligible report contains correct score, B-BBEE points, and status banner
  - Disqualified report contains the disqualification reason
  - SBD checklist items appear in the report
  - Score bar is rendered
"""

import pytest
from pathlib import Path
from datetime import datetime, timezone

from src.tender_getter.schemas import CIDBGrading, Location, CompanyProfile, TenderOpportunity
from src.tender_getter.reporter import generate_report, _safe_filename, _score_bar


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def eligible_company():
    return CompanyProfile(
        registration_number="2019/112233/07",
        company_name="Sipho Electrical and Civils (Pty) Ltd",
        csd_number="MAAA0554433",
        bbbee_level=1,
        black_ownership_pct=75.0,
        women_ownership_pct=25.0,
        youth_ownership_pct=30.0,
        cidb_gradings=[
            CIDBGrading(class_code="EE", level=3),
            CIDBGrading(class_code="CE", level=2),
        ],
        location=Location(province="Gauteng", city="Johannesburg"),
        sectors=["Electrical Engineering"],
        has_tax_pin=True,
        has_coida=True,
    )


@pytest.fixture
def eligible_tender():
    return TenderOpportunity(
        tender_id="COJ/EE/2026/012",
        title="Soweto Substation Transformer Maintenance",
        issuing_entity="City of Johannesburg",
        closing_date=datetime(2026, 8, 15, tzinfo=timezone.utc),
        estimated_value=1_500_000,
        required_cidb_class="EE",
        required_cidb_level=3,
        mandatory_csd=True,
        tax_compliance_required=True,
        location_target="Gauteng",
    )


@pytest.fixture
def western_cape_tender(eligible_tender):
    eligible_tender.location_target = "Western Cape"
    eligible_tender.tender_id = "CPT/EE/2026/089"
    eligible_tender.title = "Cape Town Harbour Electrical Reticulation"
    return eligible_tender


@pytest.fixture
def tmp_report_dir(tmp_path):
    return tmp_path


# ---------------------------------------------------------------------------
# Filename helper
# ---------------------------------------------------------------------------

def test_safe_filename():
    name = _safe_filename("Sipho Electrical (Pty) Ltd", "COJ/EE/2026/012")
    assert name.startswith("TG_REPORT_")
    assert name.endswith(".md")
    assert "/" not in name
    assert " " not in name


# ---------------------------------------------------------------------------
# Score bar helper
# ---------------------------------------------------------------------------

def test_score_bar_full():
    bar = _score_bar(100.0)
    assert "100.0%" in bar
    assert "█" in bar


def test_score_bar_zero():
    bar = _score_bar(0.0)
    assert "0.0%" in bar
    assert "░" in bar


# ---------------------------------------------------------------------------
# Eligible report
# ---------------------------------------------------------------------------

def test_eligible_report_created(eligible_company, eligible_tender, tmp_report_dir):
    path = generate_report(eligible_company, eligible_tender, output_dir=tmp_report_dir)
    assert path.exists()
    assert path.suffix == ".md"


def test_eligible_report_contains_eligible_banner(eligible_company, eligible_tender, tmp_report_dir):
    path = generate_report(eligible_company, eligible_tender, output_dir=tmp_report_dir)
    content = path.read_text()
    assert "✅ ELIGIBLE" in content


def test_eligible_report_score(eligible_company, eligible_tender, tmp_report_dir):
    path = generate_report(eligible_company, eligible_tender, output_dir=tmp_report_dir)
    content = path.read_text()
    assert "100.0%" in content


def test_eligible_report_bbbee_points(eligible_company, eligible_tender, tmp_report_dir):
    path = generate_report(eligible_company, eligible_tender, output_dir=tmp_report_dir)
    content = path.read_text()
    # Level 1, 80/20: 20/20 pts
    assert "20 / 20 pts" in content


def test_eligible_report_sbd_checklist(eligible_company, eligible_tender, tmp_report_dir):
    path = generate_report(eligible_company, eligible_tender, output_dir=tmp_report_dir)
    content = path.read_text()
    assert "SBD 1" in content
    assert "SBD 6.1" in content
    assert "B-BBEE Certificate" in content


def test_eligible_report_cidb_table(eligible_company, eligible_tender, tmp_report_dir):
    path = generate_report(eligible_company, eligible_tender, output_dir=tmp_report_dir)
    content = path.read_text()
    assert "EE" in content
    assert "Grade 3" in content


# ---------------------------------------------------------------------------
# Disqualified report
# ---------------------------------------------------------------------------

def test_disqualified_report_wrong_province(eligible_company, western_cape_tender, tmp_report_dir):
    path = generate_report(eligible_company, western_cape_tender, output_dir=tmp_report_dir)
    content = path.read_text()
    assert "❌ DISQUALIFIED" in content
    assert "Western Cape" in content


def test_disqualified_report_score_zero(eligible_company, western_cape_tender, tmp_report_dir):
    path = generate_report(eligible_company, western_cape_tender, output_dir=tmp_report_dir)
    content = path.read_text()
    assert "0.0%" in content
