"""Tests for the Port Elizabeth TVET College tender source plug-in."""
import pytest


def test_port_elizabeth_tvet_source_initialization():
    from tender_getter.sources.tvet.port_elizabeth_tvet import PortElizabethTvetSource
    src = PortElizabethTvetSource()
    assert src.source_id == "port_elizabeth_tvet"
    assert src.live is True


def test_port_elizabeth_tvet_parse_mock_html():
    from tender_getter.sources.tvet.port_elizabeth_tvet import PortElizabethTvetSource, MOCK_HTML
    src = PortElizabethTvetSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_port_elizabeth_tvet_fetch_uses_fallback_on_empty():
    from tender_getter.sources.tvet.port_elizabeth_tvet import PortElizabethTvetSource
    src = PortElizabethTvetSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
