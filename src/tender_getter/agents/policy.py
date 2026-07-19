"""Conservative autonomous policy for tender delivery.

The policy is deterministic and auditable. Gemini may enrich facts, but cannot
bypass hard compliance gates or turn unknown facts into verified facts.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any
from ..schemas import MatchResult, TenderOpportunity

class Action(str, Enum):
    ALERT = "alert"
    SUPPRESS = "suppress"
    ENRICH = "enrich"
    RETRY = "retry"

@dataclass(frozen=True)
class OpportunityDecision:
    action: Action
    confidence: float
    reason: str
    evidence: dict[str, Any]

def decide_opportunity(tender: TenderOpportunity, result: MatchResult, *, source_verified: bool, enrichment_confidence: float = 0.0) -> OpportunityDecision:
    evidence = {"source_verified": source_verified, "has_document": bool(tender.raw_document_url), "enrichment_confidence": enrichment_confidence, "eligible": result.is_eligible, "score": result.match_score}
    if not source_verified:
        return OpportunityDecision(Action.RETRY, 0.0, "Source provenance is not verified.", evidence)
    if not result.is_eligible:
        return OpportunityDecision(Action.SUPPRESS, 1.0, result.disqualification_reason or "Hard eligibility gate failed.", evidence)
    if not tender.raw_document_url:
        return OpportunityDecision(Action.ENRICH, 0.55, "Eligible on recorded facts; tender document is still required.", evidence)
    confidence = min(0.98, 0.72 + (0.20 * max(0.0, min(1.0, enrichment_confidence))) + (0.06 if result.match_score >= 90 else 0.0))
    if confidence < 0.80:
        return OpportunityDecision(Action.ENRICH, confidence, "More document evidence is required before a qualified alert.", evidence)
    return OpportunityDecision(Action.ALERT, confidence, "Verified source, open document and hard gates passed on recorded facts.", evidence)
