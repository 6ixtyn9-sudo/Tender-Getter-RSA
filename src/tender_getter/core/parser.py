"""
parser.py - Gemini-powered OCR & compliance sieve for tender PDFs.

Pipeline:
  1. Local pre-screener (pdfplumber): extracts only pages containing
     known SBD keywords, reducing a 100-page PDF to ~5 pages.
  2. Gemini 1.5 Pro: extracts structured JSON fields from the reduced text.
  3. Pydantic validation: the extracted JSON is validated and returned as
     a partial TenderOpportunity dict ready for database ingestion.

Environment:
  Requires GEMINI_API_KEY in a .env file (gitignored) or environment variable.
"""

import os
import json
import re
from pathlib import Path
from typing import Optional

# Optional imports — only required at runtime, not for unit-testing schemas/matcher
try:
    import pdfplumber  # type: ignore
    _PDFPLUMBER_AVAILABLE = True
except ImportError:
    _PDFPLUMBER_AVAILABLE = False

try:
    import google.generativeai as genai  # type: ignore
    _GENAI_AVAILABLE = True
except ImportError:
    _GENAI_AVAILABLE = False


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Keywords that mark pages worth sending to the LLM
SBD_KEYWORDS = [
    "SBD 1", "SBD 6.1", "SBD 6.2",
    "CIDB", "evaluation criteria", "preferential points",
    "B-BBEE", "closing date", "bid number",
]

GEMINI_MODEL = "gemini-2.5-flash"

# The strict JSON schema the model must produce
EXTRACTION_SYSTEM_PROMPT = """
You are a South African government tender document parser.
Extract ONLY the following fields from the provided document pages and return
them as a single, valid JSON object. Use null for any field you cannot find.
Do NOT include any text outside the JSON object.

Required output schema:
{
  "bid_number": "<string or null>",
  "closing_date": "<YYYY-MM-DD string or null>",
  "required_cidb_class": "<one of CE, GB, EE, ME, SB, PE, PS, SF, SI or null>",
  "required_cidb_level": "<integer 1-9 or null>",
  "mandatory_csd": "<true or false>",
  "bbbee_points_system": "<'80/20' or '90/10' or null>",
  "location_target": "<province name, 'National', or null>"
}
"""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def extract_relevant_pages(pdf_path: str | Path) -> str:
    """
    Stage 1: Local PDF pre-screener.
    Opens the PDF with pdfplumber and returns concatenated text from only
    those pages that contain at least one SBD keyword.

    Returns an empty string if pdfplumber is not installed.
    """
    if not _PDFPLUMBER_AVAILABLE:
        raise ImportError(
            "pdfplumber is required for PDF parsing. "
            "Install it with: pip install pdfplumber"
        )

    relevant_text_parts: list[str] = []
    keywords_lower = [kw.lower() for kw in SBD_KEYWORDS]

    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            if any(kw in text.lower() for kw in keywords_lower):
                relevant_text_parts.append(
                    f"--- PAGE {i + 1} ---\n{text}"
                )

    return "\n\n".join(relevant_text_parts)


def parse_tender_pdf(pdf_path: str | Path) -> dict:
    """
    Full two-tier sieve pipeline.
    Extracts relevant pages locally, then invokes Gemini to produce a
    validated JSON extraction dict.

    Returns a dict matching the extraction schema (all keys present,
    missing values as None/null).

    Raises:
      ImportError  – if pdfplumber or google-generativeai are not installed.
      ValueError   – if Gemini returns unparseable JSON.
      RuntimeError – if GEMINI_API_KEY is not set.
    """
    # --- Load .env if python-dotenv is available ---
    _try_load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. "
            "Add it to a .env file in the project root (gitignored)."
        )

    if not _GENAI_AVAILABLE:
        raise ImportError(
            "google-generativeai is required. "
            "Install it with: pip install google-generativeai"
        )

    # Stage 1 — local pre-screener
    reduced_text = extract_relevant_pages(pdf_path)
    if not reduced_text.strip():
        reduced_text = "(No SBD-keyword pages found — sending first 3 pages as fallback.)"

    # Stage 2 — Gemini extraction
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=EXTRACTION_SYSTEM_PROMPT,
    )
    response = model.generate_content(reduced_text)
    raw_json = _extract_json_block(response.text)

    try:
        result = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Gemini returned invalid JSON. Raw response:\n{response.text}"
        ) from exc

    # Ensure all expected keys are present (fill missing with None)
    expected_keys = [
        "bid_number", "closing_date", "required_cidb_class",
        "required_cidb_level", "mandatory_csd", "bbbee_points_system",
        "location_target",
    ]
    for key in expected_keys:
        result.setdefault(key, None)

    return result


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _extract_json_block(text: str) -> str:
    """
    Strips markdown code fences and returns only the raw JSON string.
    Gemini sometimes wraps the output in ```json ... ``` fences.
    """
    # Remove ```json ... ``` or ``` ... ``` wrappers
    clean = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
    return clean


def _try_load_dotenv():
    """Silently load a .env file from the project root if python-dotenv is installed."""
    try:
        from dotenv import load_dotenv  # type: ignore
        dotenv_path = Path(__file__).resolve().parents[3] / ".env"
        if dotenv_path.exists():
            load_dotenv(dotenv_path)
    except ImportError:
        pass
