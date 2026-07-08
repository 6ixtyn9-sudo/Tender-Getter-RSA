"""Tests for the uMsinga LM tender source plug-in."""
import pytest


def test_umsinga_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.umsinga_lm_tenders import UmsingaLmSource
    src = UmsingaLmSource()
    assert src.source_id == "umsinga_lm_tenders"
    assert src.live is False


def test_umsinga_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.umsinga_lm_tenders import UmsingaLmSource, MOCK_HTML
    src = UmsingaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umsinga_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.umsinga_lm_tenders import UmsingaLmSource
    src = UmsingaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
