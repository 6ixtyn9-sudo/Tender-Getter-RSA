"""Tests for the Nkonkobe LM tender source plug-in."""
import pytest


def test_nkonkobe_lm_source_initialization():
    from tender_getter.sources.local_municipalities.nkonkobe_lm import NkonkobeLmSource
    src = NkonkobeLmSource()
    assert src.source_id == "nkonkobe_lm"
    assert src.live is False


def test_nkonkobe_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.nkonkobe_lm import NkonkobeLmSource, MOCK_HTML
    src = NkonkobeLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_nkonkobe_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.nkonkobe_lm import NkonkobeLmSource
    src = NkonkobeLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
