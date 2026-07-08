"""Tests for the Cape Peninsula University of Technology tender source plug-in."""
import pytest


def test_cput_tenders_source_initialization():
    from tender_getter.sources.universities.cput_tenders import CputSource
    src = CputSource()
    assert src.source_id == "cput_tenders"
    assert src.live is True


def test_cput_tenders_parse_mock_html():
    from tender_getter.sources.universities.cput_tenders import CputSource, MOCK_HTML
    src = CputSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cput_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.cput_tenders import CputSource
    src = CputSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
