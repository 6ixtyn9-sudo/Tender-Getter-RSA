"""Tests for the Eastern Cape Tourism tender source plug-in."""
import pytest


def test_ec_tourism_source_initialization():
    from tender_getter.sources.research.ec_tourism import EcTourismSource
    src = EcTourismSource()
    assert src.source_id == "ec_tourism"
    assert isinstance(src.live, bool)


def test_ec_tourism_parse_mock_html():
    from tender_getter.sources.research.ec_tourism import EcTourismSource, MOCK_HTML
    src = EcTourismSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_tourism_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ec_tourism import EcTourismSource
    src = EcTourismSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
