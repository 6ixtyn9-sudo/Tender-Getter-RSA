"""Tests for the Tshwane University of Technology tender source plug-in."""
import pytest


def test_tut_source_initialization():
    from tender_getter.sources.universities.tut import TutSource
    src = TutSource()
    assert src.source_id == "tut"
    assert isinstance(src.live, bool)


def test_tut_parse_mock_html():
    from tender_getter.sources.universities.tut import TutSource, MOCK_HTML
    src = TutSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tut_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.tut import TutSource
    src = TutSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
