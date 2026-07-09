"""Tests for the Mpumalanga Economic Growth Agency (MEGA) tender source plug-in."""
import pytest


def test_mp_dev_source_initialization():
    from tender_getter.sources.research.mp_dev import MpDevSource
    src = MpDevSource()
    assert src.source_id == "mp_dev"
    assert isinstance(src.live, bool)


def test_mp_dev_parse_mock_html():
    from tender_getter.sources.research.mp_dev import MpDevSource, MOCK_HTML
    src = MpDevSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_mp_dev_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.mp_dev import MpDevSource
    src = MpDevSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
