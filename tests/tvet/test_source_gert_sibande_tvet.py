"""Tests for the Gert Sibande TVET College tender source plug-in."""
import pytest


def test_gert_sibande_tvet_source_initialization():
    from tender_getter.sources.tvet.gert_sibande_tvet import GertSibandeTvetSource
    src = GertSibandeTvetSource()
    assert src.source_id == "gert_sibande_tvet"
    assert isinstance(src.live, bool)


def test_gert_sibande_tvet_parse_mock_html():
    from tender_getter.sources.tvet.gert_sibande_tvet import GertSibandeTvetSource, MOCK_HTML
    src = GertSibandeTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gert_sibande_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.gert_sibande_tvet import GertSibandeTvetSource
    src = GertSibandeTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
