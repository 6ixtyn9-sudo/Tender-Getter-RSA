"""Tests for the Companies and Intellectual Property Commission (CIPC) tender source plug-in."""
import pytest


def test_cipc_source_initialization():
    from tender_getter.sources.soes.cipc import CipcSource
    src = CipcSource()
    assert src.source_id == "cipc"
    assert isinstance(src.live, bool)


def test_cipc_parse_mock_html():
    from tender_getter.sources.soes.cipc import CipcSource, MOCK_HTML
    src = CipcSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_cipc_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.cipc import CipcSource
    src = CipcSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
