"""Tests for the The Presidency tender source plug-in."""
import pytest


def test_presidency_tenders_source_initialization():
    from tender_getter.sources.research_extra.presidency_tenders import PresidencySource
    src = PresidencySource()
    assert src.source_id == "presidency_tenders"
    assert src.live is True


def test_presidency_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.presidency_tenders import PresidencySource, MOCK_HTML
    src = PresidencySource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_presidency_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.presidency_tenders import PresidencySource
    src = PresidencySource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
