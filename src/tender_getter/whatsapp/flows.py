"""
WhatsApp Flows JSON definitions for Tender Getter RSA.
WhatsApp Flows provide native, app-like forms within WhatsApp.
Requires Business Verification and Flow approval from Meta.
"""

from typing import Dict, Any, List


# ---------------------------------------------------------------------------
# Flow 1: Complete Onboarding Flow
# ---------------------------------------------------------------------------

ONBOARDING_FLOW_JSON = {
    "name": "tender_getter_onboarding",
    "version": "1.0",
    "title": "Tender Getter RSA - Company Setup",
    "description": "Set up your company profile to receive matched government tenders",
    "screens": [
        # Screen 1: Welcome & POPIA Consent
        {
            "id": "screen_welcome",
            "title": "Welcome to Tender Getter RSA",
            "layout": {
                "type": "vertical",
                "children": [
                    {
                        "type": "text",
                        "text": "👋 Welcome to Tender Getter RSA!",
                        "style": {"fontSize": "large", "fontWeight": "bold", "marginBottom": "16"}
                    },
                    {
                        "type": "text",
                        "text": "I find government tenders you can actually win — checking your CIDB, CSD, Tax PIN, and B-BBEE automatically.",
                        "style": {"marginBottom": "24"}
                    },
                    {
                        "type": "text",
                        "text": "To get started, I need your consent to process your company information under POPIA.",
                        "style": {"marginBottom": "16"}
                    },
                    {
                        "type": "checkbox",
                        "name": "popia_consent",
                        "label": "I consent to Tender Getter RSA processing my company data for tender matching and compliance reporting (POPIA compliant)",
                        "required": True,
                        "style": {"marginBottom": "16"}
                    },
                    {
                        "type": "checkbox",
                        "name": "marketing_opt_in",
                        "label": "Send me product updates and tips (optional)",
                        "required": False
                    }
                ]
            },
            "next": "screen_company_name"
        },
        
        # Screen 2: Company Name
        {
            "id": "screen_company_name",
            "title": "Company Details",
            "layout": {
                "type": "vertical",
                "children": [
                    {
                        "type": "text",
                        "text": "📝 What's your company name?",
                        "style": {"fontSize": "medium", "fontWeight": "bold", "marginBottom": "16"}
                    },
                    {
                        "type": "text_input",
                        "name": "company_name",
                        "label": "Company Name",
                        "placeholder": "e.g., Sipho Electrical and Civils (Pty) Ltd",
                        "required": True,
                        "maxLength": 200,
                        "style": {"marginBottom": "16"}
                    },
                    {
                        "type": "text_input",
                        "name": "registration_number",
                        "label": "CIPC Registration Number (optional)",
                        "placeholder": "e.g., 2019/123456/07",
                        "required": False,
                        "maxLength": 50
                    }
                ]
            },
            "next": "screen_cidb_lookup"
        },
        
        # Screen 3: CIDB Lookup Results
        {
            "id": "screen_cidb_lookup",
            "title": "CIDB Grading",
            "layout": {
                "type": "vertical",
                "children": [
                    {
                        "type": "text",
                        "text": "🔍 Looking up your CIDB grading...",
                        "style": {"fontSize": "medium", "fontWeight": "bold", "marginBottom": "16"}
                    },
                    {
                        "type": "text",
                        "text": "We found the following matches in the CIDB Register of Contractors:",
                        "style": {"marginBottom": "16"}
                    },
                    {
                        "type": "radio_group",
                        "name": "cidb_selection",
                        "label": "Select your company (or choose 'Manual Entry')",
                        "options": [
                            # Populated dynamically via Flow data exchange
                        ],
                        "required": True,
                        "style": {"marginBottom": "16"}
                    },
                    {
                        "type": "text",
                        "text": "Or enter manually:",
                        "style": {"marginTop": "16", "marginBottom": "8", "fontWeight": "bold"}
                    },
                    {
                        "type": "text_input",
                        "name": "manual_cidb_class",
                        "label": "CIDB Class",
                        "placeholder": "e.g., CE, GB, EE, ME",
                        "required": False,
                        "maxLength": 4
                    },
                    {
                        "type": "number_input",
                        "name": "manual_cidb_level",
                        "label": "CIDB Level",
                        "placeholder": "1-9",
                        "required": False,
                        "min": 1,
                        "max": 9
                    }
                ]
            },
            "next": "screen_documents"
        },
        
        # Screen 4: Document Upload
        {
            "id": "screen_documents",
            "title": "Upload Documents",
            "layout": {
                "type": "vertical",
                "children": [
                    {
                        "type": "text",
                        "text": "📄 Upload your compliance documents (PDF or photo)",
                        "style": {"fontSize": "medium", "fontWeight": "bold", "marginBottom": "16"}
                    },
                    {
                        "type": "text",
                        "text": "Tap each to upload. We'll extract details automatically with AI.",
                        "style": {"marginBottom": "24"}
                    },
                    {
                        "type": "file_upload",
                        "name": "csd_letter",
                        "label": "CSD Registration Letter",
                        "accept": ["application/pdf", "image/*"],
                        "required": False,
                        "style": {"marginBottom": "16"}
                    },
                    {
                        "type": "file_upload",
                        "name": "bbbee_cert",
                        "label": "B-BBEE Certificate / Sworn Affidavit",
                        "accept": ["application/pdf", "image/*"],
                        "required": False,
                        "style": {"marginBottom": "16"}
                    },
                    {
                        "type": "file_upload",
                        "name": "tax_pin",
                        "label": "SARS Tax Compliance PIN",
                        "accept": ["application/pdf", "image/*"],
                        "required": False,
                        "style": {"marginBottom": "16"}
                    },
                    {
                        "type": "file_upload",
                        "name": "cidb_cert",
                        "label": "CIDB Grading Certificate",
                        "accept": ["application/pdf", "image/*"],
                        "required": False,
                        "style": {"marginBottom": "16"}
                    }
                ]
            },
            "next": "screen_sectors"
        },
        
        # Screen 5: Sectors & Province
        {
            "id": "screen_sectors",
            "title": "Sectors & Location",
            "layout": {
                "type": "vertical",
                "children": [
                    {
                        "type": "text",
                        "text": "🏢 Select your business sectors",
                        "style": {"fontSize": "medium", "fontWeight": "bold", "marginBottom": "16"}
                    },
                    {
                        "type": "multi_select",
                        "name": "sectors",
                        "label": "Sectors (auto-filled from CIDB)",
                        "options": [
                            {"value": "General Building", "label": "General Building"},
                            {"value": "Civil Engineering", "label": "Civil Engineering"},
                            {"value": "Electrical Engineering", "label": "Electrical Engineering"},
                            {"value": "Mechanical Engineering", "label": "Mechanical Engineering"},
                            {"value": "Asphalt Works", "label": "Asphalt Works"},
                            {"value": "Building Excavations", "label": "Building Excavations"},
                            {"value": "Structural Steelwork", "label": "Structural Steelwork"},
                            {"value": "Waterproofing", "label": "Waterproofing"},
                            {"value": "Other", "label": "Other"},
                        ],
                        "required": True,
                        "style": {"marginBottom": "16"}
                    },
                    {
                        "type": "text_input",
                        "name": "other_sectors",
                        "label": "Other sectors (comma-separated)",
                        "placeholder": "e.g., Security, Cleaning, Landscaping",
                        "required": False
                    },
                    {
                        "type": "text",
                        "text": "📍 Select your province",
                        "style": {"fontSize": "medium", "fontWeight": "bold", "marginTop": "16", "marginBottom": "8"}
                    },
                    {
                        "type": "select",
                        "name": "province",
                        "label": "Province",
                        "options": [
                            {"value": "Gauteng", "label": "Gauteng"},
                            {"value": "Western Cape", "label": "Western Cape"},
                            {"value": "KwaZulu-Natal", "label": "KwaZulu-Natal"},
                            {"value": "Eastern Cape", "label": "Eastern Cape"},
                            {"value": "Free State", "label": "Free State"},
                            {"value": "Limpopo", "label": "Limpopo"},
                            {"value": "Mpumalanga", "label": "Mpumalanga"},
                            {"value": "Northern Cape", "label": "Northern Cape"},
                            {"value": "North West", "label": "North West"},
                            {"value": "National", "label": "National (work anywhere)"},
                        ],
                        "required": True,
                        "style": {"marginBottom": "16"}
                    }
                ]
            },
            "next": "screen_complete"
        },
        
        # Screen 6: Complete
        {
            "id": "screen_complete",
            "title": "All Set!",
            "layout": {
                "type": "vertical",
                "children": [
                    {
                        "type": "text",
                        "text": "🎉 You're all set!",
                        "style": {"fontSize": "large", "fontWeight": "bold", "marginBottom": "16", "textAlign": "center"}
                    },
                    {
                        "type": "text",
                        "text": "Your profile is ready. You'll receive daily tender matches at 07:00 via WhatsApp.",
                        "style": {"marginBottom": "24", "textAlign": "center"}
                    },
                    {
                        "type": "button",
                        "text": "View My Matches",
                        "action": {
                            "type": "navigate",
                            "target": "external",
                            "url": "whatsapp://send?text=tenders"
                        },
                        "style": {"marginBottom": "12"}
                    },
                    {
                        "type": "button",
                        "text": "View Profile",
                        "action": {
                            "type": "navigate",
                            "target": "external",
                            "url": "whatsapp://send?text=profile"
                        },
                        "style": {"variant": "secondary"}
                    }
                ]
            },
            "terminal": True
        }
    ]
}


