"""Tests for the Consumer Protection tender source plug-in."""
import pytest


def test_consumer_protection_source_initialization():
    from tender_getter.sources.research.consumer_protection import ConsumerProtectionSource
    src = ConsumerProtectionSource()
    assert src.source_id == "consumer_protection"
    assert isinstance(src.live, bool)


def test_consumer_protection_parse_mock_html():
    from tender_getter.sources.research.consumer_protection import ConsumerProtectionSource, MOCK_HTML
    src = ConsumerProtectionSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_consumer_protection_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research.consumer_protection import ConsumerProtectionSource
    src = ConsumerProtectionSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
