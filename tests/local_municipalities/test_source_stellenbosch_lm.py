"""Tests for the Stellenbosch Municipality tender source plug-in."""
import pytest


def test_stellenbosch_lm_source_initialization():
    from tender_getter.sources.local_municipalities.stellenbosch_lm import StellenboschLmSource
    src = StellenboschLmSource()
    assert src.source_id == "stellenbosch_lm"
    assert src.live is True


def test_stellenbosch_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.stellenbosch_lm import StellenboschLmSource, MOCK_HTML
    src = StellenboschLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_stellenbosch_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.stellenbosch_lm import StellenboschLmSource
    src = StellenboschLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
