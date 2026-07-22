FOUNDER ACCEPTANCE — Production Readiness Runbook
Purpose: personally prove that Tender Getter behaves safely, usefully and
recoverably before any potential beta customer is invited, waitlisted or promised
a date. This is a founder-operated evidence gate, not a marketing checklist.

Rule zero
text

If a scenario has not been executed and evidenced, it is not ready.
Record date, environment, input, expected outcome, actual outcome, evidence link,
and remediation ticket for every check. Never store credentials, customer documents,
Tax PINs or payment details in this file.

A. Tender process rehearsal
The founder must process at least ten real tenders across multiple sectors and
formats before customer beta.

For each tender, prove the system and founder can determine:

 Original source and issuing entity.
 Tender reference, opening/closing date and time.
 Whether the tender is open, expired, cancelled or uncertain.
 Original tender document URL and document availability.
 Briefing/session requirement and attendance implication.
 Mandatory returnables, SBD forms and submission channel.
 CSD, SARS, CIDB, B-BBEE, local-content, geography and experience requirements.
 Tender value/capacity relationship where available.
 What is verified, recorded, inferred and unknown.
 Why the system alerted, suppressed, held or asked for enrichment.
Customer truth: a Qualified Match is decision support, not a completed bid,
eligibility guarantee, submission or award guarantee.

B. Company onboarding and verification
Run each scenario using test/synthetic data where possible; never use a real
customer's documents without consent.

Scenario	Expected safe result	Evidence
New user says hello	No sensitive data disclosed; onboarding starts correctly	[ ]
Consent refused	No marketing/digest activation	[ ]
Consent accepted	Immutable consent record	[ ]
Valid CIDB construction company	Registry corroboration / correct status	[ ]
Non-construction company with no registry answer	PENDING/hold, never self-verified	[ ]
Document company name conflicts with profile	No credential status becomes verified	[ ]
Valid CSD negative/inactive fresh report	FAILED/hold according to policy	[ ]
Stale report	Never auto-fails solely because stale	[ ]
Bad CIDB/CSD/Tax/B-BBEE shape	No verification status flip	[ ]
STOP	Suppression recorded and future messages stopped	[ ]
C. Tier and entitlement matrix
Test every row with a real entitlement record, not a mocked UI message.

State	Matches	Digest	Compliance report	Document analysis	Bid-Craft	Expected
No subscription	[ ]	[ ]	[ ]	[ ]	[ ]	Paid features denied; clear upgrade path
Beta Starter	[ ]	[ ]	[ ]	[ ]	[ ]	Only Starter capabilities; beta expiry recorded
Trial Pro	[ ]	[ ]	[ ]	[ ]	[ ]	Pro capabilities until trial expiry
Active Starter	[ ]	[ ]	[ ]	[ ]	[ ]	Starter only
Active Pro	[ ]	[ ]	[ ]	[ ]	[ ]	Pro only
Active VIP	[ ]	[ ]	[ ]	[ ]	[ ]	VIP + pack meter
Past due	[ ]	[ ]	[ ]	[ ]	[ ]	Fails closed according to commercial policy
Cancelled	[ ]	[ ]	[ ]	[ ]	[ ]	Future renewal stopped; access per policy
Expired beta	[ ]	[ ]	[ ]	[ ]	[ ]	Paid capability denied
Expired trial	[ ]	[ ]	[ ]	[ ]	[ ]	Paid capability denied
Expired annual	[ ]	[ ]	[ ]	[ ]	[ ]	Paid capability denied
VIP Bid-Craft quality gate
 Two included packs in one calendar month reserve and deliver correctly.
 Duplicate tender request does not consume a second pack.
 Third pack follows approved overage/block flow.
 Ten different tender documents tested.
 Output correctly captures tender facts and mandatory requirements.
 Output never invents credentials, staff, past experience, pricing or certificates.
 CUSTOMER ACTION REQUIRED and assumptions are visible.
 PDF/report delivery works with expiring access.
D. Payment and billing rehearsal
Use sandbox/test credentials only until provider and legal readiness gates pass.

 Correct monthly checkout creates correct session/reference.
 Correct annual checkout creates correct session/reference.
 WhatsApp owner phone binds to the payment/session record.
 Payment webhook signature rejection.
 Duplicate webhook idempotency.
 Altered amount rejected.
 Altered currency rejected.
 Unknown reference rejected.
 Correct payment activates correct plan only once.
 User can ask naturally: “Have I paid?” and “What plan am I on?”
 Failed renewal/past-due transition tested.
 Cancellation tested.
 Debit-order request stores intent but makes no false claim of live mandate.
 No banking credentials, PINs, passwords or OTPs requested in WhatsApp.
E. WhatsApp and delivery resilience
Scenario	Expected safe result	Evidence
Invalid Twilio signature	403 / no processing	[ ]
Duplicate MessageSid	Exactly-once processing	[ ]
Excess sender traffic	Distributed rate guard holds/rejects safely	[ ]
Bad media MIME type	Rejected before processing	[ ]
Oversized media	Rejected before expensive work	[ ]
Twilio CDN redirect	Allowed host path only	[ ]
Template unavailable	No duplicate immediate/REST message	[ ]
24-hour window constraint	Approved template/fallback policy works	[ ]
Media delivery failure	Error recorded and retry/fallback path visible	[ ]
STOP then restart	Suppression/restart behaviour correct	[ ]
F. Infrastructure and disaster rehearsal
 Cloud Run health endpoint works with production secrets.
 Runtime service account reads only intended Secret Manager secrets.
 Worker claims a job and completes it.
 Kill/restart worker during a job; retry does not duplicate customer delivery.
 Job reaches dead-letter after bounded attempts and produces alert/evidence.
 Supabase unavailable: workflow holds/fails safely and does not claim completion.
 Gemini one-key quota failure: rotation continues.
 All Gemini keys unavailable: user receives honest temporary failure, no invented output.
 Tender source failure: real-only pipeline never injects fixtures.
 Private storage object cannot be fetched anonymously.
 Signed report URL expires.
 Secret version rotation tested in non-production first.
 Cloud cost/budget alert tested or evidenced.
G. Security and incident rehearsal
 Sensitive values redacted from feedback/logs.
 Prompt-injected tender/document text cannot override system rules.
 Domain registrar MFA enabled, auto-renewal confirmed, recovery route documented.
 Cloud, Supabase, Twilio, Stitch, GitHub and registrar accounts recorded in Account Ownership Register.
 Incident owner and contact route defined.
 Simulate exposed secret: rotate secret, redeploy/restart, confirm old secret unusable.
 Simulate incorrect tender alert: stop path, customer correction, decision-audit retrieval.
 POPIA deletion/access request process rehearsed with synthetic data.
H. Go/no-go approval
Beta recruitment may start only when all required checks are marked complete and
blocking findings are closed.

text

Founder name:
Date:
Environment:
Production webhook URL:
Worker/job version:
Outstanding non-blocking risks:
Approval decision: GO / NO-GO
Signature: