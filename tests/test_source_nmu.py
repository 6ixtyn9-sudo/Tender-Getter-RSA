"""Tests for the Nelson Mandela University tender source plug-in."""
import pytest


def test_nmu_source_initialization():
    from tender_getter.sources.universities.nmu import NmuSource
    src = NmuSource()
    assert src.source_id == "nmu"
    assert src.live is True


def test_nmu_parse_mock_html():
    from tender_getter.sources.universities.nmu import NmuSource, MOCK_HTML
    src = NmuSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nmu_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.nmu import NmuSource
    src = NmuSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
