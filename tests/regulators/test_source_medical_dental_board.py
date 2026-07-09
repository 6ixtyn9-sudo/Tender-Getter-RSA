"""Tests for the Medical & Dental Board tender source plug-in."""
import pytest


def test_medical_dental_board_source_initialization():
    from tender_getter.sources.regulators.medical_dental_board import MedicalDentalBoardSource
    src = MedicalDentalBoardSource()
    assert src.source_id == "medical_dental_board"
    assert src.live is True


def test_medical_dental_board_parse_mock_html():
    from tender_getter.sources.regulators.medical_dental_board import MedicalDentalBoardSource, MOCK_HTML
    src = MedicalDentalBoardSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_medical_dental_board_fetch_uses_fallback_on_empty():
    from tender_getter.sources.regulators.medical_dental_board import MedicalDentalBoardSource
    src = MedicalDentalBoardSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
