"""Tests for the Commission for the Promotion and Protection of the Rights of Cultural, Religious and Linguistic Communities (CRL) tender source plug-in."""
import pytest


def test_crl_source_initialization():
    from tender_getter.sources.chapter9.crl import CrlSource
    src = CrlSource()
    assert src.source_id == "crl"
    assert isinstance(src.live, bool)


def test_crl_parse_mock_html():
    from tender_getter.sources.chapter9.crl import CrlSource, MOCK_HTML
    src = CrlSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_crl_fetch_uses_fallback_on_empty():
    from tender_getter.sources.chapter9.crl import CrlSource
    src = CrlSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
