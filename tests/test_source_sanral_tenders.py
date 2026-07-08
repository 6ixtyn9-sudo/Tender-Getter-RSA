"""Tests for the SANRAL tender source plug-in."""
import pytest


def test_sanral_tenders_source_initialization():
    from tender_getter.sources.research_extra.sanral_tenders import SanralSource
    src = SanralSource()
    assert src.source_id == "sanral_tenders"
    assert src.live is True


def test_sanral_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sanral_tenders import SanralSource, MOCK_HTML
    src = SanralSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sanral_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sanral_tenders import SanralSource
    src = SanralSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
