"""Tests for the John Taolo Gaetsewe District Municipality tender source plug-in."""
import pytest


def test_john_taolo_gaetsewe_dm_source_initialization():
    from tender_getter.sources.districts.john_taolo_gaetsewe_dm import JohnTaoloGaetseweDmSource
    src = JohnTaoloGaetseweDmSource()
    assert src.source_id == "john_taolo_gaetsewe_dm"
    assert isinstance(src.live, bool)


def test_john_taolo_gaetsewe_dm_parse_mock_html():
    from tender_getter.sources.districts.john_taolo_gaetsewe_dm import JohnTaoloGaetseweDmSource, MOCK_HTML
    src = JohnTaoloGaetseweDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_john_taolo_gaetsewe_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.john_taolo_gaetsewe_dm import JohnTaoloGaetseweDmSource
    src = JohnTaoloGaetseweDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
