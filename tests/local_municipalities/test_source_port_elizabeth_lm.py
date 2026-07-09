"""Tests for the PE Municipality (legacy) tender source plug-in."""
import pytest


def test_port_elizabeth_lm_source_initialization():
    from tender_getter.sources.local_municipalities.port_elizabeth_lm import PortElizabethLmSource
    src = PortElizabethLmSource()
    assert src.source_id == "port_elizabeth_lm"
    assert isinstance(src.live, bool)


def test_port_elizabeth_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.port_elizabeth_lm import PortElizabethLmSource, MOCK_HTML
    src = PortElizabethLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_port_elizabeth_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.port_elizabeth_lm import PortElizabethLmSource
    src = PortElizabethLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
