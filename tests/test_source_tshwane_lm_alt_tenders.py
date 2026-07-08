"""Tests for the Tshwane (alt) tender source plug-in."""
import pytest


def test_tshwane_lm_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.tshwane_lm_alt_tenders import TshwaneLmAltSource
    src = TshwaneLmAltSource()
    assert src.source_id == "tshwane_lm_alt_tenders"
    assert src.live is True


def test_tshwane_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.tshwane_lm_alt_tenders import TshwaneLmAltSource, MOCK_HTML
    src = TshwaneLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tshwane_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.tshwane_lm_alt_tenders import TshwaneLmAltSource
    src = TshwaneLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
