"""Tests for the Civilian Secretariat for Police Service tender source plug-in."""
import pytest


def test_civilian_secretariat_police_tenders_source_initialization():
    from tender_getter.sources.schedule3a.civilian_secretariat_police_tenders import CivilianSecretariatPoliceSource
    src = CivilianSecretariatPoliceSource()
    assert src.source_id == "civilian_secretariat_police_tenders"
    assert src.live is True


def test_civilian_secretariat_police_tenders_parse_mock_html():
    from tender_getter.sources.schedule3a.civilian_secretariat_police_tenders import CivilianSecretariatPoliceSource, MOCK_HTML
    src = CivilianSecretariatPoliceSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_civilian_secretariat_police_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.schedule3a.civilian_secretariat_police_tenders import CivilianSecretariatPoliceSource
    src = CivilianSecretariatPoliceSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
