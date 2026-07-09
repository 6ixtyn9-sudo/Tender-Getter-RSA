"""Tests for the Ekurhuleni East TVET College tender source plug-in."""
import pytest


def test_ekurhuleni_east_tvet_source_initialization():
    from tender_getter.sources.tvet.ekurhuleni_east_tvet import EkurhuleniEastTvetSource
    src = EkurhuleniEastTvetSource()
    assert src.source_id == "ekurhuleni_east_tvet"
    assert isinstance(src.live, bool)


def test_ekurhuleni_east_tvet_parse_mock_html():
    from tender_getter.sources.tvet.ekurhuleni_east_tvet import EkurhuleniEastTvetSource, MOCK_HTML
    src = EkurhuleniEastTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ekurhuleni_east_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.ekurhuleni_east_tvet import EkurhuleniEastTvetSource
    src = EkurhuleniEastTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
