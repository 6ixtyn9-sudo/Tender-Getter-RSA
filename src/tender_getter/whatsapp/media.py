"""
Media handling for WhatsApp: download, upload to Supabase, parse with Gemini.
"""

import os
import io
import logging
import mimetypes
from typing import Optional, Dict, Any, BinaryIO
from datetime import datetime
import uuid

import httpx
from PIL import Image

from .models import DocumentType

logger = logging.getLogger(__name__)

# Supabase storage bucket
SUPABASE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "whatsapp-media")

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL_VISION", "gemini-2.5-flash")


# ---------------------------------------------------------------------------
# Document Type Detection
# ---------------------------------------------------------------------------

def guess_document_type(mime_type: str) -> Optional[DocumentType]:
    """Guess document type from MIME type and filename."""
    mime_lower = mime_type.lower()
    
    if "pdf" in mime_lower:
        return DocumentType.OTHER  # Will be determined by content
    if "image" in mime_lower:
        return DocumentType.OTHER
    
    return DocumentType.OTHER


def classify_document_by_content(parsed_data: Dict[str, Any]) -> DocumentType:
    """Classify document type based on parsed content."""
    # CSD indicators
    if any(k in parsed_data for k in ["csd_number", "supplier_number", "maaa_number"]):
        return DocumentType.CSD_LETTER
    
    # B-BBEE indicators
    if any(k in parsed_data for k in ["bbbee_level", "bbbee_status", "bee_level"]):
        return DocumentType.BBBEE_CERT
    
    # Tax PIN indicators
    if any(k in parsed_data for k in ["tax_pin", "pin_number", "sars_pin"]):
        return DocumentType.TAX_PIN
    
    # CIDB indicators
    if any(k in parsed_data for k in ["cidb_grading", "cidb_number", "grading_level"]):
        return DocumentType.CIDB_CERT
    
    # CIPC indicators
    if any(k in parsed_data for k in ["registration_number", "cipc_number", "company_number"]):
        return DocumentType.CIPC_CERT
    
    return DocumentType.OTHER


# ---------------------------------------------------------------------------
# Media Download
# ---------------------------------------------------------------------------

async def download_media(
    media_url: str,
    auth: Optional[tuple] = None,
    timeout: float = 30.0,
) -> bytes:
    """
    Download media from Twilio's media URL.
    Twilio media URLs require authentication (Account SID + Auth Token).
    """
    if auth is None:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        if account_sid and auth_token:
            auth = (account_sid, auth_token)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(media_url, auth=auth)
        response.raise_for_status()
        return response.content


async def download_media_to_file(
    media_url: str,
    filepath: str,
    auth: Optional[tuple] = None,
) -> int:
    """Download media directly to file, return size in bytes."""
    content = await download_media(media_url, auth)
    with open(filepath, "wb") as f:
        f.write(content)
    return len(content)


# ---------------------------------------------------------------------------
# Supabase Upload
# ---------------------------------------------------------------------------

async def upload_to_supabase(
    content: bytes,
    mime_type: str,
    user_id: str,
    filename: Optional[str] = None,
) -> str:
    """
    Upload media to Supabase Storage.
    Returns the storage path.
    """
    try:
        from supabase import create_client, Client
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            # Fallback: save locally for development
            return await _save_locally(content, mime_type, user_id, filename)
        
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Generate unique filename
        if not filename:
            ext = mimetypes.guess_extension(mime_type) or ".bin"
            filename = f"{uuid.uuid4().hex}{ext}"
        
        # Path: user_id/year/month/day/filename
        date_path = datetime.utcnow().strftime("%Y/%m/%d")
        storage_path = f"{user_id}/{date_path}/{filename}"
        
        # Upload
        result = supabase.storage.from_(SUPABASE_BUCKET).upload(
            path=storage_path,
            file=content,
            file_options={"content-type": mime_type, "upsert": "false"},
        )
        
        if hasattr(result, 'error') and result.error:
            raise Exception(f"Supabase upload failed: {result.error}")
        
        return storage_path
        
    except Exception as e:
        logger.warning(f"Supabase upload failed, saving locally: {e}")
        return await _save_locally(content, mime_type, user_id, filename)


async def _save_locally(
    content: bytes,
    mime_type: str,
    user_id: str,
    filename: Optional[str] = None,
) -> str:
    """Fallback: save media locally for development."""
    import pathlib
    
    base_dir = pathlib.Path("localdata/whatsapp_media")
    user_dir = base_dir / user_id.replace("+", "").replace(":", "_")
    user_dir.mkdir(parents=True, exist_ok=True)
    
    if not filename:
        ext = mimetypes.guess_extension(mime_type) or ".bin"
        filename = f"{uuid.uuid4().hex}{ext}"
    
    filepath = user_dir / filename
    with open(filepath, "wb") as f:
        f.write(content)
    
    return str(filepath)


async def get_media_url(storage_path: str, expires_in: int = 3600) -> str:
    """Get signed URL for media access."""
    try:
        from supabase import create_client, Client
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            # Local fallback
            return f"file://{storage_path}"
        
        supabase: Client = create_client(supabase_url, supabase_key)
        
        result = supabase.storage.from_(SUPABASE_BUCKET).create_signed_url(
            path=storage_path,
            expires_in=expires_in,
        )
        
        if hasattr(result, 'error') and result.error:
            raise Exception(f"Signed URL failed: {result.error}")
        
        return result.get("signedURL", "")
        
    except Exception as e:
        logger.error(f"Failed to create signed URL: {e}")
        return ""


