#!/usr/bin/env bash
set -euo pipefail
PROJECT_ID="${1:?Usage: ./deploy.sh PROJECT_ID}"
REGION="${2:-europe-west2}"
SERVICE="${3:-enterprise-conversational-ai}"
gcloud config set project "${PROJECT_ID}"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
gcloud run deploy "${SERVICE}" --source . --region "${REGION}" --allow-unauthenticated
echo "Deployment complete."
