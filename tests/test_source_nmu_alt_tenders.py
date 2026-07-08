"""Tests for the NMU (alt) tender source plug-in."""
import pytest


def test_nmu_alt_tenders_source_initialization():
    from tender_getter.sources.universities.nmu_alt_tenders import NmuAltSource
    src = NmuAltSource()
    assert src.source_id == "nmu_alt_tenders"
    assert src.live is True


def test_nmu_alt_tenders_parse_mock_html():
    from tender_getter.sources.universities.nmu_alt_tenders import NmuAltSource, MOCK_HTML
    src = NmuAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nmu_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.nmu_alt_tenders import NmuAltSource
    src = NmuAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
