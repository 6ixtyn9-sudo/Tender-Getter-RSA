"""Registry integrity tests.

The registry is discovered from executable classes, not source-text regexes.  This
prevents log strings and comments from being accidentally treated as source IDs.
"""
from tender_getter.aggregator import discover_source_classes
from tender_getter.sources import load_sources

# Metadata-only adapters are deliberately represented in YAML but are invoked
# outside normal class discovery.
ADAPTER_ONLY_IDS = {"etenders_csv", "etenders_ocds", "cidb_itender"}


def test_yaml_entries_match_discovered_source_classes():
    classes = discover_source_classes()
    class_ids = set(classes)
    yaml_ids = {entry["id"] for entry in load_sources()}
    assert class_ids - yaml_ids == set(), f"Source classes missing YAML metadata: {sorted(class_ids-yaml_ids)}"
    assert yaml_ids - class_ids - ADAPTER_ONLY_IDS == set(), f"YAML sources without classes: {sorted(yaml_ids-class_ids-ADAPTER_ONLY_IDS)}"
    assert len(class_ids) == len(classes)  # dict key uniqueness is now enforced during discovery


def test_west_rand_is_exactly_one_file():
    from pathlib import Path
    matches = list(Path("src/tender_getter/sources").rglob("west_rand*.py"))
    assert len(matches) == 1
    assert matches[0].parent.name == "districts"


def test_acsa_is_exactly_one_file():
    from pathlib import Path
    matches = list(Path("src/tender_getter/sources").rglob("acsa*.py"))
    assert len(matches) == 1
    assert matches[0].parent.name == "soes"
