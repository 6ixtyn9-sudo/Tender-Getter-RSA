"""Tests for the Vuselela TVET College tender source plug-in."""
import pytest


def test_vuselela_tvet_source_initialization():
    from tender_getter.sources.tvet.vuselela_tvet import VuselelaTvetSource
    src = VuselelaTvetSource()
    assert src.source_id == "vuselela_tvet"
    assert isinstance(src.live, bool)


def test_vuselela_tvet_parse_mock_html():
    from tender_getter.sources.tvet.vuselela_tvet import VuselelaTvetSource, MOCK_HTML
    src = VuselelaTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_vuselela_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.vuselela_tvet import VuselelaTvetSource
    src = VuselelaTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
