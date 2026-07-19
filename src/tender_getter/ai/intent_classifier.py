"""
Tender Getter Intent Classifier — Natural language → structured actions.
Ports the conversational intelligence from Operation PAWS.

Maps user messages to:
- Intent (what they want)
- Entities (tender IDs, document types, etc.)
- Confidence score
- Suggested quick replies
"""

import re
from dataclasses import dataclass
from typing import Any, Optional
from enum import Enum


class Intent(str, Enum):
    # Core tender actions
    SHOW_TENDERS = "show_tenders"
    SHOW_TENDER_DETAIL = "show_tender_detail"
    FILTER_TENDERS = "filter_tenders"

    # Profile & verification
    SHOW_PROFILE = "show_profile"
    VERIFY_DOCUMENT = "verify_document"
    UPLOAD_DOCUMENT = "upload_document"

    # Onboarding
    START_ONBOARDING = "start_onboarding"
    ONBOARDING_STEP = "onboarding_step"

    # Settings
    TOGGLE_DIGEST = "toggle_digest"
    UPDATE_PREFERENCES = "update_preferences"

    # Help & meta
    HELP = "help"
    STOP = "stop"
    GREETING = "greeting"
    THANKS = "thanks"
    COMPLAINT = "complaint"
    FEEDBACK = "feedback"

    # Info / educational
    EXPLAIN_GATE = "explain_gate"
    EXPLAIN_SCORING = "explain_scoring"
    EXPLAIN_CIDB = "explain_cidb"
    EXPLAIN_BBBEE = "explain_bbbee"
    EXPLAIN_CSD = "explain_csd"

    # Company actions
    COMPANY_LOOKUP = "company_lookup"
    MATCH_COMPANY = "match_company"
    UPGRADE_PLAN = "upgrade_plan"
    MANAGE_BILLING = "manage_billing"
    BID_CRAFT = "bid_craft"

    # Unknown
    UNKNOWN = "unknown"


@dataclass
class ClassifiedIntent:
    intent: Intent
    confidence: float  # 0.0 - 1.0
    entities: dict[str, Any]
    quick_replies: list[str]
    original_text: str
    suggested_action: Optional[str] = None


# ─────────────────────────────────────────────────────────────────────────────
# Keyword Patterns (SA English variations)
# ─────────────────────────────────────────────────────────────────────────────

