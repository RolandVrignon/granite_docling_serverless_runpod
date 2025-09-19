#!/bin/bash

# Deployment script for Granite Docling Serverless on Runpod
# This script helps deploy the serverless function to Runpod

set -e

echo "🚀 Deploying Granite Docling Serverless to Runpod..."

# Check if runpod CLI is installed
if ! command -v runpod &> /dev/null; then
    echo "❌ Runpod CLI not found. Installing..."
    pip install runpod
fi

# Check if user is logged in
if ! runpod whoami &> /dev/null; then
    echo "❌ Not logged in to Runpod. Please login first:"
    echo "runpod login"
    exit 1
fi

# Build Docker image
echo "🔨 Building Docker image..."
docker build -t granite-docling-serverless:latest .

# Tag image for Runpod registry
echo "📦 Tagging image for Runpod registry..."
docker tag granite-docling-serverless:latest runpod.io/granite-docling-serverless:latest

# Push to Runpod registry
echo "⬆️ Pushing image to Runpod registry..."
docker push runpod.io/granite-docling-serverless:latest

# Deploy serverless function
echo "🚀 Deploying serverless function..."
runpod serverless deploy \
    --name granite-docling-serverless \
    --image runpod.io/granite-docling-serverless:latest \
    --handler handler.handler \
    --timeout 300 \
    --memory 16Gi \
    --gpu 1 \
    --cpu 4

echo "✅ Deployment completed successfully!"
echo "📋 Your serverless function is now available at:"
echo "https://api.runpod.ai/v2/granite-docling-serverless"

echo ""
echo "🔧 To test your deployment:"
echo "curl -X POST https://api.runpod.ai/v2/granite-docling-serverless/runsync \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -H 'Authorization: Bearer YOUR_API_KEY' \\"
echo "  -d '{\"input\": {\"document_url\": \"https://example.com/document.pdf\"}}'"

echo ""
echo "📚 Example usage:"
echo "# Convert from URL"
echo "curl -X POST https://api.runpod.ai/v2/granite-docling-serverless/runsync \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -H 'Authorization: Bearer YOUR_API_KEY' \\"
echo "  -d '{\"input\": {\"document_url\": \"https://example.com/document.pdf\", \"output_format\": \"markdown\"}}'"

echo ""
echo "# Convert from base64"
echo "curl -X POST https://api.runpod.ai/v2/granite-docling-serverless/runsync \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -H 'Authorization: Bearer YOUR_API_KEY' \\"
echo "  -d '{\"input\": {\"document_base64\": \"BASE64_DATA\", \"filename\": \"document.pdf\"}}'"
