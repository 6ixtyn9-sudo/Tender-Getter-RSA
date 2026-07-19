"""Tests for the google-generativeai → google-genai SDK migration.

Covers the production-blocker migration before Cloud Run deployment:

1. No source file may import the deprecated google-generativeai package.
2. requirements.txt pins google-genai instead of google-generativeai.
3. The AI gateway preserves 7-key rotation with per-key genai.Client instances.
4. parser.py keeps the compliance-sieve extraction contract via the new SDK.
5. WhatsApp media parsing keeps Gemini Vision + native inline-PDF extraction.

All Gemini calls are mocked — these tests never touch the network.
"""

import asyncio
import io
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from PIL import Image

# ---------------------------------------------------------------------------
# Constants & fake google-genai client
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"

SEVEN_KEYS = ",".join(f"test-key-{i}" for i in range(1, 8))


def _api_error_429():
    from google.genai import errors

    return errors.APIError(
        code=429,
        response_json={"error": {"message": "quota exceeded", "status": "RESOURCE_EXHAUSTED"}},
    )


def _api_error_503():
    from google.genai import errors

    return errors.APIError(
        code=503,
        response_json={"error": {"message": "model overloaded", "status": "UNAVAILABLE"}},
    )


def _install_fake_client(monkeypatch, handler, calls):
    """Patch google.genai.Client with a fake driven by ``handler``.

    handler(api_key, model, contents, config) must return a response object
    (SimpleNamespace(text=...)) or raise. Every invocation is appended to
    ``calls`` as a dict.
    """

    def _record_and_handle(api_key, model, contents, config):
        calls.append(
            {"api_key": api_key, "model": model, "contents": contents, "config": config}
        )
        return handler(api_key, model, contents, config)

    class _FakeSyncModels:
        def __init__(self, api_key):
            self._api_key = api_key

        def generate_content(self, *, model, contents, config=None):
            return _record_and_handle(self._api_key, model, contents, config)

    class _FakeAsyncModels(_FakeSyncModels):
        async def generate_content(self, *, model, contents, config=None):
            return _record_and_handle(self._api_key, model, contents, config)

    class _FakeClient:
        def __init__(self, api_key=None, **kwargs):
            self.api_key = api_key
            self.models = _FakeSyncModels(api_key)
            self.aio = SimpleNamespace(models=_FakeAsyncModels(api_key))

    monkeypatch.setattr("google.genai.Client", _FakeClient)
    return _FakeClient


def _quiet_reset_task(monkeypatch):
    """Avoid spawning the hourly reset loop inside asyncio.run test loops."""
    from tender_getter.ai.gateway import AIGateway

    monkeypatch.setattr(
        AIGateway,
        "_ensure_reset_task",
        lambda self: setattr(self, "_reset_task_started", True),
    )


# ---------------------------------------------------------------------------
# 1 & 2 — package-level migration guarantees
# ---------------------------------------------------------------------------

def test_source_has_no_deprecated_sdk_imports():
    offenders = []
    for path in SRC_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "google.generativeai" in text:
            offenders.append(str(path.relative_to(REPO_ROOT)))
    assert offenders == [], f"Deprecated google-generativeai references remain: {offenders}"


