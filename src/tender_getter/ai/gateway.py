"""
Tender Getter AI Gateway — 7-key Gemini gateway with rate limiting and key rotation.
No fallbacks, no OpenRouter, single user type (SMME owner).

SDK: google-genai (the successor to the end-of-life google-generativeai package).
"""

import asyncio
import logging
import os
from dataclasses import dataclass, field
from typing import Any, Optional

from google import genai
from google.genai import errors as genai_errors
from google.genai import types as genai_types

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class GatewayConfig:
    primary_model: str = field(
        default_factory=lambda: os.getenv("GEMINI_MODEL_PRIMARY", "gemini-2.5-flash")
    )
    fallback_model: str = field(
        default_factory=lambda: os.getenv("GEMINI_MODEL_FALLBACK", "gemini-2.5-flash-lite")
    )
    max_retries: int = 2
    base_delay_ms: int = 800
    max_concurrent: int = 3
    rate_limit_reset_hours: int = 1


# ---------------------------------------------------------------------------
# Key Management
# ---------------------------------------------------------------------------

class KeyManager:
    """Manages 7 Gemini API keys with rotation and exhaustion tracking."""

    def __init__(self, config: GatewayConfig):
        self.config = config
        self.keys: list[str] = []
        self.exhausted_keys: set[str] = set()
        self._load_keys()

    def _load_keys(self) -> None:
        """Load keys from env: GEMINI_API_KEY=key1,key2,... or GEMINI_API_KEY_1..7"""
        # Legacy single key (comma-separated)
        legacy = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if legacy:
            for k in legacy.split(","):
                k = k.strip()
                if k and k not in self.keys:
                    self.keys.append(k)

        # Numbered keys
        for i in range(1, 8):
            k = os.getenv(f"GEMINI_API_KEY_{i}")
            if k and k not in self.keys:
                self.keys.append(k)

        logger.info(f"[TG-AI] Loaded {len(self.keys)} Gemini key(s)")

    def get_available_key(self, exclude: Optional[set[str]] = None) -> Optional[str]:
        """Get next available key not in exclude set."""
        exclude = exclude or set()
        for key in self.keys:
            if key not in self.exhausted_keys and key not in exclude:
                return key
        return None

    def mark_exhausted(self, key: str) -> None:
        """Mark a key as exhausted (429)."""
        self.exhausted_keys.add(key)
        logger.warning(f"[TG-AI] Key exhausted (429): {key[:4]}…")

    def reset_exhausted(self) -> None:
        """Reset exhausted keys (call periodically)."""
        self.exhausted_keys.clear()
        logger.info("[TG-AI] Rate limit reset — all keys available")


# ---------------------------------------------------------------------------
# Concurrency Control
# ---------------------------------------------------------------------------

class ConcurrencyLimiter:
    """Semaphore-based concurrency limiter."""

    def __init__(self, max_concurrent: int):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def acquire(self) -> None:
        await self.semaphore.acquire()

    def release(self) -> None:
        self.semaphore.release()


# ---------------------------------------------------------------------------
# Core Gateway
# ---------------------------------------------------------------------------

STATIC_FALLBACK = (
    "Tender Getter AI is experiencing high demand. Please try again in a moment."
)


