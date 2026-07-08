"""Tests for the Gauteng Tourism Authority tender source plug-in."""
import pytest


def test_gauteng_tourism_tenders_source_initialization():
    from tender_getter.sources.research_extra.gauteng_tourism_tenders import GautengTourismSource
    src = GautengTourismSource()
    assert src.source_id == "gauteng_tourism_tenders"
    assert src.live is False


def test_gauteng_tourism_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.gauteng_tourism_tenders import GautengTourismSource, MOCK_HTML
    src = GautengTourismSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gauteng_tourism_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.gauteng_tourism_tenders import GautengTourismSource
    src = GautengTourismSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
