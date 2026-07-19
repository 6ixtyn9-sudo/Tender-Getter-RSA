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
    if kind == "build_bid_pack":
        from tender_getter.database import get_database_client
        from tender_getter.whatsapp.database import get_user
        from tender_getter.whatsapp.matching import company_from_user
        from tender_getter.agents.bid_craft import draft_bid_pack
        from tender_getter.ai.gateway import get_gateway
        from tender_getter.whatsapp.outbound import send_text_message
        user = get_user(payload["owner_phone"])
        company = company_from_user(user) if user else None
        db = get_database_client().connect()
        try:
            tender = next((t for t in db.list_open_tenders(limit=10000) if t.tender_id == payload["tender_id"]), None)
        finally: db.close()
        if not company or not tender: raise ValueError("Bid pack references missing company or open tender")
        requirements = f"Tender title: {tender.title}\nIssuer: {tender.issuing_entity}\nDocument URL: {tender.raw_document_url or 'not available'}"
        result = await draft_bid_pack(get_gateway(), company, tender, requirements)
        if "error" in result: raise RuntimeError("Bid-Craft generation unavailable")
        draft = result["reply"]
        from tender_getter.pdf_reports import render_text_pdf
        from tender_getter.whatsapp.media import upload_to_supabase, get_media_url
        from tender_getter.whatsapp.outbound import send_media_message
        pdf = render_text_pdf(f"Tender Getter Bid-Craft — {tender.tender_id}", draft, tender.tender_id)
        storage_path = await upload_to_supabase(pdf.read_bytes(), "application/pdf", user.phone_number)
        media_url = await get_media_url(storage_path)
        store_client = AgentStore()._client
        if store_client:
            store_client.table("bid_packs").upsert({"registration_number": company.registration_number, "tender_id": tender.tender_id, "status": "ready", "draft_content": draft, "storage_path": storage_path}, on_conflict="registration_number,tender_id").execute()
        send_media_message(user.phone_number, media_url, f"✅ Bid-Craft draft for {tender.tender_id}. Review every CUSTOMER ACTION REQUIRED item before submitting.")
        return
    # Enrichment and matching require explicit payload references.
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
