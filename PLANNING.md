Tender Getter RSA - Architectural & Technical Specification
Date: 2026-07-08
Venture: Commercial B2B SaaS Bidding Matchmaker (South Africa)
Version: 1.2.0

1. Executive Summary & USP
Tender Getter RSA is a highly optimized, AI-native B2B matchmaking and proposal-drafting platform built for South African SMMEs (Small, Medium, and Micro Enterprises).

The USP is execution-focused: We do not just aggregate a list of daily links (which existing R250-R800/month portals do). We solve the disqualification and proposal-writing traps by instantly screening non-negotiable regulatory gates (CSD, SARS, CIDB, B-BBEE, Geofencing) and generating custom-synthesized compliance-win strategies and proposal drafts in seconds.

2. Core Python Architecture & Schemas
To ensure rapid, modular iteration and high reliability, our backend is structured strictly around Pydantic validation models and a SQLite relational data layer.

A. The Master Schemas (src/tender_getter/schemas.py)
Two data structures define the entire transaction space:

Python

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class CIDBGrading(BaseModel):
    class_code: str = Field(..., description="e.g. CE (Civil Engineering), GB (General Building)")
    level: int = Field(..., ge=1, le=9, description="CIDB grading level from 1 to 9")

class Location(BaseModel):
    province: str
    city: str
    municipality: Optional[str] = None

class CompanyProfile(BaseModel):
    registration_number: str = Field(..., description="CIPC registration number")
    company_name: str
    csd_number: Optional[str] = Field(None, description="MAAA supplier number")
    bbbee_level: int = Field(9, ge=1, le=9, description="B-BBEE Level, 9 is Non-Compliant")
    black_ownership_pct: float = Field(0.0, ge=0.0, le=100.0)
    youth_ownership_pct: float = Field(0.0, ge=0.0, le=100.0)
    women_ownership_pct: float = Field(0.0, ge=0.0, le=100.0)
    cidb_gradings: List[CIDBGrading] = []
    location: Location
    sectors: List[str]
    has_tax_pin: bool = False
    has_coida: bool = False
    is_active: bool = True

class TenderOpportunity(BaseModel):
    tender_id: str = Field(..., description="Official bid number/reference")
    title: str
    issuing_entity: str
    closing_date: datetime
    estimated_value: Optional[float] = None
    required_cidb_class: Optional[str] = None
    required_cidb_level: Optional[int] = None
    mandatory_csd: bool = True
    location_target: Optional[str] = Field(None, description="e.g. 'Gauteng' or 'National'")
    raw_document_url: Optional[str] = None
B. Relational Storage (src/tender_getter/database.py)
A local-first SQLite database matches these schemas for instant, zero-cost state management:

Table company_profiles: Relational store of all registered clients.
Table tenders: Relational cache of raw, parsed tenders.
Table matches: Stores historic match results, evaluation scores, and client notification records.
3. Mathematical Matching & Gating Logic (src/tender_getter/matcher.py)
The matching core does not use vague vector similarity for regulatory hurdles. It uses strict mathematical filters followed by weighted heuristic sorting.

Gate 1: Binary Disqualification Filters (Hard Blocks)
CSD Validation: If Tender.mandatory_csd is True and Company.csd_number is null -> Disqualified (0% Match).
Tax Status: If Tender.tax_compliance_required is True and Company.has_tax_pin is False -> Warning flag (Match demoted/Hold).
CIDB Capacity Gate:
Define upper financial thresholds for Grade levels:
Grade 1: R200k | Grade 2: R1m | Grade 3: R3m | Grade 4: R6m | Grade 5: R10m | Grade 6: R20m | Grade 7: R60m | Grade 8: R200m | Grade 9: No Limit.
Constraint Rule: The matching engine blocks a match if Tender.required_cidb_class is present but the client does not possess that class, OR if Company.cidb_level < Tender.required_cidb_level.
Gate 2: Preferential Procurement Scoring (B-BBEE / PPPFA Math)
80/20 System (Estimated Value < R50 Million):
Max Price points = 80.
B-BBEE preference points allocated dynamically:
Level 1 = 20 pts | Level 2 = 18 pts | Level 3 = 14 pts | Level 4 = 12 pts | Level 5 = 8 pts | Level 6 = 6 pts | Level 7 = 4 pts | Level 8 = 2 pts | Non-Compliant = 0 pts.
90/10 System (Estimated Value >= R50 Million):
Max Price points = 90.
B-BBEE preference points allocated dynamically:
Level 1 = 10 pts | Level 2 = 9 pts | Level 3 = 6 pts | Level 4 = 5 pts | Level 5 = 4 pts | Level 6 = 3 pts | Level 7 = 2 pts | Level 8 = 1 pt | Non-Compliant = 0 pts.
4. Gemini OCR & Compliance Sieve (src/tender_getter/parser.py)
Tender documents are highly complex, multi-page PDFs. To avoid blowing out our token budget and preventing lookup lag, the parsing pipeline uses a Two-Tier Sieve:

