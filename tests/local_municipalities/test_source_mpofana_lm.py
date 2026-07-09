"""Tests for the Mpofana LM tender source plug-in."""
import pytest


def test_mpofana_lm_source_initialization():
    from tender_getter.sources.local_municipalities.mpofana_lm import MpofanaLmSource
    src = MpofanaLmSource()
    assert src.source_id == "mpofana_lm"
    assert isinstance(src.live, bool)


def test_mpofana_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.mpofana_lm import MpofanaLmSource, MOCK_HTML
    src = MpofanaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mpofana_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mpofana_lm import MpofanaLmSource
    src = MpofanaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
