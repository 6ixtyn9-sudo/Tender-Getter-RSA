#!/usr/bin/env bash
# Tender Getter RSA — Cloud Run Deployment Script
# Usage: ./scripts/deploy/cloudrun.sh [PROJECT_ID] [REGION] [SERVICE_NAME]

set -euo pipefail

PROJECT_ID="${1:-${GOOGLE_CLOUD_PROJECT}}"
REGION="${2:-africa-south1}"
SERVICE_NAME="${3:-tender-getter-whatsapp}"

if [[ -z "${PROJECT_ID}" ]]; then
    echo "Usage: $0 <PROJECT_ID> [REGION] [SERVICE_NAME]"
    echo "  PROJECT_ID: Google Cloud project ID (or set GOOGLE_CLOUD_PROJECT env var)"
    echo "  REGION: Cloud Run region (default: africa-south1)"
    echo "  SERVICE_NAME: Cloud Run service name (default: tender-getter-whatsapp)"
    exit 1
fi

echo "🚀 Deploying ${SERVICE_NAME} to ${REGION} in project ${PROJECT_ID}"

# Enable required APIs
echo "📋 Enabling required APIs..."
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    secretmanager.googleapis.com \
    --project="${PROJECT_ID}"

# Create Artifact Registry repo if needed
REPO_NAME="tender-getter"
if ! gcloud artifacts repositories describe "${REPO_NAME}" --location="${REGION}" --project="${PROJECT_ID}" >/dev/null 2>&1; then
    echo "📦 Creating Artifact Registry repository..."
    gcloud artifacts repositories create "${REPO_NAME}" \
        --repository-format=docker \
        --location="${REGION}" \
        --project="${PROJECT_ID}"
fi

# Build and push image using Cloud Build
echo "🔨 Building and pushing Docker image..."
gcloud builds submit \
    --tag="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:latest" \
    --project="${PROJECT_ID}" \
    .

# Deploy to Cloud Run
echo "☁️ Deploying to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
    --image="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:latest" \
    --platform=managed \
    --region="${REGION}" \
    --allow-unauthenticated \
    --port=8080 \
    --memory=512Mi \
    --cpu=1 \
    --min-instances=0 \
    --max-instances=10 \
    --concurrency=80 \
    --timeout=300 \
    --set-env-vars="PYTHONPATH=/app/src,ENV=production" \
    --project="${PROJECT_ID}"

# Get service URL
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" \
    --platform=managed \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --format='value(status.url)')

echo ""
echo "✅ Deployment complete!"
echo "🌐 Service URL: ${SERVICE_URL}"
echo ""
echo "📋 Next steps:"
echo "1. Update Twilio webhook URL to: ${SERVICE_URL}/whatsapp/webhook"
echo "2. Set secrets in Secret Manager (see scripts/deploy/set_secrets.sh)"
echo "3. Test with: curl -X POST ${SERVICE_URL}/health"