"""Tests for the Ekurhuleni Metropolitan Municipality tender source plug-in."""
import pytest


def test_ekurhuleni_tenders_source_initialization():
    from tender_getter.sources.research_extra.ekurhuleni_tenders import EkurhuleniSource
    src = EkurhuleniSource()
    assert src.source_id == "ekurhuleni_tenders"
    assert src.live is True


def test_ekurhuleni_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.ekurhuleni_tenders import EkurhuleniSource, MOCK_HTML
    src = EkurhuleniSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ekurhuleni_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.ekurhuleni_tenders import EkurhuleniSource
    src = EkurhuleniSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
