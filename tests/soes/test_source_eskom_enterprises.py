"""Tests for the Eskom Enterprises tender source plug-in."""
import pytest


def test_eskom_enterprises_source_initialization():
    from tender_getter.sources.soes.eskom_enterprises import EskomEnterprisesSource
    src = EskomEnterprisesSource()
    assert src.source_id == "eskom_enterprises"
    assert isinstance(src.live, bool)


def test_eskom_enterprises_parse_mock_html():
    from tender_getter.sources.soes.eskom_enterprises import EskomEnterprisesSource, MOCK_HTML
    src = EskomEnterprisesSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_eskom_enterprises_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.eskom_enterprises import EskomEnterprisesSource
    src = EskomEnterprisesSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