INTENT_KEYWORDS = {
    Intent.SHOW_TENDERS: [
        "tender", "tenders", "match", "matches", "opportunit", "bid", "bids",
        "work", "jobs", "contracts", "available", "what.*work", "what.*tender",
        "show.*tender", "list.*tender", "my tender", "any.*tender",
        "new tender", "latest tender", "open tender",
    ],
    Intent.SHOW_TENDER_DETAIL: [
        "detail", "details", "more info", "tell me about", "about.*tender",
        "tender.*info", "full.*tender",
    ],
    Intent.FILTER_TENDERS: [
        "filter", "only", "just", "province", "sector", "value", "cidb",
        "under.*rand", "over.*rand", "above.*rand", "below.*rand",
        "this week", "this month", "closing soon", "urgent",
    ],
    Intent.SHOW_PROFILE: [
        "profile", "my info", "my details", "verification", "status",
        "my verification", "verified", "my company", "account",
    ],
    Intent.VERIFY_DOCUMENT: [
        "verify", "verification", "check.*doc", "validate", "confirm.*doc",
        "csd.*verify", "tax.*verify", "bbbee.*verify", "cidb.*verify",
    ],
    Intent.UPLOAD_DOCUMENT: [
        "upload", "send.*doc", "attach", "add.*doc", "submit.*doc",
        "here.*doc", "doc.*here",
    ],
    Intent.START_ONBOARDING: [
        "onboard", "register", "sign up", "start", "setup", "get started",
        "join", "create.*profile", "new.*user",
    ],
    Intent.ONBOARDING_STEP: [
        # Handled in onboarding flow context
    ],
    Intent.TOGGLE_DIGEST: [
        "digest", "daily", "morning", "notification", "alert", "notify",
        "stop.*digest", "pause.*digest", "enable.*digest", "disable.*digest",
        "digest on", "digest off",
    ],
    Intent.UPDATE_PREFERENCES: [
        "prefer", "setting", "change.*province", "change.*sector",
        "update.*profile", "edit.*profile",
    ],
    Intent.HELP: [
        "help", "menu", "command", "what can", "how.*work", "how.*use",
        "instruction", "guide", "tutorial",
    ],
    Intent.STOP: [
        "stop", "unsubscribe", "opt out", "opt-out", "leave", "quit",
        "cancel", "remove me", "delete.*account", "popia",
    ],
    Intent.GREETING: [
        "hi", "hello", "hey", "good morning", "good afternoon", "good evening",
        "morning", "afternoon", "evening", "howdy", "yebo", "molo", "dumela",
    ],
    Intent.THANKS: [
        "thank", "thanks", "thx", "ta", "appreciate", "cheers", "dankie",
        "enkosi", "ngiyabonga", "ke a leboga",
    ],
    Intent.COMPLAINT: [
        "wrong", "incorrect", "broken", "bug", "error", "problem", "issue",
        "not working", "doesn't work", "failed", "useless", "waste",
    ],
    Intent.FEEDBACK: [
        "feedback", "suggest", "improve", "feature", "idea", "request",
        "would be nice", "should add", "wish",
    ],
    Intent.EXPLAIN_GATE: [
        "why.*disqualif", "why.*block", "why.*reject", "gate", "disqualif",
        "cidb.*gate", "csd.*gate", "tax.*gate", "bbbee.*gate", "geo.*gate",
        "why.*not.*match", "why.*fail",
    ],
    Intent.EXPLAIN_SCORING: [
        "score", "scoring", "match.*score", "percentage", "percent",
        "how.*calculate", "how.*score", "points", "bbbee.*point",
    ],
    Intent.EXPLAIN_CIDB: [
        "cidb", "grading", "grade", "class", "ce", "gb", "ee", "me",
        "level.*1", "level.*2", "level.*3", "level.*4", "level.*5",
        "level.*6", "level.*7", "level.*8", "level.*9",
        "financial.*cap", "capacity",
    ],
    Intent.EXPLAIN_BBBEE: [
        "bbbee", "b-bee", "bee", "preference", "point", "level.*1", "level.*2",
        "80/20", "90/10", "ownership", "black.*own", "women.*own", "youth.*own",
    ],
    Intent.EXPLAIN_CSD: [
        "csd", "central supplier", "maaa", "supplier number", "registration",
    ],
    Intent.COMPANY_LOOKUP: [
        "lookup", "search.*company", "find.*company", "cidb.*lookup",
        "who.*cidb", "contractor.*search",
    ],
    Intent.MATCH_COMPANY: [
        "match.*company", "run.*match", "refresh.*match", "re-match",
        "check.*match", "scan.*tender",
    ],
    Intent.UPGRADE_PLAN: ["upgrade", "subscribe", "subscription", "price", "pricing", "plan", "pay monthly", "pay yearly", "annual"],
    Intent.MANAGE_BILLING: ["invoice", "billing", "debit order", "debit-order", "cancel subscription", "payment failed", "payment method"],
    Intent.BID_CRAFT: ["proposal", "bid pack", "draft bid", "prepare bid", "methodology", "executive summary"],
}

# Quick reply suggestions per intent
QUICK_REPLIES = {
    Intent.SHOW_TENDERS: ["📋 Show my tenders", "🔍 Filter by province", "💰 Filter by value", "⚙️ Settings"],
    Intent.SHOW_PROFILE: ["📄 Verify CSD", "📄 Verify Tax PIN", "📄 Verify B-BBEE", "📄 Verify CIDB", "⚙️ Settings"],
    Intent.VERIFY_DOCUMENT: ["📄 Upload CSD letter", "📄 Upload Tax PIN", "📄 Upload B-BBEE", "📄 Upload CIDB cert"],
    Intent.START_ONBOARDING: ["🚀 Start onboarding", "❓ How it works", "📖 Read first"],
    Intent.TOGGLE_DIGEST: ["☀️ Enable daily digest", "🌙 Disable digest", "⏰ Change time", "⚙️ Settings"],
    Intent.HELP: ["📋 Show tenders", "👤 My profile", "🚀 Onboard", "⚙️ Settings", "❌ Stop"],
    Intent.EXPLAIN_GATE: ["📖 Explain CIDB gate", "📖 Explain CSD gate", "📖 Explain Tax gate", "📖 Explain B-BBEE gate"],
    Intent.EXPLAIN_SCORING: ["📖 How scoring works", "📖 B-BBEE points", "📖 Match % meaning"],
    Intent.UPGRADE_PLAN: ["Upgrade", "Monthly plan", "Annual plan", "VIP Bid-Craft"],
    Intent.BID_CRAFT: ["Prepare a bid pack", "Draft methodology", "Show plans"],
    Intent.UNKNOWN: ["📋 Show tenders", "👤 My profile", "❓ Help", "⚙️ Settings"],
}