# ---------------------------------------------------------------------------
# Flow 2: Quick Document Upload
# ---------------------------------------------------------------------------

DOCUMENT_UPLOAD_FLOW_JSON = {
    "name": "tender_getter_doc_upload",
    "version": "1.0",
    "title": "Upload Compliance Document",
    "description": "Upload a single document for verification",
    "screens": [
        {
            "id": "screen_select_type",
            "title": "Document Type",
            "layout": {
                "type": "vertical",
                "children": [
                    {
                        "type": "text",
                        "text": "📄 What type of document are you uploading?",
                        "style": {"fontSize": "medium", "fontWeight": "bold", "marginBottom": "16"}
                    },
                    {
                        "type": "radio_group",
                        "name": "doc_type",
                        "label": "Document Type",
                        "options": [
                            {"value": "csd_letter", "label": "CSD Registration Letter"},
                            {"value": "bbbee_cert", "label": "B-BBEE Certificate / Sworn Affidavit"},
                            {"value": "tax_pin", "label": "SARS Tax Compliance PIN"},
                            {"value": "cidb_cert", "label": "CIDB Grading Certificate"},
                            {"value": "cipc_cert", "label": "CIPC Registration Certificate"},
                        ],
                        "required": True,
                        "style": {"marginBottom": "16"}
                    }
                ]
            },
            "next": "screen_upload"
        },
        {
            "id": "screen_upload",
            "title": "Upload Document",
            "layout": {
                "type": "vertical",
                "children": [
                    {
                        "type": "text",
                        "text": "📤 Upload your document",
                        "style": {"fontSize": "medium", "fontWeight": "bold", "marginBottom": "16"}
                    },
                    {
                        "type": "file_upload",
                        "name": "document",
                        "label": "Document (PDF or Photo)",
                        "accept": ["application/pdf", "image/jpeg", "image/png", "image/heic"],
                        "required": True,
                        "style": {"marginBottom": "16"}
                    },
                    {
                        "type": "text",
                        "text": "✅ We'll extract the details and update your profile automatically.",
                        "style": {"color": "green", "marginBottom": "16"}
                    }
                ]
            },
            "next": "screen_confirm"
        },
        {
            "id": "screen_confirm",
            "title": "Processing",
            "layout": {
                "type": "vertical",
                "children": [
                    {
                        "type": "text",
                        "text": "✅ Document uploaded successfully!",
                        "style": {"fontSize": "large", "fontWeight": "bold", "marginBottom": "16", "textAlign": "center", "color": "green"}
                    },
                    {
                        "type": "text",
                        "text": "Our AI is extracting the details. Your profile will be updated shortly.",
                        "style": {"textAlign": "center", "marginBottom": "24"}
                    },
                    {
                        "type": "button",
                        "text": "Done",
                        "action": {
                            "type": "close"
                        },
                        "style": {"marginTop": "16"}
                    }
                ]
            },
            "terminal": True
        }
    ]
}


