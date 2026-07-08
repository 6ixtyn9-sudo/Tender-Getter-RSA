"""Tests for the NWU (alt) tender source plug-in."""
import pytest


def test_nwu_alt_tenders_source_initialization():
    from tender_getter.sources.universities.nwu_alt_tenders import NwuAltSource
    src = NwuAltSource()
    assert src.source_id == "nwu_alt_tenders"
    assert src.live is True


def test_nwu_alt_tenders_parse_mock_html():
    from tender_getter.sources.universities.nwu_alt_tenders import NwuAltSource, MOCK_HTML
    src = NwuAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nwu_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.nwu_alt_tenders import NwuAltSource
    src = NwuAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
