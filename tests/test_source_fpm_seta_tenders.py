"""Tests for the Fibre Processing and Manufacturing SETA (FP&M SETA) tender source plug-in."""
import pytest


def test_fpm_seta_tenders_source_initialization():
    from tender_getter.sources.setas.fpm_seta_tenders import FpmSetaSource
    src = FpmSetaSource()
    assert src.source_id == "fpm_seta_tenders"
    assert src.live is True


def test_fpm_seta_tenders_parse_mock_html():
    from tender_getter.sources.setas.fpm_seta_tenders import FpmSetaSource, MOCK_HTML
    src = FpmSetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fpm_seta_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.fpm_seta_tenders import FpmSetaSource
    src = FpmSetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
