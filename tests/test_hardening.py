"""Regression tests for production hardening changes."""
from datetime import datetime, timezone
from pathlib import Path

from tender_getter.matcher import match
from tender_getter.pdf_reports import generate_report_pdf
from tender_getter.schemas import CompanyProfile, Location, TenderOpportunity
from tender_getter.whatsapp.webhook import validate_twilio_request


def test_core_facade_uses_canonical_matcher():
    from tender_getter.core.matcher import match as compatibility_match
    assert compatibility_match is match


def test_unsigned_webhooks_fail_closed_without_local_override(monkeypatch):
    import tender_getter.whatsapp.webhook as webhook
    monkeypatch.setattr(webhook, "validator", None)
    monkeypatch.setattr(webhook, "ENV", "production")
    monkeypatch.delenv("TG_ALLOW_INSECURE_WEBHOOK", raising=False)
    assert webhook.validate_twilio_request(type("R", (), {"url": "https://example.test"})(), {}) is False


def test_pdf_report_is_rendered(tmp_path: Path):
    company = CompanyProfile(registration_number="2020/1/07", company_name="Example CC", location=Location(province="Gauteng", city="Johannesburg"))
    tender = TenderOpportunity(tender_id="TEST/1", title="Test tender", issuing_entity="Issuer", closing_date=datetime(2026, 12, 1, tzinfo=timezone.utc), mandatory_csd=False, tax_compliance_required=False)
    result = match(company, tender)
    pdf = generate_report_pdf(company, tender, result, tmp_path)
    assert pdf.suffix == ".pdf"
    assert pdf.read_bytes().startswith(b"%PDF")
