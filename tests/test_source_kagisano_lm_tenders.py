"""Tests for the Kagisano LM tender source plug-in."""
import pytest


def test_kagisano_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.kagisano_lm_tenders import KagisanoLmSource
    src = KagisanoLmSource()
    assert src.source_id == "kagisano_lm_tenders"
    assert src.live is False


def test_kagisano_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.kagisano_lm_tenders import KagisanoLmSource, MOCK_HTML
    src = KagisanoLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kagisano_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.kagisano_lm_tenders import KagisanoLmSource
    src = KagisanoLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
