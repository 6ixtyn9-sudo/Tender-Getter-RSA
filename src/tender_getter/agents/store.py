"""Durable agent job and audit storage with a development-memory fallback."""
from __future__ import annotations
import os, uuid
from datetime import datetime, timezone
from typing import Any

class AgentStore:
    def __init__(self):
        self._memory: dict[str, dict] = {}
        self._client = None
        try:
            from supabase import create_client
            if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"):
                self._client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
        except Exception:
            pass

    def enqueue(self, job_type: str, payload: dict[str, Any], idempotency_key: str) -> str:
        row = {"job_type": job_type, "payload": payload, "idempotency_key": idempotency_key, "status": "queued"}
        if self._client:
            result = self._client.table("agent_jobs").upsert(row, on_conflict="idempotency_key").execute()
            return result.data[0]["id"]
        row["id"] = str(uuid.uuid4()); row["created_at"] = datetime.now(timezone.utc).isoformat(); self._memory[idempotency_key] = row
        return row["id"]

    def record_action(self, agent_name: str, decision: str, confidence: float, rationale: dict[str, Any], registration_number: str | None = None, tender_id: str | None = None) -> None:
        row = {"agent_name": agent_name, "decision": decision, "confidence": confidence, "rationale": rationale, "registration_number": registration_number, "tender_id": tender_id}
        if self._client: self._client.table("agent_actions").insert(row).execute()

    def record_feedback(self, owner_phone_number: str, raw_text: str, *, tender_id: str | None = None, intent: str | None = None, sentiment: str = "neutral", confidence: float = 0.0, signals: dict[str, Any] | None = None) -> None:
        row = {"owner_phone_number": owner_phone_number, "raw_text": raw_text, "tender_id": tender_id, "intent": intent, "sentiment": sentiment, "confidence": confidence, "extracted_signals": signals or {}}
        if self._client: self._client.table("natural_language_feedback").insert(row).execute()

    def claim_next(self, worker_name: str) -> dict | None:
        """Atomically claim one due task using the migration's SKIP LOCKED RPC."""
        if not self._client:
            for row in self._memory.values():
                if row.get("status") == "queued": row["status"] = "running"; return row
            return None
        result = self._client.rpc("claim_agent_job", {"worker_name": worker_name}).execute()
        return result.data[0] if result.data else None

    def finish(self, job_id: str, *, error: str | None = None) -> None:
        if not self._client: return
        if error:
            self._client.table("agent_jobs").update({"status": "retry", "last_error": error}).eq("id", job_id).execute()
        else:
            self._client.table("agent_jobs").update({"status": "succeeded", "last_error": None}).eq("id", job_id).execute()
