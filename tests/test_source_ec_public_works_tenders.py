"""Tests for the Eastern Cape Department of Public Works tender source plug-in."""
import pytest


def test_ec_public_works_tenders_source_initialization():
    from tender_getter.sources.research_extra.ec_public_works_tenders import EcPublicWorksSource
    src = EcPublicWorksSource()
    assert src.source_id == "ec_public_works_tenders"
    assert src.live is True


def test_ec_public_works_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.ec_public_works_tenders import EcPublicWorksSource, MOCK_HTML
    src = EcPublicWorksSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_public_works_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.ec_public_works_tenders import EcPublicWorksSource
    src = EcPublicWorksSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
