"""Tests for the Manufacturing, Engineering and Related Services SETA (merSETA) tender source plug-in."""
import pytest


def test_merseta_tenders_source_initialization():
    from tender_getter.sources.setas.merseta_tenders import MersetaSource
    src = MersetaSource()
    assert src.source_id == "merseta_tenders"
    assert src.live is True


def test_merseta_tenders_parse_mock_html():
    from tender_getter.sources.setas.merseta_tenders import MersetaSource, MOCK_HTML
    src = MersetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_merseta_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.merseta_tenders import MersetaSource
    src = MersetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
