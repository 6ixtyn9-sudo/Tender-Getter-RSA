"""Tests for the DoT (alt) tender source plug-in."""
import pytest


def test_dot_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.dot_alt_tenders import DotAltSource
    src = DotAltSource()
    assert src.source_id == "dot_alt_tenders"
    assert src.live is True


def test_dot_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.dot_alt_tenders import DotAltSource, MOCK_HTML
    src = DotAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dot_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dot_alt_tenders import DotAltSource
    src = DotAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
