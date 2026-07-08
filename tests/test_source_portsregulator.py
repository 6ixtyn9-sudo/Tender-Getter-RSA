"""Tests for the Ports Regulator of South Africa tender source plug-in."""
import pytest


def test_portsregulator_source_initialization():
    from tender_getter.sources.regulators.portsregulator import PortsregulatorSource
    src = PortsregulatorSource()
    assert src.source_id == "portsregulator"
    assert src.live is True


def test_portsregulator_parse_mock_html():
    from tender_getter.sources.regulators.portsregulator import PortsregulatorSource, MOCK_HTML
    src = PortsregulatorSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_portsregulator_fetch_uses_fallback_on_empty():
    from tender_getter.sources.regulators.portsregulator import PortsregulatorSource
    src = PortsregulatorSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
