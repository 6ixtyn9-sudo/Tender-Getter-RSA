from __future__ import annotations
import os, secrets
from dataclasses import dataclass
from typing import Any
from .models import BillingInterval, DEFAULT_CAPABILITIES, Entitlement, PlanCode, SubscriptionStatus
from .providers import PaystackProvider, ProviderNotConfigured

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
        plan = PlanCode(subscription["plan_code"])
        caps = DEFAULT_CAPABILITIES[plan]
        return Entitlement(plan, True, bool(caps.get("bid_craft")), True, True)

    def entitlement_for(self, registration_number: str | None) -> Entitlement:
        if not registration_number or not self.client:
            return self.entitlement(None)
        rows = self.client.table("company_subscriptions").select("plan_code,status,current_period_end,beta_expires_at").eq("registration_number", registration_number).execute().data
        return self.entitlement(rows[0] if rows else None)

    async def create_checkout(self, *, registration_number: str, owner_phone: str, email: str, plan: PlanCode, interval: BillingInterval) -> str:
        if not self.client: raise ProviderNotConfigured("Billing persistence is not configured")
        plan_row = self.client.table("subscription_plans").select("*").eq("plan_code", plan.value).eq("active", True).execute().data
        if not plan_row: raise ValueError("Selected paid plan is not available")
        row = plan_row[0]; amount = row["monthly_amount_cents"] if interval == BillingInterval.MONTHLY else row["annual_amount_cents"]
        reference = f"tg_{registration_number.replace('/','')}_{secrets.token_urlsafe(10)}"
        checkout = await self.provider.create_checkout(reference=reference, email=email, amount_cents=amount, interval=interval.value, metadata={"registration_number": registration_number, "owner_phone": owner_phone, "plan": plan.value})
        self.client.table("checkout_sessions").insert({"registration_number": registration_number, "owner_phone_number": owner_phone, "plan_code": plan.value, "billing_interval": interval.value, "provider": checkout.provider, "provider_reference": checkout.reference, "checkout_url": checkout.url}).execute()
        return checkout.url
