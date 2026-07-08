"""Tests for the Victor Khanye Local Municipality tender source plug-in."""
import pytest


def test_victor_khanye_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.victor_khanye_lm_tenders import VictorKhanyeLmSource
    src = VictorKhanyeLmSource()
    assert src.source_id == "victor_khanye_lm_tenders"
    assert src.live is True


def test_victor_khanye_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.victor_khanye_lm_tenders import VictorKhanyeLmSource, MOCK_HTML
    src = VictorKhanyeLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_victor_khanye_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.victor_khanye_lm_tenders import VictorKhanyeLmSource
    src = VictorKhanyeLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
