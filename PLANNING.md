# Tender-Getter-RSA: Architectural & Business Plan

## 1. Vision & Strategy
**Tender-Getter-RSA** is designed as a professional-grade screening engine for South African state and private tenders. Its primary goal is to automate the discovery, matching, and compliance verification of tenders against specific company profiles.

By keeping the architecture highly modular, the core matching engine can easily be spun off into subsequent high-leverage products (e.g., Job-Getter-RSA, Funding-Getter-RSA).

---

## 2. File Structure & Component Overview

```text
Tender-Getter-RSA/
│
├── README.md                  # Quick intro & how to run
├── PLANNING.md                # DAY 1 - 4 full architectural plan
│
├── src/
│   └── tender_getter/
│       ├── __init__.py
│       ├── schemas.py         # Structured models (Pydantic-based)
│       ├── matcher.py         # Match calculations (CIDB, BBBEE, Location)
│       ├── parser.py          # Gemini OCR & compliance extractor
│       └── reporter.py        # PDF & Markdown report outputs
│
├── scripts/
│   ├── run_poc.py             # CLI command to output free matched PDFs
│   └── cipc_directory.py      # Lead list generation helper
│
└── tests/
    └── test_matcher.py        # Validating math stays bulletproof
```

---

## 3. South African Regulatory Gatekeeper Logic (The Math)

The matching engine relies on precise, legally defined formulas to qualify contractors and estimate their competitiveness.

### 3.1. B-BBEE Score Calculator (80/20 & 90/10)
State tenders use the preference point system based on the tender's value.

* **80/20 System (Tenders below R50 Million):** 80 points for price, 20 points for B-BBEE.
* **90/10 System (Tenders above R50 Million):** 90 points for price, 10 points for B-BBEE.

**Implementation (Python):**
```python
BB_BEE_POINTS = {
    "80/20": {
        1: 20, 2: 18, 3: 14, 4: 12, 5: 8, 6: 6, 7: 4, 8: 2, "Non-Compliant": 0
    },
    "90/10": {
        1: 10, 2: 9, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1, "Non-Compliant": 0
    }
}
```

### 3.2. CIDB Grading Evaluator
The Construction Industry Development Board (CIDB) restricts maximum tender values based on a contractor's registered grade. 

**Implementation (Python):**
```python
CIDB_LIMITS = {
    1: 200_000,       # Grade 1: up to R200k
    2: 1_000_000,     # Grade 2: up to R1m
    3: 3_000_000,     # Grade 3: up to R3m
    4: 6_000_000,     # Grade 4: up to R6m
    5: 10_000_000,    # Grade 5: up to R10m
    6: 20_000_000,    # Grade 6: up to R20m
    7: 60_000_000,    # Grade 7: up to R60m
    8: 200_000_000,   # Grade 8: up to R200m
    9: float('inf')   # Grade 9: No Limit
}
```

**Match Rule:**
A company qualifies for a tender requiring CIDB `X` of class `Y` if and only if:
1. The company has a registered grading of class `Y` (e.g., "CE", "GB", "EE").
2. The company's registered grade level `L` is `>= L_tender` OR the estimated contract value is `<= CIDB_LIMITS[L]`.

### 3.3. Sector-Specific Gatekeepers
Different sectors require specific regulatory body registrations. We track these as mandatory "industry tags" with active verification flags:
* **Security Services:** Requires **PSIRA** registration.
* **Construction/Housing:** Requires **NHBRC** registration.
* **Electrical Work:** Requires a **Wireman's License / Department of Labour** registration.
* **Cleaning/Waste:** Requires specific municipal waste-management licenses.

---

## 4. Database & Schemas (Pydantic Models)

To maintain rigorous data integrity across scraping, matching, and reporting, we use structured Pydantic models in `src/tender_getter/schemas.py`.

### Proposed Schemas:
* **CompanyProfile:** Represents a lead/client (Name, CIDB grades, B-BBEE level, Sector tags, Location).
* **TenderDocument:** Represents a parsed tender (Issuer, Value Estimate, Required CIDB, Required Tags, Closing Date).
* **MatchResult:** The outcome of the matching algorithm (Score, Eligibility Boolean, Missing Requirements).

---

## 5. Next Steps (Day 2 - 4)
- **Day 2:** Build out `schemas.py` and `matcher.py` based on the logic defined above, implementing unit tests in `tests/test_matcher.py` to ensure compliance.
- **Day 3:** Build `parser.py` using Gemini API to OCR and extract data from tender PDFs into our Pydantic `TenderDocument` schema.
- **Day 4:** Integrate `reporter.py` to generate the automated PDF/Markdown reports for qualified leads, and test the full pipeline using `run_poc.py`.
