"""Tests for the uMngeni LM tender source plug-in."""
import pytest


def test_umngeni_lm_source_initialization():
    from tender_getter.sources.local_municipalities.umngeni_lm import UmngeniLmSource
    src = UmngeniLmSource()
    assert src.source_id == "umngeni_lm"
    assert isinstance(src.live, bool)


def test_umngeni_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.umngeni_lm import UmngeniLmSource, MOCK_HTML
    src = UmngeniLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umngeni_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.umngeni_lm import UmngeniLmSource
    src = UmngeniLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
