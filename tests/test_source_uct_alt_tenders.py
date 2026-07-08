"""Tests for the UCT (alt) tender source plug-in."""
import pytest


def test_uct_alt_tenders_source_initialization():
    from tender_getter.sources.universities.uct_alt_tenders import UctAltSource
    src = UctAltSource()
    assert src.source_id == "uct_alt_tenders"
    assert src.live is True


def test_uct_alt_tenders_parse_mock_html():
    from tender_getter.sources.universities.uct_alt_tenders import UctAltSource, MOCK_HTML
    src = UctAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_uct_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.uct_alt_tenders import UctAltSource
    src = UctAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
