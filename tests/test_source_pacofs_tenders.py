"""Tests for the Performing Arts Centre of the Free State (PACOFS) tender source plug-in."""
import pytest


def test_pacofs_tenders_source_initialization():
    from tender_getter.sources.research_extra.pacofs_tenders import PacofsSource
    src = PacofsSource()
    assert src.source_id == "pacofs_tenders"
    assert src.live is True


def test_pacofs_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.pacofs_tenders import PacofsSource, MOCK_HTML
    src = PacofsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_pacofs_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.pacofs_tenders import PacofsSource
    src = PacofsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
