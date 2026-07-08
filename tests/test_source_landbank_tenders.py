"""Tests for the Land and Agricultural Development Bank tender source plug-in."""
import pytest


def test_landbank_tenders_source_initialization():
    from tender_getter.sources.research_extra.landbank_tenders import LandbankSource
    src = LandbankSource()
    assert src.source_id == "landbank_tenders"
    assert src.live is True


def test_landbank_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.landbank_tenders import LandbankSource, MOCK_HTML
    src = LandbankSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_landbank_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.landbank_tenders import LandbankSource
    src = LandbankSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
