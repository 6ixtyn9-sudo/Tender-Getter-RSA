#!/usr/bin/env python3
"""Run one durable Tender Getter agent job. Invoke from Cloud Run Jobs/Scheduler."""
from __future__ import annotations
import asyncio, logging, os, socket
from tender_getter.agents.store import AgentStore

async def dispatch(job: dict) -> None:
    kind, payload = job["job_type"], job.get("payload") or {}
    if kind == "deliver_digest":
        from tender_getter.whatsapp.digest import run_daily_digest_job
        await run_daily_digest_job(); return
    if kind == "ingest":
        from tender_getter.database import get_database_client
        from tender_getter.pipeline import ingest_real_tenders
        db = get_database_client().connect()
        try: ingest_real_tenders(db)
        finally: db.close()
        return
    if kind == "process_document":
        from tender_getter.whatsapp.database import get_media_message, get_user
        from tender_getter.whatsapp.webhook import process_media_async
        user = get_user(payload["owner_phone"])
        media = get_media_message(payload["owner_phone"], payload["message_sid"])
        if not user or not media: raise ValueError("Document job references missing user or media")
        await process_media_async(media, user)
        return
    # Enrichment, matching and Bid-Craft require the job payload's tender/user
    # references and are deliberately retried rather than fabricated.
    raise ValueError(f"No dispatcher configured for {kind!r} payload")

async def main() -> int:
    store = AgentStore(); job = store.claim_next(os.getenv("AGENT_WORKER_ID", socket.gethostname()))
    if not job:
        logging.info("No due agent jobs"); return 0
    try:
        await dispatch(job); store.finish(job["id"]); return 0
    except Exception as exc:
        logging.exception("Agent job failed: %s", job["id"]); store.finish(job["id"], error=str(exc)[:1000]); return 1

if __name__ == "__main__": raise SystemExit(asyncio.run(main()))
