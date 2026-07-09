"""Tests for the Kagisano-Molopo LM tender source plug-in."""
import pytest


def test_kagisano_molopo_lm_source_initialization():
    from tender_getter.sources.local_municipalities.kagisano_molopo_lm import KagisanoMolopoLmSource
    src = KagisanoMolopoLmSource()
    assert src.source_id == "kagisano_molopo_lm"
    assert src.live is False


def test_kagisano_molopo_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.kagisano_molopo_lm import KagisanoMolopoLmSource, MOCK_HTML
    src = KagisanoMolopoLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kagisano_molopo_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.kagisano_molopo_lm import KagisanoMolopoLmSource
    src = KagisanoMolopoLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
