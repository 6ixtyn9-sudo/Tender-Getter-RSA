"""Tests for the Insurance Sector Education and Training Authority (INSETA) tender source plug-in."""
import pytest


def test_inseta_source_initialization():
    from tender_getter.sources.setas.inseta import InsetaSource
    src = InsetaSource()
    assert src.source_id == "inseta"
    assert src.live is True


def test_inseta_parse_mock_html():
    from tender_getter.sources.setas.inseta import InsetaSource, MOCK_HTML
    src = InsetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_inseta_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.inseta import InsetaSource
    src = InsetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
