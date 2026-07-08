"""Tests for the Greater Giyani LM tender source plug-in."""
import pytest


def test_greater_giyani_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.greater_giyani_lm_tenders import GreaterGiyaniLmSource
    src = GreaterGiyaniLmSource()
    assert src.source_id == "greater_giyani_lm_tenders"
    assert src.live is False


def test_greater_giyani_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.greater_giyani_lm_tenders import GreaterGiyaniLmSource, MOCK_HTML
    src = GreaterGiyaniLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_greater_giyani_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.greater_giyani_lm_tenders import GreaterGiyaniLmSource
    src = GreaterGiyaniLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
