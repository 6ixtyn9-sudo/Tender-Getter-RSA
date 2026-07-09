"""Tests for the Denel Dynamics tender source plug-in."""
import pytest


def test_denel_dynamics_source_initialization():
    from tender_getter.sources.soes.denel_dynamics import DenelDynamicsSource
    src = DenelDynamicsSource()
    assert src.source_id == "denel_dynamics"
    assert isinstance(src.live, bool)


def test_denel_dynamics_parse_mock_html():
    from tender_getter.sources.soes.denel_dynamics import DenelDynamicsSource, MOCK_HTML
    src = DenelDynamicsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_denel_dynamics_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes.denel_dynamics import DenelDynamicsSource
    src = DenelDynamicsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
