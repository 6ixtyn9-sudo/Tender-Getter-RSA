"""Tests for the Polokwane (alt) tender source plug-in."""
import pytest


def test_polokwane_lm_alt_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.polokwane_lm_alt_tenders import PolokwaneLmAltSource
    src = PolokwaneLmAltSource()
    assert src.source_id == "polokwane_lm_alt_tenders"
    assert src.live is True


def test_polokwane_lm_alt_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.polokwane_lm_alt_tenders import PolokwaneLmAltSource, MOCK_HTML
    src = PolokwaneLmAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_polokwane_lm_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.polokwane_lm_alt_tenders import PolokwaneLmAltSource
    src = PolokwaneLmAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
