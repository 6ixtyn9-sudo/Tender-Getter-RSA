"""Tests for the SAPU tender source plug-in."""
import pytest


def test_sapu_tenders_source_initialization():
    from tender_getter.sources.research_extra.sapu_tenders import SapuSource
    src = SapuSource()
    assert src.source_id == "sapu_tenders"
    assert src.live is False


def test_sapu_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sapu_tenders import SapuSource, MOCK_HTML
    src = SapuSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sapu_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sapu_tenders import SapuSource
    src = SapuSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
