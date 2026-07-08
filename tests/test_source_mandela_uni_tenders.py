"""Tests for the Nelson Mandela University (legacy) tender source plug-in."""
import pytest


def test_mandela_uni_tenders_source_initialization():
    from tender_getter.sources.universities.mandela_uni_tenders import MandelaUniSource
    src = MandelaUniSource()
    assert src.source_id == "mandela_uni_tenders"
    assert src.live is True


def test_mandela_uni_tenders_parse_mock_html():
    from tender_getter.sources.universities.mandela_uni_tenders import MandelaUniSource, MOCK_HTML
    src = MandelaUniSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mandela_uni_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.universities.mandela_uni_tenders import MandelaUniSource
    src = MandelaUniSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
