"""Tests for the UKZN (alt) tender source plug-in."""
import pytest


def test_ukzn_alt_tenders_source_initialization():
    from tender_getter.sources.universities.ukzn_alt_tenders import UkznAltSource
    src = UkznAltSource()
    assert src.source_id == "ukzn_alt_tenders"
    assert src.live is True


def test_ukzn_alt_tenders_parse_mock_html():
    from tender_getter.sources.universities.ukzn_alt_tenders import UkznAltSource, MOCK_HTML
    src = UkznAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ukzn_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.ukzn_alt_tenders import UkznAltSource
    src = UkznAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
