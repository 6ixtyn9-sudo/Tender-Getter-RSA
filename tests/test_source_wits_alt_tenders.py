"""Tests for the Wits (alt) tender source plug-in."""
import pytest


def test_wits_alt_tenders_source_initialization():
    from tender_getter.sources.universities.wits_alt_tenders import WitsAltSource
    src = WitsAltSource()
    assert src.source_id == "wits_alt_tenders"
    assert src.live is True


def test_wits_alt_tenders_parse_mock_html():
    from tender_getter.sources.universities.wits_alt_tenders import WitsAltSource, MOCK_HTML
    src = WitsAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wits_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.wits_alt_tenders import WitsAltSource
    src = WitsAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
