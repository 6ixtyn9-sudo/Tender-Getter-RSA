"""Tests for the Independent Police Investigative Directorate (IPID) tender source plug-in."""
import pytest


def test_ipid_tenders_source_initialization():
    from tender_getter.sources.chapter9.ipid_tenders import IpidSource
    src = IpidSource()
    assert src.source_id == "ipid_tenders"
    assert src.live is True


def test_ipid_tenders_parse_mock_html():
    from tender_getter.sources.chapter9.ipid_tenders import IpidSource, MOCK_HTML
    src = IpidSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ipid_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.chapter9.ipid_tenders import IpidSource
    src = IpidSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
