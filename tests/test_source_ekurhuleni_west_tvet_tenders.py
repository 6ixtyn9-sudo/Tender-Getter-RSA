"""Tests for the Ekurhuleni West TVET College tender source plug-in."""
import pytest


def test_ekurhuleni_west_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.ekurhuleni_west_tvet_tenders import EkurhuleniWestTvetSource
    src = EkurhuleniWestTvetSource()
    assert src.source_id == "ekurhuleni_west_tvet_tenders"
    assert src.live is True


def test_ekurhuleni_west_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.ekurhuleni_west_tvet_tenders import EkurhuleniWestTvetSource, MOCK_HTML
    src = EkurhuleniWestTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ekurhuleni_west_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.ekurhuleni_west_tvet_tenders import EkurhuleniWestTvetSource
    src = EkurhuleniWestTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
