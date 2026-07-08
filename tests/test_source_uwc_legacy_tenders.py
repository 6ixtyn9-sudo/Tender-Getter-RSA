"""Tests for the University of the Western Cape (legacy) tender source plug-in."""
import pytest


def test_uwc_legacy_tenders_source_initialization():
    from tender_getter.sources.universities.uwc_legacy_tenders import UwcLegacySource
    src = UwcLegacySource()
    assert src.source_id == "uwc_legacy_tenders"
    assert src.live is True


def test_uwc_legacy_tenders_parse_mock_html():
    from tender_getter.sources.universities.uwc_legacy_tenders import UwcLegacySource, MOCK_HTML
    src = UwcLegacySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_uwc_legacy_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.uwc_legacy_tenders import UwcLegacySource
    src = UwcLegacySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
