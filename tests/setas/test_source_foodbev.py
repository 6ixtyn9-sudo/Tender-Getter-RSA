"""Tests for the Food and Beverage Manufacturing SETA (FoodBev) tender source plug-in."""
import pytest


def test_foodbev_source_initialization():
    from tender_getter.sources.setas.foodbev import FoodbevSource
    src = FoodbevSource()
    assert src.source_id == "foodbev"
    assert isinstance(src.live, bool)


def test_foodbev_parse_mock_html():
    from tender_getter.sources.setas.foodbev import FoodbevSource, MOCK_HTML
    src = FoodbevSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_foodbev_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.foodbev import FoodbevSource
    src = FoodbevSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
