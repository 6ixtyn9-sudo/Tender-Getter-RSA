"""Tests for the Coega IDZ tender source plug-in."""
import pytest


def test_coega_idz_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.coega_idz_lm_tenders import CoegaIdzLmSource
    src = CoegaIdzLmSource()
    assert src.source_id == "coega_idz_lm_tenders"
    assert src.live is True


def test_coega_idz_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.coega_idz_lm_tenders import CoegaIdzLmSource, MOCK_HTML
    src = CoegaIdzLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_coega_idz_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.coega_idz_lm_tenders import CoegaIdzLmSource
    src = CoegaIdzLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
