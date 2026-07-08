"""Tests for the Northern Cape Rural TVET College tender source plug-in."""
import pytest


def test_northern_cape_rural_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.northern_cape_rural_tvet_tenders import NorthernCapeRuralTvetSource
    src = NorthernCapeRuralTvetSource()
    assert src.source_id == "northern_cape_rural_tvet_tenders"
    assert src.live is True


def test_northern_cape_rural_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.northern_cape_rural_tvet_tenders import NorthernCapeRuralTvetSource, MOCK_HTML
    src = NorthernCapeRuralTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_northern_cape_rural_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.northern_cape_rural_tvet_tenders import NorthernCapeRuralTvetSource
    src = NorthernCapeRuralTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
