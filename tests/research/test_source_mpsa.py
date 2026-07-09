"""Tests for the MPSA tender source plug-in."""
import pytest


def test_mpsa_source_initialization():
    from tender_getter.sources.research.mpsa import MpsaSource
    src = MpsaSource()
    assert src.source_id == "mpsa"
    assert isinstance(src.live, bool)


def test_mpsa_parse_mock_html():
    from tender_getter.sources.research.mpsa import MpsaSource, MOCK_HTML
    src = MpsaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mpsa_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.mpsa import MpsaSource
    src = MpsaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
