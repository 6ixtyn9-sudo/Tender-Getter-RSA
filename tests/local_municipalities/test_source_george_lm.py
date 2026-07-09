"""Tests for the George Municipality tender source plug-in."""
import pytest


def test_george_lm_source_initialization():
    from tender_getter.sources.local_municipalities.george_lm import GeorgeLmSource
    src = GeorgeLmSource()
    assert src.source_id == "george_lm"
    assert isinstance(src.live, bool)



