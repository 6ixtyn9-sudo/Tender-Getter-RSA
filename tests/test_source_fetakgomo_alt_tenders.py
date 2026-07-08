"""Tests for the Fetakgomo (alt) tender source plug-in."""
import pytest


def test_fetakgomo_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.fetakgomo_alt_tenders import FetakgomoAltSource
    src = FetakgomoAltSource()
    assert src.source_id == "fetakgomo_alt_tenders"
    assert src.live is False


def test_fetakgomo_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.fetakgomo_alt_tenders import FetakgomoAltSource, MOCK_HTML
    src = FetakgomoAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fetakgomo_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.fetakgomo_alt_tenders import FetakgomoAltSource
    src = FetakgomoAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
