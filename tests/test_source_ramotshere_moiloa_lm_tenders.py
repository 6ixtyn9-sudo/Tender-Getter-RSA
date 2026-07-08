"""Tests for the Ramotshere Moiloa LM tender source plug-in."""
import pytest


def test_ramotshere_moiloa_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.ramotshere_moiloa_lm_tenders import RamotshereMoiloaLmSource
    src = RamotshereMoiloaLmSource()
    assert src.source_id == "ramotshere_moiloa_lm_tenders"
    assert src.live is False


def test_ramotshere_moiloa_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.ramotshere_moiloa_lm_tenders import RamotshereMoiloaLmSource, MOCK_HTML
    src = RamotshereMoiloaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ramotshere_moiloa_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ramotshere_moiloa_lm_tenders import RamotshereMoiloaLmSource
    src = RamotshereMoiloaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
