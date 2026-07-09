"""Tests for the Metrorail tender source plug-in."""
import pytest


def test_metrorail_source_initialization():
    from tender_getter.sources.metros.metrorail import MetrorailSource
    src = MetrorailSource()
    assert src.source_id == "metrorail"
    assert isinstance(src.live, bool)


def test_metrorail_parse_mock_html():
    from tender_getter.sources.metros.metrorail import MetrorailSource, MOCK_HTML
    src = MetrorailSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_metrorail_fetch_uses_fallback_on_empty():
    from tender_getter.sources.metros.metrorail import MetrorailSource
    src = MetrorailSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
