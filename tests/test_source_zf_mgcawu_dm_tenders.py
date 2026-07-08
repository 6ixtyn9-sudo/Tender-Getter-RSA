"""Tests for the ZF Mgcawu District Municipality tender source plug-in."""
import pytest


def test_zf_mgcawu_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.zf_mgcawu_dm_tenders import ZfMgcawuDmSource
    src = ZfMgcawuDmSource()
    assert src.source_id == "zf_mgcawu_dm_tenders"
    assert src.live is True


def test_zf_mgcawu_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.zf_mgcawu_dm_tenders import ZfMgcawuDmSource, MOCK_HTML
    src = ZfMgcawuDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_zf_mgcawu_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.zf_mgcawu_dm_tenders import ZfMgcawuDmSource
    src = ZfMgcawuDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
