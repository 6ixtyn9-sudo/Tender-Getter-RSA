"""Tests for the False Bay TVET College tender source plug-in."""
import pytest


def test_false_bay_tvet_source_initialization():
    from tender_getter.sources.tvet.false_bay_tvet import FalseBayTvetSource
    src = FalseBayTvetSource()
    assert src.source_id == "false_bay_tvet"
    assert isinstance(src.live, bool)



