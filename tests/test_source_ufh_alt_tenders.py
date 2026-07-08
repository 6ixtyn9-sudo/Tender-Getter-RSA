"""Tests for the UFH (alt) tender source plug-in."""
import pytest


def test_ufh_alt_tenders_source_initialization():
    from tender_getter.sources.universities.ufh_alt_tenders import UfhAltSource
    src = UfhAltSource()
    assert src.source_id == "ufh_alt_tenders"
    assert src.live is True


def test_ufh_alt_tenders_parse_mock_html():
    from tender_getter.sources.universities.ufh_alt_tenders import UfhAltSource, MOCK_HTML
    src = UfhAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ufh_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.ufh_alt_tenders import UfhAltSource
    src = UfhAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
