"""Tests for the Pixley Ka Seme District Municipality tender source plug-in."""
import pytest


def test_pixley_ka_seme_dm_source_initialization():
    from tender_getter.sources.districts.pixley_ka_seme_dm import PixleyKaSemeDmSource
    src = PixleyKaSemeDmSource()
    assert src.source_id == "pixley_ka_seme_dm"
    assert isinstance(src.live, bool)


def test_pixley_ka_seme_dm_parse_mock_html():
    from tender_getter.sources.districts.pixley_ka_seme_dm import PixleyKaSemeDmSource, MOCK_HTML
    src = PixleyKaSemeDmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_pixley_ka_seme_dm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.districts.pixley_ka_seme_dm import PixleyKaSemeDmSource
    src = PixleyKaSemeDmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
