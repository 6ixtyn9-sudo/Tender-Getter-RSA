"""Tests for the Zamukulungisa LM tender source plug-in."""
import pytest


def test_zamukulungisa_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.zamukulungisa_lm_tenders import ZamukulungisaLmSource
    src = ZamukulungisaLmSource()
    assert src.source_id == "zamukulungisa_lm_tenders"
    assert src.live is False


def test_zamukulungisa_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.zamukulungisa_lm_tenders import ZamukulungisaLmSource, MOCK_HTML
    src = ZamukulungisaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_zamukulungisa_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.zamukulungisa_lm_tenders import ZamukulungisaLmSource
    src = ZamukulungisaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
