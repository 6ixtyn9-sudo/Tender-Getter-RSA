import re
from pathlib import Path

source_dir = Path("src/tender_getter/sources")
tests_dir = Path("tests")

fixed_count = 0

for py_file in source_dir.rglob("*.py"):
    if py_file.name in ["__init__.py", "generic.py", "common.py", "etenders_ocds.py", "etenders_csv.py", "cidb_itender.py"]:
        continue
    
    # name without .py
    stem = py_file.stem
    category = py_file.parent.name
    
    test_file = tests_dir / f"test_source_{stem}.py"
    if not test_file.exists():
        # wait, some tests don't have _tenders if the filename doesn't
        # the test file convention is test_source_<stem>.py
        continue
        
    content = test_file.read_text()
    
    # We want to replace:
    # from tender_getter.sources.<old_category>.<stem> import
    # with:
    # from tender_getter.sources.<new_category>.<stem> import
    
    # Regex to match the old import.
    # It might be: from tender_getter.sources.research_extra.acsa_tenders import
    pattern = r"from tender_getter\.sources\.[a-zA-Z0-9_]+\." + re.escape(stem) + r"\b"
    new_import = f"from tender_getter.sources.{category}.{stem}"
    
    new_content, count = re.subn(pattern, new_import, content)
    
    if count > 0 and new_content != content:
        test_file.write_text(new_content)
        fixed_count += 1

print(f"Fixed imports in {fixed_count} test files.")
