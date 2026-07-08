"""Tests for the Independent Communications Authority of South Africa (ICASA) tender source plug-in."""
import pytest


def test_icasa_tenders_source_initialization():
    from tender_getter.sources.chapter9.icasa_tenders import IcasaSource
    src = IcasaSource()
    assert src.source_id == "icasa_tenders"
    assert src.live is True


def test_icasa_tenders_parse_mock_html():
    from tender_getter.sources.chapter9.icasa_tenders import IcasaSource, MOCK_HTML
    src = IcasaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_icasa_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.chapter9.icasa_tenders import IcasaSource
    src = IcasaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
