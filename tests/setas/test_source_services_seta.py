"""Tests for the Services Sector Education and Training Authority (Services SETA) tender source plug-in."""
import pytest


def test_services_seta_source_initialization():
    from tender_getter.sources.setas.services_seta import ServicesSetaSource
    src = ServicesSetaSource()
    assert src.source_id == "services_seta"
    assert src.live is True


def test_services_seta_parse_mock_html():
    from tender_getter.sources.setas.services_seta import ServicesSetaSource, MOCK_HTML
    src = ServicesSetaSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_services_seta_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.services_seta import ServicesSetaSource
    src = ServicesSetaSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
