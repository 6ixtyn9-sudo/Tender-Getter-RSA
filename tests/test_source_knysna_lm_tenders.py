"""Tests for the Knysna Municipality tender source plug-in."""
import pytest


def test_knysna_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.knysna_lm_tenders import KnysnaLmSource
    src = KnysnaLmSource()
    assert src.source_id == "knysna_lm_tenders"
    assert src.live is True


def test_knysna_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.knysna_lm_tenders import KnysnaLmSource, MOCK_HTML
    src = KnysnaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_knysna_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.knysna_lm_tenders import KnysnaLmSource
    src = KnysnaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
