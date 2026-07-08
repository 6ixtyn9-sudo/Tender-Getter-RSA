"""Tests for the Emalahleni Local Municipality (Mpumalanga) tender source plug-in."""
import pytest


def test_emalahleni_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.emalahleni_lm_tenders import EmalahleniLmSource
    src = EmalahleniLmSource()
    assert src.source_id == "emalahleni_lm_tenders"
    assert src.live is True


def test_emalahleni_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.emalahleni_lm_tenders import EmalahleniLmSource, MOCK_HTML
    src = EmalahleniLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_emalahleni_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.emalahleni_lm_tenders import EmalahleniLmSource
    src = EmalahleniLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
