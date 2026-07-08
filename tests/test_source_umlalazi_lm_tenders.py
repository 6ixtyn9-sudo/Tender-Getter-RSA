"""Tests for the uMlalazi LM tender source plug-in."""
import pytest


def test_umlalazi_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.umlalazi_lm_tenders import UmlalaziLmSource
    src = UmlalaziLmSource()
    assert src.source_id == "umlalazi_lm_tenders"
    assert src.live is False


def test_umlalazi_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.umlalazi_lm_tenders import UmlalaziLmSource, MOCK_HTML
    src = UmlalaziLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_umlalazi_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.umlalazi_lm_tenders import UmlalaziLmSource
    src = UmlalaziLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
