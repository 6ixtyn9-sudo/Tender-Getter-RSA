"""
WhatsApp onboarding flow for Tender Getter RSA.
Multi-step conversation flow to collect company profile data.
"""

import logging
import re
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime

from .models import WhatsAppUser, OnboardingStep, DocumentType, VerificationStatus
from ..schemas import CIDBGrading, Location, CompanyProfile
from .database import upsert_user, upsert_conversation_state, get_conversation_state
from .media import guess_document_type

logger = logging.getLogger(__name__)

# CIDB class codes
CIDB_CLASSES = {
    "GB": "General Building",
    "CE": "Civil Engineering", 
    "EE": "Electrical Engineering",
    "ME": "Mechanical Engineering",
    "SB": "Asphalt Works",
    "SC": "Building Excavations",
    "SD": "Corrosion Protection",
    "SE": "Demolition & Blasting",
    "SF": "Fire Prevention & Protection",
    "SG": "Glazing / Curtain Walls",
    "SH": "Landscaping & Irrigation",
    "SI": "Lifts & Escalators",
    "SJ": "Piling & Foundations",
    "SK": "Road Markings & Signage",
    "SL": "Structural Steelwork",
    "SM": "Timber Buildings",
    "SN": "Waterproofing",
    "SO": "Water Supply & Drainage",
    "SQ": "Steel Security Fencing",
    "SP": "Electrical Engineering (Specialist)",
}


# ---------------------------------------------------------------------------
# Flow Entry Point
# ---------------------------------------------------------------------------

async def start_onboarding(user: WhatsAppUser) -> str:
    """Start or restart the onboarding flow."""
    user.onboarding_step = OnboardingStep.COMPANY_NAME
    user.onboarding_data = {}
    user.onboarding_started_at = datetime.utcnow()
    user.onboarding_completed_at = None
    upsert_user(user)
    
    return (
        "🚀 *Welcome to Tender Getter RSA Onboarding!*\n\n"
        "I'll help you set up your company profile in 5 steps:\n\n"
        "1️⃣ Company name & CIDB lookup\n"
        "2️⃣ CIDB grading confirmation\n"
        "3️⃣ Document upload (CSD, B-BBEE, Tax PIN, CIDB cert)\n"
        "4️⃣ Sector & province selection\n"
        "5️⃣ POPIA consent\n\n"
        "Let's start — what's your *company name*?\n\n"
        "(Type *cancel* anytime to exit)"
    )


async def handle_onboarding_step(user: WhatsAppUser, body: str, message_sid: str) -> str:
    """Route to appropriate step handler based on current step."""
    step = user.onboarding_step
    
    # Allow cancel at any step
    if body.lower() in ("cancel", "exit", "quit", "stop"):
        return await cancel_onboarding(user)
    
    handlers = {
        OnboardingStep.COMPANY_NAME: handle_company_name,
        OnboardingStep.CIDB_LOOKUP: handle_cidb_lookup,
        OnboardingStep.CIDB_CONFIRM: handle_cidb_confirm,
        OnboardingStep.DOCUMENT_UPLOAD: handle_document_upload_step,
        OnboardingStep.SECTOR_PROVINCE: handle_sector_province,
        OnboardingStep.POPIA_CONSENT: handle_popia_consent,
    }
    
    handler = handlers.get(step)
    if handler:
        return await handler(user, body, message_sid)
    
    # Fallback
    return await start_onboarding(user)


async def cancel_onboarding(user: WhatsAppUser) -> str:
    """Cancel onboarding and reset to welcome."""
    user.onboarding_step = OnboardingStep.WELCOME
    user.onboarding_data = {}
    upsert_user(user)
    
    return (
        "❌ Onboarding cancelled.\n\n"
        "You can restart anytime by typing *onboard*.\n\n"
        "Type *menu* for other options."
    )


# ---------------------------------------------------------------------------
# Step 1: Company Name
# ---------------------------------------------------------------------------

