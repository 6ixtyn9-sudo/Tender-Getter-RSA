"""Tests for the Kopanong LM tender source plug-in."""
import pytest


def test_kopanong_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.kopanong_lm_tenders import KopanongLmSource
    src = KopanongLmSource()
    assert src.source_id == "kopanong_lm_tenders"
    assert src.live is False


def test_kopanong_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.kopanong_lm_tenders import KopanongLmSource, MOCK_HTML
    src = KopanongLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kopanong_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.kopanong_lm_tenders import KopanongLmSource
    src = KopanongLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
