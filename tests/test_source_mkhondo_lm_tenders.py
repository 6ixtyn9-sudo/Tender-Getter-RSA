"""Tests for the Mkhondo LM tender source plug-in."""
import pytest


def test_mkhondo_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.mkhondo_lm_tenders import MkhondoLmSource
    src = MkhondoLmSource()
    assert src.source_id == "mkhondo_lm_tenders"
    assert src.live is False


def test_mkhondo_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.mkhondo_lm_tenders import MkhondoLmSource, MOCK_HTML
    src = MkhondoLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mkhondo_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mkhondo_lm_tenders import MkhondoLmSource
    src = MkhondoLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
