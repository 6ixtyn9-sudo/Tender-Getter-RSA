"""Tests for the Autopax Passenger Services tender source plug-in."""
import pytest


def test_autopax_tenders_source_initialization():
    from tender_getter.sources.soes_extra.autopax_tenders import AutopaxSource
    src = AutopaxSource()
    assert src.source_id == "autopax_tenders"
    assert src.live is False


def test_autopax_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.autopax_tenders import AutopaxSource, MOCK_HTML
    src = AutopaxSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_autopax_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.autopax_tenders import AutopaxSource
    src = AutopaxSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
