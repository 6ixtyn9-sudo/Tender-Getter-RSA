"""Tests for the Pan South African Language Board (PanSALB) tender source plug-in."""
import pytest


def test_pansalb_tenders_source_initialization():
    from tender_getter.sources.chapter9.pansalb_tenders import PansalbSource
    src = PansalbSource()
    assert src.source_id == "pansalb_tenders"
    assert src.live is True


def test_pansalb_tenders_parse_mock_html():
    from tender_getter.sources.chapter9.pansalb_tenders import PansalbSource, MOCK_HTML
    src = PansalbSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_pansalb_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.chapter9.pansalb_tenders import PansalbSource
    src = PansalbSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
