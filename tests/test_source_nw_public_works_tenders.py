"""Tests for the North West Department of Public Works and Roads tender source plug-in."""
import pytest


def test_nw_public_works_tenders_source_initialization():
    from tender_getter.sources.research_extra.nw_public_works_tenders import NwPublicWorksSource
    src = NwPublicWorksSource()
    assert src.source_id == "nw_public_works_tenders"
    assert src.live is True


def test_nw_public_works_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.nw_public_works_tenders import NwPublicWorksSource, MOCK_HTML
    src = NwPublicWorksSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nw_public_works_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.nw_public_works_tenders import NwPublicWorksSource
    src = NwPublicWorksSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