def test_requirements_pins_google_genai():
    requirements = (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8")
    assert "google-genai" in requirements
    for line in requirements.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            assert not stripped.startswith("google-generativeai"), (
                f"Deprecated dependency still pinned: {stripped}"
            )


def test_new_sdk_surface_is_available():
    from google import genai
    from google.genai import types, errors

    assert hasattr(genai, "Client")
    assert hasattr(types, "GenerateContentConfig")
    assert hasattr(types.Part, "from_bytes")
    assert hasattr(errors, "APIError")


# ---------------------------------------------------------------------------
# 3 — gateway: 7-key rotation preserved on the new SDK
# ---------------------------------------------------------------------------

def test_gateway_rotates_to_next_key_on_429(monkeypatch):
    from tender_getter.ai.gateway import AIGateway, GatewayConfig

    monkeypatch.setenv("GEMINI_API_KEY", SEVEN_KEYS)
    _quiet_reset_task(monkeypatch)

    calls = []

    def handler(api_key, model, contents, config):
        if api_key == "test-key-1":
            raise _api_error_429()
        return SimpleNamespace(text="  rotated reply  ")

    _install_fake_client(monkeypatch, handler, calls)

    gateway = AIGateway(GatewayConfig())
    result = asyncio.run(
        gateway.generate("system", [{"role": "user", "content": "hello"}])
    )

    assert result == {"reply": "rotated reply"}
    # First key attempted, second key served the request.
    assert [c["api_key"] for c in calls] == ["test-key-1", "test-key-2"]
    assert "test-key-1" in gateway.key_manager.exhausted_keys


def test_gateway_loads_all_seven_keys_and_reports_health(monkeypatch):
    from tender_getter.ai.gateway import AIGateway, GatewayConfig

    monkeypatch.setenv("GEMINI_API_KEY", SEVEN_KEYS)
    gateway = AIGateway(GatewayConfig())

    assert len(gateway.key_manager.keys) == 7

    health = asyncio.run(gateway.health_check())
    assert health["keys_loaded"] == 7
    assert health["keys_available"] == 7


def test_gateway_creates_one_client_per_key_and_caches(monkeypatch):
    from tender_getter.ai.gateway import AIGateway, GatewayConfig

    monkeypatch.setenv("GEMINI_API_KEY", "k1,k2")
    _quiet_reset_task(monkeypatch)

    created = []

    calls = {"n": 0}

    class _Client:
        def __init__(self, api_key=None, **kwargs):
            created.append(api_key)
            self.api_key = api_key

            async def gen(*, model, contents, config=None):
                calls["n"] += 1
                if calls["n"] == 1:
                    raise _api_error_429()
                return SimpleNamespace(text="ok")

            self.aio = SimpleNamespace(models=SimpleNamespace(generate_content=gen))

    monkeypatch.setattr("google.genai.Client", _Client)

    gateway = AIGateway(GatewayConfig())
    result = asyncio.run(gateway.generate("s", [{"role": "user", "content": "hi"}]))

    assert result == {"reply": "ok"}
    assert created == ["k1", "k2"]  # one client per key, on demand
    assert set(gateway._clients) == {"k1", "k2"}  # cached for reuse


def test_gateway_retries_same_key_on_503_with_backoff(monkeypatch):
    from tender_getter.ai.gateway import AIGateway, GatewayConfig

    monkeypatch.setenv("GEMINI_API_KEY", "only-key")
    _quiet_reset_task(monkeypatch)

    calls = []
    state = {"n": 0}

    def handler(api_key, model, contents, config):
        state["n"] += 1
        if state["n"] == 1:
            raise _api_error_503()
        return SimpleNamespace(text="recovered")

    _install_fake_client(monkeypatch, handler, calls)

    gateway = AIGateway(GatewayConfig(base_delay_ms=1))
    result = asyncio.run(gateway.generate("s", [{"role": "user", "content": "hi"}]))

    assert result == {"reply": "recovered"}
    assert [c["api_key"] for c in calls] == ["only-key", "only-key"]
    assert gateway.key_manager.exhausted_keys == set()


def test_gateway_returns_error_when_all_seven_keys_exhausted(monkeypatch):
    from tender_getter.ai.gateway import AIGateway, GatewayConfig

    monkeypatch.setenv("GEMINI_API_KEY", SEVEN_KEYS)
    _quiet_reset_task(monkeypatch)

    calls = []

    def handler(api_key, model, contents, config):
        raise _api_error_429()

    _install_fake_client(monkeypatch, handler, calls)

    gateway = AIGateway(GatewayConfig())
    result = asyncio.run(gateway.generate("s", [{"role": "user", "content": "hi"}]))

    assert "error" in result
    assert result["error"] == "All 7 Gemini keys exhausted"
    assert len({c["api_key"] for c in calls}) == 7


def test_gateway_message_roles_map_assistant_to_model(monkeypatch):
    from tender_getter.ai.gateway import AIGateway, GatewayConfig

    monkeypatch.setenv("GEMINI_API_KEY", "k1")
    gateway = AIGateway(GatewayConfig())

    converted = gateway._convert_messages(
        [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello there"},
            {"role": "user", "content": "again"},
        ]
    )

    assert [c.role for c in converted] == ["user", "model", "user"]
    assert converted[1].parts[0].text == "hello there"


# ---------------------------------------------------------------------------
# 4 — parser.py: compliance sieve contract on the new SDK
# ---------------------------------------------------------------------------

def test_parser_extracts_structured_json_via_new_sdk(monkeypatch):
    import tender_getter.parser as parser

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(
        parser, "extract_relevant_pages", lambda _path: "SBD 1 ... CIDB CE4 ..."
    )

    calls = []
    payload = {
        "bid_number": "TEST/2026/001",
        "closing_date": "2026-08-01",
        "required_cidb_class": "CE",
        "required_cidb_level": 4,
        "mandatory_csd": True,
        "bbbee_points_system": "80/20",
    }

    def handler(api_key, model, contents, config):
        return SimpleNamespace(text=f"```json\n{json.dumps(payload)}\n```")

    _install_fake_client(monkeypatch, handler, calls)

    result = parser.parse_tender_pdf("ignored.pdf")

    assert result["bid_number"] == "TEST/2026/001"
    assert result["required_cidb_class"] == "CE"
    assert result["required_cidb_level"] == 4
    assert result["mandatory_csd"] is True
    # All schema keys present even when the model omits some.
    assert "location_target" in result

    # New-SDK call shape: model + contents + config.system_instruction
    assert calls[0]["model"] == parser.GEMINI_MODEL
    assert "CIDB CE4" in calls[0]["contents"]
    assert calls[0]["config"].system_instruction == parser.EXTRACTION_SYSTEM_PROMPT


def test_parser_raises_clear_error_without_api_key(monkeypatch):
    import tender_getter.parser as parser

    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr(parser, "_try_load_dotenv", lambda: None)

    with pytest.raises(RuntimeError, match="GEMINI_API_KEY is not set"):
        parser.parse_tender_pdf("ignored.pdf")


# ---------------------------------------------------------------------------
# 5 — whatsapp/media.py: Vision + native inline-PDF extraction preserved
# ---------------------------------------------------------------------------

def _png_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (2, 2), color=(255, 255, 255)).save(buf, format="PNG")
    return buf.getvalue()


