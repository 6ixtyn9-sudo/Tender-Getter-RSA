import os
import re
from pathlib import Path

tests_dir = Path('tests')

for filepath in tests_dir.rglob("test_source_*.py"):
    content = filepath.read_text()
    
    # We want to replace imports from sources.xxxx_tenders to sources.xxxx
    # And variables like src.source_id == "xxxx_tenders"
    # We can just replace '_tenders' with '' inside the tests, BUT
    # we have to be careful with 'etenders'.
    
    # Safe replacement: only replace _tenders
    new_content = content.replace('_tenders', '')
    
    if new_content != content:
        filepath.write_text(new_content)
        
    if '_tenders.py' in filepath.name:
        new_name = filepath.name.replace('_tenders.py', '.py')
        filepath.rename(filepath.parent / new_name)

print("Finished renaming tests.")
