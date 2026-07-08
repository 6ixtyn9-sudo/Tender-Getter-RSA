"""Tests for the Pensions Fund Adjudicator tender source plug-in."""
import pytest


def test_pf_adjudicator_tenders_source_initialization():
    from tender_getter.sources.schedule3a.pf_adjudicator_tenders import PfAdjudicatorSource
    src = PfAdjudicatorSource()
    assert src.source_id == "pf_adjudicator_tenders"
    assert src.live is True


def test_pf_adjudicator_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.pf_adjudicator_tenders import PfAdjudicatorSource, MOCK_HTML
    src = PfAdjudicatorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_pf_adjudicator_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.pf_adjudicator_tenders import PfAdjudicatorSource
    src = PfAdjudicatorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
