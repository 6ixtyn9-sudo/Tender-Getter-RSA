"""Tests for the Department of Communications & Digital Technologies tender source plug-in."""
import pytest


def test_dcdt_tenders_source_initialization():
    from tender_getter.sources.research_extra.dcdt_tenders import DcdtSource
    src = DcdtSource()
    assert src.source_id == "dcdt_tenders"
    assert src.live is True


def test_dcdt_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dcdt_tenders import DcdtSource, MOCK_HTML
    src = DcdtSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dcdt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dcdt_tenders import DcdtSource
    src = DcdtSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
