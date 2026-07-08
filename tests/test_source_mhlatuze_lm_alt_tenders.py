"""Tests for the uMhlathuze (alt) tender source plug-in."""
import pytest


def test_mhlatuze_lm_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.mhlatuze_lm_alt_tenders import MhlatuzeLmAltSource
    src = MhlatuzeLmAltSource()
    assert src.source_id == "mhlatuze_lm_alt_tenders"
    assert src.live is True


def test_mhlatuze_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.mhlatuze_lm_alt_tenders import MhlatuzeLmAltSource, MOCK_HTML
    src = MhlatuzeLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mhlatuze_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.mhlatuze_lm_alt_tenders import MhlatuzeLmAltSource
    src = MhlatuzeLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
