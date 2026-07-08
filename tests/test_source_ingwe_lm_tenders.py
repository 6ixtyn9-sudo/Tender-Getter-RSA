"""Tests for the Ingwe LM tender source plug-in."""
import pytest


def test_ingwe_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.ingwe_lm_tenders import IngweLmSource
    src = IngweLmSource()
    assert src.source_id == "ingwe_lm_tenders"
    assert src.live is False


def test_ingwe_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.ingwe_lm_tenders import IngweLmSource, MOCK_HTML
    src = IngweLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ingwe_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ingwe_lm_tenders import IngweLmSource
    src = IngweLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
