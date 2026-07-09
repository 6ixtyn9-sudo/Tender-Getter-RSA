"""Tests for the Eastern Cape Heritage Council tender source plug-in."""
import pytest


def test_ec_heritage_source_initialization():
    from tender_getter.sources.research.ec_heritage import EcHeritageSource
    src = EcHeritageSource()
    assert src.source_id == "ec_heritage"
    assert isinstance(src.live, bool)


def test_ec_heritage_parse_mock_html():
    from tender_getter.sources.research.ec_heritage import EcHeritageSource, MOCK_HTML
    src = EcHeritageSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ec_heritage_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.ec_heritage import EcHeritageSource
    src = EcHeritageSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
