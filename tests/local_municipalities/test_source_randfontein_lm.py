"""Tests for the Randfontein LM tender source plug-in."""
import pytest


def test_randfontein_lm_source_initialization():
    from tender_getter.sources.local_municipalities.randfontein_lm import RandfonteinLmSource
    src = RandfonteinLmSource()
    assert src.source_id == "randfontein_lm"
    assert isinstance(src.live, bool)


def test_randfontein_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.randfontein_lm import RandfonteinLmSource, MOCK_HTML
    src = RandfonteinLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_randfontein_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.randfontein_lm import RandfonteinLmSource
    src = RandfonteinLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
