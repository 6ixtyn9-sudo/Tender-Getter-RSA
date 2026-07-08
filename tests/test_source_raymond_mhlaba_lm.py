"""Tests for the Raymond Mhlaba LM tender source plug-in."""
import pytest


def test_raymond_mhlaba_lm_source_initialization():
    from tender_getter.sources.local_municipalities.raymond_mhlaba_lm import RaymondMhlabaLmSource
    src = RaymondMhlabaLmSource()
    assert src.source_id == "raymond_mhlaba_lm"
    assert src.live is False


def test_raymond_mhlaba_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.raymond_mhlaba_lm import RaymondMhlabaLmSource, MOCK_HTML
    src = RaymondMhlabaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_raymond_mhlaba_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.raymond_mhlaba_lm import RaymondMhlabaLmSource
    src = RaymondMhlabaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
