from __future__ import annotations
import logging
import os, secrets, re
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Any
from .models import BillingInterval, DEFAULT_CAPABILITIES, Entitlement, PlanCode, SubscriptionStatus
from .providers import PaystackProvider, ProviderNotConfigured

logger = logging.getLogger(__name__)

class BillingService:
    """Commercial policy service. All customer plans are paid; beta access is an
    explicit expiring entitlement and exercises the same capability checks."""
    def __init__(self, client=None):
        self.client = client
        if self.client is None:
            try:
                from supabase import create_client
                if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
                    self.client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
            except Exception: pass
        self.provider = PaystackProvider(os.getenv("PAYSTACK_SECRET_KEY"))

    def entitlement(self, subscription: dict | None) -> Entitlement:
        if not subscription or subscription.get("status") not in {SubscriptionStatus.BETA.value, SubscriptionStatus.TRIAL.value, SubscriptionStatus.ACTIVE.value}:
            return Entitlement(PlanCode.STARTER, False, False, False, False)
        expiry_key = "beta_expires_at" if subscription.get("status") == SubscriptionStatus.BETA.value else "trial_expires_at" if subscription.get("status") == SubscriptionStatus.TRIAL.value else "current_period_end"
        expiry = subscription.get(expiry_key)
        if expiry:
            try:
                when = datetime.fromisoformat(str(expiry).replace("Z", "+00:00"))
                if when.tzinfo is None: when = when.replace(tzinfo=timezone.utc)
                if when <= datetime.now(timezone.utc):
                    return Entitlement(PlanCode.STARTER, False, False, False, False)
            except ValueError:
                return Entitlement(PlanCode.STARTER, False, False, False, False)
        try:
            plan = PlanCode(subscription["plan_code"])
        except (KeyError, ValueError):
            # A corrupted or unknown plan code must fail CLOSED — never crash
            # and never grant capabilities the catalogue does not define.
            logger.warning("Unknown plan_code on subscription: %r", subscription.get("plan_code"))
            return Entitlement(PlanCode.STARTER, False, False, False, False)
        caps = DEFAULT_CAPABILITIES.get(plan, {})
        return Entitlement(plan, True, bool(caps.get("bid_craft")), True, True)

    def entitlement_for(self, registration_number: str | None, owner_phone: str | None = None) -> Entitlement:
        """Entitlement for a company — optionally bound to the caller's phone.

        A WhatsApp number can claim ANY registration number at onboarding, so
        a bare registration lookup would let a squatter inherit (or burn) the
        real owner's paid subscription. When owner_phone is supplied, the
        subscription's recorded owner must match or the entitlement fails closed.
        """
        if not registration_number or not self.client:
            return self.entitlement(None)
        rows = self.client.table("company_subscriptions").select("plan_code,status,current_period_end,beta_expires_at,trial_expires_at,owner_phone_number").eq("registration_number", registration_number).execute().data
        subscription = rows[0] if rows else None
        if subscription and owner_phone is not None:
            if str(subscription.get("owner_phone_number") or "") != str(owner_phone):
                logger.warning("Entitlement lookup blocked: phone %s does not own subscription for %s", owner_phone, registration_number)
                return self.entitlement(None)
        return self.entitlement(subscription)

    def tax_configuration(self) -> dict:
        if not self.client:
            return {"tax_mode": "not_registered", "vat_rate_percent": 15.0}
        rows = self.client.table("billing_tax_configuration").select("*").eq("singleton", True).execute().data
        return rows[0] if rows else {"tax_mode": "not_registered", "vat_rate_percent": 15.0}

    def checkout_amounts(self, catalogue_amount_cents: int) -> tuple[int, int, int, str]:
        """Return subtotal, tax, total and mode from the database-owned tax policy."""
        config = self.tax_configuration(); mode = config["tax_mode"]; rate = float(config["vat_rate_percent"]) / 100
        if mode == "vat_exclusive":
            tax = round(catalogue_amount_cents * rate)
            return catalogue_amount_cents, tax, catalogue_amount_cents + tax, mode
        if mode == "vat_inclusive":
            subtotal = round(catalogue_amount_cents / (1 + rate)) if rate else catalogue_amount_cents
            return subtotal, catalogue_amount_cents - subtotal, catalogue_amount_cents, mode
        return catalogue_amount_cents, 0, catalogue_amount_cents, "not_registered"

    def tax_note(self) -> str:
        mode = self.tax_configuration()["tax_mode"]
        if mode == "not_registered": return "Tender Getter RSA is not currently VAT registered. No VAT is charged."
        if mode == "vat_inclusive": return "VAT is included in the displayed price."
        return "VAT is added at secure checkout where applicable."

    async def create_checkout(self, *, registration_number: str, owner_phone: str, email: str, plan: PlanCode, interval: BillingInterval) -> str:
        if not self.client: raise ProviderNotConfigured("Billing persistence is not configured")
        plan_row = self.client.table("subscription_plans").select("*").eq("plan_code", plan.value).eq("active", True).execute().data
        if not plan_row: raise ValueError("Selected paid plan is not available")
        row = plan_row[0]; catalogue_amount = row["monthly_amount_cents"] if interval == BillingInterval.MONTHLY else row["annual_amount_cents"]
        subtotal, tax, amount, tax_mode = self.checkout_amounts(catalogue_amount)
        # The WhatsApp owner number is the human-recognisable payment reference;
        # random entropy prevents another customer guessing or reusing it.
        phone_ref = re.sub(r"[^0-9]", "", owner_phone)[-12:]
        reference = f"TG-{phone_ref}-{secrets.token_hex(5).upper()}"
        checkout = await self.provider.create_checkout(reference=reference, email=email, amount_cents=amount, interval=interval.value, metadata={"registration_number": registration_number, "owner_phone": owner_phone, "plan": plan.value})
        self.client.table("checkout_sessions").insert({"registration_number": registration_number, "owner_phone_number": owner_phone, "plan_code": plan.value, "billing_interval": interval.value, "provider": checkout.provider, "provider_reference": checkout.reference, "customer_reference": reference, "checkout_url": checkout.url, "amount_cents": amount, "subtotal_amount_cents": subtotal, "tax_amount_cents": tax, "tax_mode": tax_mode, "currency": row["currency"]}).execute()
        return checkout.url

    def subscription_for_phone(self, owner_phone: str) -> dict | None:
        if not self.client: return None
        rows = self.client.table("company_subscriptions").select("*").eq("owner_phone_number", owner_phone).execute().data
        return rows[0] if rows else None

    def status_message(self, owner_phone: str) -> str:
        subscription = self.subscription_for_phone(owner_phone)
        if not subscription:
            return "I cannot see an active paid plan yet. Say *upgrade* when you are ready and I will create a secure checkout link."
        status = subscription["status"].replace("_", " ")
        plan = subscription["plan_code"].title()
        interval = subscription["billing_interval"]
        if subscription["status"] == "beta":
            return f"You are on the *{plan} beta* entitlement. It expires on {subscription.get('beta_expires_at') or 'the date agreed with the beta team'}."
        return f"Your *{plan}* plan is *{status}* on {interval} billing. Your WhatsApp number is the account reference."

    def available_plans_message(self) -> str:
        """Render the database catalogue; prices are never duplicated in code."""
        if not self.client:
            return "Paid plan information is temporarily unavailable. Please try again shortly."
        rows = self.client.table("subscription_plans").select("*").eq("active", True).execute().data
        if not rows:
            return "Paid plans are being finalised. Please try again shortly."
        lines = ["*Tender Getter paid plans*"]
        for row in sorted(rows, key=lambda item: (item["monthly_amount_cents"], item["plan_code"])):
            monthly = row["monthly_amount_cents"] / 100
            annual = row["annual_amount_cents"] / 100
            saving = (monthly * 12) - annual
            label = row["display_name"]
            lines.append(f"\n*{label}* — R{monthly:,.0f}/month or R{annual:,.0f}/year (save R{saving:,.0f})")
        lines.append("\n" + self.tax_note())
        lines.append("Reply naturally with _upgrade to Starter_, _I want Pro yearly_, or _VIP monthly_.")
        return "\n".join(lines)

    def request_payment_method(self, registration_number: str, owner_phone: str, method: str) -> None:
        if not self.client:
            raise ProviderNotConfigured("Billing persistence is not configured")
        self.client.table("billing_requests").insert({"registration_number": registration_number, "owner_phone_number": owner_phone, "requested_method": method}).execute()

    def reserve_bid_craft_pack(self, registration_number: str, tender_id: str, owner_phone: str | None = None) -> bool:
        """Reserve a monthly Bid-Craft pack — ownership-gated when a phone is known.

        The reservation RPC is keyed by registration number; binding it here to
        the subscription's owner phone stops a squatter from burning the real
        owner's included packs.
        """
        if not self.client:
            return False
        if owner_phone is not None:
            subscription = self.subscription_for_phone(owner_phone)
            if not subscription or str(subscription.get("registration_number") or "") != str(registration_number):
                logger.warning("Bid-Craft reservation blocked: phone %s does not own %s", owner_phone, registration_number)
                return False
        result = self.client.rpc("reserve_bid_craft_pack", {"company_reg": registration_number, "bid_tender_id": tender_id}).execute()
        return bool(result.data)
