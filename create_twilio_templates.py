#!/usr/bin/env python3
"""
Create Twilio Content Templates from JSON definitions.
Run after setting up Twilio credentials in environment.
"""

import os
import json
from pathlib import Path
from twilio.rest import Client

# Load credentials from environment
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

if not ACCOUNT_SID or not AUTH_TOKEN:
    print("❌ Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables")
    exit(1)

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Load template definitions
with open("twilio_templates.json") as f:
    data = json.load(f)

print(f"📋 Creating {len(data['templates'])} Twilio templates...\n")

for tmpl in data["templates"]:
    name = tmpl["friendly_name"]
    print(f"Creating: {name}...")
    
    try:
        # Check if template already exists
        existing = client.content.v1.contents.list(friendly_name=name, limit=1)
        if existing:
            print(f"  ⚠️  Template '{name}' already exists (SID: {existing[0].sid}), updating...")
            content = client.content.v1.contents(existing[0].sid).update(
                language=tmpl["language"],
                components=tmpl["components"]
            )
            print(f"  ✅ Updated: {content.sid}")
        else:
            content = client.content.v1.contents.create(
                friendly_name=name,
                language=tmpl["language"],
                components=tmpl["components"]
            )
            print(f"  ✅ Created: {content.sid}")
    except Exception as e:
        print(f"  ❌ Failed: {e}")

print("\n🎉 Done! View templates at:")
print("https://console.twilio.com/us1/develop/sms/content-template-builder")