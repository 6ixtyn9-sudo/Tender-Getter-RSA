"""
schemas.py - Core Pydantic data models for Tender Getter RSA.

Defines the canonical data structures for:
  - CompanyProfile (the client/bidder)
  - TenderOpportunity (the tender to be matched)
  - MatchResult (the output of the matching engine)
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CIDBGrading(BaseModel):
    """
    Represents a single CIDB grading registration for a company.
    A company can hold multiple gradings across different classes.
    """
    class_code: str = Field(
        ...,
        description=(
            "CIDB class code, e.g. 'CE' (Civil Engineering), "
            "'GB' (General Building), 'EE' (Electrical Engineering), "
            "'ME' (Mechanical Engineering), 'SB' (Specialist Building)."
        )
    )
    level: int = Field(
        ...,
        ge=1,
        le=9,
        description="CIDB grading level from 1 (smallest) to 9 (unlimited)."
    )


class Location(BaseModel):
    """Geographical location of the company or tender target."""
    province: str = Field(..., description="e.g. 'Gauteng', 'Western Cape'")
    city: str = Field(..., description="e.g. 'Johannesburg', 'Cape Town'")
    municipality: Optional[str] = Field(
        None, description="e.g. 'City of Tshwane Metropolitan Municipality'"
    )


class CompanyProfile(BaseModel):
    """
    Full regulatory and commercial profile of a client bidder.
    This is the central object used for all matching operations.
    """
    registration_number: str = Field(
        ..., description="CIPC company registration number, e.g. '2019/123456/07'"
    )
    company_name: str
    csd_number: Optional[str] = Field(
        None,
        description="CSD (Central Supplier Database) MAAA supplier number."
    )
    bbbee_level: int = Field(
        9,
        ge=1,
        le=9,
        description="B-BBEE Level 1–8. Use 9 to represent Non-Compliant."
    )
    black_ownership_pct: float = Field(0.0, ge=0.0, le=100.0)
    youth_ownership_pct: float = Field(0.0, ge=0.0, le=100.0)
    women_ownership_pct: float = Field(0.0, ge=0.0, le=100.0)
    cidb_gradings: List[CIDBGrading] = Field(
        default_factory=list,
        description="All active CIDB class/level registrations the company holds."
    )
    location: Location
    sectors: List[str] = Field(
        default_factory=list,
        description="Industry tags, e.g. ['Electrical', 'Civil', 'Security']"
    )
    has_tax_pin: bool = Field(
        False, description="True if SARS tax compliance PIN is valid and active."
    )
    has_coida: bool = Field(
        False, description="True if registered with Compensation Fund (COIDA)."
    )
    is_active: bool = True


class TenderOpportunity(BaseModel):
    """
    Represents a single tender opportunity scraped from a public platform.
    Used as the input target against which CompanyProfiles are matched.
    """
    tender_id: str = Field(..., description="Official bid number/reference, e.g. 'COJ/EE/2026/012'")
    title: str
    issuing_entity: str
    closing_date: datetime
    estimated_value: Optional[float] = Field(
        None, description="Estimated contract value in South African Rand (ZAR)."
    )
    required_cidb_class: Optional[str] = Field(
        None, description="Required CIDB class code, e.g. 'CE', 'GB', 'EE'."
    )
    required_cidb_level: Optional[int] = Field(
        None, ge=1, le=9, description="Minimum CIDB grade level required."
    )
    mandatory_csd: bool = Field(
        True, description="If True, bidder must have a valid CSD supplier number."
    )
    tax_compliance_required: bool = Field(
        True, description="If True, bidder must have an active SARS tax pin."
    )
    location_target: Optional[str] = Field(
        None,
        description=(
            "The geographic scope of the tender. "
            "Use province name for localized tenders (e.g. 'Gauteng'), "
            "or 'National' for open national bids."
        )
    )
    raw_document_url: Optional[str] = Field(
        None, description="URL to the original tender PDF on the issuing entity's portal."
    )


class MatchResult(BaseModel):
    """
    The structured output from the matching engine for a single
    (CompanyProfile, TenderOpportunity) pair.
    """
    company_name: str
    tender_id: str
    tender_title: str
    is_eligible: bool
    match_score: float = Field(..., ge=0.0, le=100.0, description="Match score as a percentage.")
    bbbee_points: float = Field(0.0, description="B-BBEE preference points awarded.")
    bbbee_max_points: float = Field(0.0, description="Maximum possible B-BBEE preference points for this tender.")
    bbbee_system: Optional[str] = Field(None, description="'80/20' or '90/10'")
    disqualification_reason: Optional[str] = None
    feedback: str = Field(..., description="Human-readable audit trail of the match decision.")
