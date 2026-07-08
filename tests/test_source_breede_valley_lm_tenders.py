"""Tests for the Breede Valley Municipality tender source plug-in."""
import pytest


def test_breede_valley_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.breede_valley_lm_tenders import BreedeValleyLmSource
    src = BreedeValleyLmSource()
    assert src.source_id == "breede_valley_lm_tenders"
    assert src.live is True


def test_breede_valley_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.breede_valley_lm_tenders import BreedeValleyLmSource, MOCK_HTML
    src = BreedeValleyLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_breede_valley_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.breede_valley_lm_tenders import BreedeValleyLmSource
    src = BreedeValleyLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
