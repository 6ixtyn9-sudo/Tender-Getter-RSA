# Tender-Getter RSA – Source Ingestion Status

Generated: 2026-07-08

## Implemented (12 / 112)

| # | Source ID | Name | Module | Test | YAML |
|---|-----------|------|--------|------|------|
| 1 | etenders_ocds | National Treasury eTenders OCDS API | `sources/etenders_ocds.py` | yes (pipelines) | ✅ |
| 2 | etenders_csv | National Treasury eTenders Bulk CSV | `sources/etenders_csv.py` | yes | ✅ |
| 3 | cidb_itender | CIDB i-Tender | `sources/cidb.py` | yes | ✅ |
| 4 | gauteng_etenders | Gauteng eTenders | `sources/gauteng.py` | yes | ✅ |
| 5 | westerncape_tenders | Western Cape Government Tenders | `sources/westerncape.py` | yes | ✅ |
| 6 | kzn_treasury | KwaZulu-Natal Treasury | `sources/kzn.py` | yes | ✅ |
| 7 | eskom | Eskom Tender Bulletin | `sources/eskom.py` | yes | ✅ |
| 8 | transnet | Transnet eTenders | `sources/transnet.py` | yes | ✅ |
| 9 | sanral | SANRAL | `sources/sanral.py` | yes | ✅ |
| 10 | sita_tenders | SITA | `sources/sita.py` | yes | ✅ *(added to YAML 2026-07-08)* |
| 11 | capetown_tenders | City of Cape Town | `sources/capetown.py` | yes | ✅ *(added to YAML 2026-07-08)* |
| 12 | **johannesburg_tenders** | **City of Johannesburg** | **`sources/johannesburg.py`** | **yes** | **✅ NEW** |

**New in this run:** `JohannesburgSource` – City of Johannesburg Metropolitan Municipality
- URL: https://joburg.org.za/work_/Pages/2025-Tenders-and-Quotations/Bid-Opening-Registers.aspx
- Parser: regex table parser, CIDB auto-extract, province auto-detect (Gauteng default)
- Mock fallback: 3 tenders (EE 4, CE 6, Building Materials)
- Tests: 3/3 passed, full suite: 95/95 passed

---

## Missing – Priority Queue (from PLANNING.md §6)

### Metropolitan Municipalities – Big 8 (6 remaining)
1. **eThekwini Metropolitan Municipality (Durban)** – NEXT RECOMMENDED
2. City of Tshwane (Pretoria)
3. Ekurhuleni Metropolitan Municipality (East Rand)
4. Nelson Mandela Bay Municipality (Gqeberha/PE)
5. Buffalo City Metropolitan Municipality (East London)
6. Mangaung Metropolitan Municipality (Bloemfontein)

### Provincial Treasuries (6 remaining)
- Eastern Cape Provincial Treasury
- Free State Provincial Treasury
- Limpopo Provincial Treasury
- Mpumalanga Provincial Treasury
- North West Provincial Treasury
- Northern Cape Provincial Treasury

### SOEs (12 remaining)
PRASA, Landbank, SABC, ACSA, Denel, Sentech, SAFCOL, NECSA, PetroSA, Broadband Infraco, ATNS, Alexkor

### Water Boards (10)
Rand Water, Umgeni Water, Mhlathuze Water, Overberg Water, Amatola Water, Lepelle Northern Water, Magalies Water, Bloem Water, Sedibeng Water, TCTA

### Development Finance / Regulators (10)
DBSA, IDC, SARS, SAMSA, SANParks, SEDA, sefa, RAF, Compensation Fund, UIF

### Research Councils (8 remaining)
CSIR, NHLS, SANSA, Council for Geoscience, Mintek, HSRC, WRC, SABS

### National Departments (26)
All currently covered via eTenders OCDS – individual department scrapers are deprioritized.

### Provincial Infrastructure Depts (15)
GDID, GDRT, GDE, GDH, WCDI, WC Health, KZN DoT, KZN Human Settlements, EC Public Works, EC Education, FS Police/Roads, Limpopo Public Works, Mpumalanga Education, NW Public Works, NC Roads

### District Municipalities (9)
West Rand, Sedibeng, Cape Winelands, Garden Route, King Cetshwayo, iLembe, OR Tambo, Capricorn, Ehlanzeni

---

## Ingestion Pattern (robust, maintainable)

Each source follows the Racket-Factory plugin protocol:

```python
class XxxSource:
    source_id: str = "xxx_tenders"
    def __init__(self, url: str = "...")
    def fetch(self, limit: Optional[int] = None, html_content: Optional[str] = None) -> List[TenderOpportunity]
    def parse_html(self, html: str, limit: Optional[int] = None) -> List[TenderOpportunity]
```

- Standard library only (urllib, re)
- High-fidelity MOCK_HTML fallback ensures POC works offline
- CIDB grading auto-extract via `re_search_cidb()`
- Province auto-detect via `province_from_text()`
- Closing dates via `parse_closing_date()` – handles ISO, DD/MM/YYYY, verbal dates
- Test file: `tests/test_source_xxx.py` – 3 tests minimum
- Registry entry in `src/tender_getter/sources.yaml`
- Export in `src/tender_getter/sources/__init__.py`

All 12 current sources pass: **95/95 tests green**.

---

## Next steps

Want me to continue with **eThekwini (Durban)** next? It's the #3 metro in the PLANNING.md Big 8, and pairs well with CoJ + CoCT for national metro coverage.

I can batch-add them one-by-one, with full test + registry updates each time, maintaining per-source isolation.
