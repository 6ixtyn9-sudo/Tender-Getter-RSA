"""Tests for the Sakhisizwe (alt) tender source plug-in."""
import pytest


def test_sakhisizwe_lm_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.sakhisizwe_lm_alt_tenders import SakhisizweLmAltSource
    src = SakhisizweLmAltSource()
    assert src.source_id == "sakhisizwe_lm_alt_tenders"
    assert src.live is False


def test_sakhisizwe_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.sakhisizwe_lm_alt_tenders import SakhisizweLmAltSource, MOCK_HTML
    src = SakhisizweLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sakhisizwe_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.sakhisizwe_lm_alt_tenders import SakhisizweLmAltSource
    src = SakhisizweLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
