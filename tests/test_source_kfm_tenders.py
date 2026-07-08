"""Tests for the KFM Radio tender source plug-in."""
import pytest


def test_kfm_tenders_source_initialization():
    from tender_getter.sources.research_extra.kfm_tenders import KfmSource
    src = KfmSource()
    assert src.source_id == "kfm_tenders"
    assert src.live is False


def test_kfm_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.kfm_tenders import KfmSource, MOCK_HTML
    src = KfmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kfm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.kfm_tenders import KfmSource
    src = KfmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
