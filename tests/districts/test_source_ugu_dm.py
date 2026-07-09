"""Tests for the Ugu District Municipality tender source plug-in."""
import pytest


def test_ugu_dm_source_initialization():
    from tender_getter.sources.districts.ugu_dm import UguDmSource
    src = UguDmSource()
    assert src.source_id == "ugu_dm"
    assert isinstance(src.live, bool)



