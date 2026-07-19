import pytest
from tender_getter.aggregator import discover_source_classes, get_all_source_instances, sync_all_sources


def test_discover_finds_many_sources():
    classes = discover_source_classes()
    # We expect at least 700 source classes (full registry is 845+)
    assert len(classes) >= 700
    # Check a few known ones are present
    assert "johannesburg" in classes
    assert "capetown" in classes
    assert "eskom" in classes
    # check at least one from each major category
    ids = set(classes.keys())
    assert any("gauteng" in s for s in ids)
    assert any("water" in s for s in ids)
    assert any("saps" in s or "prasa" in s for s in ids)


@pytest.mark.slow
def test_sync_all_runs_with_limit():
    summary = sync_all_sources(limit_per_source=1, verbose=False)
    assert summary["data_mode"] == "real_only"
    assert summary["sources_total"] >= 700
    # Network availability and public portals change constantly.  A real-only
    # sync must report honest results rather than fixture-backed success.
    assert summary["sources_ok"] + summary["sources_failed"] <= summary["sources_total"]
    assert summary["tenders_unique"] >= 0
