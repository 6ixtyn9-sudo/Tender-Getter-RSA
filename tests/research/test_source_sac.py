"""Tests for the South African Civil Aviation Authority (SACAA) tender source plug-in."""
import pytest


def test_sac_source_initialization():
    from tender_getter.sources.research.sac import SacSource
    src = SacSource()
    assert src.source_id == "sac"
    assert isinstance(src.live, bool)


def test_sac_parse_mock_html():
    from tender_getter.sources.research.sac import SacSource, MOCK_HTML
    src = SacSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sac_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.sac import SacSource
    src = SacSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
