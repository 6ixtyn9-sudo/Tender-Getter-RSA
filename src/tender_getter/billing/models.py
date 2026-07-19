from dataclasses import dataclass
from enum import Enum
from typing import Mapping

class PlanCode(str, Enum):
    STARTER = "starter"
    PRO = "pro"
    VIP = "vip"

class BillingInterval(str, Enum):
    MONTHLY = "monthly"
    ANNUAL = "annual"

class SubscriptionStatus(str, Enum):
    BETA = "beta"
    TRIAL = "trial"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

@dataclass(frozen=True)
class Entitlement:
    plan: PlanCode
    active: bool
    bid_craft: bool
    monthly: bool
    annual: bool

# Amounts are deliberately database-managed. No price is hard-coded in code;
# deployment seeds the commercial catalogue after pricing approval.
DEFAULT_CAPABILITIES: Mapping[PlanCode, dict] = {
    PlanCode.STARTER: {"tender_alerts": True, "compliance_report": True, "bid_craft": False},
    PlanCode.PRO: {"tender_alerts": True, "compliance_report": True, "document_analysis": True, "bid_craft": False},
    PlanCode.VIP: {"tender_alerts": True, "compliance_report": True, "document_analysis": True, "bid_craft": True},
}