text

[Messy 100-Page PDF] 
        │
        ▼ (Local Python Extraction)
 [Page Pre-Screener] ──► Extracts only pages containing "SBD 1", "SBD 6.1", 
        │                "CIDB", or "Evaluation Criteria". (Reduces to ~5 pages)
        ▼
[Gemini 1.5 Pro API] ──► Strict JSON Compliance Extraction (Structure Validation)
        │
        ▼
 [Relational Schema] ──► Piped into sqlite matching engine
The System Prompt & Output Schema:
Gemini 1.5 Pro is invoked with a strict JSON system schema to prevent any formatting drift:

JSON

{
  "bid_number": "string",
  "closing_date": "string (YYYY-MM-DD or null)",
  "required_cidb_class": "string ('CE', 'GB', 'EE', 'ME' or null)",
  "required_cidb_level": "integer (1-9 or null)",
  "mandatory_csd": "boolean",
  "bbbee_points_system": "string ('80/20', '90/10' or null)",
  "location_target": "string or null"
}
5. Phase 1 (Today): Ingestion Maximization Engine
To build the most comprehensive procurement catalog in South Africa, today is dedicated to maximizing active tender harvesting. We move beyond single-point failures by implementing a high-throughput, redundant pipeline strategy.

A. Ingestion Vectors
OCDS API Sync (etenders_ocds.py): Polls the /api/OCDSReleases endpoint using a rolling date filter (typically 30-day windows) to capture rapid daily modifications and brand-new bids.
CSV Bulk Backfill (source_sync.py): Utilizes historical monthly eTenders data dump URLs to bulk-ingest thousands of records, ensuring historical baseline density.
Provincial Gazettes & direct scrapers: Establishes schema mappings for direct scraping of primary municipal portals (such as City of Cape Town, City of Joburg, and eThekwini) and State-Owned Enterprises (Eskom, SANRAL, Transnet) which frequently publish off-grid.
B. Resilience & Deduplication Rules
Idempotent Insertion: Tenders are keyed on a unique, cleaned reference number (tender_id).
Title Cleansing Heuristics: If the incoming title matches a reference code pattern (contains forward slashes / and is under 60 characters) and a detailed description exists, the pipeline dynamically normalizes the name using the _pick_title strategy to avoid unreadable directories.
Duplicate Prevention: SQLite utilizes INSERT OR REPLACE / Postgres uses ON CONFLICT (tender_id) DO UPDATE to ensure bid descriptions, closing dates, and documents are always kept up-to-date without record bloat.
6. Comprehensive 10x Target Ingestion & Sourcing Registry
To guarantee we capture 100% of all public-sector procurement bids across South Africa and eliminate any need to back-pedal during subsequent growth phases, we establish an exhaustive 112-Source Master Target Registry.

