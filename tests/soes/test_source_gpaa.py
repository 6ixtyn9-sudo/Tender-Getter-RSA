"""Tests for the Government Pensions Administration Agency (GPAA) tender source plug-in."""
import pytest


def test_gpaa_source_initialization():
    from tender_getter.sources.soes.gpaa import GpaaSource
    src = GpaaSource()
    assert src.source_id == "gpaa"
    assert src.live is True


def test_gpaa_parse_mock_html():
    from tender_getter.sources.soes.gpaa import GpaaSource, MOCK_HTML
    src = GpaaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_gpaa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.gpaa import GpaaSource
    src = GpaaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
