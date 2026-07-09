"""Tests for the KZN Health tender source plug-in."""
import pytest


def test_kzn_health_source_initialization():
    from tender_getter.sources.research.kzn_health import KznHealthSource
    src = KznHealthSource()
    assert src.source_id == "kzn_health"
    assert src.live is True


def test_kzn_health_parse_mock_html():
    from tender_getter.sources.research.kzn_health import KznHealthSource, MOCK_HTML
    src = KznHealthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_health_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.kzn_health import KznHealthSource
    src = KznHealthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
