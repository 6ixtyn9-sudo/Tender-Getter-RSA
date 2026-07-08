"""Tests for the Department of Agriculture, Land Reform & Rural Development tender source plug-in."""
import pytest


def test_dalrrd_tenders_source_initialization():
    from tender_getter.sources.research_extra.dalrrd_tenders import DalrrdSource
    src = DalrrdSource()
    assert src.source_id == "dalrrd_tenders"
    assert src.live is True


def test_dalrrd_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dalrrd_tenders import DalrrdSource, MOCK_HTML
    src = DalrrdSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dalrrd_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dalrrd_tenders import DalrrdSource
    src = DalrrdSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
