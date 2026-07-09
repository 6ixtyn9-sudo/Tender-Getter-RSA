"""Tests for the Eastern Cape Health tender source plug-in."""
import pytest


def test_ec_health_source_initialization():
    from tender_getter.sources.research.ec_health import EcHealthSource
    src = EcHealthSource()
    assert src.source_id == "ec_health"
    assert isinstance(src.live, bool)


def test_ec_health_parse_mock_html():
    from tender_getter.sources.research.ec_health import EcHealthSource, MOCK_HTML
    src = EcHealthSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_health_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ec_health import EcHealthSource
    src = EcHealthSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
