"""Tests for the Xhariep District Municipality tender source plug-in."""
import pytest


def test_xhariep_dm_tenders_source_initialization():
    from tender_getter.sources.districts_full.xhariep_dm_tenders import XhariepDmSource
    src = XhariepDmSource()
    assert src.source_id == "xhariep_dm_tenders"
    assert src.live is True


def test_xhariep_dm_tenders_parse_mock_html():
    from tender_getter.sources.districts_full.xhariep_dm_tenders import XhariepDmSource, MOCK_HTML
    src = XhariepDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_xhariep_dm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts_full.xhariep_dm_tenders import XhariepDmSource
    src = XhariepDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
