"""Tests for the Chiro Council tender source plug-in."""
import pytest


def test_chiro_practitioner_tenders_source_initialization():
    from tender_getter.sources.research_extra.chiro_practitioner_tenders import ChiroPractitionerSource
    src = ChiroPractitionerSource()
    assert src.source_id == "chiro_practitioner_tenders"
    assert src.live is False


def test_chiro_practitioner_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.chiro_practitioner_tenders import ChiroPractitionerSource, MOCK_HTML
    src = ChiroPractitionerSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_chiro_practitioner_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.chiro_practitioner_tenders import ChiroPractitionerSource
    src = ChiroPractitionerSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
