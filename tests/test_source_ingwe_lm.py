"""Tests for the Ingwe LM tender source plug-in."""
import pytest


def test_ingwe_lm_source_initialization():
    from tender_getter.sources.local_municipalities.ingwe_lm import IngweLmSource
    src = IngweLmSource()
    assert src.source_id == "ingwe_lm"
    assert src.live is False


def test_ingwe_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.ingwe_lm import IngweLmSource, MOCK_HTML
    src = IngweLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ingwe_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.ingwe_lm import IngweLmSource
    src = IngweLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
