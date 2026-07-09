"""Tests for the University of the Witwatersrand tender source plug-in."""
import pytest


def test_wits_source_initialization():
    from tender_getter.sources.universities.wits import WitsSource
    src = WitsSource()
    assert src.source_id == "wits"
    assert isinstance(src.live, bool)


def test_wits_parse_mock_html():
    from tender_getter.sources.universities.wits import WitsSource, MOCK_HTML
    src = WitsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wits_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.wits import WitsSource
    src = WitsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
