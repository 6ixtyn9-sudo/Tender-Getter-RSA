"""Tests for the ZA Domain Name Authority (ZADNA) tender source plug-in."""
import pytest


def test_zadna_tenders_source_initialization():
    from tender_getter.sources.schedule3a.zadna_tenders import ZadnaSource
    src = ZadnaSource()
    assert src.source_id == "zadna_tenders"
    assert src.live is True


def test_zadna_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.zadna_tenders import ZadnaSource, MOCK_HTML
    src = ZadnaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_zadna_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.zadna_tenders import ZadnaSource
    src = ZadnaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
