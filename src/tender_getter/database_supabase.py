# database_supabase.py - Supabase PostgREST client for Tender Getter RSA
import os
from typing import Optional
from supabase import create_client, Client
from .database_base import TenderDatabaseBase
from .schemas import CompanyProfile, TenderOpportunity, MatchResult

class SupabaseDatabase(TenderDatabaseBase):
    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        self.url = url or os.environ.get("SUPABASE_URL")
        self.key = key or os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_ANON_KEY")
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        self.client: Optional[Client] = None
    def connect(self) -> "SupabaseDatabase":
        self.client = create_client(self.url, self.key)
        return self
    def close(self):
        self.client = None
    def __enter__(self): return self.connect()
    def __exit__(self, *a): self.close()
    def upsert_company(self, company: CompanyProfile) -> None:
        assert self.client
        payload = {
            "registration_number": company.registration_number,
            "company_name": company.company_name,
            "csd_number": company.csd_number,
            "bbbee_level": company.bbbee_level,
            "black_ownership_pct": company.black_ownership_pct,
            "youth_ownership_pct": company.youth_ownership_pct,
            "women_ownership_pct": company.women_ownership_pct,
            "province": company.location.province,
            "city": company.location.city,
            "municipality": company.location.municipality,
            "sectors": company.sectors,
            "has_tax_pin": company.has_tax_pin,
            "has_coida": company.has_coida,
            "is_active": company.is_active,
        }
        self.client.table("company_profiles").upsert(payload, on_conflict="registration_number").execute()
        self.client.table("cidb_gradings").delete().eq("registration_number", company.registration_number).execute()
        if company.cidb_gradings:
            gradings = [{"registration_number": company.registration_number, "class_code": g.class_code, "level": g.level} for g in company.cidb_gradings]
            self.client.table("cidb_gradings").insert(gradings).execute()
    def upsert_tender(self, tender: TenderOpportunity) -> None:
        assert self.client
        payload = {
            "tender_id": tender.tender_id,
            "title": tender.title,
            "issuing_entity": tender.issuing_entity,
            "closing_date": tender.closing_date.isoformat(),
            "estimated_value": tender.estimated_value,
            "required_cidb_class": tender.required_cidb_class,
            "required_cidb_level": tender.required_cidb_level,
            "mandatory_csd": tender.mandatory_csd,
            "tax_compliance_required": tender.tax_compliance_required,
            "location_target": tender.location_target,
            "raw_document_url": str(tender.raw_document_url) if tender.raw_document_url else None,
        }
        self.client.table("tenders").upsert(payload, on_conflict="tender_id").execute()
    def save_match(self, company: CompanyProfile, result: MatchResult) -> None:
        assert self.client
        payload = {
            "company_reg_number": company.registration_number,
            "tender_id": result.tender_id,
            "is_eligible": result.is_eligible,
            "match_score": result.match_score,
            "bbbee_points": result.bbbee_points,
            "bbbee_system": result.bbbee_system,
            "disqualification_reason": result.disqualification_reason,
            "feedback": result.feedback,
        }
        self.client.table("matches").upsert(payload, on_conflict="company_reg_number,tender_id").execute()
