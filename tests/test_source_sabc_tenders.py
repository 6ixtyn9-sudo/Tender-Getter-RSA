"""Tests for the South African Broadcasting Corporation tender source plug-in."""
import pytest


def test_sabc_tenders_source_initialization():
    from tender_getter.sources.research_extra.sabc_tenders import SabcSource
    src = SabcSource()
    assert src.source_id == "sabc_tenders"
    assert src.live is True


def test_sabc_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sabc_tenders import SabcSource, MOCK_HTML
    src = SabcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sabc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sabc_tenders import SabcSource
    src = SabcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
