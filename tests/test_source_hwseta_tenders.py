"""Tests for the Health and Welfare Sector Education and Training Authority (HWSETA) tender source plug-in."""
import pytest


def test_hwseta_tenders_source_initialization():
    from tender_getter.sources.setas.hwseta_tenders import HwsetaSource
    src = HwsetaSource()
    assert src.source_id == "hwseta_tenders"
    assert src.live is True


def test_hwseta_tenders_parse_mock_html():
    from tender_getter.sources.setas.hwseta_tenders import HwsetaSource, MOCK_HTML
    src = HwsetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_hwseta_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.hwseta_tenders import HwsetaSource
    src = HwsetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
