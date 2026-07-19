# Hardening and End-to-End Completion

This package resolves the implementation risks identified in the July 2026 system review.

## Canonical code paths

`tender_getter` root modules are canonical (`schemas`, `matcher`, `pipeline`, `database`, `reporter`, etc.). The former `core/` and duplicate `ingestion/` implementations are now small compatibility facades that import those canonical modules. Legacy imports continue to work without allowing code to diverge.

## Trusted tender data

`aggregator.sync_all_sources()` now defaults to `real_only` mode and reports its mode in the summary. It bypasses `MOCK_HTML` fallback data. The only way to use fallback fixtures is the explicit diagnostic option:

```bash
PYTHONPATH=src python scripts/sync_all.py --allow-mock-fallback
```

Do not use that diagnostic mode to populate customer matches. `pipeline.ingest_real_tenders()` remains the canonical matching ingestion path.

The source registry now rejects duplicate IDs during discovery, treats aggregator adapters separately from entity sources, and has an executable registry/YAML integrity test. The source set is **722 discoverable entity classes**, plus **two documented metadata-only eTenders adapters**.

## WhatsApp and POPIA

- Immediate inbound replies use **TwiML only**. They are not also sent by the REST API, eliminating duplicate messages.
- REST delivery is retained only for out-of-band notifications (such as media-processing completion, reports and digests).
- Twilio request signatures fail closed in production. Unsigned requests can be accepted only with `ENV=development|test` and `TG_ALLOW_INSECURE_WEBHOOK=1`.
- The webhook adds rate limiting, replay suppression, content-type and size checks for documents, and defensive response headers.
- Per-user conversation state is persisted rather than shared through a singleton router.
- Tender list, filtering, detail lookup, CIDB lookup and digest preference changes now query/update real persistence paths.
- `supabase/migrations/20260719000000_whatsapp_and_privacy.sql` adds WhatsApp users, state, media, outbound delivery, daily preferences, immutable consent logging and opt-out suppression.

Apply migrations in order before production deployment:

```bash
supabase db push
# or apply supabase/migrations/20260707000000_initial_schema.sql and then
# supabase/migrations/20260719000000_whatsapp_and_privacy.sql in Supabase SQL Editor
```

## Reports

Markdown remains the human-auditable source report. `tender_getter.pdf_reports.generate_report_pdf()` renders the same report into a portable PDF using ReportLab. `tender_getter.whatsapp.reports.deliver_report()` uploads the PDF through the configured storage layer, obtains a delivery URL and sends it as WhatsApp media.

## Required production configuration

Set the existing Supabase, Gemini and Twilio variables plus:

```bash
ENV=production
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_FROM=whatsapp:+...
TG_CORS_ORIGINS=https://your-console.example
TG_WEBHOOK_RATE_PER_MINUTE=30
TG_MAX_MEDIA_BYTES=15728640
```

Never configure `TG_ALLOW_INSECURE_WEBHOOK=1` in production.

## Verification performed

```text
2249 passed in 176.11 seconds
```

The full suite includes the live source tests. Live public sites are inherently variable; tests now verify honest real-only reporting instead of treating mock fallback as a successful live source.

Docker was not built in this workspace because Docker is not installed here. The Dockerfile consumes `requirements.txt`; it will include FastAPI, Uvicorn, Twilio, ReportLab and the rest of the declared runtime dependencies. The webhook now binds to Cloud Run's `PORT` environment variable (default `8080`) and exposes `/health`.

## Agentic billing and Bid-Craft

The commercial beta adds autonomous agent decisions, durable job/audit records, natural-language customer feedback, paid-plan entitlements and secure hosted checkout boundaries. Apply the migrations in this exact order:

```text
20260707000000_initial_schema.sql
20260719000000_whatsapp_and_privacy.sql
20260720000000_agentic_billing.sql
```

All customer plans are paid (`starter`, `pro`, `vip`). Invited pilot users receive a visible, expiring `beta` entitlement rather than a hidden free-plan bypass. See [Agentic Commercial Beta](agentic-commercial-beta.md).
