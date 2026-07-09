"""Tests for the Eastern Cape Parks Board tender source plug-in."""
import pytest


def test_ec_parks_source_initialization():
    from tender_getter.sources.research.ec_parks import EcParksSource
    src = EcParksSource()
    assert src.source_id == "ec_parks"
    assert isinstance(src.live, bool)


def test_ec_parks_parse_mock_html():
    from tender_getter.sources.research.ec_parks import EcParksSource, MOCK_HTML
    src = EcParksSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_parks_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ec_parks import EcParksSource
    src = EcParksSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
