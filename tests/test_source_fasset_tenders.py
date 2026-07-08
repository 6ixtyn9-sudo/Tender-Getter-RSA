"""Tests for the Finance and Accounting Services SETA (FASSET) tender source plug-in."""
import pytest


def test_fasset_tenders_source_initialization():
    from tender_getter.sources.setas.fasset_tenders import FassetSource
    src = FassetSource()
    assert src.source_id == "fasset_tenders"
    assert src.live is True


def test_fasset_tenders_parse_mock_html():
    from tender_getter.sources.setas.fasset_tenders import FassetSource, MOCK_HTML
    src = FassetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fasset_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.setas.fasset_tenders import FassetSource
    src = FassetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
