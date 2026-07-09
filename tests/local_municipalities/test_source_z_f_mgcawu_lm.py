"""Tests for the ZF Mgcawu LM tender source plug-in."""
import pytest


def test_z_f_mgcawu_lm_source_initialization():
    from tender_getter.sources.local_municipalities.z_f_mgcawu_lm import ZFMgcawuLmSource
    src = ZFMgcawuLmSource()
    assert src.source_id == "z_f_mgcawu_lm"
    assert isinstance(src.live, bool)


def test_z_f_mgcawu_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.z_f_mgcawu_lm import ZFMgcawuLmSource, MOCK_HTML
    src = ZFMgcawuLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_z_f_mgcawu_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.z_f_mgcawu_lm import ZFMgcawuLmSource
    src = ZFMgcawuLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
