"""Tests for the Energy and Water Sector Education and Training Authority (EWSETA) tender source plug-in."""
import pytest


def test_ewseta_source_initialization():
    from tender_getter.sources.setas.ewseta import EwsetaSource
    src = EwsetaSource()
    assert src.source_id == "ewseta"
    assert src.live is True


def test_ewseta_parse_mock_html():
    from tender_getter.sources.setas.ewseta import EwsetaSource, MOCK_HTML
    src = EwsetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ewseta_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.ewseta import EwsetaSource
    src = EwsetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
