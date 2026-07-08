"""Tests for the Gauteng Provincial Treasury tender source plug-in."""
import pytest


def test_gauteng_etenders_source_initialization():
    from tender_getter.sources.research_extra.gauteng_etenders import GautengEtendersSource
    src = GautengEtendersSource()
    assert src.source_id == "gauteng_etenders"
    assert src.live is True


def test_gauteng_etenders_parse_mock_html():
    from tender_getter.sources.research_extra.gauteng_etenders import GautengEtendersSource, MOCK_HTML
    src = GautengEtendersSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gauteng_etenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.gauteng_etenders import GautengEtendersSource
    src = GautengEtendersSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
