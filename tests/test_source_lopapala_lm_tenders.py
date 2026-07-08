"""Tests for the Lopapala LM tender source plug-in."""
import pytest


def test_lopapala_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.lopapala_lm_tenders import LopapalaLmSource
    src = LopapalaLmSource()
    assert src.source_id == "lopapala_lm_tenders"
    assert src.live is False


def test_lopapala_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.lopapala_lm_tenders import LopapalaLmSource, MOCK_HTML
    src = LopapalaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lopapala_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.lopapala_lm_tenders import LopapalaLmSource
    src = LopapalaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
