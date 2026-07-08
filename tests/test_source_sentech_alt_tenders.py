"""Tests for the Sentech (alt URL) tender source plug-in."""
import pytest


def test_sentech_alt_tenders_source_initialization():
    from tender_getter.sources.schedule3a.sentech_alt_tenders import SentechAltSource
    src = SentechAltSource()
    assert src.source_id == "sentech_alt_tenders"
    assert src.live is True


def test_sentech_alt_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.sentech_alt_tenders import SentechAltSource, MOCK_HTML
    src = SentechAltSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sentech_alt_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.sentech_alt_tenders import SentechAltSource
    src = SentechAltSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
