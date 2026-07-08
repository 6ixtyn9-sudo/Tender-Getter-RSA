"""Tests for the Eskom Rotek Industries tender source plug-in."""
import pytest


def test_eskom_rotek_tenders_source_initialization():
    from tender_getter.sources.soes_extra.eskom_rotek_tenders import EskomRotekSource
    src = EskomRotekSource()
    assert src.source_id == "eskom_rotek_tenders"
    assert src.live is True


def test_eskom_rotek_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.eskom_rotek_tenders import EskomRotekSource, MOCK_HTML
    src = EskomRotekSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_eskom_rotek_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.eskom_rotek_tenders import EskomRotekSource
    src = EskomRotekSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
