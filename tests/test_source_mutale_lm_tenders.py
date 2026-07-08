"""Tests for the Mutale LM tender source plug-in."""
import pytest


def test_mutale_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.mutale_lm_tenders import MutaleLmSource
    src = MutaleLmSource()
    assert src.source_id == "mutale_lm_tenders"
    assert src.live is False


def test_mutale_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.mutale_lm_tenders import MutaleLmSource, MOCK_HTML
    src = MutaleLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mutale_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mutale_lm_tenders import MutaleLmSource
    src = MutaleLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
