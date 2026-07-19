# Agentic Commercial Beta

Tender Getter is a WhatsApp-first autonomous procurement agent for one owner per company. It is not a customer dashboard product and it does not offer a permanent free tier. `starter`, `pro`, and `vip` are all paid plans; invited beta companies receive an explicit, expiring `beta` entitlement.

## What is now in the codebase

- `agents/`: deterministic delivery policy, natural-language signal extraction, durable job/audit store, and VIP Bid-Craft prompt boundary.
- `billing/`: paid-plan/entitlement model, provider-neutral billing contract, and Paystack hosted-checkout adapter.
- `20260720000000_agentic_billing.sql`: durable agent jobs, autonomous decision audit, natural-language feedback, subscription plans, checkout sessions and payment-event idempotency.
- WhatsApp intent routing recognises natural upgrade, billing and Bid-Craft requests. No button-only feedback is required.

## Autonomous policy

An agent may send a **Qualified Match** only when the source is verified, the tender is open, a document is available, required hard gates pass on recorded facts, and the enrichment-confidence threshold is met. Otherwise it retries/enriches/suppresses automatically. Every action is recorded in `agent_actions`.

The system must never present uncertain information as verified or claim that a bidder will win.

## Billing model

- `starter`, `pro`, and `vip` must be seeded into `subscription_plans` with approved ZAR monthly and annual prices before checkout is enabled.
- Annual prices are explicit plan catalogue values. This supports discounts without hidden percentage calculations.
- Checkout happens on a provider-hosted page opened from WhatsApp. Banking/card details are never sent to Tender Getter.
- Beta access uses `company_subscriptions.status = 'beta'` plus `beta_expires_at`; it exercises the same entitlement checks as a paid account.
- VIP enables Bid-Craft: compliance matrix, evidence-bound methodology, executive summary, assumptions, clarification questions and submission checklist.

## South African payment rollout

1. Choose and onboard one primary provider before charging customers. The included concrete checkout adapter is Paystack; it requires `PAYSTACK_SECRET_KEY` and merchant configuration.
2. Establish Stitch (or equivalent) merchant onboarding for debit order/DebiCheck. The `StitchDebitOrderProvider` boundary is intentionally not wired to an invented endpoint: its mandate, checkout, webhook and retry configuration must use credentials and API details supplied under the merchant agreement.
3. Configure provider webhook endpoint, secret validation, failed-payment handling, cancellation, receipts/invoices and reconciliation.
4. Test monthly card, annual card, debit-order mandate, failed payment, retry, cancellation and beta expiry with provider sandbox/test data.

## Deployment checklist

```bash
supabase db push
# Configure production secrets: PAYSTACK_SECRET_KEY, PAYSTACK_PLAN_* and selected provider credentials.
# Deploy scripts/agent_worker.py as a durable Cloud Run Job/worker.
# Seed the approved paid plan catalogue; do not invent prices in code.
PYTHONPATH=src:. pytest -q
```

## Required remaining provider work

The code provides the correct durable data model and checkout boundary. Provider credentials, merchant approval, actual plan/product identifiers, webhook secrets, debit-order mandate configuration and approved commercial pricing are business-controlled inputs and cannot be safely fabricated in source code.

## Security Resilience gate

Do not enable real checkout, debit orders or unattended document processing until the controls in [Security Resilience Readiness](Security Resilience-readiness.md) are executed and evidenced.

## Approved launch catalogue

The approved public prices are stored in `20260720030000_commercial_catalog.sql` and seeded into `subscription_plans`:

| Plan | Monthly | Annual | Annual saving |
|---|---:|---:|---:|
| Starter | R249 | R2,490 | R498 |
| Pro | R549 | R5,490 | R1,098 |
| VIP Bid-Craft | R1,490 | R14,900 | R2,980 |

VIP includes two Bid-Craft packs per calendar month. Additional packs are priced at R650 and must be purchased/configured through the billing catalogue before charging. Annual payment is an upfront annual checkout; a monthly debit order remains monthly billing and does not receive the annual upfront-payment price.

All displayed prices require a final VAT display decision with the business accountant before public launch.
