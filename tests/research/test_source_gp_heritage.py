"""Tests for the Gauteng Heritage Foundation tender source plug-in."""
import pytest


def test_gp_heritage_source_initialization():
    from tender_getter.sources.research.gp_heritage import GpHeritageSource
    src = GpHeritageSource()
    assert src.source_id == "gp_heritage"
    assert isinstance(src.live, bool)


def test_gp_heritage_parse_mock_html():
    from tender_getter.sources.research.gp_heritage import GpHeritageSource, MOCK_HTML
    src = GpHeritageSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gp_heritage_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.gp_heritage import GpHeritageSource
    src = GpHeritageSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
