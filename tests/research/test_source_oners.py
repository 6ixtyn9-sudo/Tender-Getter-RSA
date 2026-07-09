"""Tests for the Office of the Registrar of Agricultural Inputs tender source plug-in."""
import pytest


def test_oners_source_initialization():
    from tender_getter.sources.research.oners import OnersSource
    src = OnersSource()
    assert src.source_id == "oners"
    assert isinstance(src.live, bool)


def test_oners_parse_mock_html():
    from tender_getter.sources.research.oners import OnersSource, MOCK_HTML
    src = OnersSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_oners_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.oners import OnersSource
    src = OnersSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
