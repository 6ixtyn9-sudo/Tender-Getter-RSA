"""Tests for the SA Public Service Association tender source plug-in."""
import pytest


def test_sapsa_admin_source_initialization():
    from tender_getter.sources.research.sapsa_admin import SapsaAdminSource
    src = SapsaAdminSource()
    assert src.source_id == "sapsa_admin"
    assert src.live is False


def test_sapsa_admin_parse_mock_html():
    from tender_getter.sources.research.sapsa_admin import SapsaAdminSource, MOCK_HTML
    src = SapsaAdminSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_sapsa_admin_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.sapsa_admin import SapsaAdminSource
    src = SapsaAdminSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
