"""Tests for the Ngcobo Local Municipality tender source plug-in."""
import pytest


def test_ngcobo_lm_source_initialization():
    from tender_getter.sources.local_municipalities.ngcobo_lm import NgcoboLmSource
    src = NgcoboLmSource()
    assert src.source_id == "ngcobo_lm"
    assert isinstance(src.live, bool)


def test_ngcobo_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.ngcobo_lm import NgcoboLmSource, MOCK_HTML
    src = NgcoboLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ngcobo_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ngcobo_lm import NgcoboLmSource
    src = NgcoboLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
