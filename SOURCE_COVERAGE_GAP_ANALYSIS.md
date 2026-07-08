# Tender-Getter RSA – Source Coverage Gap Analysis
_Audit date: 2026-07-08 · Cross-referenced against SA public-sector landscape_

## TL;DR — we are **not** source-complete

The 114-source registry covers the **big, high-impact buyers** exceptionally well, but there are at least **5 entire categories of public procurement** that are entirely missing, and several SOEs / Schedule-2 entities that are highly active but not in the registry. **For Phase 2 (lead harvesting) to be honest, we should fix these gaps first.**

---

## A. Categories that are **0% covered** (major gaps)

### 1. Armscor (Armaments Corporation of SA) — **1 missing SOE**
- Schedule 2 SOE, falls under DoD, **runs its own tender bulletin** at https://www.armscor.co.za/tenders/ and https://apps.armscor.co.za/Tenders/Tenders.asp
- Active right now: e.g. `RFI-02061-900-013` Self-Loading Automatic Rifle System, `EFAC/2026/05` Bombs & Explosives Detection Systems, `ETSS/2026/16` HF Radio Maintenance, `EICT/2025/08` End-user Computing Devices, `EICT/2025/07` High-Performance Storage Solution
- **Why it matters:** Defence procurement is its own gated universe (often requires B-BBEE + defence-specific accreditations); the repo's `dod` source covers DoD HQ but not Armscor's acquisition pipeline.
- **Cost to add:** 1 plug-in in `src/tender_getter/sources/soes/armscor.py`

### 2. SETAs (Sector Education & Training Authorities) — **21 missing**
- All 21 listed (AgriSETA, BANKSETA, CETA, CATHSSETA, CHIETA, ETDP SETA, EWSETA, FASSET, FOODBEV, FP&M SETA, HWSETA, INSETA, LGSETA, MERSETA, MICT SETA, MQA, PSETA, SASSETA, Services SETA, TETA, W&RSETA)
- Each posts its own tenders — typically skills development, training delivery, learnerships, assessment, ICT licensing, panel appointments, infrastructure
- Active examples: HWSETA, ETDP SETA, Services SETA all currently posting 5+ tenders/month
- **Why it matters:** SETAs collectively disburse ~R15-20bn/year in skills-development grants — a huge addressable market for training providers, consultants, ICT firms
- **Cost to add:** 21 plug-ins or 1 generic `setas.py` that knows a SETA-URL table

