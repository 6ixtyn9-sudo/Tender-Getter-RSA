import os
import shutil
from pathlib import Path

sources_dir = Path('src/tender_getter/sources')

for d in sources_dir.iterdir():
    if d.is_dir() and d.name not in ["__pycache__", "tests"]:
        py_files = [f for f in d.rglob("*.py") if f.name != "__init__.py"]
        if not py_files:
            print(f"Removing empty directory: {d}")
            shutil.rmtree(d)

