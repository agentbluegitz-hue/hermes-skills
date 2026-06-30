#!/bin/bash
# Hermes Agent Website Deployment Script (Zensical-based)
# This script automates updating and deploying a Hermes agent website to DreamHost

# Change to website directory
WEBSITE_DIR="/home/agent-blue/.hermes/website"
mkdir -p "$WEBSITE_DIR"
cd "$WEBSITE_DIR" || { echo "Failed to change to website directory"; exit 1; }

# Check if this is a git repository, if not initialize it
if [ ! -d ".git" ]; then
  git init
  git remote add origin git@github.com:agentbluegitz-hue/hermes-agent-website.git
  git fetch origin
  git reset --hard origin/main
fi

# Pull latest changes
git fetch origin
git reset --hard origin/main

# Add and commit changes if any
if ! git diff-index --quiet HEAD --; then
  git add .
  git commit -m "Auto-update: $(date '+%Y-%m-%d %H:%M:%S')"
  git push origin main
  echo "Website updated and pushed to GitHub"
else
  echo "No changes in website repository"
fi

# Build the site with Zensical
echo "Building site with Zensical..."
source /tmp/zensical_env/bin/activate
zensical build

# Deploy to DreamHost via rsync (deploy the built site)
echo "Deploying to DreamHost..."
rsync -avz -e "ssh -o StrictHostKeyChecking=no" --delete site/ agent_blue@iad1-shared-b8-40.dreamhost.com:agent-blue.gitz.us/
echo "Deployment complete"