async def handle_company_name(user: WhatsAppUser, body: str, message_sid: str) -> str:
    """Handle company name input and lookup CIDB."""
    company_name = body.strip()
    
    if len(company_name) < 2:
        return "Please enter a valid company name (at least 2 characters)."
    
    # Store company name
    user.onboarding_data["company_name"] = company_name
    user.onboarding_step = OnboardingStep.CIDB_LOOKUP
    upsert_user(user)
    
    # Simulate CIDB lookup (in production, query CIDB register)
    cidb_matches = await lookup_cidb_register(company_name)
    
    if cidb_matches:
        user.onboarding_data["cidb_matches"] = cidb_matches
        user.onboarding_step = OnboardingStep.CIDB_CONFIRM
        upsert_user(user)
        
        # Format matches for display
        matches_text = "\n".join([
            f"{i+1}. {m['name']} — {m['grading']} (CRS: {m['crs']})"
            for i, m in enumerate(cidb_matches[:5])
        ])
        
        return (
            f"🔍 *Found {len(cidb_matches)} CIDB match(es) for \"{company_name}\":*\n\n"
            f"{matches_text}\n\n"
            f"Reply with the *number* of your company, or *0* if none match."
        )
    else:
        # No CIDB match - ask for manual entry
        return (
            f"🔍 No CIDB matches found for \"{company_name}\".\n\n"
            f"Do you have a CIDB grading? If yes, reply with:\n"
            f"`class level` (e.g., `GB 3` or `CE 2`)\n\n"
            f"Or type *skip* if you don't have CIDB grading."
        )


async def lookup_cidb_register(company_name: str) -> List[Dict[str, Any]]:
    """Lookup company in CIDB register.
    In production, this queries the CIDB Public Contractors API.
    For now, returns mock data based on our seed.
    """
    # Import our CIDB seed data
    from ..cidb_directory import _SEED_ROWS
    
    matches = []
    name_lower = company_name.lower()
    
    for row in _SEED_ROWS:
        contractor_name = row.get("Contractor Name", "").lower()
        if name_lower in contractor_name or contractor_name in name_lower:
            grading_raw = row.get("Grading", "")
            matches.append({
                "name": row.get("Contractor Name", ""),
                "crs": row.get("CRS Number", ""),
                "grading": grading_raw,
                "status": row.get("Status", ""),
            })
    
    return matches


# ---------------------------------------------------------------------------
# Step 2: CIDB Confirmation
# ---------------------------------------------------------------------------

async def handle_cidb_lookup(user: WhatsAppUser, body: str, message_sid: str) -> str:
    """Handle CIDB lookup response (step transition)."""
    # This step is handled in handle_company_name
    return await handle_cidb_confirm(user, body, message_sid)


async def handle_cidb_confirm(user: WhatsAppUser, body: str, message_sid: str) -> str:
    """Handle CIDB match selection or manual entry."""
    body_clean = body.strip().lower()
    cidb_matches = user.onboarding_data.get("cidb_matches", [])
    
    # User selected a match by number
    if body_clean.isdigit():
        idx = int(body_clean) - 1
        if 0 <= idx < len(cidb_matches):
            selected = cidb_matches[idx]
            user.onboarding_data["selected_cidb"] = selected
            user.onboarding_data["cidb_gradings"] = parse_cidb_grading(selected["grading"])
            user.onboarding_step = OnboardingStep.DOCUMENT_UPLOAD
            upsert_user(user)
            return await prompt_document_upload(user)
    
    # User entered manual grading (e.g., "GB 3")
    manual_match = re.match(r"^([A-Z]{2})\s*(\d)$", body_clean.upper())
    if manual_match:
        class_code, level = manual_match.groups()
        if class_code in CIDB_CLASSES and 1 <= int(level) <= 9:
            user.onboarding_data["cidb_gradings"] = [
                {"class_code": class_code, "level": int(level)}
            ]
            user.onboarding_step = OnboardingStep.DOCUMENT_UPLOAD
            upsert_user(user)
            return await prompt_document_upload(user)
    
    # Skip CIDB
    if body_clean in ("skip", "no", "none"):
        user.onboarding_data["cidb_gradings"] = []
        user.onboarding_step = OnboardingStep.DOCUMENT_UPLOAD
        upsert_user(user)
        return await prompt_document_upload(user)
    
    # Invalid input
    matches_text = "\n".join([
        f"{i+1}. {m['name']} — {m['grading']}"
        for i, m in enumerate(cidb_matches[:5])
    ])
    
    return (
        f"Please reply with a *number* (1-{len(cidb_matches)}),\n"
        f"enter manually as `CLASS LEVEL` (e.g., `GB 3`),\n"
        f"or type *skip*.\n\n"
        f"{matches_text}"
    )


