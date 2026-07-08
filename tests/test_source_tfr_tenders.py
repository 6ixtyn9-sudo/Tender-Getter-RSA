"""Tests for the Transnet Freight Rail (TFR) tender source plug-in."""
import pytest


def test_tfr_tenders_source_initialization():
    from tender_getter.sources.soes_extra.tfr_tenders import TfrSource
    src = TfrSource()
    assert src.source_id == "tfr_tenders"
    assert src.live is True


def test_tfr_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.tfr_tenders import TfrSource, MOCK_HTML
    src = TfrSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tfr_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.tfr_tenders import TfrSource
    src = TfrSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
