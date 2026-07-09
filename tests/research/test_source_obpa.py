"""Tests for the Onderstepoort Biological Products tender source plug-in."""
import pytest


def test_obpa_source_initialization():
    from tender_getter.sources.research.obpa import ObpaSource
    src = ObpaSource()
    assert src.source_id == "obpa"
    assert src.live is False


def test_obpa_parse_mock_html():
    from tender_getter.sources.research.obpa import ObpaSource, MOCK_HTML
    src = ObpaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_obpa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.obpa import ObpaSource
    src = ObpaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
