"""Tests for the University of Cape Town tender source plug-in."""
import pytest


def test_uct_tenders_source_initialization():
    from tender_getter.sources.universities.uct_tenders import UctSource
    src = UctSource()
    assert src.source_id == "uct_tenders"
    assert src.live is True


def test_uct_tenders_parse_mock_html():
    from tender_getter.sources.universities.uct_tenders import UctSource, MOCK_HTML
    src = UctSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_uct_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.uct_tenders import UctSource
    src = UctSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
