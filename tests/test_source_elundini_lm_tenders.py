"""Tests for the Elundini LM tender source plug-in."""
import pytest


def test_elundini_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.elundini_lm_tenders import ElundiniLmSource
    src = ElundiniLmSource()
    assert src.source_id == "elundini_lm_tenders"
    assert src.live is False


def test_elundini_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.elundini_lm_tenders import ElundiniLmSource, MOCK_HTML
    src = ElundiniLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_elundini_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.elundini_lm_tenders import ElundiniLmSource
    src = ElundiniLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
