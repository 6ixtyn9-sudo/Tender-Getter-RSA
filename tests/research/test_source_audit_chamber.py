"""Tests for the Auditor Chamber tender source plug-in."""
import pytest


def test_audit_chamber_source_initialization():
    from tender_getter.sources.research.audit_chamber import AuditChamberSource
    src = AuditChamberSource()
    assert src.source_id == "audit_chamber"
    assert src.live is True


def test_audit_chamber_parse_mock_html():
    from tender_getter.sources.research.audit_chamber import AuditChamberSource, MOCK_HTML
    src = AuditChamberSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_audit_chamber_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.audit_chamber import AuditChamberSource
    src = AuditChamberSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
