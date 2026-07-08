"""Tests for the PSP tender source plug-in."""
import pytest


def test_psp_tenders_source_initialization():
    from tender_getter.sources.research_extra.psp_tenders import PspSource
    src = PspSource()
    assert src.source_id == "psp_tenders"
    assert src.live is False


def test_psp_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.psp_tenders import PspSource, MOCK_HTML
    src = PspSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_psp_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.psp_tenders import PspSource
    src = PspSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
