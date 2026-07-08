"""Tests for the eThekwini Metropolitan Municipality tender source plug-in."""
import pytest


def test_ethekwini_tenders_source_initialization():
    from tender_getter.sources.research_extra.ethekwini_tenders import EthekwiniSource
    src = EthekwiniSource()
    assert src.source_id == "ethekwini_tenders"
    assert src.live is True


def test_ethekwini_tenders_parse_mock_html():
    from tender_getter.sources.research_extra.ethekwini_tenders import EthekwiniSource, MOCK_HTML
    src = EthekwiniSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_ethekwini_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.research_extra.ethekwini_tenders import EthekwiniSource
    src = EthekwiniSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
