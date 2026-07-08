"""Tests for the PPRA (alt) tender source plug-in."""
import pytest


def test_property_practitioners_source_initialization():
    from tender_getter.sources.research.property_practitioners import PropertyPractitionersSource
    src = PropertyPractitionersSource()
    assert src.source_id == "property_practitioners"
    assert src.live is True


def test_property_practitioners_parse_mock_html():
    from tender_getter.sources.research.property_practitioners import PropertyPractitionersSource, MOCK_HTML
    src = PropertyPractitionersSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_property_practitioners_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.property_practitioners import PropertyPractitionersSource
    src = PropertyPractitionersSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