# ─────────────────────────────────────────────────────────────────────────────
# Entity Extraction
# ─────────────────────────────────────────────────────────────────────────────

# Tender ID patterns (South African formats)
TENDER_ID_PATTERNS = [
    r"\b([A-Z]{2,4}[-/]\d{2,4}[-/]\d{3,5})\b",  # COJ/EE/2026/012
    r"\b([A-Z]{3,6}[-/]\d{4,6})\b",              # ERRUTAM 25
    r"\b(RFQ|RFP|ITQ|EOI)[-/ ]\d{4,6}\b",        # RFQ0001247
    r"\b(CSIR|DSBD|CHIETA|AGRISETA|SARS|DFFE)[-/ ]\w+\b",
]

# Document type patterns
DOC_TYPE_PATTERNS = {
    "csd_letter": [r"csd.*letter", r"csd.*cert", r"maaa.*letter", r"supplier.*letter"],
    "tax_pin": [r"tax.*pin", r"sars.*pin", r"tax.*compliance", r"pin.*cert"],
    "bbbee_cert": [r"bbbee.*cert", r"bee.*cert", r"b.*bee.*cert", r"sworn.*affidavit", r"affidavit"],
    "cidb_cert": [r"cidb.*cert", r"cidb.*grading", r"grading.*cert", r"crs.*cert"],
    "cipc_cert": [r"cipc.*cert", r"cipc.*reg", r"company.*reg", r"registration.*cert"],
}

# Province patterns
PROVINCE_PATTERNS = [
    "gauteng", "western cape", "kwazulu-natal", "kzn", "eastern cape",
    "free state", "limpopo", "mpumalanga", "northern cape", "north west",
    "national",
]

# CIDB class patterns
CIDB_CLASS_PATTERNS = [
    r"\b(GB|CE|EE|ME|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SQ|SP)\b",
]

# CIDB level patterns
CIDB_LEVEL_PATTERNS = [
    r"\b([1-9])\s*(?:GB|CE|EE|ME|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SQ|SP)\b",
    r"\b(?:GB|CE|EE|ME|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SQ|SP)\s*([1-9])\b",
]


def extract_entities(text: str) -> dict[str, Any]:
    """Extract structured entities from user text."""
    entities = {}
    text_lower = text.lower()

    # Tender IDs
    tender_ids = []
    for pattern in TENDER_ID_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        tender_ids.extend(matches)
    if tender_ids:
        entities["tender_ids"] = list(set(tender_ids))

    # Document types
    doc_types = []
    for doc_type, patterns in DOC_TYPE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                doc_types.append(doc_type)
                break
    if doc_types:
        entities["document_types"] = doc_types

    # Provinces
    provinces = [p for p in PROVINCE_PATTERNS if p in text_lower]
    if provinces:
        entities["provinces"] = provinces

    # CIDB classes
    cidb_classes = re.findall(r"\b(GB|CE|EE|ME|SB|SC|SD|SE|SF|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SQ|SP)\b", text.upper())
    if cidb_classes:
        entities["cidb_classes"] = list(set(cidb_classes))

    # CIDB levels (e.g., "GB 3" or "3GB")
    cidb_grades = []
    for pattern in CIDB_LEVEL_PATTERNS:
        matches = re.findall(pattern, text.upper())
        for match in matches:
            if isinstance(match, tuple):
                cidb_grades.append(match)
            else:
                cidb_grades.append(match)
    if cidb_grades:
        entities["cidb_grades"] = cidb_grades

    # Monetary values (R1.5M, R500k, etc.)
    money_matches = re.findall(r"R\s*(\d+(?:\.\d+)?)\s*([kmKM]?)", text)
    if money_matches:
        entities["monetary_values"] = [
            {"amount": float(m[0]), "unit": m[1].upper() if m[1] else ""}
            for m in money_matches
        ]

    return entities


