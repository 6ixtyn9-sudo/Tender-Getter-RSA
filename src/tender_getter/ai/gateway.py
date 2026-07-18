"""
Tender Getter AI Gateway — 7-key Gemini gateway with rate limiting and key rotation.
No fallbacks, no OpenRouter, single user type (SMME owner).
"""

import asyncio
import logging
import os
from dataclasses import dataclass
from typing import Any, Optional

import google.generativeai as genai

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class GatewayConfig:
    primary_model: str = "gemini-1.5-flash"
    fallback_model: str = "gemini-1.5-flash-8b"
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
        logger.warning(f"[TG-AI] Key exhausted (429): {key[:8]}...")

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
    """

    def __init__(self, config: Optional[GatewayConfig] = None):
        self.config = config or GatewayConfig()
        self.key_manager = KeyManager(self.config)
        self.limiter = ConcurrencyLimiter(self.config.max_concurrent)
        self._reset_task_started = False

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
        used_keys: Optional[set[str]] = None,
    ) -> dict[str, Any]:
        """Call Gemini with automatic key rotation on 429."""
        used_keys = used_keys or set()

        key = self.key_manager.get_available_key(exclude=used_keys)
        if not key:
            return {"error": "All 7 Gemini keys exhausted"}

        try:
            genai.configure(api_key=key)
            gemini_model = genai.GenerativeModel(model)

            gemini_messages = self._convert_messages(messages)

            response = await gemini_model.generate_content_async(
                contents=gemini_messages,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=2048,
                ),
                system_instruction=system_prompt,
            )

            text = response.text or ""
            if not text.strip():
                return {"error": "Empty response from Gemini"}

            return {"reply": text.strip()}

        except Exception as e:
            error_msg = str(e)
            logger.warning(f"[TG-AI] Gemini error with key {key[:8]}...: {error_msg}")

            if "429" in error_msg or "quota" in error_msg.lower():
                self.key_manager.mark_exhausted(key)
                used_keys.add(key)
                return await self._call_gemini_with_rotation(
                    model, system_prompt, messages, temperature, used_keys
                )

            if "503" in error_msg or "overload" in error_msg.lower():
                await asyncio.sleep(self.config.base_delay_ms / 1000)
                return await self._call_gemini_with_rotation(
                    model, system_prompt, messages, temperature, used_keys
                )

            return {"error": error_msg}

    def _convert_messages(self, messages: list[dict[str, str]]) -> list[dict]:
        """Convert standard messages to Gemini format."""
        converted = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role == "assistant":
                converted.append({"role": "model", "parts": [content]})
            else:
                converted.append({"role": "user", "parts": [content]})
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