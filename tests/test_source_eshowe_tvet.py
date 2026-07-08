"""Tests for the Eshowe TVET College tender source plug-in."""
import pytest


def test_eshowe_tvet_source_initialization():
    from tender_getter.sources.tvet.eshowe_tvet import EshoweTvetSource
    src = EshoweTvetSource()
    assert src.source_id == "eshowe_tvet"
    assert src.live is True


def test_eshowe_tvet_parse_mock_html():
    from tender_getter.sources.tvet.eshowe_tvet import EshoweTvetSource, MOCK_HTML
    src = EshoweTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_eshowe_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.eshowe_tvet import EshoweTvetSource
    src = EshoweTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
