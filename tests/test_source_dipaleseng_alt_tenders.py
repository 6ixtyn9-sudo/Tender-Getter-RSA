"""Tests for the Dipaleseng (alt) tender source plug-in."""
import pytest


def test_dipaleseng_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.dipaleseng_alt_tenders import DipalesengAltSource
    src = DipalesengAltSource()
    assert src.source_id == "dipaleseng_alt_tenders"
    assert src.live is False


def test_dipaleseng_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.dipaleseng_alt_tenders import DipalesengAltSource, MOCK_HTML
    src = DipalesengAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dipaleseng_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dipaleseng_alt_tenders import DipalesengAltSource
    src = DipalesengAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
