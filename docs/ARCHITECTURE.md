ARCHITECTURE — System Design
Condensed, current-state architecture. (This consolidates the former PLANNING.md /
architecture-and-roadmap.md / hardening.md specs; versioned changelogs were dropped —
git history is the changelog.)

System map
text

TENDER SIDE                                   CLIENT SIDE (WhatsApp-first)
─────────────                                 ─────────────────────────────
OCDS API (primary feed)                       Twilio WhatsApp webhook ─┐
731 source modules (enrichment)               FastAPI: signature validation,
        │                                      rate limit, replay idempotency
        ▼                                                              │
aggregator / source_sync ──► pipeline.ingest_real_tenders              ▼
        │                                            onboarding state machine (5 steps)
        ▼                                            media upload → Supabase storage
  [stores] ◄── persistence layer                     Gemini Vision/LLM parse per doc type
  Supabase REST ► Postgres ► SQLite (fallback)                │
        ▲                                                     ▼
        │                                            verification trust boundary:
        │                                            identity-conflict → registry guard
        │                                            (CSD hook → CIDB live → CIPC hook)
        │                                            + CSD self-report negative gate
        ▼                                                     │
  matcher.py  ◄── CompanyProfile (verified facts only)        ▼
  hard gates + PPPFA points                            onboarding_data / statuses
        │
        ▼
  agents/ (Qualified-Match policy, durable jobs, audit) ──► outbound: matches,
  digest (07:00 SAST), PDF reports, billing flows, Bid-Craft (VIP)
Canonical code paths
tender_getter root modules are canonical (schemas, matcher, pipeline,
database, reporter, aggregator, parser, company_registry, matcher…).
The former core/ and ingestion/ packages are thin compatibility facades —
safe to import, but land new work in the canonical modules.

Service packages:

Package	Responsibility
whatsapp/	Twilio webhook, onboarding state machine, media pipeline, outbound (Twilio REST), digest, flows JSON, reports delivery
agents/	Deterministic Qualified-Match delivery policy, signal extraction, durable job/audit store, Bid-Craft prompt boundary
billing/	Plan/entitlement model (DB-owned catalogue), provider-neutral contract, Paystack adapter, Stitch boundary (unwired)
ai/	Gemini gateway: google-genai SDK, per-key cached clients across up to 7 rotated keys (GEMINI_API_KEY comma-list or GEMINI_API_KEY_n), 429/503 bounded retry (kills recursion DoS), model defaults gemini-2.5-flash family
Data flow & persistence
Persistence fallback order: Supabase REST (database_supabase.py) →
psycopg2 (database_postgres.py) → SQLite (database.py, localdata/).
All upserts are idempotent.
Ingestion trust: aggregator.sync_all_sources() / sync_all.py is
real_only by default; --allow-mock-fallback is a diagnostic flag only —
never use it to populate customer matches. Source registry rejects duplicate
IDs; a registry/YAML integrity test is executable.
Migrations (apply in order — 7 total):
text

20260707000000_initial_schema.sql
20260719000000_whatsapp_and_privacy.sql
20260720000000_agentic_billing.sql
20260720010000_security_resilience.sql
20260720020000_billing_identity_and_abuse_protection.sql
20260720030000_commercial_catalog.sql
20260720040000_billing_tax_and_payment_presentation.sql
Matching engine (matcher.py)
Strict mathematical filters, not vector similarity, for regulatory gating.

Gate 1 — hard blocks

Rule	Result
Tender mandatory_csd and company has no csd_number	Disqualified (0%)
Tender requires CIDB class the company lacks, or company grade < required grade	Disqualified
tax_compliance_required and no valid tax PIN	Warning demotion (hold), not a block
CIDB capacity values: 1=R200k · 2=R1m · 3=R3m · 4=R6m · 5=R10m · 6=R20m · 7=R60m · 8=R200m · 9=unlimited.

Gate 2 — PPPFA preference points (B-BBEE)

80/20 system applies to tenders with estimated value up to and including
R50 million; 90/10 above R50m.
80/20 points: L1=20, L2=18, L3=14, L4=12, L5=8, L6=6, L7=4, L8=2, non-compliant=0.
90/10 points: L1=10, L2=9, L3=6, L4=5, L5=4, L6=3, L7=2, L8=1, non-compliant=0.
Document parsing (parser.py + whatsapp/media.py)
Two-tier sieve to bound token spend: extract_relevant_pages → page-restricted
Gemini call → _validate_extraction. Caps: TG_MAX_PDF_PAGES (default 200),
TG_MAX_EXTRACT_CHARS (default 100 000), TG_MAX_MEDIA_BYTES (default 15 MB,
streamed, SSRF host allowlist with Twilio CDN redirect handling).
Validation: CIDB class whitelist, strict booleans, ISO dates, fail-safe None,
NaN/infinity rejection. Company-compliance documents (CSD letter, B-BBEE cert,
tax PIN, CIDB cert, CIPC cert) parse through per-type prompt schemas in
whatsapp/media.py; tender PDFs through parser.py.

Public-registry guard (company_registry.py)
Root-of-truth check before any uploaded document may verify a company:
CSD hook (TG_CSD_SEARCH_URL, dormant) → CIDB register (live, keyless, name corroboration) → CIPC hook (TG_CIPC_SEARCH_URL, dormant until SearchWorks/pbVerify).
First definitive answer wins; per-status TTL cache; all sources fail soft to a
hold (never blesses, never wrongly brands fraud). Non-CIPC identifiers
(WA-… placeholders, MAAA… numbers) skip enforcement. Retired: OpenCorporates
(ZA data archived at Sept 2014 — see STATUS.md).

Deployment topology
Dockerfile → Cloud Run (africa-south1), binds PORT (8080), /health.
Webhook service: python -m tender_getter.whatsapp.webhook.
scripts/agent_worker.py must deploy as a durable Cloud Run Job/worker —
request-scoped background processing is retained for local dev only.
Secrets via Secret Manager (scripts/deploy/set_secrets.sh), e.g.
tg-gemini-api-key (7 comma-separated keys).
Twilio media 307-redirects to a CDN — the downloader follows per-hop with the
allowlist (*.twilio.com auth only, twiliocdn.com allowed).
Founder acceptance flow
Before beta, the founder rehearses the exact customer journey against production
(or production-equivalent) services:

text

company onboarding → consent → evidence upload → verification state → real tender
→ qualified/suppressed decision → explanation → report → tier entitlement →
Bid-Craft → payment/trial status → delivery/recovery evidence
The detailed acceptance matrix lives in FOUNDER_ACCEPTANCE.md.

Positioning (one paragraph)
Every competitor (ProTenders, TendersHQ, OnlineTenders, TenderPoint, TenderBulletins)
is an OCDS-fed notification service over email. None offers WhatsApp delivery,
CIDB capacity gating, PPPFA scoring, or scanned-PDF extraction — those are the
moat, and they are built. (Full competitor write-up lived in the deleted
COMPETITOR_REPORT.md; the conclusion is what matters and it is this paragraph.)