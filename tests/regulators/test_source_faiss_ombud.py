"""Tests for the Office of the Ombud for Financial Services Providers tender source plug-in."""
import pytest


def test_faiss_ombud_source_initialization():
    from tender_getter.sources.regulators.faiss_ombud import FaissOmbudSource
    src = FaissOmbudSource()
    assert src.source_id == "faiss_ombud"
    assert isinstance(src.live, bool)


def test_faiss_ombud_parse_mock_html():
    from tender_getter.sources.regulators.faiss_ombud import FaissOmbudSource, MOCK_HTML
    src = FaissOmbudSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_faiss_ombud_fetch_uses_fallback_on_empty():
    from tender_getter.sources.regulators.faiss_ombud import FaissOmbudSource
    src = FaissOmbudSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
