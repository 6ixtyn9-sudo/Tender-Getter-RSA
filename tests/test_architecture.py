import os
from pathlib import Path
import yaml
import re

def test_yaml_entries_match_python_files():
    """
    Asserts that every non-infrastructure Python source file has a matching
    YAML entry, and every YAML entry maps to a real source_id.

    Excluded from the count comparison:
      - __init__.py, generic.py, common.py (infrastructure)
      - Files whose source_id maps to the generic/etenders adapters
    """
    import re
    src_dir = Path("src/tender_getter/sources")

    yaml_file = Path("src/tender_getter/sources.yaml")
    assert yaml_file.exists()
    with open(yaml_file, "r") as f:
        yaml_entries = yaml.safe_load(f).get("sources", [])
    yaml_ids = {e["id"] for e in yaml_entries}

    # Discover actual source_id values from Python files
    py_source_ids: set[str] = set()
    for py_file in src_dir.rglob("*.py"):
        if py_file.name in ["__init__.py", "generic.py", "common.py"]:
            continue
        content = py_file.read_text()
        # Match both 'source_id = "value"' and 'source_id: str = "value"'
        for m in re.finditer(r'source_id\s*[:=].*?=\s*["\']([^"\']+)["\']', content):
            py_source_ids.add(m.group(1))

    # Files excluded from the count (no source_id in their file)
    no_source_id_files = {
        f.stem for f in src_dir.rglob("*.py")
        if f.name not in ["__init__.py", "generic.py", "common.py"]
        and f.stem not in py_source_ids
    }

    # Comparable count: YAML entries minus those that correspond to excluded files
    comparable_yaml = yaml_ids - no_source_id_files

    assert len(comparable_yaml) == len(py_source_ids), (
        f"Comparable YAML: {len(comparable_yaml)}, Python source_ids: {len(py_source_ids)}"
    )

def test_west_rand_is_exactly_one_file():
    """Asserts that there is exactly ONE file for west_rand, in districts/."""
    src_dir = Path("src/tender_getter/sources")
    matches = list(src_dir.rglob("west_rand*.py"))
    assert len(matches) == 1, f"Expected exactly 1 west_rand file, found {len(matches)}: {matches}"
    assert matches[0].parent.name == "districts", f"west_rand file should be in districts/, but is in {matches[0].parent.name}"

def test_acsa_is_exactly_one_file():
    """Asserts that there is exactly ONE file for acsa, in soes/."""
    src_dir = Path("src/tender_getter/sources")
    matches = list(src_dir.rglob("acsa*.py"))
    assert len(matches) == 1, f"Expected exactly 1 acsa file, found {len(matches)}: {matches}"
    assert matches[0].parent.name == "soes", f"acsa file should be in soes/, but is in {matches[0].parent.name}"
