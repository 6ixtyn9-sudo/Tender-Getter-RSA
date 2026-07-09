"""Tests for the Transnet Port Terminals (TPT) tender source plug-in."""
import pytest


def test_tpt_source_initialization():
    from tender_getter.sources.soes.tpt import TptSource
    src = TptSource()
    assert src.source_id == "tpt"
    assert isinstance(src.live, bool)


def test_tpt_parse_mock_html():
    from tender_getter.sources.soes.tpt import TptSource, MOCK_HTML
    src = TptSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_tpt_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.tpt import TptSource
    src = TptSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