class AIGateway:
    """
    7-key Gemini gateway with automatic key rotation on 429.
    No OpenRouter, no model fallback, single SMME owner persona.

    Uses one cached ``genai.Client`` per API key (the google-genai SDK is
    client-per-key rather than the old global ``genai.configure()``).
    """

    def __init__(self, config: Optional[GatewayConfig] = None):
        self.config = config or GatewayConfig()
        self.key_manager = KeyManager(self.config)
        self.limiter = ConcurrencyLimiter(self.config.max_concurrent)
        self._clients: dict[str, genai.Client] = {}
        self._reset_task_started = False

    def _client_for(self, key: str) -> genai.Client:
        """Return the cached google-genai client for a key, creating it on first use."""
        client = self._clients.get(key)
        if client is None:
            client = genai.Client(api_key=key)
            self._clients[key] = client
        return client

    def _ensure_reset_task(self) -> None:
        """Start periodic key reset task on first use."""
        if self._reset_task_started:
            return
        try:
            async def reset_loop():
                while True:
                    await asyncio.sleep(self.config.rate_limit_reset_hours * 3600)
                    self.key_manager.reset_exhausted()
            asyncio.create_task(reset_loop())
            self._reset_task_started = True
        except RuntimeError:
            pass  # No event loop yet

    async def generate(
        self,
        system_prompt: str,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
    ) -> dict[str, Any]:
        """
        Generate AI response with key rotation on 429.
        Returns {"reply": str} or {"error": str}.
        """
        self._ensure_reset_task()
        await self.limiter.acquire()
        try:
            return await self._call_gemini_with_rotation(
                model=self.config.primary_model,
                system_prompt=system_prompt,
                messages=messages,
                temperature=temperature,
            )
        finally:
            self.limiter.release()

    async def _call_gemini_with_rotation(
        self,
        model: str,
        system_prompt: str,
        messages: list[dict[str, str]],
        temperature: float,
    ) -> dict[str, Any]:
        """
        Call Gemini with automatic key rotation on 429 and bounded retries
        on 503.

        The attempt budget is ``len(keys) + config.max_retries`` so a
        persistent upstream outage fails fast with an error dict — it can
        never recurse into a stack overflow (previous unbounded-recursion DoS).
        """
        used_keys: set[str] = set()
        max_attempts = max(1, len(self.key_manager.keys) + self.config.max_retries)

        for _ in range(1, max_attempts + 1):
            key = self.key_manager.get_available_key(exclude=used_keys)
            if not key:
                return {"error": "All 7 Gemini keys exhausted"}

            try:
                client = self._client_for(key)
                gemini_contents = self._convert_messages(messages)

                response = await client.aio.models.generate_content(
                    model=model,
                    contents=gemini_contents,
                    config=genai_types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=temperature,
                        max_output_tokens=2048,
                    ),
                )

                text = response.text or ""
                if not text.strip():
                    return {"error": "Empty response from Gemini"}

                return {"reply": text.strip()}

            except genai_errors.APIError as e:
                error_msg = e.message or str(e)
                outcome = self._classify_error(key, error_msg, e.code)
                if outcome == "rotate":
                    self.key_manager.mark_exhausted(key)
                    used_keys.add(key)
                    continue
                if outcome == "retry":
                    await asyncio.sleep(self.config.base_delay_ms / 1000)
                    continue
                return {"error": error_msg}

            except Exception as e:
                error_msg = str(e)
                outcome = self._classify_error(key, error_msg, None)
                if outcome == "rotate":
                    self.key_manager.mark_exhausted(key)
                    used_keys.add(key)
                    continue
                if outcome == "retry":
                    await asyncio.sleep(self.config.base_delay_ms / 1000)
                    continue
                return {"error": error_msg}

        logger.warning(
            f"[TG-AI] Gemini retry budget exhausted after {max_attempts} attempt(s)"
        )
        return {"error": "Gemini unavailable after bounded retries"}

    def _classify_error(self, key: str, error_msg: str, code: Optional[int]) -> str:
        """Classify an upstream error: 'rotate' (429/quota), 'retry' (503/overload) or 'fatal'."""
        logger.warning(f"[TG-AI] Gemini error with key {key[:4]}…: {error_msg}")
        if code == 429 or (code is None and ("429" in error_msg or "quota" in error_msg.lower())):
            return "rotate"
        if code == 503 or (code is None and ("503" in error_msg or "overload" in error_msg.lower())):
            return "retry"
        return "fatal"

    def _convert_messages(self, messages: list[dict[str, str]]) -> list[genai_types.Content]:
        """Convert standard messages to google-genai ``Content`` objects."""
        converted = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            gemini_role = "model" if role == "assistant" else "user"
            converted.append(
                genai_types.Content(
                    role=gemini_role,
                    parts=[genai_types.Part.from_text(text=content)],
                )
            )
        return converted

    async def health_check(self) -> dict[str, Any]:
        return {
            "status": "ok",
            "model": self.config.primary_model,
            "keys_loaded": len(self.key_manager.keys),
            "keys_available": len(self.key_manager.keys) - len(self.key_manager.exhausted_keys),
        }


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------

_gateway: Optional[AIGateway] = None


def get_gateway(config: Optional[GatewayConfig] = None) -> AIGateway:
    global _gateway
    if _gateway is None:
        _gateway = AIGateway(config)
    return _gateway
