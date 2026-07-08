"""Tests for the Rustenburg (alt) tender source plug-in."""
import pytest


def test_rustenburg_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.rustenburg_alt_tenders import RustenburgAltSource
    src = RustenburgAltSource()
    assert src.source_id == "rustenburg_alt_tenders"
    assert src.live is True


def test_rustenburg_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.rustenburg_alt_tenders import RustenburgAltSource, MOCK_HTML
    src = RustenburgAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_rustenburg_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.rustenburg_alt_tenders import RustenburgAltSource
    src = RustenburgAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
