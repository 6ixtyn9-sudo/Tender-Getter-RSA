"""Tests for the Denel Dynamics tender source plug-in."""
import pytest


def test_denel_dynamics_tenders_source_initialization():
    from tender_getter.sources.soes_extra.denel_dynamics_tenders import DenelDynamicsSource
    src = DenelDynamicsSource()
    assert src.source_id == "denel_dynamics_tenders"
    assert src.live is True


def test_denel_dynamics_tenders_parse_mock_html():
    from tender_getter.sources.soes_extra.denel_dynamics_tenders import DenelDynamicsSource, MOCK_HTML
    src = DenelDynamicsSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_denel_dynamics_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.soes_extra.denel_dynamics_tenders import DenelDynamicsSource
    src = DenelDynamicsSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