# ---------------------------------------------------------------------------
# Flow 3: Profile Update
# ---------------------------------------------------------------------------

PROFILE_UPDATE_FLOW_JSON = {
    "name": "tender_getter_profile_update",
    "version": "1.0",
    "title": "Update Profile",
    "description": "Update your sectors, province, or notification preferences",
    "screens": [
        {
            "id": "screen_select_action",
            "title": "Update Profile",
            "layout": {
                "type": "vertical",
                "children": [
                    {
                        "type": "text",
                        "text": "⚙️ What would you like to update?",
                        "style": {"fontSize": "medium", "fontWeight": "bold", "marginBottom": "16"}
                    },
                    {
                        "type": "radio_group",
                        "name": "update_type",
                        "label": "Update Type",
                        "options": [
                            {"value": "sectors", "label": "Sectors / Industries"},
                            {"value": "province", "label": "Province / Location"},
                            {"value": "notifications", "label": "Notification Preferences"},
                            {"value": "documents", "label": "Re-upload Documents"},
                        ],
                        "required": True,
                        "style": {"marginBottom": "16"}
                    }
                ]
            },
            "next": "dynamic"  # Determined by selection
        },
        # Sectors screen
        {
            "id": "screen_sectors",
            "title": "Update Sectors",
            "layout": {
                "type": "vertical",
                "children": [
                    {
                        "type": "multi_select",
                        "name": "sectors",
                        "label": "Select your sectors",
                        "options": [
                            {"value": "General Building", "label": "General Building"},
                            {"value": "Civil Engineering", "label": "Civil Engineering"},
                            {"value": "Electrical Engineering", "label": "Electrical Engineering"},
                            {"value": "Mechanical Engineering", "label": "Mechanical Engineering"},
                            {"value": "Other", "label": "Other"},
                        ],
                        "required": True,
                    },
                    {
                        "type": "text_input",
                        "name": "other_sectors",
                        "label": "Other sectors (comma-separated)",
                        "placeholder": "e.g., Security, Cleaning",
                        "required": False,
                    }
                ]
            },
            "next": "screen_done"
        },
        # Province screen
        {
            "id": "screen_province",
            "title": "Update Province",
            "layout": {
                "type": "vertical",
                "children": [
                    {
                        "type": "select",
                        "name": "province",
                        "label": "Province",
                        "options": [
                            {"value": "Gauteng", "label": "Gauteng"},
                            {"value": "Western Cape", "label": "Western Cape"},
                            {"value": "KwaZulu-Natal", "label": "KwaZulu-Natal"},
                            {"value": "Eastern Cape", "label": "Eastern Cape"},
                            {"value": "Free State", "label": "Free State"},
                            {"value": "Limpopo", "label": "Limpopo"},
                            {"value": "Mpumalanga", "label": "Mpumalanga"},
                            {"value": "Northern Cape", "label": "Northern Cape"},
                            {"value": "North West", "label": "North West"},
                            {"value": "National", "label": "National"},
                        ],
                        "required": True,
                    }
                ]
            },
            "next": "screen_done"
        },
        # Notifications screen
        {
            "id": "screen_notifications",
            "title": "Notifications",
            "layout": {
                "type": "vertical",
                "children": [
                    {
                        "type": "checkbox",
                        "name": "daily_digest",
                        "label": "Daily tender digest (07:00)",
                        "required": False,
                    },
                    {
                        "type": "checkbox",
                        "name": "high_value_alerts",
                        "label": "High-value tender alerts (>R5M)",
                        "required": False,
                    },
                    {
                        "type": "checkbox",
                        "name": "report_notifications",
                        "label": "Compliance report ready notifications",
                        "required": False,
                    },
                    {
                        "type": "time_input",
                        "name": "digest_time",
                        "label": "Digest delivery time",
                        "required": False,
                    }
                ]
            },
            "next": "screen_done"
        },
        # Done screen
        {
            "id": "screen_done",
            "title": "Updated",
            "layout": {
                "type": "vertical",
                "children": [
                    {
                        "type": "text",
                        "text": "✅ Profile updated successfully!",
                        "style": {"fontSize": "large", "fontWeight": "bold", "marginBottom": "16", "textAlign": "center", "color": "green"}
                    },
                    {
                        "type": "button",
                        "text": "Done",
                        "action": {"type": "close"},
                        "style": {"marginTop": "16"}
                    }
                ]
            },
            "terminal": True
        }
    ]
}


