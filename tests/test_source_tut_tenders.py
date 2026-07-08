"""Tests for the Tshwane University of Technology tender source plug-in."""
import pytest


def test_tut_tenders_source_initialization():
    from tender_getter.sources.universities.tut_tenders import TutSource
    src = TutSource()
    assert src.source_id == "tut_tenders"
    assert src.live is True


def test_tut_tenders_parse_mock_html():
    from tender_getter.sources.universities.tut_tenders import TutSource, MOCK_HTML
    src = TutSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tut_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.tut_tenders import TutSource
    src = TutSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
