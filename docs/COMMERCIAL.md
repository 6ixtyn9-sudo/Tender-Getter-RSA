COMMERCIAL — Plans, Billing Boundaries, Tax & Language Policy
(Consolidates the former agentic-commercial-beta.md and payments-and-tax-policy.md.)

Product posture
Tender Getter is a WhatsApp-first autonomous procurement agent for one owner
per company. It is not a dashboard product and has no permanent free tier:
starter, pro and vip are all paid plans. Invited beta companies receive an
explicit, expiring beta entitlement that exercises the same entitlement checks
as a paid account — never a hidden free-plan bypass.

Approved launch catalogue
Prices are seeded into subscription_plans by 20260720030000_commercial_catalog.sql
(database-owned; code never invents prices):

Plan	Monthly	Annual (upfront)	Annual saving
Starter	R249	R2,490	R498
Pro	R549	R5,490	R1,098
VIP Bid-Craft	R1,490	R14,900	R2,980
VIP includes two Bid-Craft packs per calendar month; extra packs R650 each,
purchased/configured through the billing catalogue before charging.
Annual pricing is an upfront annual checkout. A monthly debit order remains
monthly billing and never receives the annual upfront price.
All displayed prices require a final VAT-display decision with the business
accountant before public launch (see tax policy below).
Billing architecture
Provider-neutral billing contract; concrete adapter is Paystack hosted
checkout (card/secure bank payment) — requires PAYSTACK_SECRET_KEY,
PAYSTACK_PLAN_* IDs and BILLING_CALLBACK_URL. Checkout intentionally stays
disabled until those are set (fail-closed, locked by tests).
Stitch / DebiCheck (debit order): boundary only, deliberately unwired —
mandate, checkout, webhook and retry config require credentials and approved
API docs from the merchant agreement. Do not fabricate endpoints.
Banking/card details never touch Tender Getter: checkout happens on a
provider-hosted page opened from WhatsApp.
Subscriptions and pack reservations bind to the subscription's owner phone
number (anti-squat, round 3); checkout webhooks are signature-verified and
hostile-body hardened (round 2).
Autonomous agent policy
An agent may send a Qualified Match only when the source is verified, the
tender is open, a document is available, required hard gates pass on recorded
facts, and the enrichment-confidence threshold is met. Otherwise it retries,
enriches or suppresses automatically. Every action is recorded in
agent_actions. The system must never present uncertain information as verified
and must never claim a bidder will win.

VIP Bid-Craft produces: compliance matrix, evidence-bound methodology, executive
summary, assumptions, clarification questions and submission checklist — strictly
inside the <<TENDER_EVIDENCE>> untrusted-data boundary.

Payments & tax presentation policy
Current configuration: tax_mode: not_registered (in billing_tax_configuration).

Displayed catalogue amounts are final; customer messages and invoices must state:
"Tender Getter RSA is not currently VAT registered. No VAT is charged."
Never use "VAT inclusive/exclusive", "plus VAT", or show a VAT line in this mode.
Future modes (vat_inclusive, vat_exclusive) activate only via an authorised
business decision after VAT registration. This is not a runtime env variable
and the AI agent must never guess it.
Bank-neutral customer language. Never imply a tie to any bank; never say
"all banks are supported". Use: "Pay securely by card, secure bank payment, or
debit order, depending on the options available to you." Debit-order/DebiCheck
messages must say the customer approves a provider-hosted mandate through their
own banking channel. Tender Getter never collects banking details, PINs,
passwords, OTPs or mandate information in WhatsApp.

Provider rollout (business-controlled inputs)
The code provides the durable data model and checkout boundary; the following
are inputs that cannot be safely fabricated in source and gate real charging:

Onboard one primary payment provider (Paystack) → merchant approval →
product/plan IDs → webhook secret.
Stitch (or equivalent) merchant onboarding for debit-order/DebiCheck (post-beta).
Configure webhook endpoint, secret validation, failed-payment handling,
cancellation, receipts/reconciliation.
Sandbox-test: monthly card, annual card, debit-order mandate, failed payment,
retry, cancellation, beta expiry — before enabling real checkout (the full
go-live gate is in SECURITY.md).
Customer-recruitment hold
Do not generate a public waitlist, recruit beta customers or imply availability
until the founder has passed the tier, payment, WhatsApp, tender-process and
Bid-Craft checks in FOUNDER_ACCEPTANCE.md. Paid-plan
copy must describe only provider capabilities that are live and tested.

Beta plan (current)
~10 invited construction companies (construction-first deliberately maximizes
free public-registry verification via the live CIDB provider). Beta =
company_subscriptions.status='beta' + beta_expires_at. Prerequisite chain
(CIPC company registration → production WhatsApp number → Paystack merchant →
Cloud Run deploy) is tracked in STATUS.md.