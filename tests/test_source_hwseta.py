"""Tests for the Health and Welfare Sector Education and Training Authority (HWSETA) tender source plug-in."""
import pytest


def test_hwseta_source_initialization():
    from tender_getter.sources.setas.hwseta import HwsetaSource
    src = HwsetaSource()
    assert src.source_id == "hwseta"
    assert src.live is True


def test_hwseta_parse_mock_html():
    from tender_getter.sources.setas.hwseta import HwsetaSource, MOCK_HTML
    src = HwsetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_hwseta_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.hwseta import HwsetaSource
    src = HwsetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
