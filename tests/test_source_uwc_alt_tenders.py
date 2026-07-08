"""Tests for the UWC (alt) tender source plug-in."""
import pytest


def test_uwc_alt_tenders_source_initialization():
    from tender_getter.sources.universities.uwc_alt_tenders import UwcAltSource
    src = UwcAltSource()
    assert src.source_id == "uwc_alt_tenders"
    assert src.live is True


def test_uwc_alt_tenders_parse_mock_html():
    from tender_getter.sources.universities.uwc_alt_tenders import UwcAltSource, MOCK_HTML
    src = UwcAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_uwc_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.uwc_alt_tenders import UwcAltSource
    src = UwcAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
