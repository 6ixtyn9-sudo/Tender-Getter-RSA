"""Tests for the Fibre Processing and Manufacturing SETA (FP&M SETA) tender source plug-in."""
import pytest


def test_fpm_seta_source_initialization():
    from tender_getter.sources.setas.fpm_seta import FpmSetaSource
    src = FpmSetaSource()
    assert src.source_id == "fpm_seta"
    assert isinstance(src.live, bool)


def test_fpm_seta_parse_mock_html():
    from tender_getter.sources.setas.fpm_seta import FpmSetaSource, MOCK_HTML
    src = FpmSetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fpm_seta_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.fpm_seta import FpmSetaSource
    src = FpmSetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
