"""Tests for the Free State Tourism tender source plug-in."""
import pytest


def test_fs_tourism_source_initialization():
    from tender_getter.sources.research.fs_tourism import FsTourismSource
    src = FsTourismSource()
    assert src.source_id == "fs_tourism"
    assert isinstance(src.live, bool)


def test_fs_tourism_parse_mock_html():
    from tender_getter.sources.research.fs_tourism import FsTourismSource, MOCK_HTML
    src = FsTourismSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fs_tourism_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.fs_tourism import FsTourismSource
    src = FsTourismSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
