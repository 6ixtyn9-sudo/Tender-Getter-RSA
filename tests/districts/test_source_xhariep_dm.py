"""Tests for the Xhariep District Municipality tender source plug-in."""
import pytest


def test_xhariep_dm_source_initialization():
    from tender_getter.sources.districts.xhariep_dm import XhariepDmSource
    src = XhariepDmSource()
    assert src.source_id == "xhariep_dm"
    assert isinstance(src.live, bool)


def test_xhariep_dm_parse_mock_html():
    from tender_getter.sources.districts.xhariep_dm import XhariepDmSource, MOCK_HTML
    src = XhariepDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_xhariep_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.xhariep_dm import XhariepDmSource
    src = XhariepDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
