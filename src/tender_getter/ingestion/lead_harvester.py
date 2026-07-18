"""
lead_harvester.py - CSV-based company profile importer for Tender Getter RSA.

Reads a CSV (from CIPC municipal registry scrapes or manual lists) containing
raw supplier data, constructs CompanyProfile objects, and upserts them into
the local SQLite database.

Expected CSV columns (header row required):
  company_name, registration_number, csd_number, bbbee_level,
  black_ownership_pct, province, city, sectors, cidb_codes, has_tax_pin

  sectors:    semicolon-separated list, e.g. "Electrical;Construction"
  cidb_codes: semicolon-separated grading strings, e.g. "3EE;2CE" or "None"
  has_tax_pin: "true" / "false" / "1" / "0"

Example CSV row:
  Sipho Electrics,2024/111111/07,MAAA0111111,1,100.0,Gauteng,Johannesburg,Electrical;Construction,3EE;2CE,true
"""

import csv
import io
import logging
from typing import Optional

from tender_getter.core.schemas import CIDBGrading, Location, CompanyProfile
from tender_getter.core.database import TenderDatabase

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# CIDB code parser helper
# ---------------------------------------------------------------------------

def _parse_cidb_codes(raw: str) -> list[CIDBGrading]:
    """
    Parses a semicolon-delimited string of CIDB codes like "3EE;2CE"
    into a list of CIDBGrading objects.

    Returns an empty list for "None", "", or unparseable strings.
    """
    gradings: list[CIDBGrading] = []
    if not raw or raw.strip().lower() in ("none", "n/a", ""):
        return gradings

    for token in raw.split(";"):
        token = token.strip()
        if not token:
            continue
        # Expect format: <digit><2-letter-code> e.g. "3EE", "2CE"
        if len(token) >= 3 and token[0].isdigit():
            level_str = token[0]
            class_code = token[1:].upper()
            try:
                gradings.append(
                    CIDBGrading(class_code=class_code, level=int(level_str))
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning("Skipping invalid CIDB token '%s': %s", token, exc)
        else:
            logger.warning("Unrecognised CIDB token format: '%s'", token)

    return gradings


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "yes", "y")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def import_suppliers_from_csv(
    csv_text: str,
    db: Optional[TenderDatabase] = None,
) -> int:
    """
    Parses a CSV string and upserts all valid company profiles into the database.

    Parameters:
      csv_text: Raw CSV content as a string (with header row).
      db: Optional TenderDatabase instance. If None, a new default-path db
          is used (will be opened and closed inside this function).

    Returns:
      The number of company profiles successfully imported.
    """
    reader = csv.DictReader(io.StringIO(csv_text))
    profiles: list[CompanyProfile] = []

    for i, row in enumerate(reader, start=2):  # row 2 onwards (row 1 = header)
        try:
            profile = CompanyProfile(
                registration_number=row["registration_number"].strip(),
                company_name=row["company_name"].strip(),
                csd_number=row.get("csd_number", "").strip() or None,
                bbbee_level=int(row.get("bbbee_level", 9)),
                black_ownership_pct=float(row.get("black_ownership_pct", 0.0)),
                cidb_gradings=_parse_cidb_codes(row.get("cidb_codes", "")),
                location=Location(
                    province=row["province"].strip(),
                    city=row["city"].strip(),
                ),
                sectors=[
                    s.strip()
                    for s in row.get("sectors", "").split(";")
                    if s.strip()
                ],
                has_tax_pin=_parse_bool(row.get("has_tax_pin", "false")),
                is_active=True,
            )
            profiles.append(profile)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Skipping CSV row %d due to error: %s", i, exc)

    if not profiles:
        return 0

    # Use provided db or open a fresh one
    if db is not None:
        for profile in profiles:
            db.upsert_company(profile)
    else:
        with TenderDatabase() as _db:
            for profile in profiles:
                _db.upsert_company(profile)

    logger.info("import_suppliers_from_csv: imported %d profiles.", len(profiles))
    return len(profiles)
