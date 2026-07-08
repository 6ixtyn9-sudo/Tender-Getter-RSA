"""Tests for the KZN Industrial Economic Cluster (alt) tender source plug-in."""
import pytest


def test_kzn_iec_tenders_source_initialization():
    from tender_getter.sources.soes_extra.kzn_iec_tenders import KznIecSource
    src = KznIecSource()
    assert src.source_id == "kzn_iec_tenders"
    assert src.live is False


def test_kzn_iec_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.kzn_iec_tenders import KznIecSource, MOCK_HTML
    src = KznIecSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_iec_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.kzn_iec_tenders import KznIecSource
    src = KznIecSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
