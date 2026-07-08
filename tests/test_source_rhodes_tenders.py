"""Tests for the Rhodes University tender source plug-in."""
import pytest


def test_rhodes_tenders_source_initialization():
    from tender_getter.sources.universities.rhodes_tenders import RhodesSource
    src = RhodesSource()
    assert src.source_id == "rhodes_tenders"
    assert src.live is True


def test_rhodes_tenders_parse_mock_html():
    from tender_getter.sources.universities.rhodes_tenders import RhodesSource, MOCK_HTML
    src = RhodesSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_rhodes_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.rhodes_tenders import RhodesSource
    src = RhodesSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
