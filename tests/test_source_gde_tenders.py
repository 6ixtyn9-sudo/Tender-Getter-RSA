"""Tests for the Gauteng Department of Education tender source plug-in."""
import pytest


def test_gde_tenders_source_initialization():
    from tender_getter.sources.research_extra.gde_tenders import GdeSource
    src = GdeSource()
    assert src.source_id == "gde_tenders"
    assert src.live is True


def test_gde_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.gde_tenders import GdeSource, MOCK_HTML
    src = GdeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gde_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.gde_tenders import GdeSource
    src = GdeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
