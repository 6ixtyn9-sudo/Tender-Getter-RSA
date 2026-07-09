"""Tests for the North-West University tender source plug-in."""
import pytest


def test_nwu_source_initialization():
    from tender_getter.sources.universities.nwu import NwuSource
    src = NwuSource()
    assert src.source_id == "nwu"
    assert src.live is True


def test_nwu_parse_mock_html():
    from tender_getter.sources.universities.nwu import NwuSource, MOCK_HTML
    src = NwuSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nwu_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.nwu import NwuSource
    src = NwuSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
