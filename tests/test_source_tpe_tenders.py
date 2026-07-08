"""Tests for the Transnet Pipelines (TPE) tender source plug-in."""
import pytest


def test_tpe_tenders_source_initialization():
    from tender_getter.sources.soes_extra.tpe_tenders import TpeSource
    src = TpeSource()
    assert src.source_id == "tpe_tenders"
    assert src.live is True


def test_tpe_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.tpe_tenders import TpeSource, MOCK_HTML
    src = TpeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tpe_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.tpe_tenders import TpeSource
    src = TpeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
