"""Tests for the SADC tender source plug-in."""
import pytest


def test_sadc_tenders_source_initialization():
    from tender_getter.sources.research_extra.sadc_tenders import SadcSource
    src = SadcSource()
    assert src.source_id == "sadc_tenders"
    assert src.live is False


def test_sadc_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sadc_tenders import SadcSource, MOCK_HTML
    src = SadcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sadc_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sadc_tenders import SadcSource
    src = SadcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
