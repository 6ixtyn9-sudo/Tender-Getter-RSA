"""Tests for the Mthashana TVET College tender source plug-in."""
import pytest


def test_mthashana_tvet_source_initialization():
    from tender_getter.sources.tvet.mthashana_tvet import MthashanaTvetSource
    src = MthashanaTvetSource()
    assert src.source_id == "mthashana_tvet"
    assert isinstance(src.live, bool)


def test_mthashana_tvet_parse_mock_html():
    from tender_getter.sources.tvet.mthashana_tvet import MthashanaTvetSource, MOCK_HTML
    src = MthashanaTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mthashana_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.mthashana_tvet import MthashanaTvetSource
    src = MthashanaTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
