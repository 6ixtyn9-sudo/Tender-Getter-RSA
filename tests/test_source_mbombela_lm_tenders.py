"""Tests for the Mbombela Local Municipality tender source plug-in."""
import pytest


def test_mbombela_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.mbombela_lm_tenders import MbombelaLmSource
    src = MbombelaLmSource()
    assert src.source_id == "mbombela_lm_tenders"
    assert src.live is True


def test_mbombela_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.mbombela_lm_tenders import MbombelaLmSource, MOCK_HTML
    src = MbombelaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mbombela_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mbombela_lm_tenders import MbombelaLmSource
    src = MbombelaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