# ---------------------------------------------------------------------------
# Flow Registry
# ---------------------------------------------------------------------------

FLOW_REGISTRY = {
    "onboarding": ONBOARDING_FLOW_JSON,
    "document_upload": DOCUMENT_UPLOAD_FLOW_JSON,
    "profile_update": PROFILE_UPDATE_FLOW_JSON,
}


def get_onboarding_flow_json() -> Dict[str, Any]:
    """Get the onboarding flow JSON for Meta Flow Builder."""
    return ONBOARDING_FLOW_JSON


def get_document_upload_flow_json() -> Dict[str, Any]:
    """Get the document upload flow JSON."""
    return DOCUMENT_UPLOAD_FLOW_JSON


def get_profile_update_flow_json() -> Dict[str, Any]:
    """Get the profile update flow JSON."""
    return PROFILE_UPDATE_FLOW_JSON


def get_all_flows() -> Dict[str, Dict[str, Any]]:
    """Get all flow definitions."""
    return FLOW_REGISTRY


# ---------------------------------------------------------------------------
# Template Messages (for Twilio Content Template Builder)
# ---------------------------------------------------------------------------

TEMPLATE_DEFINITIONS = {
    "daily_digest": {
        "name": "tender_getter_daily_digest",
        "language": "en",
        "category": "UTILITY",
        "components": [
            {
                "type": "HEADER",
                "format": "TEXT",
                "text": "🌅 Daily Tender Matches"
            },
            {
                "type": "BODY",
                "text": "Good morning {{1}}! You have {{2}} new tender match{{3}} today. Top match: {{4}} ({{5}} match)."
            },
            {
                "type": "FOOTER",
                "text": "Reply 'tenders' to view all | 'digest off' to pause"
            },
            {
                "type": "BUTTONS",
                "buttons": [
                    {
                        "type": "QUICK_REPLY",
                        "text": "View Tenders"
                    },
                    {
                        "type": "QUICK_REPLY",
                        "text": "My Profile"
                    }
                ]
            }
        ]
    },
    
    "tender_alert": {
        "name": "tender_getter_high_value_alert",
        "language": "en",
        "category": "UTILITY",
        "components": [
            {
                "type": "HEADER",
                "format": "TEXT",
                "text": "🚨 High-Value Tender Alert"
            },
            {
                "type": "BODY",
                "text": "New high-value tender: {{1}}\nValue: R{{2}}\nCloses: {{3}}\nMatch: {{4}}%"
            },
            {
                "type": "FOOTER",
                "text": "Reply 'verify csd' to check documents"
            },
            {
                "type": "BUTTONS",
                "buttons": [
                    {
                        "type": "QUICK_REPLY",
                        "text": "Verify CSD"
                    },
                    {
                        "type": "QUICK_REPLY",
                        "text": "View Details"
                    }
                ]
            }
        ]
    },
    
    "report_ready": {
        "name": "tender_getter_report_ready",
        "language": "en",
        "category": "UTILITY",
        "components": [
            {
                "type": "HEADER",
                "format": "DOCUMENT"
            },
            {
                "type": "BODY",
                "text": "Your compliance report for {{1}} is ready.\nMatch Score: {{2}}%\nBid: {{3}}"
            },
            {
                "type": "FOOTER",
                "text": "Tender Getter RSA"
            },
            {
                "type": "BUTTONS",
                "buttons": [
                    {
                        "type": "QUICK_REPLY",
                        "text": "View Report"
                    }
                ]
            }
        ]
    },
    
    "welcome": {
        "name": "tender_getter_welcome",
        "language": "en",
        "category": "UTILITY",
        "components": [
            {
                "type": "HEADER",
                "format": "TEXT",
                "text": "👋 Welcome to Tender Getter RSA"
            },
            {
                "type": "BODY",
                "text": "I find tenders you can actually win. Type 'onboard' to set up your profile, or 'menu' for commands."
            },
            {
                "type": "FOOTER",
                "text": "Tender Getter RSA"
            },
            {
                "type": "BUTTONS",
                "buttons": [
                    {
                        "type": "QUICK_REPLY",
                        "text": "Onboard"
                    },
                    {
                        "type": "QUICK_REPLY",
                        "text": "Menu"
                    }
                ]
            }
        ]
    },
    
    "verification_reminder": {
        "name": "tender_getter_verification_reminder",
        "language": "en",
        "category": "UTILITY",
        "components": [
            {
                "type": "HEADER",
                "format": "TEXT",
                "text": "📋 Document Verification Needed"
            },
            {
                "type": "BODY",
                "text": "Your {{1}} document needs to be uploaded/updated for tender eligibility."
            },
            {
                "type": "FOOTER",
                "text": "Reply 'verify {{1}}' to upload"
            },
            {
                "type": "BUTTONS",
                "buttons": [
                    {
                        "type": "QUICK_REPLY",
                        "text": f"Verify {{1}}"
                    }
                ]
            }
        ]
    },
}


