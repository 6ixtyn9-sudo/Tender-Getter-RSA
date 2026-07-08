"""Tender-Getter RSA – Unified Source Aggregator

Discovers all TenderSource plug-ins via pkgutil walk of `sources/*/*.py`.
Each entity has its own per-source file (sources/<dir>/<entity_id>.py).
sources.yaml is the metadata index for documentation/health-check only;
the registry is determined entirely by what Python files exist.
"""
from __future__ import annotations
import logging
import inspect
import pkgutil
import importlib
import time
from typing import List, Dict, Optional
from datetime import datetime, timezone
from contextlib import nullcontext

from .schemas import TenderOpportunity
from .database import TenderDatabase
try:
    from .database import get_database_client as get_database
except ImportError:
    def get_database():
        return TenderDatabase()
from .sources import TenderSource, load_sources

logger = logging.getLogger(__name__)


def discover_source_classes() -> Dict[str, type]:
    """Walk all modules under tender_getter.sources.* and collect every class
    that has a string `source_id` attribute and a callable `fetch()` method.
    """
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
                logger.debug("Skipping module %s: %s", mod_name, exc)
                continue
            for _, obj in inspect.getmembers(mod, inspect.isclass):
                if obj.__name__ == "TenderSource":
                    continue
                if hasattr(obj, "source_id") and callable(getattr(obj, "fetch", None)):
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
    return found


def _load_yaml_live_flags() -> Dict[str, bool]:
    """Read sources.yaml and return source_id -> live bool."""
    try:
        entries = load_sources()
    except Exception as exc:
        logger.debug("Could not load sources.yaml: %s", exc)
        return {}
    return {e["id"]: bool(e.get("live", True)) for e in entries if "id" in e}


def build_registry() -> List[TenderSource]:
    """Instantiate every discovered source class.

    Honours the `live` flag from sources.yaml. Per-source files declare
    their own class-level `live: bool` attribute, but YAML takes priority
    so that operators can flip liveness without touching Python code.
    """
    classes = discover_source_classes()
    yaml_live = _load_yaml_live_flags()
    instances = []
    for sid, cls in classes.items():
        try:
            inst = cls()
            # YAML `live` overrides the class-level default.
            if sid in yaml_live:
                inst.live = yaml_live[sid]
            instances.append(inst)
        except Exception as exc:
            logger.warning("Could not instantiate %s: %s", cls, exc)
    return instances


def get_all_source_instances(live_only: bool = False) -> List[TenderSource]:
    """Return all source instances, optionally filtered to live=true only."""
    all_inst = build_registry()
    if not live_only:
        return all_inst
    return [inst for inst in all_inst if getattr(inst, "live", True)]


def sync_all_sources(
    limit_per_source: int | None = None,
    db=None,
    stop_on_error: bool = False,
    verbose: bool = True,
    max_workers: int = 20,
    use_threads: bool = True,
    live_only: bool = False,
) -> Dict:
    """Fetch all sources, deduplicate, upsert to DB."""
    start = datetime.now(timezone.utc)
    if db is None:
        db = get_database()

    sources = get_all_source_instances(live_only=live_only)
    yaml_count = len(load_sources())
    class_count = len(discover_source_classes())
    per_source = []
    all_tenders: List[TenderOpportunity] = []
    failed = 0
    ok = 0

    def _fetch_one(inst):
        sid = getattr(inst, "source_id", inst.__class__.__name__)
        t0 = time.time()
        try:
            tenders = inst.fetch(limit=limit_per_source)
            elapsed = time.time() - t0
            count = len(tenders) if tenders else 0
            return {"source_id": sid, "status": "ok", "count": count,
                    "elapsed_s": round(elapsed, 3), "tenders": tenders or [], "error": None}
        except Exception as exc:
            elapsed = time.time() - t0
            logger.error("[%s] FAILED after %.2fs: %s", sid, elapsed, exc, exc_info=True)
            return {"source_id": sid, "status": "error", "count": 0,
                    "elapsed_s": round(elapsed, 3), "tenders": [], "error": str(exc)}

    if use_threads and len(sources) > 1:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        workers = min(max_workers, len(sources))
        with ThreadPoolExecutor(max_workers=workers) as ex:
            future_to_sid = {
                ex.submit(_fetch_one, inst): getattr(inst, "source_id", inst.__class__.__name__)
                for inst in sources
            }
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
        for inst in sources:
            res = _fetch_one(inst)
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

    unique: Dict[str, TenderOpportunity] = {}
    for t in all_tenders:
        unique[t.tender_id] = t
    unique_tenders = list(unique.values())

    upserted = 0
    if unique_tenders:
        try:
            ctx = db if hasattr(db, "__enter__") else nullcontext(db)
            with ctx:
                if hasattr(db, "upsert_tender"):
                    for t in unique_tenders:
                        try:
                            db.upsert_tender(t)
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
        "yaml_total": yaml_count,
        "class_total": class_count,
        "sources_total": len(sources),
        "sources_skipped_live_false": class_count - len(sources),
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
