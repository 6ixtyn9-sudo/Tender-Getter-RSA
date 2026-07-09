"""Tests for the Safety and Security Sector Education and Training Authority (SASSETA) tender source plug-in."""
import pytest


def test_sasseta_source_initialization():
    from tender_getter.sources.setas.sasseta import SassetaSource
    src = SassetaSource()
    assert src.source_id == "sasseta"
    assert isinstance(src.live, bool)


def test_sasseta_parse_mock_html():
    from tender_getter.sources.setas.sasseta import SassetaSource, MOCK_HTML
    src = SassetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sasseta_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.sasseta import SassetaSource
    src = SassetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
