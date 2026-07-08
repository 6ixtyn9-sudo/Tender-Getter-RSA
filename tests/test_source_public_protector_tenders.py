"""Tests for the Office of the Public Protector tender source plug-in."""
import pytest


def test_public_protector_tenders_source_initialization():
    from tender_getter.sources.chapter9.public_protector_tenders import PublicProtectorSource
    src = PublicProtectorSource()
    assert src.source_id == "public_protector_tenders"
    assert src.live is True


def test_public_protector_tenders_parse_mock_html():
    from tender_getter.sources.chapter9.public_protector_tenders import PublicProtectorSource, MOCK_HTML
    src = PublicProtectorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_public_protector_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.chapter9.public_protector_tenders import PublicProtectorSource
    src = PublicProtectorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
