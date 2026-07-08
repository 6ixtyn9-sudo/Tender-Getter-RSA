"""Tests for the Ngcobo Local Municipality tender source plug-in."""
import pytest


def test_ngcobo_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.ngcobo_lm_tenders import NgcoboLmSource
    src = NgcoboLmSource()
    assert src.source_id == "ngcobo_lm_tenders"
    assert src.live is True


def test_ngcobo_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.ngcobo_lm_tenders import NgcoboLmSource, MOCK_HTML
    src = NgcoboLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ngcobo_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ngcobo_lm_tenders import NgcoboLmSource
    src = NgcoboLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
