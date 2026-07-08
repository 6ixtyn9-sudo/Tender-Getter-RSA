"""Tests for the Department of Public Service & Administration tender source plug-in."""
import pytest


def test_dpsa_tenders_source_initialization():
    from tender_getter.sources.research_extra.dpsa_tenders import DpsaSource
    src = DpsaSource()
    assert src.source_id == "dpsa_tenders"
    assert src.live is True


def test_dpsa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dpsa_tenders import DpsaSource, MOCK_HTML
    src = DpsaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dpsa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dpsa_tenders import DpsaSource
    src = DpsaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
