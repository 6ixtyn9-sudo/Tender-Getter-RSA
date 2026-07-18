"""
Media handling for WhatsApp: download, upload to Supabase, parse with Gemini.
SECURE VERSION: SSL verification, PDF validation, path sanitization, size limits.
"""

import os
import io
import re
import logging
import mimetypes
import certifi
import ssl
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
GEMINI_MODEL = os.getenv("GEMINI_MODEL_VISION", "gemini-1.5-pro")

# Security constants
MAX_MEDIA_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_MEDIA_TYPES = {
    "image/jpeg", "image/png", "image/heic", "image/webp",
    "application/pdf",
}

# SSL context with proper CA verification
_SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


# ---------------------------------------------------------------------------
# Document Type Detection
# ---------------------------------------------------------------------------

def guess_document_type(mime_type: str) -> Optional[DocumentType]:
    """Guess document type from MIME type."""
    mime_lower = mime_type.lower()
    if "pdf" in mime_lower:
        return DocumentType.OTHER  # Will be determined by content
    if "image" in mime_lower:
        return DocumentType.OTHER
    return DocumentType.OTHER


def classify_document_by_content(parsed_data: Dict[str, Any]) -> DocumentType:
    """Classify document type based on parsed content."""
    if any(k in parsed_data for k in ["csd_number", "supplier_number", "maaa_number"]):
        return DocumentType.CSD_LETTER
    if any(k in parsed_data for k in ["bbbee_level", "bbbee_status", "bee_level"]):
        return DocumentType.BBBEE_CERT
    if any(k in parsed_data for k in ["tax_pin", "pin_number", "sars_pin"]):
        return DocumentType.TAX_PIN
    if any(k in parsed_data for k in ["cidb_grading", "cidb_number", "grading_level"]):
        return DocumentType.CIDB_CERT
    if any(k in parsed_data for k in ["registration_number", "cipc_number", "company_number"]):
        return DocumentType.CIPC_CERT
    return DocumentType.OTHER


# ---------------------------------------------------------------------------
# Media Download (SECURE: SSL verification, size limits, auth)
# ---------------------------------------------------------------------------

async def download_media(
    media_url: str,
    auth: Optional[tuple] = None,
    timeout: float = 30.0,
    max_size: int = MAX_MEDIA_SIZE,
) -> bytes:
    """
    Download media from Twilio's media URL with security controls.
    - SSL verification enforced
    - Size limit enforced
    - Twilio auth required
    """
    # Validate URL scheme
    if not media_url.startswith("https://"):
        raise ValueError("Media URL must use HTTPS")
    
    # Twilio auth required
    if auth is None:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        if not account_sid or not auth_token:
            raise ValueError("Twilio credentials not configured")
        auth = (account_sid, auth_token)
    
    # Download with streaming to enforce size limit
    async with httpx.AsyncClient(
        timeout=timeout,
        verify=_SSL_CONTEXT,  # SSL verification enforced
    ) as client:
        async with client.stream("GET", media_url, auth=auth) as response:
            response.raise_for_status()
            
            # Check content length header
            content_length = response.headers.get("content-length")
            if content_length and int(content_length) > max_size:
                raise ValueError(f"Media file too large: {content_length} bytes (max {max_size})")
            
            # Stream download with size enforcement
            content = bytearray()
            async for chunk in response.aiter_bytes():
                content.extend(chunk)
                if len(content) > max_size:
                    raise ValueError(f"Media file exceeds size limit ({max_size} bytes)")
            
            return bytes(content)


async def download_media_to_file(
    media_url: str,
    filepath: str,
    auth: Optional[tuple] = None,
) -> int:
    """Download media directly to file with size enforcement."""
    content = await download_media(media_url, auth=auth)
    with open(filepath, "wb") as f:
        f.write(content)
    return len(content)


# ---------------------------------------------------------------------------
# Supabase Upload (SECURE: path sanitization)
# ---------------------------------------------------------------------------

async def upload_to_supabase(
    content: bytes,
    mime_type: str,
    user_id: str,
    filename: Optional[str] = None,
) -> str:
    """
    Upload media to Supabase Storage with path sanitization.
    Returns the storage path.
    """
    try:
        from supabase import create_client, Client
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            return await _save_locally(content, mime_type, filename)
        
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Generate safe filename
        if not filename:
            ext = mimetypes.guess_extension(mime_type) or ".bin"
            filename = f"{uuid.uuid4().hex}{ext}"
        
        # Sanitize user_id for path safety (no path traversal)
        safe_user_id = re.sub(r"[^+\d]", "", user_id)
        
        # Path: safe_user_id/year/month/day/filename
        date_path = datetime.utcnow().strftime("%Y/%m/%d")
        storage_path = f"{safe_user_id}/{date_path}/{filename}"
        
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
        return await _save_locally(content, mime_type, filename)


async def _save_locally(
    content: bytes,
    mime_type: str,
    filename: Optional[str] = None,
) -> str:
    """Fallback: save media locally for development."""
    import pathlib
    
    base_dir = pathlib.Path("localdata/whatsapp_media")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    if not filename:
        ext = mimetypes.guess_extension(mime_type) or ".bin"
        filename = f"{uuid.uuid4().hex}{ext}"
    
    filepath = base_dir / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
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
# Document Parsing with Gemini (SECURE: PDF validation)
# ---------------------------------------------------------------------------

async def parse_document_with_gemini(
    content: bytes,
    mime_type: str,
    hint_type: Optional[DocumentType] = None,
) -> Optional[Dict[str, Any]]:
    """
    Parse document using Gemini Vision with security controls.
    - PDF validation before sending
    - Size limits enforced
    """
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set — skipping document parsing")
        return None
    
    # Validate PDF before sending to Gemini
    if mime_type == "application/pdf":
        if not content.startswith(b"%PDF"):
            logger.warning("Invalid PDF file rejected")
            return {"error": "Invalid PDF file"}
        if len(content) > MAX_MEDIA_SIZE:
            logger.warning("PDF too large for processing")
            return {"error": "PDF too large for processing"}
    
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        prompt = _build_parsing_prompt(hint_type)
        
        if mime_type.startswith("image/"):
            # Preprocess image for better OCR
            processed_content = preprocess_image(content)
            image = Image.open(io.BytesIO(processed_content))
            response = model.generate_content([prompt, image])
        elif "pdf" in mime_type:
            # Basic PDF validation
            if not content.startswith(b"%PDF"):
                return {"error": "Invalid PDF file"}
            # For PDF, convert first page to image would be better
            # Simplified: try as image
            response = model.generate_content([prompt, content])
        else:
            text = content.decode("utf-8", errors="ignore")
            response = model.generate_content([prompt, text])
        
        return _parse_gemini_response(response.text)
        
    except Exception as e:
        logger.error(f"Gemini parsing failed: {type(e).__name__}")
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
    """Parse Gemini response, extracting JSON safely."""
    import json
    import re
    
    # Try to find JSON in response
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
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
        
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        if image.width > max_size[0] or image.height > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        output = io.BytesIO()
        image.save(output, format="JPEG", quality=85)
        return output.getvalue()
        
    except Exception as e:
        logger.warning(f"Image preprocessing failed: {type(e).__name__}")
        return content