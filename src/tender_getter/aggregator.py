"""Tender-Getter RSA – Unified Source Aggregator

Discovers all TenderSource plug-ins in tender_getter.sources.*,
fetches tenders, deduplicates by tender_id, and bulk-upserts
into the configured database (SQLite / Postgres / Supabase).

Robust per-source: one source failing never kills the whole run.
"""
from __future__ import annotations
import logging
import inspect
import pkgutil
import importlib
import time
from typing import List, Dict, Tuple
from datetime import datetime, timezone
from contextlib import nullcontext

from .schemas import TenderOpportunity
from .database import TenderDatabase
try:
    from .database import get_database_client as get_database
except ImportError:
    # fallback – direct SQLite
    def get_database():
        return TenderDatabase()
from .sources import TenderSource

logger = logging.getLogger(__name__)

def discover_source_classes() -> List[type]:
    """Auto-discover all TenderSource implementations under tender_getter.sources."""
    import tender_getter.sources as sources_pkg
    found: Dict[str, type] = {}
    
    def walk(package):
        prefix = package.__name__ + "."
        try:
            path = package.__path__
        except AttributeError:
            return
        for finder, mod_name, is_pkg in pkgutil.iter_modules(path, prefix):
            try:
                mod = importlib.import_module(mod_name)
            except Exception as exc:
                logger.warning("Skipping module %s: %s", mod_name, exc)
                continue
            # inspect classes in module
            for _, obj in inspect.getmembers(mod, inspect.isclass):
                # must look like a TenderSource: has source_id and fetch
                if hasattr(obj, "source_id") and callable(getattr(obj, "fetch", None)):
                    # avoid the Protocol itself
                    if obj.__name__ == "TenderSource":
                        continue
                    # ensure it actually conforms
                    try:
                        sid = getattr(obj, "source_id", None)
                        if isinstance(sid, str) and sid:
                            found[sid] = obj
                    except Exception:
                        pass
            if is_pkg:
                try:
                    sub_pkg = importlib.import_module(mod_name)
                    walk(sub_pkg)
                except Exception:
                    pass
    walk(sources_pkg)
    # deterministic order
    return [found[k] for k in sorted(found)]

def get_all_source_instances() -> List[TenderSource]:
    """Instantiate all discovered sources (no-arg constructors)."""
    classes = discover_source_classes()
    instances = []
    for cls in classes:
        try:
            inst = cls()  # type: ignore
            instances.append(inst)
        except Exception as exc:
            logger.warning("Could not instantiate %s: %s", cls, exc)
    return instances


def sync_all_sources(
    limit_per_source: int | None = None,
    db=None,
    stop_on_error: bool = False,
    verbose: bool = True,
    max_workers: int = 20,
    use_threads: bool = True,
) -> Dict:
    """
    Fetch all sources, deduplicate, upsert to DB.
    
    Returns summary dict:
    {
      'started_at': ...,
      'ended_at': ...,
      'sources_total': int,
      'sources_ok': int,
      'sources_failed': int,
      'tenders_fetched': int,
      'tenders_unique': int,
      'tenders_upserted': int,
      'per_source': [...]
    }
    """
    start = datetime.now(timezone.utc)
    if db is None:
        db = get_database()
    
    sources = get_all_source_instances()
    per_source = []
    all_tenders: List[TenderOpportunity] = []
    failed = 0
    ok = 0

    def _fetch_one(src):
        sid = getattr(src, "source_id", src.__class__.__name__)
        t0 = time.time()
        try:
            tenders = src.fetch(limit=limit_per_source)  # type: ignore
            elapsed = time.time() - t0
            count = len(tenders) if tenders else 0
            return {
                "source_id": sid,
                "status": "ok",
                "count": count,
                "elapsed_s": round(elapsed, 3),
                "tenders": tenders or [],
                "error": None,
            }
        except Exception as exc:
            elapsed = time.time() - t0
            logger.error("[%s] FAILED after %.2fs: %s", sid, elapsed, exc, exc_info=True)
            return {
                "source_id": sid,
                "status": "error",
                "count": 0,
                "elapsed_s": round(elapsed, 3),
                "tenders": [],
                "error": str(exc),
            }

    if use_threads and len(sources) > 1:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        workers = min(max_workers, len(sources))
        with ThreadPoolExecutor(max_workers=workers) as ex:
            future_to_sid = {ex.submit(_fetch_one, src): getattr(src, "source_id", src.__class__.__name__) for src in sources}
            for fut in as_completed(future_to_sid):
                res = fut.result()
                per_source.append({k: v for k, v in res.items() if k != "tenders"})
                if res["status"] == "ok":
                    ok += 1
                    if res["tenders"]:
                        all_tenders.extend(res["tenders"])
                    if verbose:
                        logger.info("[%s] %d tenders (%.2fs)", res["source_id"], res["count"], res["elapsed_s"])
                else:
                    failed += 1
                    if stop_on_error:
                        raise RuntimeError(f"Source {res['source_id']} failed: {res['error']}")
    else:
        # sequential fallback
        for src in sources:
            res = _fetch_one(src)
            per_source.append({k: v for k, v in res.items() if k != "tenders"})
            if res["status"] == "ok":
                ok += 1
                if res["tenders"]:
                    all_tenders.extend(res["tenders"])
                if verbose:
                    logger.info("[%s] %d tenders (%.2fs)", res["source_id"], res["count"], res["elapsed_s"])
            else:
                failed += 1
                if stop_on_error:
                    raise RuntimeError(f"Source {res['source_id']} failed: {res['error']}")

    # Deduplicate by tender_id – last seen wins (allows newer sources to override)
    unique: Dict[str, TenderOpportunity] = {}
    for t in all_tenders:
        unique[t.tender_id] = t
    unique_tenders = list(unique.values())

    # Upsert
    upserted = 0
    if unique_tenders:
        try:
            # Ensure DB connection – TenderDatabase needs .connect(), others are stateless
            ctx = db if hasattr(db, "__enter__") else nullcontext(db)
            with ctx:
                if hasattr(db, "upsert_tender"):
                    for t in unique_tenders:
                        try:
                            db.upsert_tender(t)  # type: ignore
                            upserted += 1
                        except Exception as exc:
                            logger.warning("Upsert failed for %s: %s", t.tender_id, exc)
                else:
                    logger.warning("DB client has no upsert_tender – skipping persistence")
        except Exception as exc:
            logger.error("Bulk upsert failed: %s", exc, exc_info=True)

    end = datetime.now(timezone.utc)
    summary = {
        "started_at": start.isoformat(),
        "ended_at": end.isoformat(),
        "duration_s": round((end - start).total_seconds(), 2),
        "sources_total": len(sources),
        "sources_ok": ok,
        "sources_failed": failed,
        "tenders_fetched": len(all_tenders),
        "tenders_unique": len(unique_tenders),
        "tenders_upserted": upserted,
        "per_source": sorted(per_source, key=lambda x: x["source_id"]),
    }
    return summary


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    s = sync_all_sources(limit_per_source=20)
    print(f"\nSync complete: {s['tenders_unique']} unique tenders from {s['sources_ok']}/{s['sources_total']} sources in {s['duration_s']}s")
    for row in s["per_source"]:
        print(f"  {row['source_id']:<30} {row['status']:6} {row['count']:3} tenders  {row['elapsed_s']}s")
