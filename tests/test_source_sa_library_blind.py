"""Tests for the South African Library for the Blind tender source plug-in."""
import pytest


def test_sa_library_blind_source_initialization():
    from tender_getter.sources.research.sa_library_blind import SaLibraryBlindSource
    src = SaLibraryBlindSource()
    assert src.source_id == "sa_library_blind"
    assert src.live is True


def test_sa_library_blind_parse_mock_html():
    from tender_getter.sources.research.sa_library_blind import SaLibraryBlindSource, MOCK_HTML
    src = SaLibraryBlindSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sa_library_blind_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.sa_library_blind import SaLibraryBlindSource
    src = SaLibraryBlindSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
