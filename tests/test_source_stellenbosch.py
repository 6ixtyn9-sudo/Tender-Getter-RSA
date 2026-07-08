"""Tests for the Stellenbosch University tender source plug-in."""
import pytest


def test_stellenbosch_source_initialization():
    from tender_getter.sources.universities.stellenbosch import StellenboschSource
    src = StellenboschSource()
    assert src.source_id == "stellenbosch"
    assert src.live is True


def test_stellenbosch_parse_mock_html():
    from tender_getter.sources.universities.stellenbosch import StellenboschSource, MOCK_HTML
    src = StellenboschSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_stellenbosch_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.stellenbosch import StellenboschSource
    src = StellenboschSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