def test_media_image_parsing_uses_vision_contents(monkeypatch):
    import tender_getter.whatsapp.media as media

    monkeypatch.setattr(media, "GEMINI_API_KEY", "test-key")

    calls = []

    def handler(api_key, model, contents, config):
        return SimpleNamespace(text='{"csd_number": "MAAA0001234"}')

    _install_fake_client(monkeypatch, handler, calls)

    result = asyncio.run(
        media.parse_document_with_gemini(_png_bytes(), "image/png")
    )

    assert result == {"csd_number": "MAAA0001234"}

    contents = calls[0]["contents"]
    assert isinstance(contents[0], str)  # prompt first
    assert any(isinstance(item, Image.Image) for item in contents)
    assert calls[0]["model"] == media.GEMINI_MODEL


def test_media_pdf_parsing_sends_inline_pdf_part(monkeypatch):
    import tender_getter.whatsapp.media as media

    monkeypatch.setattr(media, "GEMINI_API_KEY", "test-key")

    calls = []

    def handler(api_key, model, contents, config):
        return SimpleNamespace(text='{"bid_number": "BID/1"}')

    _install_fake_client(monkeypatch, handler, calls)

    pdf_bytes = b"%PDF-1.4 fake"
    result = asyncio.run(
        media.parse_document_with_gemini(pdf_bytes, "application/pdf")
    )

    assert result == {"bid_number": "BID/1"}

    pdf_parts = [
        item
        for item in calls[0]["contents"]
        if getattr(item, "inline_data", None) is not None
    ]
    assert len(pdf_parts) == 1
    assert pdf_parts[0].inline_data.mime_type == "application/pdf"
    assert pdf_parts[0].inline_data.data == pdf_bytes


def test_media_parsing_skips_gracefully_without_key(monkeypatch):
    import tender_getter.whatsapp.media as media

    monkeypatch.setattr(media, "GEMINI_API_KEY", None)

    result = asyncio.run(media.parse_document_with_gemini(b"data", "image/png"))
    assert result is None
