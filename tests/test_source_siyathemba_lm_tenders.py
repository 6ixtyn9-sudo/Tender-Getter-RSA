"""Tests for the Siyathemba LM tender source plug-in."""
import pytest


def test_siyathemba_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.siyathemba_lm_tenders import SiyathembaLmSource
    src = SiyathembaLmSource()
    assert src.source_id == "siyathemba_lm_tenders"
    assert src.live is False


def test_siyathemba_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.siyathemba_lm_tenders import SiyathembaLmSource, MOCK_HTML
    src = SiyathembaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_siyathemba_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.siyathemba_lm_tenders import SiyathembaLmSource
    src = SiyathembaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
