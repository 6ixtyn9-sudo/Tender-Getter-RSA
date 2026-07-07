Tender Getter RSA 🇿🇦💎
An AI-native B2B procurement co-pilot and matchmaking platform that instantly screens, filters, and pairs South African SMMEs (Small, Medium, and Micro Enterprises) with active government and corporate tenders, while auto-generating compliance checklists and win-strategy proposals.

Submitted to the $2,000,000 Build with Gemini XPRIZE hackathon.

🚀 The Core Problem & Our Value Proposition (USP)
Existing tender notification systems in South Africa (charging R250 - R800/month) do nothing but flood business owners with raw, overwhelming email lists of daily links.

Tender Getter RSA is different — we do the actual heavy lifting:

Automated Gatekeeper: Screens tenders instantly against client company profiles (CSD registration, SARS Tax status, geographical local-content targets, and CIDB grading capacity limits) before the client wastes time reading.
Scanned PDF Compliance Sieve: Uses Gemini 1.5 Pro to parse messy, scanned, 100-page tender documents and extract a precise, structured compliance scorecard in seconds.
Bid-Craft Proposal Co-Pilot: Generates custom-synthesized executive summaries, compliance checklists, and professional project methodologies tailored to the tender's exact evaluation criteria.
🛠️ Repository Architecture & Tech Stack
The system is built to be modular, offline-first, highly reliable, and zero-latency:

src/tender_getter/schemas.py: Strict data validation contracts for CompanyProfile and TenderOpportunity using Pydantic V2.
src/tender_getter/matcher.py: The mathematical matching core. Computes strict regulatory disqualifications and calculates B-BBEE preference points (using both 80/20 and 90/10 point models per the Preferential Procurement Policy Framework Act - PPPFA).
src/tender_getter/database.py: Idempotent transactional persistence layer utilizing SQLite with ROW factory mappings to keep the codebase lightweight and serverless.
src/tender_getter/source_sync.py: Real data ingestion. Syncs directly with the official South African National Treasury OCDS Public REST API to harvest active bids.
src/tender_getter/lead_harvester.py: Standardized CSV importer to parse and onboard directories of active local companies.
src/tender_getter/reporter.py: Generates premium, audit-ready Tender Opportunity Reports (our R500 B2B deliverable) formatted cleanly in Markdown.
🚦 Getting Started & Local Setup
1. Clone & Install Dependencies
Ensure you have Python 3.10+ installed:

Bash

git clone https://github.com/6ixtyn9-sudo/Tender-Getter-RSA.git
cd Tender-Getter-RSA
pip install -r requirements.txt
2. Configure Environment Keys
Create a .env file in the project root (gitignored) and append your Google AI Studio credentials:

env

GEMINI_API_KEY=your_google_ai_studio_api_key_here
3. Run the Unit Test Suite
To verify that the regulatory gates, point calculations, and database structures are 100% correct:

Bash

PYTHONPATH=. pytest -v
4. Execute the Proof of Concept (POC)
Run the automated runner to see the matching engine evaluate eligibility, populate the local SQLite database (localdata/tender_getter.db), and write premium client scorecards to disk:

Bash

PYTHONPATH=. python3 scripts/run_poc.py
Outputs are saved directly to localdata/TG_REPORT_*.md.

📈 XPRIZE Submission Details
Category: Small Business Services
Build Window: May 19 — August 17, 2026
Production Deployment: Google Cloud Run (Containerized Serverless Engine)
LLM Engine: Gemini 1.5 Pro (Deep Document Auditing) & Gemini 1.5 Flash (Categorization)
Disclaimer: Tender Getter RSA is an independent software tool utilizing AI-native analytics. Bidders must verify all final compliance items with official state platforms (CSD, SARS, CIDB).Tender Getter RSA 🇿🇦💎
An AI-native B2B procurement co-pilot and matchmaking platform that instantly screens, filters, and pairs South African SMMEs (Small, Medium, and Micro Enterprises) with active government and corporate tenders, while auto-generating compliance checklists and win-strategy proposals.

Submitted to the $2,000,000 Build with Gemini XPRIZE hackathon.

🚀 The Core Problem & Our Value Proposition (USP)
Existing tender notification systems in South Africa (charging R250 - R800/month) do nothing but flood business owners with raw, overwhelming email lists of daily links.

Tender Getter RSA is different — we do the actual heavy lifting:

Automated Gatekeeper: Screens tenders instantly against client company profiles (CSD registration, SARS Tax status, geographical local-content targets, and CIDB grading capacity limits) before the client wastes time reading.
Scanned PDF Compliance Sieve: Uses Gemini 1.5 Pro to parse messy, scanned, 100-page tender documents and extract a precise, structured compliance scorecard in seconds.
Bid-Craft Proposal Co-Pilot: Generates custom-synthesized executive summaries, compliance checklists, and professional project methodologies tailored to the tender's exact evaluation criteria.
🛠️ Repository Architecture & Tech Stack
The system is built to be modular, offline-first, highly reliable, and zero-latency:

src/tender_getter/schemas.py: Strict data validation contracts for CompanyProfile and TenderOpportunity using Pydantic V2.
src/tender_getter/matcher.py: The mathematical matching core. Computes strict regulatory disqualifications and calculates B-BBEE preference points (using both 80/20 and 90/10 point models per the Preferential Procurement Policy Framework Act - PPPFA).
src/tender_getter/database.py: Idempotent transactional persistence layer utilizing SQLite with ROW factory mappings to keep the codebase lightweight and serverless.
src/tender_getter/source_sync.py: Real data ingestion. Syncs directly with the official South African National Treasury OCDS Public REST API to harvest active bids.
src/tender_getter/lead_harvester.py: Standardized CSV importer to parse and onboard directories of active local companies.
src/tender_getter/reporter.py: Generates premium, audit-ready Tender Opportunity Reports (our R500 B2B deliverable) formatted cleanly in Markdown.
🚦 Getting Started & Local Setup
1. Clone & Install Dependencies
Ensure you have Python 3.10+ installed:

Bash

git clone https://github.com/6ixtyn9-sudo/Tender-Getter-RSA.git
cd Tender-Getter-RSA
pip install -r requirements.txt
2. Configure Environment Keys
Create a .env file in the project root (gitignored) and append your Google AI Studio credentials:

env

GEMINI_API_KEY=your_google_ai_studio_api_key_here
3. Run the Unit Test Suite
To verify that the regulatory gates, point calculations, and database structures are 100% correct:

Bash

PYTHONPATH=. pytest -v
4. Execute the Proof of Concept (POC)
Run the automated runner to see the matching engine evaluate eligibility, populate the local SQLite database (localdata/tender_getter.db), and write premium client scorecards to disk:

Bash

PYTHONPATH=. python3 scripts/run_poc.py
Outputs are saved directly to localdata/TG_REPORT_*.md.

📈 XPRIZE Submission Details
Category: Small Business Services
Build Window: May 19 — August 17, 2026
Production Deployment: Google Cloud Run (Containerized Serverless Engine)
LLM Engine: Gemini 1.5 Pro (Deep Document Auditing) & Gemini 1.5 Flash (Categorization)
Disclaimer: Tender Getter RSA is an independent software tool utilizing AI-native analytics. Bidders must verify all final compliance items with official state platforms (CSD, SARS, CIDB).