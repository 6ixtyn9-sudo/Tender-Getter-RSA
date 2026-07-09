"""Tests for the Mutale LM tender source plug-in."""
import pytest


def test_mutale_lm_source_initialization():
    from tender_getter.sources.local_municipalities.mutale_lm import MutaleLmSource
    src = MutaleLmSource()
    assert src.source_id == "mutale_lm"
    assert isinstance(src.live, bool)


def test_mutale_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.mutale_lm import MutaleLmSource, MOCK_HTML
    src = MutaleLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mutale_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mutale_lm import MutaleLmSource
    src = MutaleLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
