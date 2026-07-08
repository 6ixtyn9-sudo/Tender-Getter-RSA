"""Tests for the Rhodes (alt) tender source plug-in."""
import pytest


def test_rhodes_alt_tenders_source_initialization():
    from tender_getter.sources.universities.rhodes_alt_tenders import RhodesAltSource
    src = RhodesAltSource()
    assert src.source_id == "rhodes_alt_tenders"
    assert src.live is True


def test_rhodes_alt_tenders_parse_mock_html():
    from tender_getter.sources.universities.rhodes_alt_tenders import RhodesAltSource, MOCK_HTML
    src = RhodesAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_rhodes_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.rhodes_alt_tenders import RhodesAltSource
    src = RhodesAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
