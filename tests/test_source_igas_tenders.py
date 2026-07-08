"""Tests for the iGas (SA Gas Development Company) tender source plug-in."""
import pytest


def test_igas_tenders_source_initialization():
    from tender_getter.sources.soes_extra.igas_tenders import IgasSource
    src = IgasSource()
    assert src.source_id == "igas_tenders"
    assert src.live is True


def test_igas_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.igas_tenders import IgasSource, MOCK_HTML
    src = IgasSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_igas_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.igas_tenders import IgasSource
    src = IgasSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
