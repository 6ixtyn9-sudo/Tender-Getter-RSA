# Tender Getter RSA 🇿🇦

An AI-native B2B procurement co-pilot for South African SMMEs: it screens active
government and corporate tenders against each company's real compliance profile
(CSD, SARS, CIDB, B-BBEE), parses scanned tender PDFs into structured scorecards,
and delivers matches, digests and Bid-Craft proposal packs over **WhatsApp**.

Submitted to the Build with Gemini XPRIZE hackathon (Small Business Services, May–Aug 2026).

## Why it exists

The South African state is the biggest buyer in the economy, and procurement law
(the PPPFA) reserves preference points specifically to push that spend toward
small, black-owned businesses. The demand for the township electrician, the
Limpopo security company, the Eastern Cape builder is **written into legislation**.

But the road to a bid was built for companies with a tender office: 100-page
scanned PDFs, CSD/SARS/CIDB compliance gates, PPPFA point math, briefing-session
logistics. Incumbent "tender alert" services sell the raw start of that road —
a daily email of links, R250–R800/month, laptop-first, in procurement-speak —
and stop there. The one-person CC that could do the work either never hears
about the tender or drowns in the paperwork before the closing date.
Transformation policy dies in the last mile, and the work flows to whoever
already has a bid office.

Tender Getter RSA **is** the bid office — in the pocket of the business that
can't afford one, on the platform it already runs on. It knows the company's
CIDB grade and tax status, watches every public tender source, says in plain
language on WhatsApp which tenders they actually qualify for and exactly what
each one demands, then helps draft the response. And because access only matters
if it's fair, the same pipeline verifies that companies are real and active —
phantom paperwork doesn't crowd legitimate SMMEs out.

## Start here: repository state

Read **[docs/STATUS.md](docs/STATUS.md) first** — it records what is verified
working, what is pending (and on whom), known gaps, and the ordered next actions.
The other operating docs:

| Document | Contents |
|---|---|
| [docs/STATUS.md](docs/STATUS.md) | Live state, pending items, next actions — **read first** |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, module map, matching math, data flow |
| [docs/SECURITY.md](docs/SECURITY.md) | Agent rules, production invariants, red-team history, go-live gate |
| [docs/COMMERCIAL.md](docs/COMMERCIAL.md) | Plans/catalogue, billing boundaries, tax & language policy |

## Quickstart

Requires Python 3.10+ (CI runs 3.13).

```bash
git clone https://github.com/6ixtyn9-sudo/Tender-Getter-RSA.git
cd Tender-Getter-RSA
pip install -r requirements.txt
cp .env.example .env        # set SUPABASE_*, GEMINI_API_KEY, etc.
PYTHONPATH=src:. python scripts/doctor.py
pytest -q                   # full suite: 2347 tests
PYTHONPATH=src:. python scripts/run_poc.py   # local matching PoC → localdata/
```

## Repository layout

```text
src/                 Application packages (tender_getter canonical modules)
scripts/             Operational CLI tools
  deploy/            Cloud Run deployment and Secret Manager setup
  twilio/            Twilio Content Template administration
  manual/            Explicit local smoke checks (not pytest tests)
docs/                STATUS (live state), ARCHITECTURE, SECURITY, COMMERCIAL
config/twilio/       Twilio template definitions
supabase/migrations/ Database schema changes (apply in timestamp order)
tests/               Automated test suite (one security file: test_security_regression.py)
```

## Environment

All runtime configuration is environment-driven; see `.env.example` for the
annotated reference (Supabase, Gemini key rotation, Twilio, Paystack, the
public-registry guard hooks, and every `TG_*` tuning knob).

**Disclaimer:** Tender Getter RSA is an independent analytics tool. Bidders must
verify all final compliance items on the official platforms (CSD, SARS, CIDB, CIPC).
