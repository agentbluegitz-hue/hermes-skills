# Environment Variable Configuration for Hermes Website Deployment

This document explains how to configure the Hermes Agent website deployment using environment variables instead of hard-coded values.

## Overview

To avoid IP blocking from repeated failed connection attempts and to make the deployment more flexible, the website deployment process uses environment variables for configuration rather than hard-coded values.

## Environment Variables

The following environment variables are used:

| Variable | Description | Default Value | Example |
|----------|-------------|---------------|---------|
| `WEBHOST_USER` | SSH/SFTP username for DreamHost deployment | `agent_blue` | `agent_blue` |
| `WEBHOST_SFTP` | SSH/SFTP host for DreamHost deployment | `iad1-shared-b8-40.dreamhost.com` | `iad1-shared-b8-40.dreamhost.com` |
| `WEBHOST_URL` | Base URL for the website | `https://agent-blue.gitz.us/` | `https://agent-blue.gitz.us/` |

These variables are typically set in the `.env` file in the Hermes home directory (`/home/agent-blue/.hermes/.env`).

## Usage in Deployment Script

The deployment script (`auto-deploy-website.sh`) uses these variables as follows:

```bash
# Use environment variables with fallbacks
USER="${WEBHOST_USER:-agent_blue}"
HOST="${WEBHOST_SFTP:-iad1-shared-b8-40.dreamhost.com}"
RSYNC_DEST="${USER}@${HOST}:~/public_html/"

# Test SSH connection first
if ssh -i ~/.ssh/id_ed25519 -o BatchMode=yes -o PreferredAuthentications=publickey "$USER@$HOST" true 2>/dev/null; then
  # Sync the site directory to DreamHost
  rsync -avz --delete site/ "$RSYNC_DEST"
  echo "Site deployed to DreamHost at $RSYNC_DEST"
else
  echo "SSH connection to $USER@$HOST failed. Skipping DreamHost deployment."
  echo "Website built and pushed to GitHub only."
fi
```

## Benefits

1. **Prevents IP Blocking**: By testing the SSH connection before attempting rsync, we avoid repeated failed connection attempts that could trigger IP blocking.
2. **Flexibility**: Easy to change deployment targets without modifying scripts.
3. **Security**: Keeps sensitive configuration out of version control (when using `.env` files).
4. **Graceful Degradation**: If environment variables aren't set or SSH fails, the script falls back to GitHub-only deployment.

## Implementation in Skills

The `hermes-website-deployment` skill has been updated to use these environment variables with appropriate fallbacks:

- SSH connectivity check: `ssh -i ~/.ssh/id_ed25519 -o BatchMode=yes -o PreferredAuthentications=publickey ${WEBHOST_USER:-agent_blue}@${WEBHOST_SFTP:-iad1-shared-b8-40.dreamhost.com} true`
- Verification URL: `${WEBHOST_URL:-https://agent-blue.gitz.us/}`
- Username verification: `${WEBHOST_USER:-agent_blue}`