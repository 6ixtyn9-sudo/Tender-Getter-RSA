"""Tests for the Mnambithi TVET College tender source plug-in."""
import pytest


def test_mnambithi_tvet_source_initialization():
    from tender_getter.sources.tvet.mnambithi_tvet import MnambithiTvetSource
    src = MnambithiTvetSource()
    assert src.source_id == "mnambithi_tvet"
    assert isinstance(src.live, bool)


def test_mnambithi_tvet_parse_mock_html():
    from tender_getter.sources.tvet.mnambithi_tvet import MnambithiTvetSource, MOCK_HTML
    src = MnambithiTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mnambithi_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.mnambithi_tvet import MnambithiTvetSource
    src = MnambithiTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
