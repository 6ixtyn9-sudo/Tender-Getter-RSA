"""Tests for the National Gambling Board (NGB) tender source plug-in."""
import pytest


def test_ngb_tenders_source_initialization():
    from tender_getter.sources.schedule3a.ngb_tenders import NgbSource
    src = NgbSource()
    assert src.source_id == "ngb_tenders"
    assert src.live is True


def test_ngb_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.ngb_tenders import NgbSource, MOCK_HTML
    src = NgbSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ngb_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.ngb_tenders import NgbSource
    src = NgbSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
