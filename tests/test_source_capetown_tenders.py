"""Tests for the City of Cape Town tender source plug-in."""
import pytest


def test_capetown_tenders_source_initialization():
    from tender_getter.sources.research_extra.capetown_tenders import CapetownSource
    src = CapetownSource()
    assert src.source_id == "capetown_tenders"
    assert src.live is True


def test_capetown_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.capetown_tenders import CapetownSource, MOCK_HTML
    src = CapetownSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_capetown_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.capetown_tenders import CapetownSource
    src = CapetownSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
