"""Tests for the Matjhabeng (alt) tender source plug-in."""
import pytest


def test_matjhabeng_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.matjhabeng_alt_tenders import MatjhabengAltSource
    src = MatjhabengAltSource()
    assert src.source_id == "matjhabeng_alt_tenders"
    assert src.live is True


def test_matjhabeng_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.matjhabeng_alt_tenders import MatjhabengAltSource, MOCK_HTML
    src = MatjhabengAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_matjhabeng_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.matjhabeng_alt_tenders import MatjhabengAltSource
    src = MatjhabengAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
