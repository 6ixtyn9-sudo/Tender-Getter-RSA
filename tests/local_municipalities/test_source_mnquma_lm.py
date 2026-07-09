"""Tests for the Mnquma LM tender source plug-in."""
import pytest


def test_mnquma_lm_source_initialization():
    from tender_getter.sources.local_municipalities.mnquma_lm import MnqumaLmSource
    src = MnqumaLmSource()
    assert src.source_id == "mnquma_lm"
    assert isinstance(src.live, bool)


def test_mnquma_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.mnquma_lm import MnqumaLmSource, MOCK_HTML
    src = MnqumaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mnquma_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mnquma_lm import MnqumaLmSource
    src = MnqumaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
