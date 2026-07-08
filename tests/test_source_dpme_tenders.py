"""Tests for the Department of Planning, Monitoring & Evaluation tender source plug-in."""
import pytest


def test_dpme_tenders_source_initialization():
    from tender_getter.sources.research_extra.dpme_tenders import DpmeSource
    src = DpmeSource()
    assert src.source_id == "dpme_tenders"
    assert src.live is True


def test_dpme_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.dpme_tenders import DpmeSource, MOCK_HTML
    src = DpmeSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dpme_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.dpme_tenders import DpmeSource
    src = DpmeSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
