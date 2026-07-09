"""Tests for the Fetakgomo Tubatse Local Municipality tender source plug-in."""
import pytest


def test_fetakgomo_tubatse_lm_source_initialization():
    from tender_getter.sources.local_municipalities.fetakgomo_tubatse_lm import FetakgomoTubatseLmSource
    src = FetakgomoTubatseLmSource()
    assert src.source_id == "fetakgomo_tubatse_lm"
    assert isinstance(src.live, bool)


def test_fetakgomo_tubatse_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.fetakgomo_tubatse_lm import FetakgomoTubatseLmSource, MOCK_HTML
    src = FetakgomoTubatseLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_fetakgomo_tubatse_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.fetakgomo_tubatse_lm import FetakgomoTubatseLmSource
    src = FetakgomoTubatseLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
