"""Tests for the QS Council tender source plug-in."""
import pytest


def test_quantity_surveyors_council_source_initialization():
    from tender_getter.sources.research.quantity_surveyors_council import QuantitySurveyorsCouncilSource
    src = QuantitySurveyorsCouncilSource()
    assert src.source_id == "quantity_surveyors_council"
    assert src.live is False


def test_quantity_surveyors_council_parse_mock_html():
    from tender_getter.sources.research.quantity_surveyors_council import QuantitySurveyorsCouncilSource, MOCK_HTML
    src = QuantitySurveyorsCouncilSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_quantity_surveyors_council_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.quantity_surveyors_council import QuantitySurveyorsCouncilSource
    src = QuantitySurveyorsCouncilSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
