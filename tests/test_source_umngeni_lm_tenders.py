"""Tests for the uMngeni LM tender source plug-in."""
import pytest


def test_umngeni_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.umngeni_lm_tenders import UmngeniLmSource
    src = UmngeniLmSource()
    assert src.source_id == "umngeni_lm_tenders"
    assert src.live is False


def test_umngeni_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.umngeni_lm_tenders import UmngeniLmSource, MOCK_HTML
    src = UmngeniLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umngeni_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.umngeni_lm_tenders import UmngeniLmSource
    src = UmngeniLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
