"""Tests for the Lekwetse LM tender source plug-in."""
import pytest


def test_lekwetse_lm_source_initialization():
    from tender_getter.sources.local_municipalities.lekwetse_lm import LekwetseLmSource
    src = LekwetseLmSource()
    assert src.source_id == "lekwetse_lm"
    assert isinstance(src.live, bool)


def test_lekwetse_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.lekwetse_lm import LekwetseLmSource, MOCK_HTML
    src = LekwetseLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lekwetse_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.lekwetse_lm import LekwetseLmSource
    src = LekwetseLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
