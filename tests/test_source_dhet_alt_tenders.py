"""Tests for the Department of Higher Education and Training (alt URL) tender source plug-in."""
import pytest


def test_dhet_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.dhet_alt_tenders import DhetAltSource
    src = DhetAltSource()
    assert src.source_id == "dhet_alt_tenders"
    assert src.live is True


def test_dhet_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.dhet_alt_tenders import DhetAltSource, MOCK_HTML
    src = DhetAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dhet_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dhet_alt_tenders import DhetAltSource
    src = DhetAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
