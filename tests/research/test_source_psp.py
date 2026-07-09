"""Tests for the PSP tender source plug-in."""
import pytest


def test_psp_source_initialization():
    from tender_getter.sources.research.psp import PspSource
    src = PspSource()
    assert src.source_id == "psp"
    assert isinstance(src.live, bool)


def test_psp_parse_mock_html():
    from tender_getter.sources.research.psp import PspSource, MOCK_HTML
    src = PspSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_psp_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.psp import PspSource
    src = PspSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
