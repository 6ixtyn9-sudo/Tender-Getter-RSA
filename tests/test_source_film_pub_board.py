"""Tests for the Film and Publication Board tender source plug-in."""
import pytest


def test_film_pub_board_source_initialization():
    from tender_getter.sources.regulators.film_pub_board import FilmPubBoardSource
    src = FilmPubBoardSource()
    assert src.source_id == "film_pub_board"
    assert src.live is True


def test_film_pub_board_parse_mock_html():
    from tender_getter.sources.regulators.film_pub_board import FilmPubBoardSource, MOCK_HTML
    src = FilmPubBoardSource()
    tenders = src.parse_html(MOCK_HTML)
    assert len(tenders) >= 2


def test_film_pub_board_fetch_uses_fallback_on_empty():
    from tender_getter.sources.regulators.film_pub_board import FilmPubBoardSource
    src = FilmPubBoardSource()
    tenders = src.fetch(html_content="<html><body>no tenders here</body></html>")
    assert len(tenders) >= 2
