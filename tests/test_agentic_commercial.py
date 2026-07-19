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