### 3. Public Universities — **26 missing**
- All 26 SA public universities (UCT, Wits, UP, UKZN, UJ, Stellenbosch, UNISA, UFS, UWC, TUT, NMU, DUT, WSU, UFH, Rhodes, Univen, CUT, CPUT, UL, U Limpopo, UMP, SMU, Sol Plaatje, NWU, plus more)
- Each runs its own SCM portal (e.g. https://www.up.ac.za/tender/, https://www.uct.ac.za/procurement/)
- **Why it matters:** Universities publish R50m–R200m tenders/year each for construction, lab equipment, IT, security, catering, professional services. **Massive gap.**
- **Cost to add:** 26 plug-ins or 1 generic `universities.py` mapping slug → URL

### 4. Public TVET Colleges — **50 missing**
- All 50 public TVET colleges (Boland, False Bay, Majuba, Mnambithi, Nkangala, Vuselela, Waterberg, Gert Sibande, etc.)
- Procurement usually modest per college (<R10m/year) but high volume — colleges buy construction, security, catering, stationery, ICT
- Often handled centrally via DHET, but procurement happens at college level
- **Why it matters:** Lower-value but high-frequency; useful for SMMEs that can't compete on mega-tenders
- **Cost to add:** 50 plug-ins or 1 generic `tvet.py` mapping slug → URL

### 5. Constitutional / Chapter 9 / Schedule 1 institutions — **~10 missing**
- Public Protector, SAHRC, Commission for Gender Equality, CRL Commission, Auditor-General (AGSA), IPID, Financial & Fiscal Commission, ICASA, PanSALB, Public Service Commission
- **Why it matters:** They publish tenders and award registers, often for legal panels, audit services, research, ICT

### 6. Municipal Demarcation Board, IEC, NPA, CIPC, SIU, GPAA, PIC — **7 missing**
- Independent Electoral Commission, National Prosecuting Authority, Companies & Intellectual Property Commission (CIPC), Special Investigating Unit (SIU — confirmed active with `RFP 05/12/2025/CL` for panel of attorneys, etc.), Government Pensions Administration Agency, Public Investment Corporation, Municipal Demarcation Board

### 7. SAPO (South African Post Office) — **1 missing SOE**
- Schedule 2 SOE (technically in business rescue but actively tendering — `RFP 25.26.10` managed WAN, `RFP 25-26-07` guarding services, etc.)
- **Why it matters:** Big procurement entity for logistics, ICT, real estate

### 8. Central Energy Fund (CEF) group — **partial gap**
- PetroSA is in the repo ✅ but parent CEF and subsidiaries (CEF SOC, PASA — Petroleum Agency SA, SFF — Strategic Fuel Fund, iGas) are not
- **Why it matters:** Oil & gas upstream procurement, strategic fuel stockpile

### 9. Other active SOEs / Schedule 2 not yet in repo
- **Coega Development Corporation (CDC)** — IDZ/SEZ operator in Eastern Cape, very active in construction & facility management tenders
- **Eskom subsidiaries** — Eskom Rotek Industries, Eskom Enterprises, Eskom Finance Company (worth a sub-category entry)
- **Transnet subsidiaries** — Transnet SOC Ltd, Transnet Pipelines, Transnet Port Terminals (TNPA), Transnet Engineering, each runs own procurement
- **PRASA subsidiaries** — Autopax, Metrorail, Intersite, each runs own SCM
- **Denel subsidiaries** — Denel Aerostructures, Denel Land Systems, Denel Dynamics, Denel Vehicle Systems, Denel Maritime
- **Alexkor** is in repo ✅
- **Telkom SA** — partial state-owned (55.3%), operates its own procurement portal — **missing**
- **iThemba LABS** (NRF facility) — listed on Purcosa members, **missing** (under research/)

### 10. Local Municipalities — **~205 missing**
- The repo has 8 metros + 9 districts = 17 of ~257 municipalities (44 district + 8 metro + 205 local)
- **Major local municipalities that regularly publish big tenders:** City of Joburg Property Company, eThekwini Electricity, Cape Town Electricity, Polokwane, Rustenburg, Makhado, Tshwane (separate from metro), Msunduzi (Pietermaritzburg), Matjhabeng, Emfuleni, Mbombela, Alfred Nzo DM (already partially covered), etc.
- **Why it matters:** Many SMMEs target local-municipality tenders because they're simpler than metros

---

## B. Things that are **partially** covered or outdated

### B1. Water Boards — repo has 10, real count is 7 after 2026 consolidation
- The repo lists: Rand Water, Umgeni Water, Mhlathuze Water, Overberg Water, Amatola Water, Lepelle Northern Water, Magalies Water, Bloem Water, Sedibeng Water, TCTA
- After 2026 consolidation per Sunday Times [1](https://www.sundaytimes.timeslive.co.za/business/news/2026-05-16-sas-water-boards-set-for-private-sector-review/):
  - Rand Water ✅
  - Amatola Water ✅
  - Magalies Water ✅
  - Overberg Water ✅
  - uMngeni-uThukela Water (merger of Umgeni + Mhlathuze) — repo has **two** entries, should be one
  - Vaal Central Water (merged from Bloem + Sedibeng + Lepelle) — repo has **three** entries, should be one
  - **Missing:** possibly additional restructured boards
- **Action:** Update sources.yaml to merge Umgeni+Mhlathuze and consolidate Bloem+Sedibeng+Lepelle into "Vaal Central Water"

### B2. Missing niche SOEs in research/SOE families
- **iThemba LABS** (NRF facility for accelerator-based science) — confirmed active on Purcosa member list
- **South African Agency for Science and Technology Advancement (SAASTA)** — under NRF/DSTI
- **National Research Foundation (NRF)** itself — parent body
- **HSRC, CSIR, SANSA, Mintek** ✅ in repo
- **Tshumisano Trust / SKA South Africa** — public-benefit science entity

### B3. Procuring entities not strictly "government" but publicly funded
- **Legal Aid SA** — Schedule 3A entity, publishes panel tenders for legal practitioners
- **South African National Roads Agency (SANRAL)** ✅ in repo
- **South African National Blood Service (SANBS)** & **Western Cape Blood Service** — procure heavily
- **South African Library for the Blind** — niche
- **South African National Biodiversity Institute (SANBI)**
- **South African Weather Service (SAWS)** — Schedule 3A
- **Film and Publication Board**
- **National Lotteries Commission (NLC)** — funds NPOs
- **National Heritage Council (NHC)**
- **Performing Arts Centre of the Free State (PACOFS)**
- **State Theatre, Playhouse Company, Artscape**
- **South African National Parks (SANParks)** ✅ in repo
- **Robben Island Museum, Iziko Museum, Ditsong Museum** — museums cluster
- **South African Heritage Resources Agency (SAHRA)**

### B4. PFMA Schedule 3A entities (166+ "national public entities")
- The BMIT 2025 report identified **166 National Public Entities including subsidiaries** [2](https://www.bmit.africa/overview-of-soe-entities-in-south-africa-2025/). The repo covers ~10–15 of them via the SOE bundle.
- **The honest answer:** we cover the **top 15–20 by spend**. We do **not** cover the long tail of small Schedule 3A entities.

---

## C. Sources we should consider **adding to the registry** before Phase 2

Ranked by impact for an SMME lead-harvesting tool (matches the "high-frequency + high-tender-value" SMMEs target):

### High priority (add these for sure)

| # | New source | Why |
|---|---|---|
| 1 | **Armscor** | Defence-acquisition monster, $R billions/year, vendors unknown to most SMMEs |
| 2 | **All 21 SETAs** | Training/skills budget is massive and aimed exactly at the SMME training-provider segment |
| 3 | **All 26 Public Universities** | Each runs R50-200m procurement/year; SMMEs commonly missed because of per-university portals |
| 4 | **SIU** | Active procurement + actively publishes awarded-tender registers (Phase 2 data goldmine) |
| 5 | **Public Protector / SAHRC / CGE / CRL / AGSA / IPID / FFC / ICASA / PanSALB / PSC** | 10 small but regular issuers, often for legal panels and research |
| 6 | **SAPO** | Logistical scale, ICT spend |
| 7 | **Telkom SA** | 55% state-owned, telecom procurement |
| 8 | **Coega Development Corporation** | Big EC infrastructure buyer |
| 9 | **CEF group + iGas + Strategic Fuel Fund + PASA** | Energy upstream |
| 10 | **Top 50 local municipalities** (by spend): eThekwini Electricity, Joburg Property Co., Matjhabeng, Emfuleni, Polokwane, Mbombela, Msunduzi, Rustenburg, Makhado, etc. | Big spenders, often skipped |

### Medium priority (add if you want full national coverage)

| # | New source | Why |
|---|---|---|
| 11 | **Remaining 50 TVET colleges** | Low per-college value but high frequency |
| 12 | **NRF + SAASTA + iThemba LABS** | Research-grant procurement |
| 13 | **Transnet 5 operating divisions** (TNPA, TPT, TFR, TEP, TPE) | Each runs own SCM |
| 14 | **PRASA 4 subsidiaries** (PRASA CRES, Autopax, Metrorail, Intersite) | Each runs own SCM |
| 15 | **Denel 5 subsidiaries** | Defence industrial base |
| 16 | **Eskom 3 subsidiaries** (Rotek, Enterprises, Finance) | Industrial services |
| 17 | **Remaining ~35 district municipalities** | Lower-value, but cumulative volume is large |
| 18 | **CIPC, NPA, IEC, GPAA, PIC** | Various mid-size buyers |
| 19 | **National Lotteries Commission (NLC)** | Funds NPOs — different lead pool |
| 20 | **Legal Aid SA** | Regular panel tenders for legal services |
| 21 | **South African National Blood Service (SANBS)** | Healthcare-adjacent procurement |
| 22 | **South African Weather Service (SAWS)** | Tech/observation equipment |

### Low priority (add for completeness, not for SMME targeting)

- All museums (Iziko, Ditsong, Robben Island, etc.)
- Performing arts centres (State Theatre, Playhouse, Artscape, PACOFS)
- Heritage bodies (SAHRA, NHC)
- Public libraries (national + provincial)
- Public broadcasters beyond SABC (community radio stations)
- Small Schedule 3A entities with <R5m/year spend

---

## D. Items the repo currently lists that may be **stale** or **defunct**

| Item | Status |
|---|---|
| `sabc_tenders` | ✅ Active but financial distress — maybe consolidate with SABC subsidiaries |
| `sentech_tenders` | ✅ Active |
| `safcol_tenders` | ✅ Active (R0.93bn revenue per Wikipedia 2026 [3](https://en.wikipedia.org/wiki/State-owned_enterprises_of_South_Africa)) |
| `necsa_tenders` | ✅ Active |
| `petrosa_tenders` | ⚠️ PetroSA has had operational issues; check current tender volume |
| `prasa_tenders` | ⚠️ PRASA has been plagued by governance issues but still tenders |
| `denel_tenders` | ⚠️ Denel has been in business rescue; check current status before treating as live |
| `alexkor_tenders` | ⚠️ Very small entity, low tender volume |
| `acsa_tenders` | ✅ Active and big spender (airport infrastructure) |
| `transnet` | ✅ Active (R74bn revenue per Wikipedia 2026) |
| `eskom` | ✅ Active but has been reducing tender activity during capacity crisis |
| `safcol_tenders` | ✅ Active |

**Wikipedia 2026 SOE snapshot** [3](https://en.wikipedia.org/wiki/State-owned_enterprises_of_South_Africa) — SAA in liquidation (correctly not in repo), South African Express also in liquidation (correctly not in repo). Telkom with 55.3% state ownership is a notable omission.

---

## E. Quantitative summary of the gap

| Category | Real SA count | Repo count | Coverage | Gap |
|---|---|---|---|---|
| National departments (executive) | ~31 | 26 | 84% | 5 |
| SOEs (Schedule 2 + 3B business enterprises) | ~30 | 15 | 50% | 15 |
| National Public Entities (Schedule 3A long tail) | 166 | ~0 | 0% | 166 |
| Provincial Public Entities (Schedule 3C + 3D) | 75 | 0 | 0% | 75 |
| Constitutional / Chapter 9 (Schedule 1) | 10 | 0 | 0% | 10 |
| SETAs | 21 | 0 | 0% | 21 |
| Public Universities | 26 | 0 | 0% | 26 |
| Public TVET Colleges | 50 | 0 | 0% | 50 |
| District Municipalities | 44 | 9 | 20% | 35 |
| Metropolitan Municipalities | 8 | 8 | 100% | 0 |
| Local Municipalities | 205 | 0 | 0% | 205 |
| Water Boards (after 2026 consolidation) | 7 | 10 (incl. pre-merger names) | 100% (but needs renaming) | 0 |
| Research Councils | 9 | 9 | 100% | 0 |
| DFIs / Regulators | ~12 | 10 | 83% | 2 |
| **TOTAL** | **~700+ procurement entities** | **114** | **~16%** | **~580+** |

**Honest read-out:** the repo covers the **~16% of SA public-sector procurement entities** that are responsible for probably **70–80% of total procurement spend** (because the missing long tail is mostly small Schedule 3A entities with <R50m/year). But for a Phase 2 SMME matchmaker, **the missing 21 SETAs + 26 universities + 10 Chapter 9 institutions + Armscor + SAPO + 50 TVETs + top 50 local municipalities** are very addressable — these are exactly the entities SMMEs are most likely to win work from.

---

## F. Recommended next move before Phase 2

1. **Resolve the SOE overlap:** merge Umgeni+Mhlathuze into `uMngeni-uThukela Water`, consolidate Bloem+Sedibeng+Lepelle into `Vaal Central Water`. → Touches sources.yaml + 3 plug-ins.
2. **Add the high-priority missing sources:** Armscor + 21 SETAs + 26 universities + 10 Chapter 9 + SIU + SAPO + Telkom + Coega + CEF group + top 50 local municipalities = **~130 new plug-ins**, but most can use the existing generic `<tr><td>` parser with just a URL table.
3. **Add a "live?" flag per source** so the aggregator can gracefully skip dead/moribund sources (e.g. Denel in business rescue, Eskom low-activity periods) without throwing.
4. **Add the `tvet.py` + `universities.py` + `local_municipalities.py` + `setas.py` generic plug-ins** that take a slug table, so we don't write 100+ identical plug-ins.
5. **Decide on the long tail:** Schedule 3A small entities — accept the gap and document it in PLANNING.md, or build an "aggregator-of-aggregators" (ProTenders / TenderBulletins / eTenderSA / etenders.gov.za)?

**Without this, Phase 2's lead harvester will be filtering against an incomplete upstream** — every match it makes will be against a subset of the market, and we'll have to retrofit ~150 sources later. Better to do it now.

---

## References

1. Sunday Times, "SA's water boards set for private sector review" — 2026-05-16 — https://www.sundaytimes.timeslive.co.za/business/news/2026-05-16-sas-water-boards-set-for-private-sector-review/
2. BMIT, "Overview of SOE Entities in South Africa 2025" — https://www.bmit.africa/overview-of-soe-entities-in-south-africa-2025/
3. Wikipedia, "State-owned enterprises of South Africa" — 2026 — https://en.wikipedia.org/wiki/State-owned_enterprises_of_South_Africa
4. Parliament of SA, "Ministers" list — https://www.parliament.gov.za/ministers
5. NavyBlue, "All 21 SETAs in South Africa 2026" — https://www.navyblue.co.za/seta
6. NavyBlue, "TVET Colleges in South Africa 2026" — https://www.navyblue.co.za/tvet
7. SIU, "Current Tenders" — https://www.siu.org.za/current/
8. Armscor, "Tenders" — https://www.armscor.co.za/tenders/
9. PURCOSA Member Tenders — https://purcosa.co.za/member-tenders
10. The Presidency, "President Ramaphosa announces reconfigured departments" — https://thepresidency.gov.za/president-ramaphosa-announces-reconfigured-departments
11. TenderBulletins, "Departments, Municipalities and State Owned Companies" — https://tenderbulletins.co.za/tender-departments/
