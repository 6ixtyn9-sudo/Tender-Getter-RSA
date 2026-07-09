"""Tests for the South African Rugby Football Union (Federation) tender source plug-in."""
import pytest


def test_sarfu_source_initialization():
    from tender_getter.sources.research.sarfu import SarfuSource
    src = SarfuSource()
    assert src.source_id == "sarfu"
    assert isinstance(src.live, bool)


def test_sarfu_parse_mock_html():
    from tender_getter.sources.research.sarfu import SarfuSource, MOCK_HTML
    src = SarfuSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sarfu_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.sarfu import SarfuSource
    src = SarfuSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
