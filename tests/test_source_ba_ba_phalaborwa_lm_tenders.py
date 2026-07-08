"""Tests for the Ba-Phalaborwa LM tender source plug-in."""
import pytest


def test_ba_ba_phalaborwa_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.ba_ba_phalaborwa_lm_tenders import BaBaPhalaborwaLmSource
    src = BaBaPhalaborwaLmSource()
    assert src.source_id == "ba_ba_phalaborwa_lm_tenders"
    assert src.live is False


def test_ba_ba_phalaborwa_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.ba_ba_phalaborwa_lm_tenders import BaBaPhalaborwaLmSource, MOCK_HTML
    src = BaBaPhalaborwaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ba_ba_phalaborwa_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ba_ba_phalaborwa_lm_tenders import BaBaPhalaborwaLmSource
    src = BaBaPhalaborwaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
