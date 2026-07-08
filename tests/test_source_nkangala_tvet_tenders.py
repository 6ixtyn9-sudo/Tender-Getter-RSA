"""Tests for the Nkangala TVET College tender source plug-in."""
import pytest


def test_nkangala_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.nkangala_tvet_tenders import NkangalaTvetSource
    src = NkangalaTvetSource()
    assert src.source_id == "nkangala_tvet_tenders"
    assert src.live is True


def test_nkangala_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.nkangala_tvet_tenders import NkangalaTvetSource, MOCK_HTML
    src = NkangalaTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nkangala_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.nkangala_tvet_tenders import NkangalaTvetSource
    src = NkangalaTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
