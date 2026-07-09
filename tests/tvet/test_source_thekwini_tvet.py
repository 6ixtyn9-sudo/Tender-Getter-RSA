"""Tests for the Thekwini TVET College tender source plug-in."""
import pytest


def test_thekwini_tvet_source_initialization():
    from tender_getter.sources.tvet.thekwini_tvet import ThekwiniTvetSource
    src = ThekwiniTvetSource()
    assert src.source_id == "thekwini_tvet"
    assert isinstance(src.live, bool)


def test_thekwini_tvet_parse_mock_html():
    from tender_getter.sources.tvet.thekwini_tvet import ThekwiniTvetSource, MOCK_HTML
    src = ThekwiniTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_thekwini_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.thekwini_tvet import ThekwiniTvetSource
    src = ThekwiniTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