I. National Government Departments (The Core Ministries - 26 Sources)
SAPS (South African Police Service) - Safety gear, security infrastructure, uniforms, vehicle fleets, catering, station facilities.
DoEL (Department of Employment and Labour) - Corporate training, facilities maintenance, protective gear, regional offices.
DPWI (Department of Public Works & Infrastructure) - The largest national buyer of civil engineering (CE) and building construction (GB).
DWS (Department of Water and Sanitation) - Massive dam builds, pipelines, water treatment equipment, hydrology services.
DoD (Department of Defence) / Armscor - Specialized electronics, military catering, uniform fabrication, logistical services.
DoH (Department of Health) - Hospital equipment, pharmaceuticals, surgical supplies, medical gas installations.
DBE (Department of Basic Education) - School construction projects (ASIDI), textbook printing, student feeding schemes.
DHET (Department of Higher Education & Training) - Tertiary software, IT infrastructure, university facilities development.
DHA (Department of Home Affairs) - Document printing, citizen services IT systems, biometric scanners, local security.
DMRE (Department of Mineral Resources & Energy) - Solar infrastructure, grid connections, geological consultancies.
DALRRD (Department of Agriculture, Land Reform & Rural Development) - Spatial mapping, farm assets, regional fencing, borehole builds.
DFFE (Department of Forestry, Fisheries & the Environment) - Hazardous waste clearing, wildfire gear, eco-consulting.
DoT (Department of Transport) - Rail crossing studies, traffic safety systems, maritime logistics.
National Treasury - Financial planning consulting, state audit software, public sector training.
DCS (Department of Correctional Services) - Inmate nutrition, secure hardware, facility rehabilitation.
Department of Tourism - Regional marketing campaigns, tourism infrastructure, event coordination.
DSAC (Department of Sports, Arts & Culture) - Cultural heritage conservation, sports kit manufacturing, national exhibitions.
DSI (Department of Science & Innovation) - Research funding schemes, university laboratory instrumentation, advanced ICT.
DCDT (Department of Communications & Digital Technologies) - Broadband rollout consultancies, public telecommunication bids.
DSBD (Department of Small Business Development) - SMME training, mentorship management software, exhibition logistics.
DHS (Department of Human Settlements) - Social housing projects, urban bulk infrastructure, planning consultancies.
COGTA (Department of Cooperative Governance & Traditional Affairs) - Municipal SCM audit consultancies, support programs.
DPSA (Department of Public Service & Administration) - National public services training platforms, HR management systems.
DTIC (Department of Trade, Industry & Competition) - SEZ feasibility studies, industrial park construction, economic research.
DPME (Department of Planning, Monitoring & Evaluation) - State performance monitoring software, data analysis consulting.
The Presidency - Specialized legal consulting, high-level advisory panels, administrative support bids.
II. Major State-Owned Enterprises (SOEs - 15 Sources)
Eskom - Grid upgrades, transformer repairs, power station maintenance (EE / ME Grades 1-9).
SANRAL - Toll gate mechanics, highway paving, bridge structures (CE Grades 6-9).
Transnet - Rail wagons, locomotive repairs, harbor marine dredging, bulk fuel pipelines (ME / CE).
PRASA (Passenger Rail Agency of SA) - Station cleaning, signal repairs, passenger coaches, station security.
Landbank (Land & Agricultural Development Bank of SA) - Financial auditing, banking software, agricultural advisory.
SABC (South African Broadcasting Corporation) - Studio cameras, acoustic insulation, satellite rigs, media consulting.
ACSA (Airports Company South Africa) - Airport runway resurfacing, baggage systems, airport retail logistics.
Denel - Defence component fabrication, precision manufacturing, specialized aeronautical consultancies.
Sentech - Signal towers, RF transmitters, telecom infrastructure, mast maintenance.
SAFCOL (South African Forestry Company) - Forest equipment, timber shipping, environmental rehabilitation.
NECSA (South African Nuclear Energy Corporation) - Nuclear safety research gear, hazardous chemical logistics.
PetroSA - Offshore gas rigs, oil refinery turnarounds, coastal pipeline maintenance.
Broadband Infraco - Nationwide fiber layout, backhaul connections, telecom software.
ATNS (Air Traffic & Navigation Services) - Air traffic control tech, radar maintenance, navigation consultancies.
Alexkor - Diamond mining equipment, coastal land rehabilitation, security details.
III. Regional Water Boards (10 Sources)
Rand Water - Giant water treatment basins, trunk main pipelines (Gauteng & Free State).
Umgeni Water - Dam walls, bulk purification units, water distribution networks (KwaZulu-Natal).
Mhlathuze Water - Desalination plants, water pipeline structures (Northern KZN).
Overberg Water - Water pipelines, bulk storage tanks (Western Cape).
Amatola Water - Community water schemes, treatment logistics (Eastern Cape).
Lepelle Northern Water - Regional pipeline maintenance, water tankers (Limpopo).
Magalies Water - Reservoir construction, distribution lines (North West).
Bloem Water - Water quality laboratory supplies, reservoir upgrades (Free State).
Sedibeng Water - Pump station repairs, rural water piping (Free State & North West).
TCTA (Trans-Caledon Tunnel Authority) - Mega-tunnel financing, heavy subterranean engineering.
IV. Development Finance Institutions & Regulators (10 Sources)
DBSA (Development Bank of Southern Africa) - Municipal infrastructure design, mega-project consultancies.
IDC (Industrial Development Corporation) - SMME development software, economic feasibility studies, auditing.
SARS (South African Revenue Service) - Customs inspection hardware, border scanning tech, enterprise ICT.
SAMSA (South African Maritime Safety Authority) - Ocean pollution cleanup, vessel safety inspections, salvage consultancies.
SANParks (South African National Parks) - Game reserve fencing, tourist road paving, lodge upkeep.
SEDA (Small Enterprise Development Agency) - Entrepreneurship training, incubation software, marketing consulting.
sefa (Small Enterprise Finance Agency) - Credit scoring systems, loan management platforms, software.
RAF (Road Accident Fund) - Legal panel services, medical assessment panels, cloud database operations.
Compensation Fund (COIDA) - Injury claim systems, physical rehabilitation consulting, medical scanning equipment.
UIF (Unemployment Insurance Fund) - Fraud prevention systems, payout software, financial auditing.
V. Provincial Government Treasuries (All 9 Provinces)
Gauteng Provincial Treasury - Central Gauteng eTenders register.
Western Cape Provincial Treasury - WC Government Tender Portal.
KwaZulu-Natal Provincial Treasury - KZN Treasury Procurement Hub.
Eastern Cape Provincial Treasury - EC Bid Notification Board.
Free State Provincial Treasury - FS Central eTenders database.
Limpopo Provincial Treasury - LP Bid Register.
Mpumalanga Provincial Treasury - MP Procurement bulletin.
North West Provincial Treasury - NW Treasury bids list.
Northern Cape Provincial Treasury - NC Procurement portal.
VI. Provincial Infrastructure & SCM Departments (15 Sources)
Gauteng Department of Infrastructure Development (GDID) - Hospital and school building.
Gauteng Department of Roads and Transport (GDRT) - Provincial road networks, bridges.
Gauteng Department of Education (GDE) - Classroom mobile units, textbooks, catering.
Gauteng Department of Health (GDH) - Local clinic supplies, medical logistics.
Western Cape Department of Infrastructure (WCDI) - Housing, provincial facilities.
Western Cape Department of Health & Wellness - Clinic maintenance, medicine transport.
KZN Department of Transport (KZN DoT) - District roads, bridge building.
KZN Department of Human Settlements - Social housing developments, civil services.
Eastern Cape Department of Public Works - EC office maintenance, school construction.
Eastern Cape Department of Education - School nutritional programs, mobile classrooms.
Free State Department of Police, Roads & Transport - Provincial road overlays, security gear.
Limpopo Department of Public Works, Roads & Infrastructure - Rural road construction, bridges.
Mpumalanga Department of Education - Textbook distribution, school structural repairs.
North West Department of Public Works and Roads - Tar road resurfacing, building repairs.
Northern Cape Department of Roads and Public Works - Desert road maintenance, government offices.
VII. Metropolitan Municipalities (The "Big 8" Cities)
City of Johannesburg (CoJ) - Gauteng urban electrical grids, road paving, water pipes.
City of Cape Town (CoCT) - Western Cape coastal civil works, municipal IT, waste plants.
eThekwini Metropolitan Municipality (Durban) - KZN coastal ports roads, local water structures.
City of Tshwane (Pretoria) - Capital city administration infrastructure, local road works.
Ekurhuleni Metropolitan Municipality (East Rand) - Heavy industrial bulk infrastructure, SCM.
Nelson Mandela Bay Municipality (Gqeberha/PE) - Coastal industrial municipal roads, water lines.
Buffalo City Metropolitan Municipality (East London) - Waste management, park upgrades, security systems.
Mangaung Metropolitan Municipality (Bloemfontein) - Central city civil repairs, electrical maintenance.
VIII. Research & Scientific Councils (10 Sources)
SITA (State Information Technology Agency) - Government ICT, software, and hardware.
Sentech - Telecommunications, digital platforms, signal tower construction.
CSIR (Council for Scientific & Industrial Research) - Advanced chemical research, high-tech lab equipment.
NHLS (National Health Laboratory Service) - Clinical diagnostic gear, mobile clinics, lab consumables.
SANSA (South African National Space Agency) - Satellite tracking, remote sensing software, space science gear.
Council for Geoscience - Land seismic mapping, deep core drilling, geophysics consultancies.
Mintek - Minerals research, metallurgy consultancies, metallurgical lab supplies.
HSRC (Human Sciences Research Council) - Large-scale socio-economic surveys, census software.
WRC (Water Research Commission) - Water preservation consulting, hydrology research grants.
SABS (South African Bureau of Standards) - Testing laboratories, standards compliance auditing software.
IX. Major High-Value District Municipalities (9 Sources)
West Rand District Municipality (Gauteng)
Sedibeng District Municipality (Gauteng)
Cape Winelands District Municipality (Western Cape)
Garden Route District Municipality (Western Cape)
King Cetshwayo District Municipality (KZN)
iLembe District Municipality (KZN)
OR Tambo District Municipality (Eastern Cape)
Capricorn District Municipality (Limpopo)
Ehlanzeni District Municipality (Mpumalanga)
7. Phase 2 (Tomorrow): Ethical & Legal Go-To-Market & Lead Harvesting
To transition this technical infrastructure into a commercial powerhouse, tomorrow's sprint will focus on ethically and legally identifying active contractors and suppliers to solicit them for our compliance matching and proposal generation service.

