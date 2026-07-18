"""
Daily digest delivery for Tender Getter RSA.
Sends matched tenders to users via WhatsApp template messages.
"""

import logging
from datetime import datetime, time, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .models import WhatsAppUser, DailyDigestPreferences
from .database import get_users_by_step, upsert_digest_preferences, get_digest_preferences
from .outbound import send_template_message, send_text_message, send_media_message

logger = logging.getLogger(__name__)

# Template SIDs (to be created in Twilio Console)
TEMPLATE_DAILY_DIGEST = "HX_daily_digest_v1"  # Replace with actual SID
TEMPLATE_TENDER_ALERT = "HX_tender_alert_v1"   # Replace with actual SID
TEMPLATE_REPORT_READY = "HX_report_ready_v1"   # Replace with actual SID


@dataclass
class TenderMatch:
    """Simplified tender match for digest."""
    tender_id: str
    title: str
    issuing_entity: str
    closing_date: datetime
    estimated_value: Optional[float]
    required_cidb_class: Optional[str]
    required_cidb_level: Optional[int]
    location_target: Optional[str]
    match_score: float
    bbbee_points: float
    bbbee_system: str
    report_url: Optional[str] = None


async def send_daily_digest(user: WhatsAppUser, matches: List[TenderMatch]) -> bool:
    """Send daily digest to a single user."""
    prefs = get_digest_preferences(user.phone_number)
    if not prefs or not prefs.enabled:
        return False
    
    if not matches:
        # Send empty digest message
        try:
            send_text_message(
                user.phone_number,
                "🌅 *Good morning!*\n\nNo new tender matches for you today.\n"
                "I'll check again tomorrow."
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send empty digest to {user.phone_number}: {e}")
            return False
    
    # Filter by preferences
    filtered = [
        m for m in matches
        if m.match_score >= prefs.min_match_score
    ][:prefs.max_tenders]
    
    if not filtered:
        return await send_daily_digest(user, [])  # Send empty
    
    # Build digest message
    message = build_digest_message(user, filtered, prefs)
    
    try:
        # Try template first (better delivery rates)
        send_template_message(
            user.phone_number,
            TEMPLATE_DAILY_DIGEST,
            {
                "user_name": user.onboarding_data.get("company_name", "there"),
                "match_count": str(len(filtered)),
                "top_tender": filtered[0].title[:40] if filtered else "None",
                "top_score": f"{filtered[0].match_score:.0f}%" if filtered else "0%",
            }
        )
        # Also send detailed text as fallback
        send_text_message(user.phone_number, message)
        return True
    except Exception as e:
        logger.warning(f"Template failed, sending text only: {e}")
        try:
            send_text_message(user.phone_number, message)
            return True
        except Exception as e2:
            logger.error(f"Failed to send digest to {user.phone_number}: {e2}")
            return False


def build_digest_message(user: WhatsAppUser, matches: List[TenderMatch], prefs: DailyDigestPreferences) -> str:
    """Build formatted digest message."""
    company_name = user.onboarding_data.get("company_name", "there")
    date_str = datetime.now().strftime("%d %B %Y")
    
    lines = [
        f"🌅 *Good morning, {company_name}!*",
        f"📅 {date_str}",
        f"",
        f"🎯 *{len(matches)} new tender match(es) for you:*",
        f"",
    ]
    
    for i, match in enumerate(matches, 1):
        value_str = f"R{match.estimated_value:,.0f}" if match.estimated_value else "Value not disclosed"
        cidb_str = ""
        if match.required_cidb_class and match.required_cidb_level:
            cidb_str = f" | CIDB: {match.required_cidb_class}{match.required_cidb_level}"
        
        lines.extend([
            f"{i}. *{match.title[:50]}...*",
            f"   📋 {match.tender_id} | {match.issuing_entity}",
            f"   💰 {value_str}{cidb_str}",
            f"   📍 {match.location_target or 'National'} | ⏰ Closes: {match.closing_date.strftime('%d %b %Y')}",
            f"   📊 Match: {match.match_score:.0f}% | B-BBEE: {match.bbbee_points:.0f}/{20 if match.bbbee_system == '80/20' else 10} pts ({match.bbbee_system})",
        ])
        
        if match.report_url and prefs.include_report_links:
            lines.append(f"   📄 [View Compliance Report]({match.report_url})")
        
        lines.append("")
    
    lines.extend([
        "---",
        "Reply *tenders* to view all matches.",
        "Reply *verify csd/tax/bbbee/cidb* to update documents.",
        "Reply *digest off* to pause daily messages.",
    ])
    
    return "\n".join(lines)


async def send_tender_alert(user: WhatsAppUser, match: TenderMatch) -> bool:
    """Send immediate alert for high-value match."""
    try:
        message = (
            f"🚨 *High-Value Tender Alert!*\n\n"
            f"*{match.title}*\n"
            f"📋 {match.tender_id} | {match.issuing_entity}\n"
            f"💰 R{match.estimated_value:,.0f}\n"
            f"📍 {match.location_target or 'National'}\n"
            f"⏰ Closes: {match.closing_date.strftime('%d %b %Y')}\n"
            f"📊 Match: {match.match_score:.0f}%\n\n"
            f"Reply *verify csd* to ensure your documents are ready."
        )
        send_text_message(user.phone_number, message)
        return True
    except Exception as e:
        logger.error(f"Failed to send alert to {user.phone_number}: {e}")
        return False


async def send_report_notification(user: WhatsAppUser, match: TenderMatch, report_url: str) -> bool:
    """Send notification that compliance report is ready."""
    try:
        # Send PDF via media message
        send_media_message(
            user.phone_number,
            report_url,
            f"📋 *Compliance Report Ready*\n\n"
            f"*{match.title}*\n"
            f"📋 {match.tender_id}\n"
            f"📊 Match Score: {match.match_score:.0f}%\n\n"
            f"Your detailed compliance checklist and bid strategy are attached."
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send report to {user.phone_number}: {e}")
        # Fallback to text with link
        try:
            send_text_message(
                user.phone_number,
                f"📋 *Compliance Report Ready*\n\n"
                f"*{match.title}* ({match.tender_id})\n"
                f"📊 Match: {match.match_score:.0f}%\n\n"
                f"View report: {report_url}"
            )
            return True
        except Exception as e2:
            logger.error(f"Failed to send report link to {user.phone_number}: {e2}")
            return False


async def run_daily_digest_job() -> Dict[str, int]:
    """
    Main job to run daily (scheduled via cron/Cloud Scheduler).
    Fetches matches for all users and sends digests.
    """
    from ..pipeline import run_pipeline_match
    from ..database import get_database_client
    from ..schemas import CompanyProfile
    
    stats = {"sent": 0, "failed": 0, "skipped": 0, "total_users": 0}
    
    # Get all onboarded users
    users = get_users_by_step("complete")  # OnboardingStep.COMPLETE
    stats["total_users"] = len(users)
    
    if not users:
        logger.info("No onboarded users for daily digest")
        return stats
    
    # Get database client
    db = get_database_client()
    if hasattr(db, "connect"):
        db.connect()
    
    try:
        # Get all open tenders
        tenders = db.list_open_tenders(limit=10000)
        
        # Filter to open, valid tenders
        from ..pipeline import _is_open_and_valid
        now = datetime.now()
        valid_tenders = [t for t in tenders if _is_open_and_valid(t, now)]
        
        # Process each user
        for user in users:
            if not user.registration_number:
                stats["skipped"] += 1
                continue
            
            # Load company profile
            company = CompanyProfile(
                registration_number=user.registration_number,
                company_name=user.onboarding_data.get("company_name", ""),
                csd_number=user.onboarding_data.get("csd_number"),
                bbbee_level=user.onboarding_data.get("bbbee_level", 9),
                cidb_gradings=[
                    type('CIDBGrading', (), g)() for g in user.onboarding_data.get("cidb_gradings", [])
                ],
                location=type('Location', (), {
                    "province": user.province,
                    "city": "Unknown",
                })(),
                sectors=user.sectors,
                has_tax_pin=user.tax_status == "verified",
            )
            
            # Run matching
            from ..matcher import match as run_match
            matches = []
            for tender in valid_tenders:
                result = run_match(company, tender)
                if result.is_eligible:
                    matches.append(TenderMatch(
                        tender_id=result.tender_id,
                        title=result.tender_title,
                        issuing_entity=tender.issuing_entity,
                        closing_date=tender.closing_date,
                        estimated_value=tender.estimated_value,
                        required_cidb_class=tender.required_cidb_class,
                        required_cidb_level=tender.required_cidb_level,
                        location_target=tender.location_target,
                        match_score=result.match_score,
                        bbbee_points=result.bbbee_points,
                        bbbee_system=result.bbbee_system or "80/20",
                    ))
            
            # Sort by score
            matches.sort(key=lambda m: -m.match_score)
            
            # Send digest
            success = await send_daily_digest(user, matches)
            if success:
                stats["sent"] += 1
            else:
                stats["failed"] += 1
                
    finally:
        if hasattr(db, "close"):
            db.close()
    
    logger.info(f"Daily digest job completed: {stats}")
    return stats


# ---------------------------------------------------------------------------
# Scheduler Integration
# ---------------------------------------------------------------------------

def schedule_daily_digest():
    """Configure daily digest scheduling.
    
    For production, use one of:
    1. Google Cloud Scheduler + Cloud Run Job
    2. GitHub Actions cron
    3. APScheduler in-process
    4. System cron on VM
    
    Example Cloud Scheduler:
    ```
    gcloud scheduler jobs create http daily-digest \
        --schedule="0 5 * * *" \  # 05:00 UTC = 07:00 SAST
        --uri="https://your-cloud-run-url/digest/trigger" \
        --http-method=POST \
        --oidc-service-account-email=your-sa@project.iam.gserviceaccount.com
    ```
    """
    pass


# Manual trigger endpoint (add to FastAPI app)
async def trigger_daily_digest_manual() -> Dict[str, int]:
    """Manual trigger for testing."""
    return await run_daily_digest_job()