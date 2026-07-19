# STATUS — Live Repository State

> **Read this first.** This file is the single source of truth for what works,
> what is pending (and on whom), what is known-broken, and what happens next.
> Update it whenever a checkbox flips. Git history is the changelog — do not
> keep versioned changelogs in docs.

**Snapshot:** 2026-07-19 · HEAD `63325ed` · test suite **2347 passed** ·
migrations **7** · source modules **731** · Cloud Run deploy **not yet executed**.

---

## ✅ Working and verified (code-complete, test-locked)

| Area | State |
|---|---|
| Tender ingestion | OCDS-first (National Treasury public API) + 731 direct-scrape source modules as enrichment; `sync_all.py` defaults to `real_only` (mock fallback is diagnostic-only via `--allow-mock-fallback`) |
| Matching engine | Hard gates (CSD mandatory, CIDB class+level capacity, tax warning) + PPPFA 80/20 & 90/10 preference-point math; 80/20 applies **up to and including R50m** |
| Document parsing | Gemini (google-genai SDK, per-key clients, 7-key rotation) two-tier PDF sieve; page/char caps; strict extraction validation (CIDB whitelist, strict bools, ISO dates, NaN-safe) |
| WhatsApp layer | Twilio webhook (signature fail-closed, rate limit, replay idempotency, TwiML-only immediate replies), 5-step onboarding, media upload → parse pipeline, digest job, PDF report delivery |
| Verification trust boundary | Identity-conflict gate → **public-registry guard** (CSD→CIDB→CIPC chain) → per-credential shape checks. Uploaded documents never self-bless |
| Registry guard — live | **CIDB Register of Contractors**: free, keyless, definitive allow/block for construction companies |
| Registry guard — CSD self-report | Fresh CSD Registration Report stating "supplier inactive" / deregistration status → auto-FAILED (`TG_CSD_REPORT_MAX_AGE_DAYS`, default 30). Positives corroborate only; stale reports never auto-fail |
| Billing boundary | Paid-plan/entitlement model, subscription anti-squat ownership binding, Paystack hosted-checkout adapter (unsigned/malformed webhooks rejected; entitlement fails closed; amounts coerced). **Checkout disabled until real plan IDs configured — intentional** |
| Agent layer | Deterministic Qualified-Match policy, durable job/audit store, feedback storage with SA-ID/card redaction, Bid-Craft with `<<TENDER_EVIDENCE>>` injection boundary |
| Prompt-injection defenses | Bid-Craft evidence markers, parser validation, outbound content JSON-encoded, display-name sanitization |
| Red-team rounds | Rounds 1–7 shipped and audited (see [SECURITY.md](SECURITY.md) for the full table). All findings locked in `tests/test_security_regression.py` |

## 🟡 Pending — external/business (not code problems)

In the order the founder plans to execute them:

| # | Item | Blocked on | Notes |
|---|---|---|---|
| 1 | **Register the operating company at CIPC** | Founder (manual, eServices) | Name candidates: Tender Getter RSA / Tender Helper RSA / Tender Finder RSA / Tender Source RSA. Needed for banking + Paystack FICA. Manual name reservation (~R50) is a legitimate use of a CIPC login |
| 2 | **Production WhatsApp Business number** | Twilio/Meta onboarding (needs #1) | Currently Twilio **Sandbox**. WhatsApp Flows JSON: Meta approval pending |
| 3 | **Paystack merchant live** | Merchant approval + plan IDs (needs #1) | Set `PAYSTACK_SECRET_KEY`, `PAYSTACK_PLAN_*`, `BILLING_CALLBACK_URL`; then sandbox-test the full readiness gate in [SECURITY.md](SECURITY.md) before real checkout |
| 4 | **Cloud Run deploy** | Founder (needs 1–3 for prod values) | `./scripts/deploy/cloudrun.sh <PROJECT_ID>` then `scripts/deploy/set_secrets.sh`; GCP project/APIs/Artifact Registry already prepared; secret `tg-gemini-api-key` holds 7 rotated keys. Deploy `scripts/agent_worker.py` as a durable worker/Job |
| 5 | **Beta cohort: ~10 construction companies** | Needs #1–#4 | Construction-first is deliberate: CIDB public register gives free definitive verification for this segment |
| 6 | **SearchWorks CIPC API (Standard Bank OneHub)** | Awaiting OneHub reply (request sent 2026-07-19) | When docs/schema arrive → write adapter behind `TG_CIPC_SEARCH_URL` |
| 7 | **CSD supplier-interface access** | Municipality sponsorship (meeting this week) | CSD interface access is granted by National Treasury to organs of state only; a municipal sponsor is the realistic route. Hook: `TG_CSD_SEARCH_URL` |
| 8 | **Stitch / DebiCheck debit orders** | Merchant agreement (post-beta) | Boundary exists, intentionally unwired — requires real credentials + approved API docs |

## ❌ Known gaps and dead ends (do not re-litigate)

- **OpenCorporates — evaluated and retired.** Its ZA dataset is an archive frozen at Sept 2014 (CIPRO-era). Stale in both directions (false blocks for post-2014 companies, false blessings from outdated statuses). A tripwire test keeps it out of the chain.
- **No free machine API exists for CIPC status.** eServices/BizPortal login-walled since 2024 (POPI); CIPC ToS prohibit automated extraction — credentialed login automation was considered and rejected (ToS breach, account-ban risk on the founder's own CIPC identity, due-diligence poison).
- **PENDING verification holds have no admin UI** — by design they are rare (CIDB answers for construction; CSD self-report negatives auto-fail). Non-construction uploads with no reachable registry sit PENDING until OneHub/CSD lands.
- **Live-source tests depend on upstream sites** being up; the suite treats honesty (reporting a dead source) as success.
- ~50 `datetime.utcnow()` deprecation warnings from model defaults — cosmetic, no functional impact; cleanup optional.

## ➡️ Next actions

**Business (founder):** items 1–5 in the Pending table, in order.
**Code (next agent):** nothing blocking. Candidate work, in priority order:

1. SearchWorks/pbVerify adapter when API docs arrive (slot: `TG_CIPC_SEARCH_URL` provider in `company_registry.py`).
2. Red-team round 8: crafted-PDF prompt injection against the live parse pipeline end-to-end; then outbound/digest flood-control deep-dive.
3. Optional: `datetime.utcnow()` deprecation cleanup for a zero-warning suite.

## Next-agent operating protocol (short version)

1. Read this file, then [SECURITY.md](SECURITY.md) (the agent rules are binding).
2. **One security test file** — every security lock goes in `tests/test_security_regression.py`. Never create round-specific test files.
3. **No bloat:** no temp/scratch files, no root-level scripts, no doc duplication.
4. Deliver changes as full-file zips via the established apply protocol; the founder runs pytest and commits; every push is audited (byte parity + full suite) before further work builds on it.
5. Full suite must pass before shipping: current baseline **2347 passed**.
