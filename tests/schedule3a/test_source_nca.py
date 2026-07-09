"""Tests for the National Consumer Commission tender source plug-in."""
import pytest


def test_nca_source_initialization():
    from tender_getter.sources.schedule3a.nca import NcaSource
    src = NcaSource()
    assert src.source_id == "nca"
    assert isinstance(src.live, bool)


def test_nca_parse_mock_html():
    from tender_getter.sources.schedule3a.nca import NcaSource, MOCK_HTML
    src = NcaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nca_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.nca import NcaSource
    src = NcaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
