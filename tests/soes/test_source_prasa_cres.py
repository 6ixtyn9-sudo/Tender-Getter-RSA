"""Tests for the PRASA CRES (Capital, Real Estate & Sustainability) tender source plug-in."""
import pytest


def test_prasa_cres_source_initialization():
    from tender_getter.sources.soes.prasa_cres import PrasaCresSource
    src = PrasaCresSource()
    assert src.source_id == "prasa_cres"
    assert isinstance(src.live, bool)


def test_prasa_cres_parse_mock_html():
    from tender_getter.sources.soes.prasa_cres import PrasaCresSource, MOCK_HTML
    src = PrasaCresSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_prasa_cres_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.prasa_cres import PrasaCresSource
    src = PrasaCresSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
