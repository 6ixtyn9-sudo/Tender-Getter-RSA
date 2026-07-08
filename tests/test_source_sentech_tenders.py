"""Tests for the Sentech SOC Ltd tender source plug-in."""
import pytest


def test_sentech_tenders_source_initialization():
    from tender_getter.sources.research_extra.sentech_tenders import SentechSource
    src = SentechSource()
    assert src.source_id == "sentech_tenders"
    assert src.live is True


def test_sentech_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.sentech_tenders import SentechSource, MOCK_HTML
    src = SentechSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sentech_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.sentech_tenders import SentechSource
    src = SentechSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
