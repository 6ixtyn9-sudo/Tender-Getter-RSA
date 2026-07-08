"""Tests for the Central University of Technology, Free State tender source plug-in."""
import pytest


def test_cut_tenders_source_initialization():
    from tender_getter.sources.universities.cut_tenders import CutSource
    src = CutSource()
    assert src.source_id == "cut_tenders"
    assert src.live is True


def test_cut_tenders_parse_mock_html():
    from tender_getter.sources.universities.cut_tenders import CutSource, MOCK_HTML
    src = CutSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cut_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.cut_tenders import CutSource
    src = CutSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
