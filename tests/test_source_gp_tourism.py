"""Tests for the GP Tourism tender source plug-in."""
import pytest


def test_gp_tourism_source_initialization():
    from tender_getter.sources.research.gp_tourism import GpTourismSource
    src = GpTourismSource()
    assert src.source_id == "gp_tourism"
    assert src.live is False


def test_gp_tourism_parse_mock_html():
    from tender_getter.sources.research.gp_tourism import GpTourismSource, MOCK_HTML
    src = GpTourismSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gp_tourism_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.gp_tourism import GpTourismSource
    src = GpTourismSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
