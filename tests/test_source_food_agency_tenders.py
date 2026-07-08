"""Tests for the Food Agency tender source plug-in."""
import pytest


def test_food_agency_tenders_source_initialization():
    from tender_getter.sources.research_extra.food_agency_tenders import FoodAgencySource
    src = FoodAgencySource()
    assert src.source_id == "food_agency_tenders"
    assert src.live is False


def test_food_agency_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.food_agency_tenders import FoodAgencySource, MOCK_HTML
    src = FoodAgencySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_food_agency_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.food_agency_tenders import FoodAgencySource
    src = FoodAgencySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
