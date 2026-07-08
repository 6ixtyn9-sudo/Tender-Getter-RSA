"""Tests for the Department of Health tender source plug-in."""
import pytest


def test_doh_tenders_source_initialization():
    from tender_getter.sources.research_extra.doh_tenders import DohSource
    src = DohSource()
    assert src.source_id == "doh_tenders"
    assert src.live is True


def test_doh_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.doh_tenders import DohSource, MOCK_HTML
    src = DohSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_doh_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.doh_tenders import DohSource
    src = DohSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
