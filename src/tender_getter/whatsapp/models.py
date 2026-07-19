"""
WhatsApp-specific data models for Tender Getter RSA.
Extends core schemas with WhatsApp-specific fields.
"""

from enum import Enum
from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field, ConfigDict


class OnboardingStep(str, Enum):
    """Steps in the WhatsApp onboarding flow."""
    WELCOME = "welcome"
    COMPANY_NAME = "company_name"
    CIDB_LOOKUP = "cidb_lookup"
    CIDB_CONFIRM = "cidb_confirm"
    DOCUMENT_UPLOAD = "document_upload"
    SECTOR_PROVINCE = "sector_province"
    POPIA_CONSENT = "popia_consent"
    COMPLETE = "complete"


class VerificationStatus(str, Enum):
    """Document verification status."""
    NOT_PROVIDED = "not_provided"
    PENDING = "pending"
    VERIFIED = "verified"
    FAILED = "failed"
    EXPIRED = "expired"


class DocumentType(str, Enum):
    """Types of documents users can upload."""
    CSD_LETTER = "csd_letter"
    BBBEE_CERT = "bbbee_cert"
    TAX_PIN = "tax_pin"
    CIDB_CERT = "cidb_cert"
    CIPC_CERT = "cipc_cert"
    OTHER = "other"


class WhatsAppUser(BaseModel):
    """Extended user profile with WhatsApp-specific fields."""
    # Core identification
    whatsapp_id: str = Field(..., description="WhatsApp ID (wa_id from Business API)")
    phone_number: str = Field(..., description="E.164 format: +27733587019")
    
    # Link to core CompanyProfile (via registration_number)
    registration_number: Optional[str] = None
    
    # Onboarding state
    onboarding_step: OnboardingStep = OnboardingStep.WELCOME
    onboarding_data: Dict[str, Any] = Field(default_factory=dict)
    onboarding_started_at: Optional[datetime] = None
    onboarding_completed_at: Optional[datetime] = None
    
    # Verification status
    csd_status: VerificationStatus = VerificationStatus.NOT_PROVIDED
    bbbee_status: VerificationStatus = VerificationStatus.NOT_PROVIDED
    tax_status: VerificationStatus = VerificationStatus.NOT_PROVIDED
    cidb_status: VerificationStatus = VerificationStatus.NOT_PROVIDED
    
    # Document references (Supabase storage paths)
    documents: Dict[DocumentType, str] = Field(default_factory=dict)
    
    # Preferences
    sectors: List[str] = Field(default_factory=list)
    province: Optional[str] = None
    language: str = "en"
    timezone: str = "Africa/Johannesburg"
    
    # POPIA compliance
    popia_consent: bool = False
    popia_consent_at: Optional[datetime] = None
    popia_consent_version: str = "1.0"
    marketing_opt_in: bool = False
    
    # Engagement tracking
    last_active_at: Optional[datetime] = None
    total_messages_sent: int = 0
    total_messages_received: int = 0
    opted_out_at: Optional[datetime] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(use_enum_values=True)


class ConversationState(BaseModel):
    """Tracks conversation context for multi-step interactions."""
    user_id: str
    current_flow: Optional[str] = None
    current_step: Optional[str] = None
    context_data: Dict[str, Any] = Field(default_factory=dict)
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MediaMessage(BaseModel):
    """Incoming media message metadata."""
    message_sid: str
    user_id: str
    media_url: str
    media_content_type: str
    media_size: Optional[int] = None
    guessed_type: Optional[DocumentType] = None
    downloaded: bool = False
    supabase_path: Optional[str] = None
    parsed_data: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class OutboundMessage(BaseModel):
    """Outbound message tracking for delivery receipts."""
    message_sid: str
    user_id: str
    message_type: str  # text, template, media
    template_sid: Optional[str] = None
    content: Optional[str] = None
    media_url: Optional[str] = None
    status: str = "queued"  # queued, sent, delivered, read, failed
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DailyDigestPreferences(BaseModel):
    """User preferences for daily digest delivery."""
    user_id: str
    enabled: bool = True
    delivery_time: str = "07:00"  # HH:MM in user's timezone
    timezone: str = "Africa/Johannesburg"
    max_tenders: int = 5
    min_match_score: float = 70.0
    include_report_links: bool = True
    language: str = "en"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Database table names (for Supabase/PostgreSQL)
TABLES = {
    "whatsapp_users": "whatsapp_users",
    "conversation_states": "conversation_states",
    "media_messages": "media_messages",
    "outbound_messages": "outbound_messages",
    "digest_preferences": "daily_digest_preferences",
}