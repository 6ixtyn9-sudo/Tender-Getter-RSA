"""Tests for the Mtubatuba LM tender source plug-in."""
import pytest


def test_mtubatuba_lm_source_initialization():
    from tender_getter.sources.local_municipalities.mtubatuba_lm import MtubatubaLmSource
    src = MtubatubaLmSource()
    assert src.source_id == "mtubatuba_lm"
    assert isinstance(src.live, bool)


def test_mtubatuba_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.mtubatuba_lm import MtubatubaLmSource, MOCK_HTML
    src = MtubatubaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mtubatuba_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mtubatuba_lm import MtubatubaLmSource
    src = MtubatubaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