def parse_cidb_grading(grading_str: str) -> List[Dict[str, Any]]:
    """Parse CIDB grading string like '8CE PE' or '5CE'."""
    import re
    gradings = []
    # Pattern: number followed by 2-letter class code
    matches = re.findall(r"(\d)\s*([A-Z]{2})", grading_str.upper())
    for level_str, class_code in matches:
        if class_code != "PE" and class_code in CIDB_CLASSES:
            gradings.append({
                "class_code": class_code,
                "level": int(level_str),
            })
    return gradings


# ---------------------------------------------------------------------------
# Step 3: Document Upload
# ---------------------------------------------------------------------------

async def prompt_document_upload(user: WhatsAppUser) -> str:
    """Prompt user to upload required documents."""
    docs_status = user.onboarding_data.get("documents_uploaded", {})
    
    required_docs = [
        (DocumentType.CSD_LETTER, "CSD Registration Letter"),
        (DocumentType.BBBEE_CERT, "B-BBEE Certificate / Sworn Affidavit"),
        (DocumentType.TAX_PIN, "SARS Tax Compliance PIN"),
        (DocumentType.CIDB_CERT, "CIDB Grading Certificate"),
    ]
    
    status_lines = []
    for doc_type, label in required_docs:
        status = "✅" if docs_status.get(doc_type.value) else "⬜"
        status_lines.append(f"{status} {label}")
    
    return (
        f"📄 *Step 3: Document Upload*\n\n"
        f"Please upload the following documents (PDF or photo):\n\n"
        f"{chr(10).join(status_lines)}\n\n"
        f"Send each document as a separate message.\n"
        f"I'll extract the details automatically using AI.\n\n"
        f"Type *done* when finished, or *skip* to continue."
    )


async def handle_document_upload_step(user: WhatsAppUser, body: str, message_sid: str) -> str:
    """Handle document upload step commands."""
    body_clean = body.strip().lower()
    
    if body_clean == "done":
        user.onboarding_step = OnboardingStep.SECTOR_PROVINCE
        upsert_user(user)
        return await prompt_sector_province(user)
    
    if body_clean == "skip":
        user.onboarding_step = OnboardingStep.SECTOR_PROVINCE
        upsert_user(user)
        return await prompt_sector_province(user)
    
    # If they sent text instead of media, remind them
    return (
        "Please *upload a document* (PDF or photo) from your phone.\n\n"
        "Or type *done* when finished, *skip* to continue."
    )


async def handle_media_document_upload(
    user: WhatsAppUser,
    media_msg,
    parsed_data: Dict[str, Any],
) -> str:
    """Process uploaded document and update onboarding data."""
    # Classify document
    doc_type = classify_document_by_content(parsed_data)
    
    # Store in onboarding data
    if "documents_uploaded" not in user.onboarding_data:
        user.onboarding_data["documents_uploaded"] = {}
    
    user.onboarding_data["documents_uploaded"][doc_type.value] = {
        "parsed": parsed_data,
        "media_sid": media_msg.message_sid,
        "supabase_path": media_msg.supabase_path,
        "uploaded_at": datetime.utcnow().isoformat(),
    }
    
    # Update user verification status
    if doc_type == DocumentType.CSD_LETTER:
        user.csd_status = "verified"
        csd_num = parsed_data.get("csd_number") or parsed_data.get("supplier_number")
        if csd_num:
            user.onboarding_data["csd_number"] = csd_num
    
    elif doc_type == DocumentType.BBBEE_CERT:
        user.bbbee_status = "verified"
        bbbee_level = parsed_data.get("bbbee_level")
        if bbbee_level:
            user.onboarding_data["bbbee_level"] = bbbee_level
    
    elif doc_type == DocumentType.TAX_PIN:
        user.tax_status = "verified"
    
    elif doc_type == DocumentType.CIDB_CERT:
        user.cidb_status = "verified"
        cidb_gradings = parsed_data.get("cidb_gradings", [])
        if cidb_gradings:
            user.onboarding_data["cidb_gradings"] = cidb_gradings
    
    upsert_user(user)
    
    # Show updated status
    return await prompt_document_upload(user)


