"""Provider contracts. Payment credentials never enter WhatsApp or application logs."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Any

@dataclass(frozen=True)
class Checkout:
    provider: str
    reference: str
    url: str

class BillingProvider(Protocol):
    name: str
    async def create_checkout(self, *, reference: str, email: str, amount_cents: int, interval: str, metadata: dict[str, Any]) -> Checkout: ...
    def verify_webhook(self, body: bytes, signature: str) -> bool: ...

class ProviderNotConfigured(RuntimeError): pass

class PaystackProvider:
    """Hosted Paystack checkout adapter. Recurring plan setup is configured in
    the merchant account; this adapter only creates a secure first checkout."""
    name = "paystack"
    def __init__(self, secret_key: str | None): self.secret_key = secret_key
    async def create_checkout(self, *, reference: str, email: str, amount_cents: int, interval: str, metadata: dict[str, Any]) -> Checkout:
        if not self.secret_key: raise ProviderNotConfigured("Paystack is not configured")
        import httpx
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post("https://api.paystack.co/transaction/initialize", headers={"Authorization": f"Bearer {self.secret_key}"}, json={"email": email, "amount": amount_cents, "reference": reference, "metadata": {**metadata, "billing_interval": interval}})
            response.raise_for_status(); data = response.json()["data"]
        return Checkout(self.name, data.get("reference", reference), data["authorization_url"])
    def verify_webhook(self, body: bytes, signature: str) -> bool:
        import hashlib, hmac
        return bool(self.secret_key) and hmac.compare_digest(hmac.new(self.secret_key.encode(), body, hashlib.sha512).hexdigest(), signature)

class StitchDebitOrderProvider:
    """Integration boundary for card + debit order/DebiCheck onboarding.
    Provider-specific mandate and hosted checkout details are configured only
    after a Stitch merchant agreement; no invented API endpoint is used."""
    name = "stitch"
    def __init__(self, configured: bool = False): self.configured = configured
    async def create_checkout(self, **kwargs) -> Checkout:
        raise ProviderNotConfigured("Stitch debit-order checkout requires merchant credentials and approved mandate configuration")
    def verify_webhook(self, body: bytes, signature: str) -> bool: return False
