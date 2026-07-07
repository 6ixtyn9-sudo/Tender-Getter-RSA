"""
reporter.py - Generates the R500 "Tender Opportunity Report" deliverable.

Takes a CompanyProfile and a MatchResult and produces a professional
Markdown audit report that can be:
  - Printed as a PDF via any Markdown renderer
  - Emailed / WhatsApp'd directly to a client
  - Used as a compliance record in the bidding process

Output file naming convention:
  TG_REPORT_<CompanyName>_<TenderID>.md
  (spaces and special chars replaced with underscores)
"""

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .schemas import CompanyProfile, TenderOpportunity, MatchResult
from .matcher import match as run_match, CIDB_LIMITS

# Default output directory relative to project root
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[3] / "localdata"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_report(
    company: CompanyProfile,
    tender: TenderOpportunity,
    result: Optional[MatchResult] = None,
    output_dir: Optional[Path] = None,
) -> Path:
    """
    Generates a Markdown Tender Opportunity Report for the given
    company / tender pair and writes it to disk.

    Parameters:
      company:    The client's CompanyProfile.
      tender:     The TenderOpportunity being evaluated.
      result:     Pre-computed MatchResult. If None, the matcher is run automatically.
      output_dir: Directory to write the report to. Defaults to localdata/.

    Returns:
      The Path to the generated .md report file.
    """
    if result is None:
        result = run_match(company, tender)

    out_dir = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = _safe_filename(company.company_name, tender.tender_id)
    output_path = out_dir / filename

    content = _build_report(company, tender, result)
    output_path.write_text(content, encoding="utf-8")

    return output_path


# ---------------------------------------------------------------------------
# Report builder
# ---------------------------------------------------------------------------