# ---------------------------------------------------------------------------
# Document Parsing with Gemini
# ---------------------------------------------------------------------------

async def parse_document_with_gemini(
    content: bytes,
    mime_type: str,
    hint_type: Optional[DocumentType] = None,
) -> Optional[Dict[str, Any]]:
    """
    Parse document using Gemini Vision.
    Extracts structured data based on document type.
    """
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set — skipping document parsing")
        return None
    
    try:
        from google import genai
        from google.genai import types as genai_types

        # google-genai uses a per-key client (no global configure()).
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Prepare prompt based on document type
        prompt = _build_parsing_prompt(hint_type)

        # Prepare image/PDF/text for Gemini
        if mime_type.startswith("image/"):
            image = Image.open(io.BytesIO(content))
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[prompt, image],
            )
        elif "pdf" in mime_type:
            # Native inline PDF support — send the document bytes directly.
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[
                    prompt,
                    genai_types.Part.from_bytes(
                        data=content, mime_type="application/pdf"
                    ),
                ],
            )
        else:
            # Try as text
            text = content.decode("utf-8", errors="ignore")
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[prompt, text],
            )

        # Parse JSON response
        return _parse_gemini_response(response.text)
        
    except Exception as e:
        logger.error(f"Gemini parsing failed: {e}")
        return None


def _build_parsing_prompt(hint_type: Optional[DocumentType]) -> str:
    """Build parsing prompt based on expected document type."""
    base_prompt = """
You are a document parser for South African business compliance documents.
Extract structured JSON data from the document.

Return ONLY valid JSON with the following schema:
"""
    
    if hint_type == DocumentType.CSD_LETTER:
        return base_prompt + """
{
  "csd_number": "string (MAAA... format)",
  "supplier_number": "string",
  "company_name": "string",
  "registration_number": "string (CIPC format)",
  "status": "string (Active/Inactive)",
  "address": "string",
  "contact_person": "string",
  "email": "string",
  "phone": "string"
}
"""
    
    elif hint_type == DocumentType.BBBEE_CERT:
        return base_prompt + """
{
  "bbbee_level": "integer (1-8, or 9 for non-compliant)",
  "bbbee_status": "string",
  "certificate_number": "string",
  "issue_date": "string (YYYY-MM-DD)",
  "expiry_date": "string (YYYY-MM-DD)",
  "company_name": "string",
  "registration_number": "string",
  "black_ownership_pct": "float",
  "women_ownership_pct": "float",
  "youth_ownership_pct": "float",
  "scorecard_type": "string (QSE/EME/Generic)"
}
"""
    
    elif hint_type == DocumentType.TAX_PIN:
        return base_prompt + """
{
  "tax_pin": "string",
  "pin_number": "string",
  "company_name": "string",
  "registration_number": "string",
  "issue_date": "string (YYYY-MM-DD)",
  "status": "string (Active/Expired)"
}
"""
    
    elif hint_type == DocumentType.CIDB_CERT:
        return base_prompt + """
{
  "cidb_number": "string (CRS number)",
  "company_name": "string",
  "cidb_gradings": [
    {"class_code": "string (CE/GB/EE/ME/SB...)", "level": "integer (1-9)"}
  ],
  "status": "string (Active/Expired)",
  "expiry_date": "string (YYYY-MM-DD)"
}
"""
    
    elif hint_type == DocumentType.CIPC_CERT:
        return base_prompt + """
{
  "registration_number": "string (YYYY/NNNNNN/NN)",
  "company_name": "string",
  "company_type": "string (Pty Ltd/CC/etc)",
  "registration_date": "string (YYYY-MM-DD)",
  "status": "string (In Business/Deregistered)",
  "directors": [{"name": "string", "id_number": "string"}]
}
"""
    
    # Generic prompt
    return base_prompt + """
{
  "document_type": "string (csd_letter/bbbee_cert/tax_pin/cidb_cert/cipc_cert/other)",
  "company_name": "string",
  "registration_number": "string",
  "key_fields": {},
  "raw_text": "string (first 500 chars for reference)"
}
"""


def _parse_gemini_response(text: str) -> Optional[Dict[str, Any]]:
    """Parse Gemini response, extracting JSON."""
    import json
    import re
    
    # Try to find JSON in response
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    # Try full text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    logger.warning(f"Failed to parse Gemini response as JSON: {text[:200]}")
    return None


# ---------------------------------------------------------------------------
# Image Preprocessing
# ---------------------------------------------------------------------------

def preprocess_image(content: bytes, max_size: tuple = (2048, 2048)) -> bytes:
    """Preprocess image for better OCR: resize, enhance contrast."""
    try:
        image = Image.open(io.BytesIO(content))
        
        # Convert to RGB if needed
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        # Resize if too large
        if image.width > max_size[0] or image.height > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Enhance contrast slightly
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        # Save to bytes
        output = io.BytesIO()
        image.save(output, format="JPEG", quality=85)
        return output.getvalue()
        
    except Exception as e:
        logger.warning(f"Image preprocessing failed: {e}")
        return content