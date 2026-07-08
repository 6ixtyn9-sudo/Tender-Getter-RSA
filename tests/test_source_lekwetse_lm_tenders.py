"""Tests for the Lekwetse LM tender source plug-in."""
import pytest


def test_lekwetse_lm_tenders_source_initialization():
    from tender_getter.sources.local_municipalities.lekwetse_lm_tenders import LekwetseLmSource
    src = LekwetseLmSource()
    assert src.source_id == "lekwetse_lm_tenders"
    assert src.live is False


def test_lekwetse_lm_tenders_parse_mock_html():
    from tender_getter.sources.local_municipalities.lekwetse_lm_tenders import LekwetseLmSource, MOCK_HTML
    src = LekwetseLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_lekwetse_lm_tenders_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.lekwetse_lm_tenders import LekwetseLmSource
    src = LekwetseLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