# ---------------------------------------------------------------------------
# Step 4: Sector & Province
# ---------------------------------------------------------------------------

async def prompt_sector_province(user: WhatsAppUser) -> str:
    """Prompt for sector and province selection."""
    # Get sectors from CIDB gradings
    cidb_sectors = []
    for g in user.onboarding_data.get("cidb_gradings", []):
        class_name = CIDB_CLASSES.get(g.get("class_code", ""), g.get("class_code", ""))
        if class_name not in cidb_sectors:
            cidb_sectors.append(class_name)
    
    provinces = [
        "Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape",
        "Free State", "Limpopo", "Mpumalanga", "Northern Cape", "North West",
        "National"
    ]
    
    return (
        f"🏢 *Step 4: Sectors & Province*\n\n"
        f"Based on your CIDB grading(s), suggested sectors:\n"
        f"{', '.join(cidb_sectors) if cidb_sectors else 'None detected'}\n\n"
        f"Reply with your sectors (comma-separated) or type *auto* to use suggested.\n\n"
        f"Then I'll ask for your province."
    )


async def handle_sector_province(user: WhatsAppUser, body: str, message_sid: str) -> str:
    """Handle sector and province input."""
    body_clean = body.strip()
    
    # Check if we're waiting for province
    if "awaiting_province" in user.onboarding_data:
        province = body_clean
        if province in [
            "Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape",
            "Free State", "Limpopo", "Mpumalanga", "Northern Cape", "North West",
            "National"
        ]:
            user.province = province
            user.onboarding_data.pop("awaiting_province", None)
            user.onboarding_step = OnboardingStep.POPIA_CONSENT
            upsert_user(user)
            return await prompt_popia_consent(user)
        else:
            return "Please enter a valid South African province (e.g., Gauteng, Western Cape)."
    
    # Handle sectors
    if body_clean.lower() == "auto":
        cidb_sectors = []
        for g in user.onboarding_data.get("cidb_gradings", []):
            class_name = CIDB_CLASSES.get(g.get("class_code", ""), g.get("class_code", ""))
            if class_name not in cidb_sectors:
                cidb_sectors.append(class_name)
        user.sectors = cidb_sectors
    else:
        user.sectors = [s.strip() for s in body_clean.split(",") if s.strip()]
    
    upsert_user(user)
    user.onboarding_data["awaiting_province"] = True
    upsert_user(user)
    
    return (
        f"✅ Sectors saved: {', '.join(user.sectors)}\n\n"
        f"Now, which *province* is your company based in?\n"
        f"(e.g., Gauteng, Western Cape, KwaZulu-Natal, or National)"
    )


# ---------------------------------------------------------------------------
# Step 5: POPIA Consent
# ---------------------------------------------------------------------------

async def prompt_popia_consent(user: WhatsAppUser) -> str:
    """Prompt for POPIA consent."""
    return (
        f"🔒 *Step 5: POPIA Consent*\n\n"
        f"To receive matched tenders and compliance reports via WhatsApp, "
        f"I need your consent to process your personal and company information "
        f"under the Protection of Personal Information Act (POPIA).\n\n"
        f"*What I'll do with your data:*\n"
        f"• Match your profile against government tenders\n"
        f"• Send you daily tender matches via WhatsApp\n"
        f"• Generate compliance reports for eligible tenders\n"
        f"• Store your documents securely (encrypted)\n\n"
        f"*Your rights:*\n"
        f"• Access your data anytime (*profile*)\n"
        f"• Update or delete your data (*onboard* to update, *stop* to delete)\n"
        f"• Opt out of marketing while keeping matching (*digest off*)\n\n"
        f"Reply *yes* to consent, or *no* to decline."
    )


