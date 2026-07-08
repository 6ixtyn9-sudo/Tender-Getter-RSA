"""Tests for the Federated Hospitality Association of SA tender source plug-in."""
import pytest


def test_fedhasa_tenders_source_initialization():
    from tender_getter.sources.research_extra.fedhasa_tenders import FedhasaSource
    src = FedhasaSource()
    assert src.source_id == "fedhasa_tenders"
    assert src.live is False


def test_fedhasa_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.fedhasa_tenders import FedhasaSource, MOCK_HTML
    src = FedhasaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fedhasa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.fedhasa_tenders import FedhasaSource
    src = FedhasaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
