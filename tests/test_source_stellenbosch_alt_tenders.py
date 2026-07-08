"""Tests for the Stellenbosch (alt) tender source plug-in."""
import pytest


def test_stellenbosch_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.stellenbosch_alt_tenders import StellenboschAltSource
    src = StellenboschAltSource()
    assert src.source_id == "stellenbosch_alt_tenders"
    assert src.live is True


def test_stellenbosch_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.stellenbosch_alt_tenders import StellenboschAltSource, MOCK_HTML
    src = StellenboschAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_stellenbosch_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.stellenbosch_alt_tenders import StellenboschAltSource
    src = StellenboschAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
