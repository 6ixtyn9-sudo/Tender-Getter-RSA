# Tender Getter RSA - Architectural & Technical Specification
Date: 2026-07-07
Venture: Commercial B2B SaaS Bidding Matchmaker (South Africa)
Version: 1.0.0

## 1. Executive Summary & USP
Tender Getter RSA is a highly optimized, AI-native B2B matchmaking and proposal-drafting platform built for South African SMMEs (Small, Medium, and Micro Enterprises).

The USP is execution-focused: We do not just aggregate a list of daily links (which existing R250-R800/month portals do). We solve the disqualification and proposal-writing traps by instantly screening non-negotiable regulatory gates (CSD, SARS, CIDB, B-BBEE, Geofencing) and generating custom-synthesized compliance-win strategies and proposal drafts in seconds.

## 2. Core Python Architecture & Schemas
To ensure rapid, modular iteration and high reliability, our backend is structured strictly around Pydantic validation models and a SQLite relational data layer.

### A. The Master Schemas (src/tender_getter/schemas.py)
Two data structures define the entire transaction space:

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class CIDBGrading(BaseModel):
    class_code: str = Field(..., description="e.g. CE (Civil Engineering), GB (General Building)")
    level: int = Field(..., ge=1, le=9, description="CIDB grading level from 1 to 9")

class Location(BaseModel):
    province: str
    city: str
    municipality: Optional[str] = None

class CompanyProfile(BaseModel):
    registration_number: str = Field(..., description="CIPC registration number")
    company_name: str
    csd_number: Optional[str] = Field(None, description="MAAA supplier number")
    bbbee_level: int = Field(9, ge=1, le=9, description="B-BBEE Level, 9 is Non-Compliant")
    black_ownership_pct: float = Field(0.0, ge=0.0, le=100.0)
    youth_ownership_pct: float = Field(0.0, ge=0.0, le=100.0)
    women_ownership_pct: float = Field(0.0, ge=0.0, le=100.0)
    cidb_gradings: List[CIDBGrading] = []
    location: Location
    sectors: List[str]
    has_tax_pin: bool = False
    has_coida: bool = False
    is_active: bool = True

class TenderOpportunity(BaseModel):
    tender_id: str = Field(..., description="Official bid number/reference")
    title: str
    issuing_entity: str
    closing_date: datetime
    estimated_value: Optional[float] = None
    required_cidb_class: Optional[str] = None
    required_cidb_level: Optional[int] = None
    mandatory_csd: bool = True
    location_target: Optional[str] = Field(None, description="e.g. 'Gauteng' or 'National'")
    raw_document_url: Optional[str] = None
```

### B. Relational Storage (src/tender_getter/database.py)
A local-first SQLite database matches these schemas for instant, zero-cost state management:
* **Table company_profiles:** Relational store of all registered clients.
* **Table tenders:** Relational cache of raw, parsed tenders.
* **Table matches:** Stores historic match results, evaluation scores, and client notification records.

## 3. Mathematical Matching & Gating Logic (src/tender_getter/matcher.py)
The matching core does not use vague vector similarity for regulatory hurdles. It uses strict mathematical filters followed by weighted heuristic sorting.

### Gate 1: Binary Disqualification Filters (Hard Blocks)
* **CSD Validation:** If Tender.mandatory_csd is True and Company.csd_number is null -> Disqualified (0% Match).
* **Tax Status:** If Tender.tax_compliance_required is True and Company.has_tax_pin is False -> Warning flag (Match demated/Hold).
* **CIDB Capacity Gate:**
  Define upper financial thresholds for Grade levels:
  Grade 1: R200k | Grade 2: R1m | Grade 3: R3m | Grade 4: R6m | Grade 5: R10m | Grade 6: R20m | Grade 7: R60m | Grade 8: R200m | Grade 9: No Limit.
  Constraint Rule: The matching engine blocks a match if Tender.required_cidb_class is present but the client does not possess that class, OR if Company.cidb_level < Tender.required_cidb_level.

### Gate 2: Preferential Procurement Scoring (B-BBEE / PPPFA Math)
* **80/20 System (Estimated Value < R50 Million):**
  Max Price points = 80.
  B-BBEE preference points allocated dynamically:
  Level 1 = 20 pts | Level 2 = 18 pts | Level 3 = 14 pts | Level 4 = 12 pts | Level 5 = 8 pts | Level 6 = 6 pts | Level 7 = 4 pts | Level 8 = 2 pts | Non-Compliant = 0 pts.
* **90/10 System (Estimated Value >= R50 Million):**
  Max Price points = 90.
  B-BBEE preference points allocated dynamically:
  Level 1 = 10 pts | Level 2 = 9 pts | Level 3 = 6 pts | Level 4 = 5 pts | Level 5 = 4 pts | Level 6 = 3 pts | Level 7 = 2 pts | Level 8 = 1 pt | Non-Compliant = 0 pts.

## 4. Gemini OCR & Compliance Sieve (src/tender_getter/parser.py)
Tender documents are highly complex, multi-page PDFs. To avoid blowing out our token budget and preventing lookup lag, the parsing pipeline uses a Two-Tier Sieve:

```text
[Messy 100-Page PDF] 
        │
        ▼ (Local Python Extraction)
 [Page Pre-Screener] ──► Extracts only pages containing "SBD 1", "SBD 6.1", 
        │                "CIDB", or "Evaluation Criteria". (Reduces to ~5 pages)
        ▼
[Gemini 1.5 Pro API] ──► Strict JSON Compliance Extraction (Structure Validation)
        │
        ▼
 [Relational Schema] ──► Piped into sqlite matching engine
```

**The System Prompt & Output Schema:**
Gemini 1.5 Pro is invoked with a strict JSON system schema to prevent any formatting drift:

```json
{
  "bid_number": "string",
  "closing_date": "string (YYYY-MM-DD or null)",
  "required_cidb_class": "string ('CE', 'GB', 'EE', 'ME' or null)",
  "required_cidb_level": "integer (1-9 or null)",
  "mandatory_csd": "boolean",
  "bbbee_points_system": "string ('80/20', '90/10' or null)",
  "location_target": "string or null"
}
```

## 5. Next Agent Playbook & Rapid Bootstrap Checklist
For future agents starting on this repository, do not build sprawling cloud wrappers. Follow this step-by-step technical implementation path immediately:

1. **Verify Python Environment:** Install standard lightweight requirements: pydantic, sqlite3, pypdf, pdfplumber, and google-generativeai.
2. **Build src/tender_getter/schemas.py:** Standardize the Pydantic models exactly as spec'd out in Section 2.
3. **Build src/tender_getter/matcher.py:** Write the binary gates and the BBBEE 80/20 & 90/10 point mapping.
4. **Wire up src/tender_getter/parser.py:** Connect to the Gemini 1.5 Pro API using Google AI Studio keys stored in a gitignored .env file.
5. **Construct scripts/run_poc.py:** A CLI runner that takes an inputted Company Profile, parses a mock/local SBD 1 PDF, executes the matcher, and spits out a clean Markdown terminal scorecard showing eligibility.
