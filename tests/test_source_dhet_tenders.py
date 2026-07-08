"""Tests for the Department of Higher Education & Training tender source plug-in."""
import pytest


def test_dhet_tenders_source_initialization():
    from tender_getter.sources.research_extra.dhet_tenders import DhetSource
    src = DhetSource()
    assert src.source_id == "dhet_tenders"
    assert src.live is True


def test_dhet_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dhet_tenders import DhetSource, MOCK_HTML
    src = DhetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dhet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dhet_tenders import DhetSource
    src = DhetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
