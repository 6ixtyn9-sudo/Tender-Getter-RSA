"""Tests for the Eastern Cape Agriculture tender source plug-in."""
import pytest


def test_ec_agriculture_source_initialization():
    from tender_getter.sources.research.ec_agriculture import EcAgricultureSource
    src = EcAgricultureSource()
    assert src.source_id == "ec_agriculture"
    assert isinstance(src.live, bool)


def test_ec_agriculture_parse_mock_html():
    from tender_getter.sources.research.ec_agriculture import EcAgricultureSource, MOCK_HTML
    src = EcAgricultureSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_agriculture_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ec_agriculture import EcAgricultureSource
    src = EcAgricultureSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
