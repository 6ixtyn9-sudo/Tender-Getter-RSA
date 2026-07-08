"""Tests for the KwaZulu-Natal Tourism Authority tender source plug-in."""
import pytest


def test_kzn_tourism_tenders_source_initialization():
    from tender_getter.sources.research_extra.kzn_tourism_tenders import KznTourismSource
    src = KznTourismSource()
    assert src.source_id == "kzn_tourism_tenders"
    assert src.live is False


def test_kzn_tourism_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.kzn_tourism_tenders import KznTourismSource, MOCK_HTML
    src = KznTourismSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kzn_tourism_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.kzn_tourism_tenders import KznTourismSource
    src = KznTourismSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
