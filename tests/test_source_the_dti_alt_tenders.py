"""Tests for the DTIC (legacy) tender source plug-in."""
import pytest


def test_the_dti_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.the_dti_alt_tenders import TheDtiAltSource
    src = TheDtiAltSource()
    assert src.source_id == "the_dti_alt_tenders"
    assert src.live is True


def test_the_dti_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.the_dti_alt_tenders import TheDtiAltSource, MOCK_HTML
    src = TheDtiAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_the_dti_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.the_dti_alt_tenders import TheDtiAltSource
    src = TheDtiAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
