"""Tests for the Gauteng Health (alt) tender source plug-in."""
import pytest


def test_gp_health_source_initialization():
    from tender_getter.sources.research.gp_health import GpHealthSource
    src = GpHealthSource()
    assert src.source_id == "gp_health"
    assert isinstance(src.live, bool)


def test_gp_health_parse_mock_html():
    from tender_getter.sources.research.gp_health import GpHealthSource, MOCK_HTML
    src = GpHealthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gp_health_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.gp_health import GpHealthSource
    src = GpHealthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
