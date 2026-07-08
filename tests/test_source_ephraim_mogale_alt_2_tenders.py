"""Tests for the Ephraim Mogale (alt 2) tender source plug-in."""
import pytest


def test_ephraim_mogale_alt_2_tenders_source_initialization():
    from tender_getter.sources.research_extra.ephraim_mogale_alt_2_tenders import EphraimMogaleAlt2Source
    src = EphraimMogaleAlt2Source()
    assert src.source_id == "ephraim_mogale_alt_2_tenders"
    assert src.live is False


def test_ephraim_mogale_alt_2_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.ephraim_mogale_alt_2_tenders import EphraimMogaleAlt2Source, MOCK_HTML
    src = EphraimMogaleAlt2Source()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ephraim_mogale_alt_2_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.ephraim_mogale_alt_2_tenders import EphraimMogaleAlt2Source
    src = EphraimMogaleAlt2Source()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
