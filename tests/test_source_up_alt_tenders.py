"""Tests for the UP (alt) tender source plug-in."""
import pytest


def test_up_alt_tenders_source_initialization():
    from tender_getter.sources.universities.up_alt_tenders import UpAltSource
    src = UpAltSource()
    assert src.source_id == "up_alt_tenders"
    assert src.live is True


def test_up_alt_tenders_parse_mock_html():
    from tender_getter.sources.universities.up_alt_tenders import UpAltSource, MOCK_HTML
    src = UpAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_up_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.up_alt_tenders import UpAltSource
    src = UpAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
