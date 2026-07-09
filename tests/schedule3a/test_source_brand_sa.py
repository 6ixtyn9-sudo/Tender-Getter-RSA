"""Tests for the Brand South Africa tender source plug-in."""
import pytest


def test_brand_sa_source_initialization():
    from tender_getter.sources.schedule3a.brand_sa import BrandSaSource
    src = BrandSaSource()
    assert src.source_id == "brand_sa"
    assert isinstance(src.live, bool)


def test_brand_sa_parse_mock_html():
    from tender_getter.sources.schedule3a.brand_sa import BrandSaSource, MOCK_HTML
    src = BrandSaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_brand_sa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.brand_sa import BrandSaSource
    src = BrandSaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
