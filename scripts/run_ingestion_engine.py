#!/usr/bin/env python3
"""
run_ingestion_engine.py - Phase 1 Unified Aggregator & Scheduler

This script dynamically loads all registered sources from tender_getter.sources,
runs them concurrently with a conservative thread pool, deduplicates the
results, and pushes them to the database.

Usage:
 PYTHONPATH=src:. python scripts/run_ingestion_engine.py
"""

import sys
import time
import inspect
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load .env automatically if python-dotenv is installed
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

from tender_getter.database_base import TenderDatabaseBase
from tender_getter.database_sqlite import SQLiteTenderDatabase
from tender_getter.database_supabase import SupabaseTenderDatabase
import tender_getter.sources as sources
from tender_getter.sources import TenderSource

def get_database_client() -> TenderDatabaseBase:
    """Returns the appropriate DB client (Supabase if configured, else SQLite)."""
    try:
        db = SupabaseTenderDatabase()
        if db.test_connection():
            print("Connected to Supabase/PostgreSQL.")
            return db
    except Exception as e:
        print(f"Supabase connection skipped/failed: {e}")
    
    print("Falling back to local SQLite database.")
    db_path = Path("localdata/tenders.db")
    db_path.parent.mkdir(exist_ok=True)
    return SQLiteTenderDatabase(db_path=str(db_path))

def get_all_source_classes() -> list[type]:
    """Dynamically find all classes implementing TenderSource in the sources package."""
    source_classes = []
    for name in dir(sources):
        obj = getattr(sources, name)
        if inspect.isclass(obj) and issubclass(obj, TenderSource) and obj is not TenderSource:
            source_classes.append(obj)
    return source_classes

def run_source(source_class: type, db: TenderDatabaseBase) -> tuple[str, int, int, float]:
    """Instantiate and run a single source, saving results to the DB."""
    start_time = time.time()
    source_name = source_class.__name__
    fetched = 0
    saved = 0
    try:
        instance = source_class()
        tenders = instance.fetch()
        fetched = len(tenders)
        
        for tender in tenders:
            db.upsert_tender(tender)
            saved += 1
            
    except Exception as e:
        print(f"[{source_name}] Error during fetch: {e}")
        
    duration = time.time() - start_time
    return source_name, fetched, saved, duration

def main():
    print("==================================================")
    print(" TENDER GETTER RSA - PHASE 1 INGESTION ENGINE")
    print("==================================================")
    
    db = get_database_client()
    source_classes = get_all_source_classes()
    
    print(f"\nDiscovered {len(source_classes)} tender sources in registry.")
    print("Starting concurrent ingestion (max 5 workers to prevent IP bans)...")
    
    total_fetched = 0
    total_saved = 0
    start_time = time.time()
    
    # Using 5 workers to balance speed and politeness to government servers
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(run_source, cls, db): cls for cls in source_classes}
        
        for i, future in enumerate(as_completed(futures), 1):
            try:
                name, fetched, saved, duration = future.result()
                total_fetched += fetched
                total_saved += saved
                print(f"[{i}/{len(source_classes)}] {name} completed in {duration:.1f}s -> {saved} tenders saved")
            except Exception as exc:
                cls = futures[future]
                print(f"[{i}/{len(source_classes)}] {cls.__name__} generated an exception: {exc}")
                
    total_duration = time.time() - start_time
    print("\n==================================================")
    print(" INGESTION COMPLETE")
    print("==================================================")
    print(f"Total Sources Run: {len(source_classes)}")
    print(f"Total Tenders Fetched: {total_fetched}")
    print(f"Total Tenders Saved: {total_saved}")
    print(f"Total Time: {total_duration:.1f} seconds")
    print("==================================================")

if __name__ == "__main__":
    main()
