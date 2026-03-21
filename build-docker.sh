#!/bin/bash
# Docker build and push script for memobot

set -e  # Exit on error

DOCKER_USERNAME="axkralj990"
IMAGE_NAME="memobot"
TAG="latest"

echo "🐳 Building Docker image for linux/amd64..."
docker buildx build --platform linux/amd64 \
  -t ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG} \
  --push .

echo ""
echo "✅ Successfully built and pushed:"
echo "   ${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}"
echo ""
echo "📦 To pull on Synology:"
echo "   docker-compose pull"
echo "   docker-compose up -d"
