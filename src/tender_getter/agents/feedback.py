"""Natural-language customer signal extraction; no button-only feedback required."""
from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class FeedbackSignal:
    sentiment: str
    intent: str | None
    confidence: float
    signals: dict[str, bool]

def interpret_feedback(text: str) -> FeedbackSignal:
    value = text.lower().strip()
    positive = bool(re.search(r"\b(useful|relevant|great|good|interested|bid|apply|go ahead|prepare)\b", value))
    negative = bool(re.search(r"\b(not relevant|irrelevant|wrong|already knew|spam|bad|useless|don't send|do not send)\b", value))
    bid_pack = bool(re.search(r"\b(prepare|draft|proposal|bid pack|methodology|help me bid)\b", value))
    if bid_pack: return FeedbackSignal("action_requested", "bid_craft", .88, {"bid_craft": True})
    if positive and not negative: return FeedbackSignal("positive", "relevance_positive", .72, {"relevant": True})
    if negative: return FeedbackSignal("negative", "relevance_negative", .78, {"not_relevant": True})
    return FeedbackSignal("neutral", None, .25, {})
