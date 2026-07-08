"""Tests for the State Information Technology Agency (SITA) tender source plug-in."""
import pytest


def test_sita_tenders_source_initialization():
    from tender_getter.sources.research_extra.sita_tenders import SitaSource
    src = SitaSource()
    assert src.source_id == "sita_tenders"
    assert src.live is True


def test_sita_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sita_tenders import SitaSource, MOCK_HTML
    src = SitaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sita_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sita_tenders import SitaSource
    src = SitaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
