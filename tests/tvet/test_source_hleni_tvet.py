"""Tests for the Lephalale TVET College tender source plug-in."""
import pytest


def test_hleni_tvet_source_initialization():
    from tender_getter.sources.tvet.hleni_tvet import HleniTvetSource
    src = HleniTvetSource()
    assert src.source_id == "hleni_tvet"
    assert src.live is True


def test_hleni_tvet_parse_mock_html():
    from tender_getter.sources.tvet.hleni_tvet import HleniTvetSource, MOCK_HTML
    src = HleniTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_hleni_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.hleni_tvet import HleniTvetSource
    src = HleniTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
