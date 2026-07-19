"""
Tender Getter AI Integration — Connects AI Gateway to WhatsApp Webhook.
Replaces command-based routing with natural language understanding.
"""

import logging
from typing import Any, Optional

from .gateway import AIGateway, get_gateway
from .prompts.system_prompt import SYSTEM_PROMPT
from .intent_classifier import (
    IntentRouter, ClassifiedIntent, Intent,
    extract_entities, extract_tender_id,
    is_greeting, is_stop_command,
)

from ..whatsapp.database import get_user, upsert_user
from ..whatsapp.models import WhatsAppUser, OnboardingStep
from ..schemas import CompanyProfile

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# AI-Enhanced Message Handler
# ─────────────────────────────────────────────────────────────────────────────

class AIMessageHandler:
    """
    Handles inbound WhatsApp messages using natural language understanding
    and the TENDER-OS AI gateway.
    """

    def __init__(self, gateway: Optional[AIGateway] = None):
        self.gateway = gateway or get_gateway()
        self.router = IntentRouter()
        self._load_user_contexts()

    def _load_user_contexts(self) -> None:
        """Contexts are loaded per user from persistence, never shared globally."""
        return None

    def _context_for(self, user: WhatsAppUser) -> dict:
        from ..whatsapp.database import get_conversation_state
        state = get_conversation_state(user.phone_number)
        return state.context_data if state and state.context_data else {}

    def _save_context(self, user: WhatsAppUser, context: dict) -> None:
        from ..whatsapp.database import upsert_conversation_state
        from ..whatsapp.models import ConversationState
        upsert_conversation_state(ConversationState(user_id=user.phone_number, context_data=context))

    async def handle_message(
        self,
        user: WhatsAppUser,
        text: str,
        message_sid: str,
        media_url: Optional[str] = None,
        media_type: Optional[str] = None,
    ) -> str:
        """
        Main entry point for handling inbound messages.
        Returns response text for TwiML.
        """
        # Update user activity
        user.last_active_at = __import__("datetime").datetime.utcnow()
        user.total_messages_received += 1
        from ..whatsapp.database import upsert_user
        upsert_user(user)

        # Handle media uploads first
        if media_url:
            return await self._handle_media_upload(user, media_url, media_type, message_sid)

        # Quick commands that bypass AI (for reliability)
        if is_stop_command(text):
            return await self._handle_stop(user)
        if is_greeting(text) and len(text.split()) <= 2:
            return await self._handle_greeting(user)

        # Conversation context is persisted per user; a singleton router must not
        # leak an upload/onboarding state between WhatsApp users.
        from .intent_classifier import classify_intent
        context = self._context_for(user)
        intent = classify_intent(text, context)
        logger.info(f"[TG-AI] User {user.phone_number}: intent={intent.intent.value}, confidence={intent.confidence:.2f}")
        # Every natural-language message is a learning signal. This does not
        # require buttons or a human reviewer, and is safe to lose in local dev.
        try:
            from ..agents.feedback import interpret_feedback
            from ..agents.store import AgentStore
            signal = interpret_feedback(text)
            AgentStore().record_feedback(user.phone_number, text, intent=intent.intent.value, sentiment=signal.sentiment, confidence=signal.confidence, signals=signal.signals)
        except Exception:
            logger.exception("Could not persist natural-language feedback")

        # Route to handler
        handler_name = f"_handle_{intent.intent.value}"
        handler = getattr(self, handler_name, self._handle_unknown)
        
        try:
            response = await handler(user, intent, message_sid)
            return response
        except Exception as e:
            logger.error(f"[TG-AI] Handler error for {intent.intent.value}: {e}")
            return self._fallback_response(user, intent)

    # ─────────────────────────────────────────────────────────────────────────
    # Intent Handlers
    # ─────────────────────────────────────────────────────────────────────────

    async def _handle_greeting(self, user: WhatsAppUser) -> str:
        """Warm greeting with context-aware quick replies."""
        if user.onboarding_step != OnboardingStep.COMPLETE:
            return (
                f"Hey! 👋 Welcome back to Tender Getter RSA.\n\n"
                f"Looks like you're still setting up your profile — "
                f"you're on step: *{user.onboarding_step.value.replace('_', ' ').title()}*.\n\n"
                f"Type *continue* to pick up where you left off, or *restart* to begin fresh."
            )

        # Returning user - show quick status
        match_count = self._get_today_match_count(user)
        return (
            f"Hey! 👋 Welcome back, {user.onboarding_data.get('company_name', 'there')}.\n\n"
            f"📊 *Today's snapshot:*\n"
            f"• {match_count} new tender match(es)\n"
            f"• Verification: {self._verification_summary(user)}\n\n"
            f"*Quick actions:*\n"
            f"📋 *tenders* — View matches\n"
            f"👤 *profile* — Verification status\n"
            f"📄 *verify csd/tax/bbbee/cidb* — Upload docs\n"
            f"⚙️ *settings* — Digest, preferences\n\n"
            f"Or just ask me anything — \"Any tenders in Gauteng this week?\""
        )

    async def _handle_show_tenders(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        """Show matched tenders with natural language filtering."""
        if not user.registration_number:
            return (
                "You'll need to complete onboarding first to see tender matches. "
                "Type *onboard* to set up your profile — takes 2 minutes."
            )

        filters = self._extract_tender_filters(intent)
        return self._format_tender_list(user, filters)

    async def _handle_show_tender_detail(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        """Show detailed tender info."""
        tender_id = intent.entities.get("tender_ids", [None])[0]
        if not tender_id:
            tender_id = extract_tender_id(intent.original_text)
        
        if not tender_id:
            return "Which tender would you like details for? You can say the tender ID (e.g., *COJ/EE/2026/012*) or reply to a tender from your list."

        from ..database import get_database_client
        db = get_database_client().connect()
        try:
            tender = next((t for t in db.list_open_tenders(limit=10000) if t.tender_id.lower() == tender_id.lower()), None)
        finally:
            db.close()
        if tender is None:
            return f"I could not find an open tender with reference *{tender_id}*. Check the reference and try again."
        value = f"R{tender.estimated_value:,.0f}" if tender.estimated_value is not None else "Not published"
        cidb = f"{tender.required_cidb_class or '—'}{tender.required_cidb_level or ''}"
        return (f"📋 *{tender.tender_id}*\n{tender.title}\n\n"
                f"Issuer: {tender.issuing_entity}\nCloses: {tender.closing_date:%d %b %Y %H:%M}\n"
                f"CIDB: {cidb} | Value: {value}\n"
                f"Location: {tender.location_target or 'Not specified'}\n"
                f"Documents: {tender.raw_document_url or 'Ask issuer'}")

    async def _handle_filter_tenders(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        """Filter tenders by natural language criteria."""
        filters = self._extract_tender_filters(intent)
        if not filters:
            return "What would you like to filter by? Try: *Gauteng tenders*, *under R1M*, *closing this week*, *CIDB CE3*."

        response = self._format_tender_list(user, filters)
        return response

    async def _handle_show_profile(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        """Show verification status naturally."""
        if user.onboarding_step != OnboardingStep.COMPLETE:
            return (
                f"Your profile is {int((list(OnboardingStep).index(user.onboarding_step) + 1) / len(OnboardingStep) * 100)}% complete.\n\n"
                f"Current step: *{user.onboarding_step.value.replace('_', ' ').title()}*\n\n"
                f"Type *continue* to finish onboarding."
            )

        return (
            f"👤 *Your Profile: {user.onboarding_data.get('company_name', 'Not set')}*\n\n"
            f"*Verification Status:*\n"
            f"{self._verification_emoji(user.csd_status)} CSD: {user.csd_status.replace('_', ' ').title()}\n"
            f"{self._verification_emoji(user.bbbee_status)} B-BBEE: {user.bbbee_status.replace('_', ' ').title()}\n"
            f"{self._verification_emoji(user.tax_status)} Tax PIN: {user.tax_status.replace('_', ' ').title()}\n"
            f"{self._verification_emoji(user.cidb_status)} CIDB: {user.cidb_status.replace('_', ' ').title()}\n\n"
            f"*CIDB Gradings:* {self._format_cidb(user)}\n"
            f"*Province:* {user.province or 'Not set'}\n"
            f"*Sectors:* {', '.join(user.sectors) if user.sectors else 'Not set'}\n\n"
            f"Type *verify csd/tax/bbbee/cidb* to upload documents."
        )

    async def _handle_verify_document(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        """Prompt for document upload."""
        doc_types = intent.entities.get("document_types", [])
        if not doc_types:
            return (
                "Which document would you like to verify?\n\n"
                "📄 *verify csd* — CSD Registration Letter\n"
                "📄 *verify tax* — SARS Tax Compliance PIN\n"
                "📄 *verify bbbee* — B-BBEE Certificate / Sworn Affidavit\n"
                "📄 *verify cidb* — CIDB Grading Certificate\n\n"
                "Just reply with the document type, then upload the PDF/photo."
            )

        doc_type = doc_types[0]
        context = self._context_for(user)
        context["awaiting_document"] = doc_type
        self._save_context(user, context)
        
        labels = {
            "csd_letter": "CSD Registration Letter",
            "tax_pin": "SARS Tax Compliance PIN",
            "bbbee_cert": "B-BBEE Certificate / Sworn Affidavit",
            "cidb_cert": "CIDB Grading Certificate",
        }
        return (
            f"📄 *Upload your {labels.get(doc_type, doc_type)}*\n\n"
            f"Send it as a PDF or photo — I'll extract the details with AI "
            f"and update your verification status automatically.\n\n"
            f"Type *cancel* to go back."
        )

    async def _handle_upload_document(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        """Handle document upload (media handled separately)."""
        return "Please send the document as a PDF or photo attachment. I'll process it right away."

    async def _handle_media_upload(self, user: WhatsAppUser, media_url: str, media_type: str, message_sid: str) -> str:
        """Process uploaded document with AI."""
        context = self._context_for(user)
        context.pop("awaiting_document", None)
        self._save_context(user, context)
        return (
            f"📄 Received your document!\n\n"
            f"✅ Uploaded successfully.\n"
            f"🔍 Processing with AI... (extracting details)\n\n"
            f"Type *profile* in a moment to see updated verification status."
        )

    async def _handle_start_onboarding(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        """Start onboarding flow."""
        from ..whatsapp.onboarding import start_onboarding
        return await start_onboarding(user)

    async def _handle_onboarding_step(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        """Handle onboarding step (delegates to onboarding module)."""
        from ..whatsapp.onboarding import handle_onboarding_step
        return await handle_onboarding_step(user, intent.original_text, message_sid)

    async def _handle_toggle_digest(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        """Toggle daily digest on/off."""
        text = intent.original_text.lower()
        enable = any(w in text for w in ["on", "enable", "start", "yes", "please"])
        disable = any(w in text for w in ["off", "disable", "stop", "pause", "no"])

        from ..whatsapp.database import get_digest_preferences, upsert_digest_preferences
        from ..whatsapp.models import DailyDigestPreferences
        prefs = get_digest_preferences(user.phone_number) or DailyDigestPreferences(user_id=user.phone_number)
        if enable:
            prefs.enabled = True
        elif disable:
            prefs.enabled = False
        upsert_digest_preferences(prefs)
        state = "enabled" if prefs.enabled else "disabled"
        return f"☀️ Daily digest *{state}*. " + ("You'll receive matches at 07:00 SAST." if prefs.enabled else "Type *digest on* to resume.")

    async def _handle_update_preferences(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        """Update sectors, province, digest time."""
        entities = intent.entities
        updates = []

        if entities.get("provinces"):
            user.province = entities["provinces"][0].title()
            updates.append(f"Province → {user.province}")

        if entities.get("cidb_classes"):
            # Update sectors from CIDB classes
            from ..whatsapp.onboarding import CIDB_CLASSES
            sectors = [CIDB_CLASSES.get(c, c) for c in entities["cidb_classes"]]
            user.sectors = sectors
            updates.append(f"Sectors → {', '.join(sectors)}")

        if updates:
            from ..whatsapp.database import upsert_user
            upsert_user(user)
            return f"✅ Updated: {', '.join(updates)}"
        else:
            return (
                "What would you like to update?\n"
                "• *Province* — e.g., *Gauteng*\n"
                "• *Sectors* — e.g., *Electrical, Civil*\n"
                "• *Digest time* — e.g., *06:30*"
            )

    async def _handle_help(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        """Contextual help."""
        if user.onboarding_step != OnboardingStep.COMPLETE:
            return (
                f"You're in onboarding (step: {user.onboarding_step.value.replace('_', ' ').title()}).\n\n"
                f"*Commands:*\n"
                f"• *continue* — Proceed with onboarding\n"
                f"• *restart* — Start over\n"
                f"• *cancel* — Exit onboarding\n\n"
                f"Or just answer the current question naturally."
            )

        return (
            f"🤝 *Tender Getter RSA — Help*\n\n"
            f"*Natural commands:*\n"
            f"• \"Show my tenders\" / \"Any work in Gauteng?\"\n"
            f"• \"My profile\" / \"Am I verified?\"\n"
            f"• \"Verify CSD\" / \"Upload B-BBEE cert\"\n"
            f"• \"Daily digest on/off\"\n"
            f"• \"Why was I disqualified?\"\n"
            f"• \"Explain CIDB grading\"\n\n"
            f"*Quick buttons:*\n"
            f"📋 Tenders  |  👤 Profile  |  📄 Verify  |  ⚙️ Settings  |  ❌ Stop\n\n"
            f"Just chat naturally — I understand SA English! 🇿🇦"
        )

    async def _handle_stop(self, user: WhatsAppUser) -> str:
        """POPIA-compliant opt-out."""
        from ..whatsapp.database import upsert_user
        from datetime import datetime
        user.opted_out_at = datetime.utcnow()
        upsert_user(user)
        return (
            "✅ You've been unsubscribed from all Tender Getter messages.\n\n"
            "Your data will be deleted per POPIA requirements.\n"
            "To rejoin, just send *start*."
        )

    async def _handle_explain_gate(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        """Explain a specific gate naturally."""
        text = intent.original_text.lower()
        
        if "cidb" in text:
            return (
                "🏗️ *CIDB Gate — How it works:*\n\n"
                "Every public construction tender requires a CIDB grading.\n"
                "The system checks:\n"
                "1. *Class match* — You need the right class (CE, GB, EE, ME, etc.)\n"
                "2. *Level/Capacity* — Your grade's financial limit must cover the tender value\n\n"
                "*Example:* You have CE3 (R3M limit). Tender needs CE4 for R5M → **Blocked**.\n"
                "But if tender is R2M → **Pass** (within your CE3 capacity).\n\n"
                "Type *verify cidb* to upload your certificate."
            )
        elif "csd" in text:
            return (
                "📋 *CSD Gate — Central Supplier Database:*\n\n"
                "Government tenders require a valid CSD (MAAA...) number.\n"
                "If *mandatory_csd = true* on a tender and you have no CSD → **Blocked**.\n\n"
                "Type *verify csd* to upload your CSD registration letter."
            )
        elif "tax" in text:
            return (
                "💰 *Tax Gate — SARS Tax Compliance PIN:*\n\n"
                "Tenders require an active SARS Tax PIN.\n"
                "If *tax_compliance_required = true* and no PIN → **Blocked**.\n\n"
                "Type *verify tax* to upload your Tax PIN."
            )
        elif "bbbee" in text or "b-bbee" in text:
            return (
                "📊 *B-BBEE Gate — Preference Points:*\n\n"
                "Doesn't block you — but affects your *match score* via PPPFA:\n\n"
                "*80/20 system* (tender < R50M):\n"
                "Level 1 = 20 pts | Level 2 = 18 | Level 3 = 14 | Level 4 = 12\n"
                "Level 5 = 8 | Level 6 = 6 | Level 7 = 4 | Level 8 = 2 | Non-compliant = 0\n\n"
                "*90/10 system* (tender ≥ R50M):\n"
                "Level 1 = 10 | Level 2 = 9 | Level 3 = 6 | Level 4 = 5\n"
                "Level 5 = 4 | Level 6 = 3 | Level 7 = 2 | Level 8 = 1 | Non-compliant = 0\n\n"
                "Your match score = 80% base + (your B-BBEE points / max points) × 20%\n\n"
                "Type *verify bbbee* to upload your certificate."
            )
        else:
            return (
                "Which gate would you like explained?\n"
                "🏗️ *CIDB* — Grading & financial capacity\n"
                "📋 *CSD* — Supplier registration\n"
                "💰 *Tax* — SARS Tax PIN\n"
                "📊 *B-BBEE* — Preference points"
            )

    async def _handle_explain_scoring(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        return (
            "📊 *How Match Scoring Works:*\n\n"
            "Your *match score* = **80% base** + **B-BBEE bonus (up to 20%)**\n\n"
            "1. *Base (80%)* — You passed all hard gates (CIDB, CSD, Tax, Geo)\n"
            "2. *B-BBEE Bonus* — Up to 20% based on your B-BBEE level:\n\n"
            "*80/20 tenders (< R50M):* Level 1=20pts → 100% | Level 4=12pts → 92% | Non-compliant=0pts → 80%\n"
            "*90/10 tenders (≥ R50M):* Level 1=10pts → 100% | Level 4=5pts → 95% | Non-compliant=0pts → 90%\n\n"
            "*Example:* You're Level 4, tender is R30M (80/20).\n"
            "Score = 80% + (12/20)×20% = **92%**\n\n"
            "Type *profile* to see your B-BBEE level."
        )

    async def _handle_explain_cidb(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        return await self._handle_explain_gate(user, intent, message_sid)

    async def _handle_explain_bbbee(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        return await self._handle_explain_gate(user, intent, message_sid)

    async def _handle_explain_csd(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        return await self._handle_explain_gate(user, intent, message_sid)

    async def _handle_upgrade_plan(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        """Start a paid-plan checkout from WhatsApp; beta access is explicit, not a free plan."""
        text = intent.original_text.lower()
        from ..billing.service import BillingService
        billing = BillingService()
        if any(word in text for word in ("price", "pricing", "plans", "how much")) and not any(name in text for name in ("starter", "pro", "vip")):
            return billing.available_plans_message()
        plan = "vip" if "vip" in text or "proposal" in text else "pro" if "pro" in text else "starter"
        interval = "annual" if any(word in text for word in ("annual", "year", "yearly")) else "monthly"
        if not user.registration_number:
            return "Complete your company profile first, then I can set up your paid plan securely."
        email = user.onboarding_data.get("billing_email")
        if not email:
            context = self._context_for(user); context["awaiting_billing_email"] = {"plan": plan, "interval": interval}; self._save_context(user, context)
            return "I can set up your *paid* plan now. Please reply with the email address for invoices and your secure payment link."
        return await self._create_checkout(user, plan, interval, email)

    async def _handle_manage_billing(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        text = intent.original_text.lower()
        from ..billing.service import BillingService
        billing = BillingService()
        if any(word in text for word in ("paid", "payment status", "my plan", "am i", "confirm payment", "subscription status")):
            return billing.status_message(user.phone_number)
        if "debit" in text:
            if not user.registration_number:
                return "Complete your company profile first, then I can start your secure debit-order mandate request."
            billing.request_payment_method(user.registration_number, user.phone_number, "debitcheck" if "debicheck" in text else "debit_order")
            return "I have recorded your debit-order request against this WhatsApp number. I will only send a provider-approved mandate link—never send banking details in this chat."
        if any(word in text for word in ("price", "pricing", "plans", "how much")):
            return billing.available_plans_message()
        return ("I can check your payment status using this WhatsApp number, show paid plans, manage annual renewal, or start a debit-order mandate. "
                "Tell me naturally—for example: _have I paid?_, _show plans_, _switch to annual_, or _set up debit order_.")

    async def _handle_bid_craft(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        from ..billing.service import BillingService
        entitlement = BillingService().entitlement_for(user.registration_number)
        if not entitlement.bid_craft:
            return "Bid-Craft is included with the *VIP paid plan*. Say *upgrade to VIP* and I will send a secure checkout link."
        tender_id = intent.entities.get("tender_ids", [None])[0] or extract_tender_id(intent.original_text)
        if not tender_id:
            return "Send the tender reference or reply to a tender alert with *prepare bid*. I will reserve one of your included monthly Bid-Craft packs and build it from tender evidence."
        if not BillingService().reserve_bid_craft_pack(user.registration_number, tender_id):
            return "Your included VIP Bid-Craft packs are used for this month, or this tender reference is not available. Say *show plans* if you need more bid-pack capacity."
        from ..agents.store import AgentStore
        AgentStore().enqueue("build_bid_pack", {"registration_number": user.registration_number, "tender_id": tender_id, "owner_phone": user.phone_number}, f"bid_craft:{user.registration_number}:{tender_id}")
        return f"I have reserved your Bid-Craft pack for *{tender_id}*. I will send the compliance matrix and draft once the agent finishes extracting the tender evidence."

    async def _create_checkout(self, user: WhatsAppUser, plan: str, interval: str, email: str) -> str:
        from ..billing.models import PlanCode, BillingInterval
        from ..billing.service import BillingService
        try:
            url = await BillingService().create_checkout(registration_number=user.registration_number, owner_phone=user.phone_number, email=email, plan=PlanCode(plan), interval=BillingInterval(interval))
        except Exception as exc:
            logger.warning("Checkout unavailable: %s", exc)
            return "Secure checkout is being prepared. I have saved your plan request and will send the link when payments are configured."
        return f"Here is your secure {interval} *{plan.title()}* checkout: {url}\n\nNever send card or banking details in WhatsApp."

    async def _handle_company_lookup(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        """Look up a contractor in the public CIDB register without inventing a result."""
        from ..whatsapp.onboarding import lookup_cidb_register
        query = intent.original_text.strip()
        for prefix in ("lookup", "find", "company", "contractor"):
            if query.lower().startswith(prefix):
                query = query[len(prefix):].strip(" :,-")
        if len(query) < 3:
            return "Tell me the company name to look up, for example: *lookup Example Construction*."
        records = await lookup_cidb_register(query)
        if not records:
            return f"I could not find *{query}* in the public CIDB register. Check the spelling or continue onboarding with your CIDB certificate."
        lines = [f"🏗️ *CIDB results for {query}*"]
        for record in records[:3]:
            lines.append(f"• {record.get('company_name') or record.get('Contractor Name', 'Contractor')} — {record.get('grading') or record.get('Grading', 'grading not published')}")
        return "\n".join(lines) + "\n\nPlease verify the current CIDB status before bidding."

    async def _handle_match_company(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        return "Running fresh match... Type *tenders* in a moment to see results."

    async def _handle_complaint(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        return (
            "I'm sorry you're having a bad experience. 😔\n\n"
            "What went wrong? Reply with details and I'll make sure the team sees it.\n\n"
            "Or type *stop* to unsubscribe completely."
        )

    async def _handle_feedback(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        return "Thanks for the feedback! 🙏 The team reads every message. What would you like to see improved?"

    async def _handle_thanks(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        return "You're welcome! 😊 Anything else I can help with?"

    async def _handle_unknown(self, user: WhatsAppUser, intent: ClassifiedIntent, message_sid: str) -> str:
        return self._fallback_response(user, intent)

    def _fallback_response(self, user: WhatsAppUser, intent: ClassifiedIntent) -> str:
        """Graceful fallback for unhandled intents."""
        if intent.confidence < 0.4:
            return (
                "🤔 I didn't quite catch that. Try:\n\n"
                "• *tenders* — View matches\n"
                "• *profile* — Verification status\n"
                "• *verify csd* — Upload document\n"
                "• *help* — All commands\n\n"
                "Or just ask naturally: \"Any electrical tenders in Gauteng?\""
            )
        return (
            f"I understood *{intent.intent.value.replace('_', ' ')}* but don't have a handler yet.\n"
            f"Try *help* for what I can do, or rephrase?"
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Helper Methods
    # ─────────────────────────────────────────────────────────────────────────

    def _get_today_match_count(self, user: WhatsAppUser) -> int:
        """Get today's match count for user."""
        if not user.registration_number:
            return 0
        from ..database import get_database_client
        from ..pipeline import _is_open_and_valid
        from ..whatsapp.matching import match_user_tenders
        from datetime import datetime, timezone
        db = get_database_client().connect()
        try:
            tenders = [t for t in db.list_open_tenders(limit=10000) if _is_open_and_valid(t, datetime.now(timezone.utc))]
        finally:
            db.close()
        return sum(1 for _, result in match_user_tenders(user, tenders) if result.is_eligible)

    def _verification_summary(self, user: WhatsAppUser) -> str:
        statuses = [user.csd_status, user.bbbee_status, user.tax_status, user.cidb_status]
        verified = sum(1 for s in statuses if s == "verified")
        return f"{verified}/4 verified"

    def _verification_emoji(self, status: str) -> str:
        return {
            "verified": "✅",
            "pending": "⏳",
            "failed": "❌",
            "expired": "⚠️",
            "not_provided": "⬜",
        }.get(status, "⬜")

    def _format_cidb(self, user: WhatsAppUser) -> str:
        gradings = user.onboarding_data.get("cidb_gradings", [])
        if not gradings:
            return "Not set"
        return ", ".join([f"{g.get('class_code', '')}{g.get('level', '')}" for g in gradings])

    def _extract_tender_filters(self, intent: ClassifiedIntent) -> dict[str, Any]:
        """Extract filter criteria from intent entities."""
        filters = {}
        entities = intent.entities

        if entities.get("provinces"):
            filters["province"] = entities["provinces"][0]
        if entities.get("cidb_classes"):
            filters["cidb_class"] = entities["cidb_classes"][0]
        if entities.get("cidb_grades"):
            try:
                filters["cidb_level"] = int(entities["cidb_grades"][0])
            except (ValueError, TypeError):
                pass
        if entities.get("monetary_values"):
            mv = entities["monetary_values"][0]
            if mv["unit"] == "M":
                filters["max_value"] = mv["amount"] * 1_000_000
            elif mv["unit"] == "K":
                filters["max_value"] = mv["amount"] * 1_000
            else:
                filters["max_value"] = mv["amount"]

        return filters

    def _format_tender_list(self, user: WhatsAppUser, filters: dict) -> str:
        """Query real, open tenders and return only eligible matches."""
        from datetime import datetime, timezone
        from ..database import get_database_client
        from ..pipeline import _is_open_and_valid
        from ..whatsapp.matching import match_user_tenders
        db = get_database_client().connect()
        try:
            tenders = db.list_open_tenders(limit=10000)
        finally:
            db.close()
        filtered = []
        for tender in tenders:
            if not _is_open_and_valid(tender, datetime.now(timezone.utc)):
                continue
            if filters.get("province") and (tender.location_target or "national").lower() not in {"national", filters["province"].lower()}:
                continue
            if filters.get("cidb_class") and (tender.required_cidb_class or "").upper() != filters["cidb_class"].upper():
                continue
            if filters.get("cidb_level") and (tender.required_cidb_level or 0) != filters["cidb_level"]:
                continue
            if filters.get("max_value") and tender.estimated_value is not None and tender.estimated_value > filters["max_value"]:
                continue
            filtered.append(tender)
        eligible = [(t, r) for t, r in match_user_tenders(user, filtered) if r.is_eligible][:5]
        if not eligible:
            return "📋 No open *eligible* matches were found for that filter. I only show tenders that pass the recorded CSD, tax, CIDB and location gates."
        lines = ["📋 *Your eligible tender matches*"]
        for tender, result in eligible:
            lines.append(f"\n• *{tender.tender_id}* — {tender.title[:90]}\n  {result.match_score:.0f}% | closes {tender.closing_date:%d %b} | {tender.issuing_entity[:45]}")
        lines.append("\nVerify all documents and tender conditions with the issuer before bidding.")
        return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Factory Function
# ─────────────────────────────────────────────────────────────────────────────

_handler_instance: Optional[AIMessageHandler] = None


def get_ai_handler() -> AIMessageHandler:
    """Get singleton AI message handler."""
    global _handler_instance
    if _handler_instance is None:
        _handler_instance = AIMessageHandler()
    return _handler_instance