def get_flow_templates() -> Dict[str, Dict[str, Any]]:
    """Get all template definitions for Twilio Content Template Builder."""
    return TEMPLATE_DEFINITIONS


# ---------------------------------------------------------------------------
# Flow Deployment Helpers
# ---------------------------------------------------------------------------

def get_flow_deployment_instructions() -> str:
    """Return instructions for deploying WhatsApp Flows."""
    return """
# WhatsApp Flows Deployment Instructions

## Prerequisites
1. Meta Business Verification completed
2. WhatsApp Business Account (WABA) set up
3. Twilio/360Dialog/Clickatell connected to WABA
4. Flow permissions approved in Meta Developer Dashboard

## Deployment Steps

### 1. Create Flows in Meta Flow Builder
- Go to Meta Developer Dashboard > WhatsApp > Flows
- Create new flow for each JSON definition
- Use the JSON from `get_onboarding_flow_json()`, etc.
- Configure data exchange endpoints (your webhook)

### 2. Configure Data Exchange Endpoint
- Endpoint: `https://your-domain.com/whatsapp/flow/data`
- Method: POST
- Headers: X-Hub-Signature-256 for validation
- Response: JSON with screen data or next screen

### 3. Test in WhatsApp
- Use "Preview" in Flow Builder
- Test with test phone numbers
- Verify data exchange works

### 4. Publish & Link
- Submit for review (if required)
- Once approved, get Flow IDs
- Link to your WhatsApp Business number

### 5. Trigger Flows from Chat
- Send template message with Flow CTA button
- Or use Flow deep link: `https://wa.me/YOUR_NUMBER?flow_id=FLOW_ID`

## Flow IDs (after publishing)
Replace in code:
- ONBOARDING_FLOW_ID = "your_onboarding_flow_id"
- DOC_UPLOAD_FLOW_ID = "your_doc_upload_flow_id"
- PROFILE_UPDATE_FLOW_ID = "your_profile_update_flow_id"

## Data Exchange Webhook Example
```python
@app.post("/whatsapp/flow/data")
async def flow_data_exchange(request: Request):
    # Validate signature
    # Parse flow_token, action, data
    # Return next screen or data
    return {
        "screen": "next_screen_id",
        "data": {
            "prefilled_field": "value_from_db"
        }
    }
```

## Template Creation in Twilio
1. Go to Twilio Console > Messaging > Content Template Builder
2. Create templates using `TEMPLATE_DEFINITIONS`
3. Submit for approval
4. Note Content SIDs for use in code
"""