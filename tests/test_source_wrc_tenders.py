"""Tests for the Water Research Commission tender source plug-in."""
import pytest


def test_wrc_tenders_source_initialization():
    from tender_getter.sources.research_extra.wrc_tenders import WrcSource
    src = WrcSource()
    assert src.source_id == "wrc_tenders"
    assert src.live is True


def test_wrc_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.wrc_tenders import WrcSource, MOCK_HTML
    src = WrcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_wrc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.wrc_tenders import WrcSource
    src = WrcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
