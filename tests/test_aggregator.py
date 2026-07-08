import pytest
from tender_getter.aggregator import discover_source_classes, get_all_source_instances, sync_all_sources


def test_discover_finds_many_sources():
    classes = discover_source_classes()
    # We expect at least 800 source classes (full registry is 845+)
    assert len(classes) >= 800
    # Check a few known ones are present
    assert "johannesburg_tenders" in classes
    assert "capetown_tenders" in classes
    assert "eskom_tenders" in classes
    # check at least one from each major category
    ids = set(classes.keys())
    assert any("gauteng" in s for s in ids)
    assert any("water" in s for s in ids)
    assert any("saps" in s or "prasa" in s for s in ids)


@pytest.mark.slow
def test_sync_all_runs_with_limit():
    summary = sync_all_sources(limit_per_source=1, verbose=False)
    assert summary["sources_total"] >= 800
    assert summary["sources_ok"] >= summary["sources_total"] * 0.9
    assert summary["tenders_unique"] >= 100
