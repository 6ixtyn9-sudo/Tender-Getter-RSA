"""Tests for the Dr Kenneth Kaunda District Municipality tender source plug-in."""
import pytest


def test_dr_kennga_kaunda_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.dr_kennga_kaunda_dm_tenders import DrKenngaKaundaDmSource
    src = DrKenngaKaundaDmSource()
    assert src.source_id == "dr_kennga_kaunda_dm_tenders"
    assert src.live is True


def test_dr_kennga_kaunda_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.dr_kennga_kaunda_dm_tenders import DrKenngaKaundaDmSource, MOCK_HTML
    src = DrKenngaKaundaDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dr_kennga_kaunda_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.dr_kennga_kaunda_dm_tenders import DrKenngaKaundaDmSource
    src = DrKenngaKaundaDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
