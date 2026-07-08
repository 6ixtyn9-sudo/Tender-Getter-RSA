"""Tests for the Metrorail tender source plug-in."""
import pytest


def test_metrorail_tenders_source_initialization():
    from tender_getter.sources.soes_extra.metrorail_tenders import MetrorailSource
    src = MetrorailSource()
    assert src.source_id == "metrorail_tenders"
    assert src.live is True


def test_metrorail_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.metrorail_tenders import MetrorailSource, MOCK_HTML
    src = MetrorailSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_metrorail_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.metrorail_tenders import MetrorailSource
    src = MetrorailSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
