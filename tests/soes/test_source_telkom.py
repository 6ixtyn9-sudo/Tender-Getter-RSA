"""Tests for the Telkom SA SOC Ltd tender source plug-in."""
import pytest


def test_telkom_source_initialization():
    from tender_getter.sources.soes.telkom import TelkomSource
    src = TelkomSource()
    assert src.source_id == "telkom"
    assert src.live is True


def test_telkom_parse_mock_html():
    from tender_getter.sources.soes.telkom import TelkomSource, MOCK_HTML
    src = TelkomSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_telkom_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.telkom import TelkomSource
    src = TelkomSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