async def handle_popia_consent(user: WhatsAppUser, body: str, message_sid: str) -> str:
    """Handle POPIA consent response."""
    body_clean = body.strip().lower()
    
    if body_clean in ("yes", "y", "consent", "agree", "accept"):
        user.popia_consent = True
        user.popia_consent_at = datetime.utcnow()
        user.popia_consent_version = "1.0"
        user.marketing_opt_in = True
        user.onboarding_step = OnboardingStep.COMPLETE
        user.onboarding_completed_at = datetime.utcnow()
        upsert_user(user)
        
        return await complete_onboarding(user)
    
    elif body_clean in ("no", "n", "decline", "reject"):
        return (
            "❌ Consent declined. You can still use the service manually, "
            "but I won't be able to send you automated tender matches.\n\n"
            "Type *menu* for options, or *onboard* to try again later."
        )
    
    else:
        return "Please reply *yes* to consent or *no* to decline."


async def complete_onboarding(user: WhatsAppUser) -> str:
    """Complete onboarding and create CompanyProfile in core system."""
    # Create core CompanyProfile
    from ..schemas import CompanyProfile, CIDBGrading, Location
    
    cidb_gradings = []
    for g in user.onboarding_data.get("cidb_gradings", []):
        cidb_gradings.append(CIDBGrading(
            class_code=g.get("class_code", ""),
            level=g.get("level", 1),
        ))
    
    profile = CompanyProfile(
        registration_number=user.registration_number or f"WA-{user.phone_number}",
        company_name=user.onboarding_data.get("company_name", ""),
        csd_number=user.onboarding_data.get("csd_number"),
        bbbee_level=user.onboarding_data.get("bbbee_level", 9),
        cidb_gradings=cidb_gradings,
        location=Location(
            province=user.province or "Gauteng",
            city="Unknown",
        ),
        sectors=user.sectors,
        has_tax_pin=user.tax_status == "verified",
    )
    
    # Save to core database
    from ..database import get_database_client
    db = get_database_client()
    if hasattr(db, "connect"):
        db.connect()
    db.upsert_company(profile)
    if hasattr(db, "close"):
        db.close()
    
    # Clear onboarding data
    user.onboarding_data = {}
    upsert_user(user)
    
    return (
        f"🎉 *Onboarding Complete!*\n\n"
        f"Welcome, {profile.company_name}!\n\n"
        f"✅ Profile saved\n"
        f"✅ CIDB grading(s): {', '.join([f'{g.class_code}{g.level}' for g in cidb_gradings]) or 'None'}\n"
        f"✅ Province: {user.province}\n"
        f"✅ Sectors: {', '.join(user.sectors) or 'None'}\n\n"
        f"You'll now receive daily tender matches at 07:00.\n\n"
        f"Type *tenders* to see current matches.\n"
        f"Type *profile* to view your verification status.\n"
        f"Type *menu* for all commands."
    )


def classify_document_by_content(parsed_data: Dict[str, Any]):
    """Classify document type based on parsed content."""
    from .models import DocumentType
    
    if any(k in parsed_data for k in ["csd_number", "supplier_number", "maaa_number"]):
        return DocumentType.CSD_LETTER
    if any(k in parsed_data for k in ["bbbee_level", "bbbee_status", "bee_level"]):
        return DocumentType.BBBEE_CERT
    if any(k in parsed_data for k in ["tax_pin", "pin_number", "sars_pin"]):
        return DocumentType.TAX_PIN
    if any(k in parsed_data for k in ["cidb_grading", "cidb_number", "grading_level", "cidb_gradings"]):
        return DocumentType.CIDB_CERT
    if any(k in parsed_data for k in ["registration_number", "cipc_number", "company_number"]):
        return DocumentType.CIPC_CERT
    return DocumentType.OTHER