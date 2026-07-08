"""Tests for the University of the Western Cape tender source plug-in."""
import pytest


def test_uwc_tenders_source_initialization():
    from tender_getter.sources.universities.uwc_tenders import UwcSource
    src = UwcSource()
    assert src.source_id == "uwc_tenders"
    assert src.live is True


def test_uwc_tenders_parse_mock_html():
    from tender_getter.sources.universities.uwc_tenders import UwcSource, MOCK_HTML
    src = UwcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_uwc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.uwc_tenders import UwcSource
    src = UwcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
