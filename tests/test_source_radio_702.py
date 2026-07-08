"""Tests for the Radio 702 tender source plug-in."""
import pytest


def test_radio_702_source_initialization():
    from tender_getter.sources.research.radio_702 import Radio702Source
    src = Radio702Source()
    assert src.source_id == "radio_702"
    assert src.live is False


def test_radio_702_parse_mock_html():
    from tender_getter.sources.research.radio_702 import Radio702Source, MOCK_HTML
    src = Radio702Source()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_radio_702_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.radio_702 import Radio702Source
    src = Radio702Source()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
