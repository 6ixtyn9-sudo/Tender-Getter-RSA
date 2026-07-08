"""Tests for the Moretele LM tender source plug-in."""
import pytest


def test_moretele_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.moretele_lm_tenders import MoreteleLmSource
    src = MoreteleLmSource()
    assert src.source_id == "moretele_lm_tenders"
    assert src.live is False


def test_moretele_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.moretele_lm_tenders import MoreteleLmSource, MOCK_HTML
    src = MoreteleLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_moretele_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.moretele_lm_tenders import MoreteleLmSource
    src = MoreteleLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
