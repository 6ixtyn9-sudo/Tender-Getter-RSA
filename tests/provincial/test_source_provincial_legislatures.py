"""Tests for the Provincial Legislatures (collective) tender source plug-in."""
import pytest


def test_provincial_legislatures_source_initialization():
    from tender_getter.sources.provincial.provincial_legislatures import ProvincialLegislaturesSource
    src = ProvincialLegislaturesSource()
    assert src.source_id == "provincial_legislatures"
    assert isinstance(src.live, bool)


def test_provincial_legislatures_parse_mock_html():
    from tender_getter.sources.provincial.provincial_legislatures import ProvincialLegislaturesSource, MOCK_HTML
    src = ProvincialLegislaturesSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_provincial_legislatures_fetch_uses_fallback_on_empty():
    from tender_getter.sources.provincial.provincial_legislatures import ProvincialLegislaturesSource
    src = ProvincialLegislaturesSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
