#!/usr/bin/env bash
# Tender Getter RSA — Secret Manager Setup
# Run after Cloud Run deployment to store secrets securely

set -euo pipefail

PROJECT_ID="${1:-${GOOGLE_CLOUD_PROJECT}}"
SERVICE_NAME="${2:-tender-getter-whatsapp}"
REGION="${3:-africa-south1}"

if [[ -z "${PROJECT_ID}" ]]; then
    echo "Usage: $0 <PROJECT_ID> [SERVICE_NAME] [REGION]"
    exit 1
fi

echo "🔐 Setting up secrets for ${SERVICE_NAME} in ${PROJECT_ID}"

# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com --project="${PROJECT_ID}"

# Create secrets (will prompt for values)
create_secret() {
    local name=$1
    local prompt=$2
    echo "${prompt}"
    read -s value
    echo "${value}" | gcloud secrets create "${name}" \
        --data-file=- \
        --project="${PROJECT_ID}" \
        --replication-policy="automatic" 2>/dev/null || \
    echo "${value}" | gcloud secrets versions add "${name}" \
        --data-file=- \
        --project="${PROJECT_ID}"
}

echo "Creating secrets (values hidden)..."
create_secret "twilio-account-sid" "Enter Twilio Account SID (ACxxxx):"
create_secret "twilio-auth-token" "Enter Twilio Auth Token:"
create_secret "tg-gemini-api-key" "Enter 7 Gemini API keys (comma-separated):"
create_secret "supabase-url" "Enter Supabase URL (https://xxx.supabase.co):"
create_secret "supabase-service-key" "Enter Supabase Service Role Key:"
create_secret "supabase-bucket" "Enter Supabase Storage Bucket (default: whatsapp-media):" 

# Grant Cloud Run service account access to secrets
SERVICE_ACCOUNT=$(gcloud run services describe "${SERVICE_NAME}" \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --format='value(spec.template.spec.serviceAccountName)')

if [[ -z "${SERVICE_ACCOUNT}" ]]; then
    SERVICE_ACCOUNT="${PROJECT_ID}@appspot.gserviceaccount.com"
fi

echo "🔑 Granting ${SERVICE_ACCOUNT} access to secrets..."
for secret in twilio-account-sid twilio-auth-token tg-gemini-api-key supabase-url supabase-service-key supabase-bucket; do
    gcloud secrets add-iam-policy-binding "${secret}" \
        --member="serviceAccount:${SERVICE_ACCOUNT}" \
        --role="roles/secretmanager.secretAccessor" \
        --project="${PROJECT_ID}"
done

# Update Cloud Run service to use secrets as environment variables
echo "☁️ Updating Cloud Run service with secret references..."
gcloud run services update "${SERVICE_NAME}" \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --update-secrets="TWILIO_ACCOUNT_SID=twilio-account-sid:latest,TWILIO_AUTH_TOKEN=twilio-auth-token:latest,GEMINI_API_KEY=tg-gemini-api-key:latest,SUPABASE_URL=supabase-url:latest,SUPABASE_SERVICE_ROLE_KEY=supabase-service-key:latest,SUPABASE_STORAGE_BUCKET=supabase-bucket:latest"

echo ""
echo "✅ Secrets configured! Service will restart with new secrets."
echo "🔗 View secrets: https://console.cloud.google.com/security/secret-manager?project=${PROJECT_ID}"