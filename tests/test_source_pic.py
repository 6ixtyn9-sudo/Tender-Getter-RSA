"""Tests for the Public Investment Corporation (PIC) tender source plug-in."""
import pytest


def test_pic_source_initialization():
    from tender_getter.sources.soes.pic import PicSource
    src = PicSource()
    assert src.source_id == "pic"
    assert src.live is True


def test_pic_parse_mock_html():
    from tender_getter.sources.soes.pic import PicSource, MOCK_HTML
    src = PicSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_pic_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.pic import PicSource
    src = PicSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
