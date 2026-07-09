"""Tests for the Pixley Ka Seme LM tender source plug-in."""
import pytest


def test_pixley_ka_seme_lm_source_initialization():
    from tender_getter.sources.local_municipalities.pixley_ka_seme_lm import PixleyKaSemeLmSource
    src = PixleyKaSemeLmSource()
    assert src.source_id == "pixley_ka_seme_lm"
    assert isinstance(src.live, bool)


def test_pixley_ka_seme_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.pixley_ka_seme_lm import PixleyKaSemeLmSource, MOCK_HTML
    src = PixleyKaSemeLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_pixley_ka_seme_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.pixley_ka_seme_lm import PixleyKaSemeLmSource
    src = PixleyKaSemeLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