A. Core Directives for Legal & Ethical Lead Generation
We operate strictly within South African legislative boundaries:

POPIA Compliance (Protection of Personal Information Act): We do not harvest private, non-consenting personal data. We strictly utilize public-domain business registries, open state records, and official direct business-to-business communications.
Opt-In and Frictionless Opt-Out: All B2B outreach will carry immediate, one-click opt-out capabilities and clear, transparent descriptions of how public contact information was sourced.
B. Lead Identification Methodologies
We will execute three highly structured avenues to aggregate target business profiles:

Method 1: Public Bid Award Registers (Historical Win/Loss Analysis)
What it is: Under the Public Finance Management Act (PFMA) and Municipal Finance Management Act (MFMA), all South African organs of state are legally mandated to publish "Awarded Bids" registers. These public registers list:
Company names and registration numbers of winning bidders.
In many cases, lists of all companies that submitted bids for that specific tender (e.g. City of Johannesburg opening registers).
Execution: Write targeted scraper templates to parse public municipal "Bids Received" and "Bids Awarded" PDF files and web tables. This extracts high-intent, active businesses currently bidding in specific sectors (e.g., electrical, construction, IT).
Method 2: Public Professional Registries (CIDB Active Contractor Directories)
What it is: The Construction Industry Development Board (CIDB) maintains a fully public, legally mandated database of active contractors in South Africa.
Execution: Gather public database information of active construction companies graded 1 to 9. Since these businesses are grouped by grading levels (e.g., CE Grade 2, EE Grade 3), we can target those who have expired tax clearances or outdated profiles, offering them automated matching before their next bid.
Method 3: Official Supply Chain & Chamber Partnerships
What it is: Approaching formal public and private business facilitators who already aggregate lists of active vendors.
Execution: Create formal communication and value proposals for:
Local Business Chambers (e.g., Johannesburg Chamber of Commerce and Industry - JCCI, Cape Chamber of Commerce) to offer the tool as an exclusive value-add for their SMME members.
Municipal Supply Chain Management (SCM) Departments: Position Tender Getter RSA as a "Compliance Sieve Partner." SCM offices face massive delays due to SMMEs failing basic SBD compliance. By introducing them to our portal, they can direct local vendors to pre-screen their bids, dramatically reducing SCM administrative burdens.
8. Next Agent Playbook & Rapid Bootstrap Checklist
For future agents starting on this repository, do not build sprawling cloud wrappers. Follow this step-by-step technical implementation path immediately:

Verify Python Environment: Install standard lightweight requirements: pydantic, sqlite3, pypdf, pdfplumber, and google-generativeai.
Build src/tender_getter/schemas.py: Standardize the Pydantic models exactly as spec'd out in Section 2.
Build src/tender_getter/matcher.py: Write the binary gates and the BBBEE 80/20 & 90/10 point mapping.
Wire up src/tender_getter/parser.py: Connect to the Gemini 1.5 Pro API using Google AI Studio keys stored in a gitignored .env file.
Construct scripts/run_poc.py: A CLI runner that takes an inputted Company Profile, parses a mock/local SBD 1 PDF, executes the matcher, and spits out a clean Markdown terminal scorecard showing eligibility.
Deploy Ingestion Pipelines: Run and schedule run_poc.py and source_sync.py to continuously expand SQLite/PostgreSQL cached tenders.
Initiate Ethical Outreach Ingestion: Implement Phase 2's direct SCM and award register PDF parsers to generate a warm outreach pipeline of highly active SMME contractors.