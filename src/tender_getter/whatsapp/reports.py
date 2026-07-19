"""Generate, store and send a tender report as WhatsApp media."""
from __future__ import annotations
from ..pdf_reports import generate_report_pdf
from ..schemas import CompanyProfile, MatchResult, TenderOpportunity
from .media import get_media_url, upload_to_supabase
from .outbound import send_media_message

async def deliver_report(user_phone: str, company: CompanyProfile, tender: TenderOpportunity, result: MatchResult) -> str:
    """Returns Twilio SID after generating a PDF and obtaining a signed storage URL."""
    pdf_path = generate_report_pdf(company, tender, result)
    storage_path = await upload_to_supabase(pdf_path.read_bytes(), "application/pdf", user_phone)
    url = await get_media_url(storage_path)
    return send_media_message(user_phone, url, f"Tender Getter compliance report: {tender.tender_id}")
