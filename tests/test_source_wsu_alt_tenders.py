"""Tests for the WSU (alt) tender source plug-in."""
import pytest


def test_wsu_alt_tenders_source_initialization():
    from tender_getter.sources.universities.wsu_alt_tenders import WsuAltSource
    src = WsuAltSource()
    assert src.source_id == "wsu_alt_tenders"
    assert src.live is True


def test_wsu_alt_tenders_parse_mock_html():
    from tender_getter.sources.universities.wsu_alt_tenders import WsuAltSource, MOCK_HTML
    src = WsuAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wsu_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.wsu_alt_tenders import WsuAltSource
    src = WsuAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
