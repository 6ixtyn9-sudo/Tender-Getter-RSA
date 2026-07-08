"""Tests for the University of the Witwatersrand tender source plug-in."""
import pytest


def test_wits_tenders_source_initialization():
    from tender_getter.sources.universities.wits_tenders import WitsSource
    src = WitsSource()
    assert src.source_id == "wits_tenders"
    assert src.live is True


def test_wits_tenders_parse_mock_html():
    from tender_getter.sources.universities.wits_tenders import WitsSource, MOCK_HTML
    src = WitsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wits_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.wits_tenders import WitsSource
    src = WitsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