def _build_report(
    company: CompanyProfile,
    tender: TenderOpportunity,
    result: MatchResult,
) -> str:
    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    status_banner = "✅ ELIGIBLE" if result.is_eligible else "❌ DISQUALIFIED"
    score_bar = _score_bar(result.match_score)

    # B-BBEE label
    bbbee_label = (
        "Non-Compliant" if company.bbbee_level == 9
        else f"Level {company.bbbee_level}"
    )

    # CIDB gradings table
    cidb_rows = "\n".join(
        f"| {g.class_code} | Grade {g.level} | R{CIDB_LIMITS[g.level]:,.0f} |"
        for g in company.cidb_gradings
    ) or "| — | — | — |"

    # Geofence indicator
    geo_scope = tender.location_target or "National"
    geo_match = (
        geo_scope.lower() == "national"
        or geo_scope.lower() == company.location.province.lower()
    )
    geo_icon = "✅" if geo_match else "❌"

    # CSD indicator
    csd_icon = "✅" if company.csd_number else "❌"
    csd_display = company.csd_number or "Not Registered"

    # Tax indicator
    tax_icon = "✅" if company.has_tax_pin else "❌"

    # COIDA indicator
    coida_icon = "✅" if company.has_coida else "⚠️"

    # B-BBEE points display
    bbbee_pts_display = (
        f"{result.bbbee_points:.0f} / {result.bbbee_max_points:.0f} pts "
        f"({result.bbbee_system} system)"
    )

    # SBD compliance checklist
    sbd_checklist = _build_sbd_checklist(company, tender)

    # Closing date
    closing = tender.closing_date.strftime("%d %B %Y at %H:%M UTC")

    # Estimated value
    est_val = (
        f"R{tender.estimated_value:,.0f}"
        if tender.estimated_value
        else "Not Disclosed"
    )

    return f"""\
# 📋 Tender Opportunity Report
**Tender Getter RSA** | Confidential Client Report
Generated: {now}

---

## Company: {company.company_name}
| Field | Value |
|---|---|
| CIPC Registration | {company.registration_number} |
| CSD Supplier Number | {csd_display} |
| B-BBEE Status | {bbbee_label} |
| Black Ownership | {company.black_ownership_pct:.1f}% |
| Women Ownership | {company.women_ownership_pct:.1f}% |
| Youth Ownership | {company.youth_ownership_pct:.1f}% |
| Province | {company.location.province} |
| City | {company.location.city} |
| Sectors | {", ".join(company.sectors) or "—"} |

### CIDB Registered Gradings
| Class | Grade | Financial Cap |
|---|---|---|
{cidb_rows}

---

## Tender: {tender.title}
| Field | Value |
|---|---|
| Bid Number | {tender.tender_id} |
| Issuing Entity | {tender.issuing_entity} |
| Closing Date | {closing} |
| Estimated Value | {est_val} |
| Geographic Scope | {geo_scope} |
| Required CIDB | {(tender.required_cidb_class or "—") + str(tender.required_cidb_level or "")} |
| CSD Mandatory | {"Yes" if tender.mandatory_csd else "No"} |

---

## Match Verdict: {status_banner}

**Match Score: {result.match_score:.1f}%**
{score_bar}

**B-BBEE Preference Points: {bbbee_pts_display}**

> {result.feedback}

---

## Compliance Gate Summary
| Gate | Requirement | Status |
|---|---|---|
| CSD Registration | MAAA Supplier Number | {csd_icon} {csd_display} |
| SARS Tax Compliance | Active Tax PIN | {tax_icon} {"Active" if company.has_tax_pin else "Not Active"} |
| COIDA Registration | Compensation Fund | {coida_icon} {"Registered" if company.has_coida else "Not Registered"} |
| Geofencing | {geo_scope} | {geo_icon} {company.location.province} |
| B-BBEE Preference | {result.bbbee_system or "—"} system | {"✅" if result.bbbee_points > 0 else "⚠️"} {bbbee_pts_display} |

---

## SBD Document Compliance Checklist
{sbd_checklist}

---

## Next Steps
{"### ✅ You are eligible to bid! Follow these steps:" if result.is_eligible else "### ❌ You cannot bid on this tender. Reasons and recommendations:"}

{"1. **Download the bid documents** from the issuing entity's e-portal." if result.is_eligible else f"1. **Root Cause:** {result.disqualification_reason}"}
{"2. **Complete SBD forms** (SBD 1, SBD 4, SBD 6.1, SBD 6.2, SBD 8)." if result.is_eligible else "2. **Remediation:** Contact Tender Getter RSA for a compliance upgrade roadmap."}
{"3. **Attach your CSD printout**, B-BBEE certificate, and CIDB grading certificate." if result.is_eligible else "3. **Alternative tenders:** Our engine will continue scanning for matching opportunities."}
{"4. **Submit before:** " + closing if result.is_eligible else ""}

---

*This report was generated automatically by **Tender Getter RSA**.*
*It is provided for informational purposes only and does not constitute legal or procurement advice.*
*Always verify tender requirements against the official bid documents before submitting.*

**© {datetime.now().year} Tender Getter RSA — Confidential**
"""


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _safe_filename(company_name: str, tender_id: str) -> str:
    """Generates a safe, filesystem-friendly .md filename."""
    def sanitise(s: str) -> str:
        return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return f"TG_REPORT_{sanitise(company_name)}_{sanitise(tender_id)}.md"


def _score_bar(score: float, width: int = 20) -> str:
    """Returns a simple ASCII progress bar for the match score."""
    filled = int(round(score / 100 * width))
    empty = width - filled
    return f"`[{'█' * filled}{'░' * empty}] {score:.1f}%`"


def _build_sbd_checklist(company: CompanyProfile, tender: TenderOpportunity) -> str:
    """Builds a Markdown checklist of standard SBD form requirements."""
    items = [
        ("SBD 1 — Invitation to Bid", True),
        ("SBD 4 — Declaration of Interest", True),
        (
            "SBD 6.1 — Preference Points Claim (B-BBEE)",
            company.bbbee_level <= 8,
        ),
        ("SBD 6.2 — Declaration of B-BBEE Status", True),
        (
            "SBD 7.2 — Contract Performance Guarantee",
            tender.estimated_value is not None and tender.estimated_value > 500_000,
        ),
        ("SBD 8 — Declaration of Supplier Past Supply Chain Fraud", True),
        ("B-BBEE Certificate / Sworn Affidavit", True),
        (
            "CIDB Grading Certificate",
            bool(tender.required_cidb_class),
        ),
        ("CSD Supplier Registration Printout", tender.mandatory_csd),
        ("SARS Tax Compliance PIN / Certificate", tender.tax_compliance_required),
        ("COIDA Letter of Good Standing", company.has_coida),
    ]
    lines = []
    for label, required in items:
        if required:
            lines.append(f"- [ ] {label}")
    return "\n".join(lines)
