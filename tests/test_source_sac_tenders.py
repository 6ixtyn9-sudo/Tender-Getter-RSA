"""Tests for the South African Civil Aviation Authority (SACAA) tender source plug-in."""
import pytest


def test_sac_tenders_source_initialization():
    from tender_getter.sources.research_extra.sac_tenders import SacSource
    src = SacSource()
    assert src.source_id == "sac_tenders"
    assert src.live is True


def test_sac_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sac_tenders import SacSource, MOCK_HTML
    src = SacSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sac_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sac_tenders import SacSource
    src = SacSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
