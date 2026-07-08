"""Tests for the Department of International Relations and Cooperation (DIRCO) tender source plug-in."""
import pytest


def test_dirco_source_initialization():
    from tender_getter.sources.schedule3a.dirco import DircoSource
    src = DircoSource()
    assert src.source_id == "dirco"
    assert src.live is True


def test_dirco_parse_mock_html():
    from tender_getter.sources.schedule3a.dirco import DircoSource, MOCK_HTML
    src = DircoSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_dirco_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.dirco import DircoSource
    src = DircoSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
