"""Tests for the Eastern Cape Department of Education tender source plug-in."""
import pytest


def test_ec_education_tenders_source_initialization():
    from tender_getter.sources.research_extra.ec_education_tenders import EcEducationSource
    src = EcEducationSource()
    assert src.source_id == "ec_education_tenders"
    assert src.live is True


def test_ec_education_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.ec_education_tenders import EcEducationSource, MOCK_HTML
    src = EcEducationSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_education_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.ec_education_tenders import EcEducationSource
    src = EcEducationSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
