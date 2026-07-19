from datetime import datetime, timedelta, timezone
from tender_getter.agents.feedback import interpret_feedback
from tender_getter.agents.policy import Action, decide_opportunity
from tender_getter.billing.models import PlanCode
from tender_getter.billing.service import BillingService
from tender_getter.schemas import CompanyProfile, Location, TenderOpportunity
from tender_getter.matcher import match

def tender(doc=True):
    return TenderOpportunity(tender_id="A/1", title="Electrical works", issuing_entity="State", closing_date=datetime.now(timezone.utc)+timedelta(days=7), mandatory_csd=False, tax_compliance_required=False, raw_document_url="https://example.test/bid.pdf" if doc else None)

def company():
    return CompanyProfile(registration_number="2026/1/07", company_name="Example", location=Location(province="Gauteng", city="Johannesburg"))

def test_agent_alerts_only_when_evidence_is_sufficient():
    t=tender(); result=match(company(), t)
    decision=decide_opportunity(t, result, source_verified=True, enrichment_confidence=.9)
    assert decision.action == Action.ALERT
    assert decision.confidence >= .8

def test_agent_enriches_instead_of_claiming_eligibility_without_document():
    t=tender(doc=False); result=match(company(), t)
    assert decide_opportunity(t, result, source_verified=True).action == Action.ENRICH

def test_natural_language_feedback_requires_no_button():
    assert interpret_feedback("This is relevant, please prepare the bid pack").intent == "bid_craft"
    assert interpret_feedback("Please do not send work like this again").sentiment == "negative"

def test_all_commercial_plans_are_paid_codes():
    assert {p.value for p in PlanCode} == {"starter", "pro", "vip"}
    assert BillingService().entitlement({"plan_code":"vip", "status":"beta"}).bid_craft

def test_agent_never_alerts_an_expired_tender():
    t = tender(); t.closing_date = datetime.now(timezone.utc)-timedelta(minutes=1)
    assert decide_opportunity(t, match(company(), t), source_verified=True, enrichment_confidence=.99).action == Action.SUPPRESS

def test_feedback_redacts_supplier_and_tax_identifiers_before_persistence(monkeypatch):
    from tender_getter.agents.store import AgentStore
    captured = {}
    class Table:
        def insert(self, row): captured.update(row); return self
        def execute(self): return None
    class Client:
        def table(self, _): return Table()
    store = AgentStore(); store._client = Client()
    store.record_feedback("+27123456789", "My CSD is MAAA123456 and tax pin: ABCD123456")
    assert "MAAA123456" not in captured["raw_text"]
    assert "ABCD123456" not in captured["raw_text"]


def test_distributed_inbound_guard_has_development_fallback(monkeypatch):
    from tender_getter.whatsapp import database
    monkeypatch.setattr(database, "_use_supabase", False)
    assert database.claim_inbound_message("sid-security-test", "+27123456789", "text")
    assert not database.claim_inbound_message("sid-security-test", "+27123456789", "text")

def test_expired_beta_has_no_entitlements():
    expired = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()
    assert not BillingService().entitlement({"plan_code":"vip", "status":"beta", "beta_expires_at": expired}).active

def test_expiry_requires_the_correct_status_timestamp():
    future = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    assert BillingService().entitlement({"plan_code":"vip", "status":"trial", "trial_expires_at":future}).bid_craft
