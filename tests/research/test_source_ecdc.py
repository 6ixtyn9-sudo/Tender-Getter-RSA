"""Tests for the Eastern Cape Development Corporation (ECDC) tender source plug-in."""
import pytest


def test_ecdc_source_initialization():
    from tender_getter.sources.research.ecdc import EcdcSource
    src = EcdcSource()
    assert src.source_id == "ecdc"
    assert isinstance(src.live, bool)


def test_ecdc_parse_mock_html():
    from tender_getter.sources.research.ecdc import EcdcSource, MOCK_HTML
    src = EcdcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ecdc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ecdc import EcdcSource
    src = EcdcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
