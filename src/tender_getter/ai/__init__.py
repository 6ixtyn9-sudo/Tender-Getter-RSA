"""
Tender Getter AI Module — Natural language intelligence for WhatsApp (SMME owner only).
"""

from .gateway import AIGateway, get_gateway, GatewayConfig
from .prompts.system_prompt import SYSTEM_PROMPT, VERIFIED_FACTS, HARD_RULES, PERSONALITY
from .intent_classifier import (
    IntentRouter, ClassifiedIntent, Intent,
    extract_entities, extract_tender_id,
    is_greeting, is_stop_command, classify_intent,
)
from .integration import AIMessageHandler, get_ai_handler

__all__ = [
    "AIGateway", "get_gateway", "GatewayConfig",
    "SYSTEM_PROMPT", "VERIFIED_FACTS", "HARD_RULES", "PERSONALITY",
    "IntentRouter", "ClassifiedIntent", "Intent",
    "extract_entities", "extract_tender_id",
    "is_greeting", "is_stop_command", "classify_intent",
    "AIMessageHandler", "get_ai_handler",
]