"""Tests for the Polokwane Local Municipality tender source plug-in."""
import pytest


def test_polokwane_lm_source_initialization():
    from tender_getter.sources.local_municipalities.polokwane_lm import PolokwaneLmSource
    src = PolokwaneLmSource()
    assert src.source_id == "polokwane_lm"
    assert src.live is True


def test_polokwane_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.polokwane_lm import PolokwaneLmSource, MOCK_HTML
    src = PolokwaneLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_polokwane_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.polokwane_lm import PolokwaneLmSource
    src = PolokwaneLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
