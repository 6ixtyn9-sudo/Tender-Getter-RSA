"""Tests for the Matlosana Local Municipality tender source plug-in."""
import pytest


def test_matlosana_lm_source_initialization():
    from tender_getter.sources.local_municipalities.matlosana_lm import MatlosanaLmSource
    src = MatlosanaLmSource()
    assert src.source_id == "matlosana_lm"
    assert isinstance(src.live, bool)


def test_matlosana_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.matlosana_lm import MatlosanaLmSource, MOCK_HTML
    src = MatlosanaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_matlosana_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.matlosana_lm import MatlosanaLmSource
    src = MatlosanaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
