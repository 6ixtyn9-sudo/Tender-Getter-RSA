#!/usr/bin/env python3
"""
Test the WhatsApp webhook locally with ngrok.
Run this after starting the server: PYTHONPATH=src python -m tender_getter.whatsapp.webhook
"""

import asyncio
import httpx

BASE_URL = "http://localhost:8080"

TEST_CASES = [
    ("hi", "greeting"),
    ("show tenders", "show_tenders"),
    ("any tenders in Gauteng?", "show_tenders"),
    ("verify csd", "verify_document"),
    ("upload my B-BBEE cert", "upload_document"),
    ("why was I disqualified?", "explain_gate"),
    ("explain CIDB grading", "explain_cidb"),
    ("daily digest off", "toggle_digest"),
    ("help", "help"),
    ("stop", "stop"),
]

async def test_webhook():
    async with httpx.AsyncClient(timeout=30.0) as client:
        for text, expected_intent in TEST_CASES:
            print(f"\n🧪 Testing: '{text}'")
            try:
                resp = await client.post(
                    f"{BASE_URL}/whatsapp/webhook",
                    data={
                        "From": "whatsapp:+27733587019",
                        "Body": text,
                        "MessageSid": f"test_{hash(text)}",
                        "NumMedia": "0",
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                print(f"   Status: {resp.status_code}")
                # Extract message from TwiML
                if "<Message>" in resp.text:
                    start = resp.text.index("<Message>") + 9
                    end = resp.text.index("</Message>")
                    msg = resp.text[start:end]
                    print(f"   Response: {msg[:100]}...")
            except Exception as e:
                print(f"   ❌ Error: {e}")

async def test_health():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/health")
        print(f"\n🏥 Health check: {resp.status_code} - {resp.json()}")

if __name__ == "__main__":
    print("🧪 Testing Tender Getter WhatsApp Webhook\n")
    asyncio.run(test_health())
    asyncio.run(test_webhook())
    print("\n✅ All tests complete!")