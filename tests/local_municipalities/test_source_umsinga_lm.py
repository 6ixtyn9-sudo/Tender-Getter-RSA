"""Tests for the uMsinga LM tender source plug-in."""
import pytest


def test_umsinga_lm_source_initialization():
    from tender_getter.sources.local_municipalities.umsinga_lm import UmsingaLmSource
    src = UmsingaLmSource()
    assert src.source_id == "umsinga_lm"
    assert isinstance(src.live, bool)


def test_umsinga_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.umsinga_lm import UmsingaLmSource, MOCK_HTML
    src = UmsingaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umsinga_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.umsinga_lm import UmsingaLmSource
    src = UmsingaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
