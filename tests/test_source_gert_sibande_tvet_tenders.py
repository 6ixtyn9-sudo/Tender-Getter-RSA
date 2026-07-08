"""Tests for the Gert Sibande TVET College tender source plug-in."""
import pytest


def test_gert_sibande_tvet_tenders_source_initialization():
    from tender_getter.sources.tvet.gert_sibande_tvet_tenders import GertSibandeTvetSource
    src = GertSibandeTvetSource()
    assert src.source_id == "gert_sibande_tvet_tenders"
    assert src.live is True


def test_gert_sibande_tvet_tenders_parse_mock_html():
    from tender_getter.sources.tvet.gert_sibande_tvet_tenders import GertSibandeTvetSource, MOCK_HTML
    src = GertSibandeTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gert_sibande_tvet_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.gert_sibande_tvet_tenders import GertSibandeTvetSource
    src = GertSibandeTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
