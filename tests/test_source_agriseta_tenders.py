"""Tests for the Agricultural Sector Education and Training Authority (AgriSETA) tender source plug-in."""
import pytest


def test_agriseta_tenders_source_initialization():
    from tender_getter.sources.setas.agriseta_tenders import AgrisetaSource
    src = AgrisetaSource()
    assert src.source_id == "agriseta_tenders"
    assert src.live is True


def test_agriseta_tenders_parse_mock_html():
    from tender_getter.sources.setas.agriseta_tenders import AgrisetaSource, MOCK_HTML
    src = AgrisetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_agriseta_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.agriseta_tenders import AgrisetaSource
    src = AgrisetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
