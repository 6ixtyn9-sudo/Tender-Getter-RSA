import pytest
from tender_getter.sources.research.hsrc import HsrcSource
def test_hsrc_source_initialization():
    source = HsrcSource()
    assert source.source_id == "hsrc"
    assert source.url.startswith("http")

