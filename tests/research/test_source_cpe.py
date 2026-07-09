"""Tests for the Commission for the Promotion of Cultural Communities (CRL) tender source plug-in."""
import pytest


def test_cpe_source_initialization():
    from tender_getter.sources.research.cpe import CpeSource
    src = CpeSource()
    assert src.source_id == "cpe"
    assert isinstance(src.live, bool)


def test_cpe_parse_mock_html():
    from tender_getter.sources.research.cpe import CpeSource, MOCK_HTML
    src = CpeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cpe_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.cpe import CpeSource
    src = CpeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
