"""Tests for the Dr Ruth Segomotsi Mompati District Municipality tender source plug-in."""
import pytest


def test_dr_ruth_segomotsi_mompati_dm_source_initialization():
    from tender_getter.sources.districts.dr_ruth_segomotsi_mompati_dm import DrRuthSegomotsiMompatiDmSource
    src = DrRuthSegomotsiMompatiDmSource()
    assert src.source_id == "dr_ruth_segomotsi_mompati_dm"
    assert src.live is True


def test_dr_ruth_segomotsi_mompati_dm_parse_mock_html():
    from tender_getter.sources.districts.dr_ruth_segomotsi_mompati_dm import DrRuthSegomotsiMompatiDmSource, MOCK_HTML
    src = DrRuthSegomotsiMompatiDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dr_ruth_segomotsi_mompati_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.dr_ruth_segomotsi_mompati_dm import DrRuthSegomotsiMompatiDmSource
    src = DrRuthSegomotsiMompatiDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
