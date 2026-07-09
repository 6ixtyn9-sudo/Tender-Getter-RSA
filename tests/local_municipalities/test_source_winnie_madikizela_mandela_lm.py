"""Tests for the Winnie Madikizela-Mandela LM tender source plug-in."""
import pytest


def test_winnie_madikizela_mandela_lm_source_initialization():
    from tender_getter.sources.local_municipalities.winnie_madikizela_mandela_lm import WinnieMadikizelaMandelaLmSource
    src = WinnieMadikizelaMandelaLmSource()
    assert src.source_id == "winnie_madikizela_mandela_lm"
    assert isinstance(src.live, bool)


def test_winnie_madikizela_mandela_lm_parse_mock_html():
    from tender_getter.sources.local_municipalities.winnie_madikizela_mandela_lm import WinnieMadikizelaMandelaLmSource, MOCK_HTML
    src = WinnieMadikizelaMandelaLmSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_winnie_madikizela_mandela_lm_fetch_uses_fallback_on_empty():
    from tender_getter.sources.local_municipalities.winnie_madikizela_mandela_lm import WinnieMadikizelaMandelaLmSource
    src = WinnieMadikizelaMandelaLmSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
