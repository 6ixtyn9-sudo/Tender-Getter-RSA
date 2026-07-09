"""Tests for the Film and Publication Board (already in research_extra/) tender source plug-in."""
import pytest


def test_fp_source_initialization():
    from tender_getter.sources.research.fp import FpSource
    src = FpSource()
    assert src.source_id == "fp"
    assert src.live is True


def test_fp_parse_mock_html():
    from tender_getter.sources.research.fp import FpSource, MOCK_HTML
    src = FpSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fp_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.fp import FpSource
    src = FpSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
