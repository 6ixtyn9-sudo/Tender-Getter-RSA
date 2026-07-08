import pytest
from datetime import datetime, timezone
from tender_getter.sources.metros.mangaung import MangaungSource, MOCK_MANGAUNG_HTML

def test_mangaung_source_initialization():
    source = MangaungSource()
    assert source.source_id == "mangaung_tenders"
    assert source.url.startswith("http")

def test_mangaung_parse_mock_html():
    source = MangaungSource()
    tenders = source.parse_html(MOCK_MANGAUNG_HTML)
    
    assert len(tenders) == 3
    
    # Verify first tender
    t1 = tenders[0]
    assert t1.tender_id == "MMM/CE/2025/018"
    assert "Sewer Pipeline Replacement" in t1.title
    assert t1.required_cidb_class == "CE"
    assert t1.required_cidb_level == 5
    assert t1.location_target == "Free State"
    assert t1.closing_date.year == 2026
    assert t1.closing_date.month == 9
    assert t1.closing_date.day == 15

    # Verify second tender
    t2 = tenders[1]
    assert t2.tender_id == "MMM/EE/2025/004"
    assert t2.required_cidb_class == "EE"
    assert t2.required_cidb_level == 3
    assert t2.location_target == "Free State"

def test_mangaung_fetch_uses_fallback_on_empty_or_error():
    source = MangaungSource()
    tenders = source.fetch(html_content="<html><body>No tenders or tables here!</body></html>")
    assert len(tenders) == 3
    assert any(t.tender_id == "MMM/EE/2025/004" for t in tenders)
