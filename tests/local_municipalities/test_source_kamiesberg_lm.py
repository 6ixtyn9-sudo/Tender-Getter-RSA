"""Tests for the Kamiesberg LM tender source plug-in."""
import pytest


def test_kamiesberg_lm_source_initialization():
    from tender_getter.sources.local_municipalities.kamiesberg_lm import KamiesbergLmSource
    src = KamiesbergLmSource()
    assert src.source_id == "kamiesberg_lm"
    assert src.live is False


def test_kamiesberg_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.kamiesberg_lm import KamiesbergLmSource, MOCK_HTML
    src = KamiesbergLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_kamiesberg_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.kamiesberg_lm import KamiesbergLmSource
    src = KamiesbergLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