# ─────────────────────────────────────────────────────────────────────────────
# Intent Classification
# ─────────────────────────────────────────────────────────────────────────────

def classify_intent(text: str, context: Optional[dict] = None) -> ClassifiedIntent:
    """
    Classify user intent from natural language text.

    Args:
        text: User's message
        context: Optional conversation context (e.g., {"onboarding_step": "company_name"})

    Returns:
        ClassifiedIntent with intent, confidence, entities, quick_replies
    """
    text_lower = text.strip().lower()
    context = context or {}

    # Handle onboarding flow context first
    if context.get("onboarding_step"):
        return ClassifiedIntent(
            intent=Intent.ONBOARDING_STEP,
            confidence=0.95,
            entities=extract_entities(text),
            quick_replies=[],
            original_text=text,
            suggested_action="handle_onboarding_step",
        )

    # Handle media upload context
    if context.get("awaiting_document"):
        doc_type = context.get("awaiting_document")
        return ClassifiedIntent(
            intent=Intent.UPLOAD_DOCUMENT,
            confidence=0.9,
            entities={"document_types": [doc_type] if doc_type else [], **extract_entities(text)},
            quick_replies=[],
            original_text=text,
            suggested_action="handle_media_upload",
        )

    # Score each intent
    scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Exact word boundary match
            if re.search(rf"\b{re.escape(keyword)}\b", text_lower):
                score += 2
            # Substring match
            elif keyword in text_lower:
                score += 1
        scores[intent] = score

    # Boost based on context
    if context.get("last_intent") == Intent.VERIFY_DOCUMENT:
        scores[Intent.UPLOAD_DOCUMENT] = scores.get(Intent.UPLOAD_DOCUMENT, 0) + 3

    # Get top intent
    if not scores or max(scores.values()) == 0:
        return ClassifiedIntent(
            intent=Intent.UNKNOWN,
            confidence=0.1,
            entities=extract_entities(text),
            quick_replies=QUICK_REPLIES[Intent.UNKNOWN],
            original_text=text,
        )

    top_intent = max(scores, key=scores.get)
    max_score = scores[top_intent]

    # Normalize confidence (rough heuristic)
    confidence = min(0.95, 0.3 + (max_score * 0.1))

    return ClassifiedIntent(
        intent=top_intent,
        confidence=confidence,
        entities=extract_entities(text),
        quick_replies=QUICK_REPLIES.get(top_intent, QUICK_REPLIES[Intent.UNKNOWN]),
        original_text=text,
        suggested_action=f"handle_{top_intent.value}",
    )


# ─────────────────────────────────────────────────────────────────────────────
# High-level Intent Router (for WhatsApp webhook integration)
# ─────────────────────────────────────────────────────────────────────────────

class IntentRouter:
    """
    Routes classified intents to handler functions.
    Maintains conversation context.
    """

    def __init__(self):
        self.context: dict[str, Any] = {}

    def update_context(self, key: str, value: Any) -> None:
        self.context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        return self.context.get(key, default)

    def clear_context(self) -> None:
        self.context.clear()

    def classify_and_route(self, text: str) -> ClassifiedIntent:
        """Classify intent with current context."""
        intent = classify_intent(text, self.context)
        # Update context with this intent
        self.context["last_intent"] = intent.intent
        self.context["last_entities"] = intent.entities
        return intent


# ─────────────────────────────────────────────────────────────────────────────
# Convenience Functions
# ─────────────────────────────────────────────────────────────────────────────

def is_greeting(text: str) -> bool:
    """Quick check for greeting."""
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "morning", "yebo", "molo", "dumela"]
    return any(g in text.lower() for g in greetings)


def is_stop_command(text: str) -> bool:
    """Quick check for stop/opt-out."""
    stops = ["stop", "unsubscribe", "opt out", "opt-out", "leave", "quit", "cancel", "remove me"]
    return any(s in text.lower() for s in stops)


def extract_tender_id(text: str) -> Optional[str]:
    """Extract first tender ID from text."""
    for pattern in TENDER_ID_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None