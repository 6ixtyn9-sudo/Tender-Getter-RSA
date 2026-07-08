"""Tests for the Construction Education and Training Authority (CETA) tender source plug-in."""
import pytest


def test_ceta_tenders_source_initialization():
    from tender_getter.sources.setas.ceta_tenders import CetaSource
    src = CetaSource()
    assert src.source_id == "ceta_tenders"
    assert src.live is True


def test_ceta_tenders_parse_mock_html():
    from tender_getter.sources.setas.ceta_tenders import CetaSource, MOCK_HTML
    src = CetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ceta_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.ceta_tenders import CetaSource
    src = CetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
