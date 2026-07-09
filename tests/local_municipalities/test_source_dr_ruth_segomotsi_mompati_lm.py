"""Tests for the Ruth Mompati LM tender source plug-in."""
import pytest


def test_dr_ruth_segomotsi_mompati_lm_source_initialization():
    from tender_getter.sources.local_municipalities.dr_ruth_segomotsi_mompati_lm import DrRuthSegomotsiMompatiLmSource
    src = DrRuthSegomotsiMompatiLmSource()
    assert src.source_id == "dr_ruth_segomotsi_mompati_lm"
    assert isinstance(src.live, bool)


def test_dr_ruth_segomotsi_mompati_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.dr_ruth_segomotsi_mompati_lm import DrRuthSegomotsiMompatiLmSource, MOCK_HTML
    src = DrRuthSegomotsiMompatiLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dr_ruth_segomotsi_mompati_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.dr_ruth_segomotsi_mompati_lm import DrRuthSegomotsiMompatiLmSource
    src = DrRuthSegomotsiMompatiLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
