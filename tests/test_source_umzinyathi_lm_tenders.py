"""Tests for the uMzinyathi LM tender source plug-in."""
import pytest


def test_umzinyathi_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.umzinyathi_lm_tenders import UmzinyathiLmSource
    src = UmzinyathiLmSource()
    assert src.source_id == "umzinyathi_lm_tenders"
    assert src.live is False


def test_umzinyathi_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.umzinyathi_lm_tenders import UmzinyathiLmSource, MOCK_HTML
    src = UmzinyathiLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umzinyathi_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.umzinyathi_lm_tenders import UmzinyathiLmSource
    src = UmzinyathiLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
