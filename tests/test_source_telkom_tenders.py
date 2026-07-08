"""Tests for the Telkom SA SOC Ltd tender source plug-in."""
import pytest


def test_telkom_tenders_source_initialization():
    from tender_getter.sources.soes_extra.telkom_tenders import TelkomSource
    src = TelkomSource()
    assert src.source_id == "telkom_tenders"
    assert src.live is True


def test_telkom_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.telkom_tenders import TelkomSource, MOCK_HTML
    src = TelkomSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_telkom_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.telkom_tenders import TelkomSource
    src = TelkomSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
