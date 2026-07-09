"""Tests for the Stevetsberg LM tender source plug-in."""
import pytest


def test_stevetsberg_lm_source_initialization():
    from tender_getter.sources.local_municipalities.stevetsberg_lm import StevetsbergLmSource
    src = StevetsbergLmSource()
    assert src.source_id == "stevetsberg_lm"
    assert src.live is False


def test_stevetsberg_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.stevetsberg_lm import StevetsbergLmSource, MOCK_HTML
    src = StevetsbergLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_stevetsberg_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.stevetsberg_lm import StevetsbergLmSource
    src = StevetsbergLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
