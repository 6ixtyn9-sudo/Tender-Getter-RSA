"""Tests for the Ulundi LM tender source plug-in."""
import pytest


def test_ulundi_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.ulundi_lm_tenders import UlundiLmSource
    src = UlundiLmSource()
    assert src.source_id == "ulundi_lm_tenders"
    assert src.live is False


def test_ulundi_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.ulundi_lm_tenders import UlundiLmSource, MOCK_HTML
    src = UlundiLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ulundi_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ulundi_lm_tenders import UlundiLmSource
    src = UlundiLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
