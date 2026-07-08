"""Tests for the Education, Training and Development Practices SETA (ETDP SETA) tender source plug-in."""
import pytest


def test_etdp_seta_tenders_source_initialization():
    from tender_getter.sources.setas.etdp_seta_tenders import EtdpSetaSource
    src = EtdpSetaSource()
    assert src.source_id == "etdp_seta_tenders"
    assert src.live is True


def test_etdp_seta_tenders_parse_mock_html():
    from tender_getter.sources.setas.etdp_seta_tenders import EtdpSetaSource, MOCK_HTML
    src = EtdpSetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_etdp_seta_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.etdp_seta_tenders import EtdpSetaSource
    src = EtdpSetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
