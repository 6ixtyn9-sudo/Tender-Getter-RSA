"""VIP Bid-Craft agent: structured, evidence-bound proposal drafting."""
from __future__ import annotations
from ..ai.gateway import AIGateway
from ..schemas import CompanyProfile, TenderOpportunity

BID_CRAFT_RULES = """You draft a South African tender response from tender facts and company facts.
Never invent experience, personnel, certificates, pricing, partnerships or compliance.
Label missing evidence as CUSTOMER ACTION REQUIRED. Output: executive summary, compliance matrix,
methodology, assumptions/exclusions, clarification questions, and a submission checklist."""

async def draft_bid_pack(gateway: AIGateway, company: CompanyProfile, tender: TenderOpportunity, extracted_requirements: str) -> dict:
    payload = {"company": company.model_dump(mode="json"), "tender": tender.model_dump(mode="json"), "requirements": extracted_requirements}
    return await gateway.generate(BID_CRAFT_RULES, [{"role": "user", "content": str(payload)}], temperature=.2)
