"""Tests for the Mantsopa (alt) tender source plug-in."""
import pytest


def test_mantsopa_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.mantsopa_alt_tenders import MantsopaAltSource
    src = MantsopaAltSource()
    assert src.source_id == "mantsopa_alt_tenders"
    assert src.live is False


def test_mantsopa_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.mantsopa_alt_tenders import MantsopaAltSource, MOCK_HTML
    src = MantsopaAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mantsopa_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.mantsopa_alt_tenders import MantsopaAltSource
    src = MantsopaAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
