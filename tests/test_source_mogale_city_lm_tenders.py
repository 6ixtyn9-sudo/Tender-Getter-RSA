"""Tests for the Mogale City Local Municipality tender source plug-in."""
import pytest


def test_mogale_city_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.mogale_city_lm_tenders import MogaleCityLmSource
    src = MogaleCityLmSource()
    assert src.source_id == "mogale_city_lm_tenders"
    assert src.live is True


def test_mogale_city_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.mogale_city_lm_tenders import MogaleCityLmSource, MOCK_HTML
    src = MogaleCityLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mogale_city_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.mogale_city_lm_tenders import MogaleCityLmSource
    src = MogaleCityLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
