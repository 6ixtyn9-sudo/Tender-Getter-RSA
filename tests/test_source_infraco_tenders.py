"""Tests for the Broadband Infraco tender source plug-in."""
import pytest


def test_infraco_tenders_source_initialization():
    from tender_getter.sources.research_extra.infraco_tenders import InfracoSource
    src = InfracoSource()
    assert src.source_id == "infraco_tenders"
    assert src.live is True


def test_infraco_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.infraco_tenders import InfracoSource, MOCK_HTML
    src = InfracoSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_infraco_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.infraco_tenders import InfracoSource
    src = InfracoSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
