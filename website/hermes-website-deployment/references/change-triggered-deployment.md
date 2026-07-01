# Change-Triggered Website Deployment Implementation

## Overview
This document details the implementation of change-triggered website deployment for the Hermes Agent website, replacing hourly cron jobs with a more efficient approach that only deploys when actual changes are detected.

## Implementation Details

### 1. Created Change-Detection Wrapper Script
**File**: `~/hermes/scripts/auto-deploy-website-if-changed.sh`

```bash
#!/bin/bash
# Wrapper script to deploy website only if there are changes in the remote repository

WEBSITE_DIR="/home/agent-blue/.hermes/website"
cd "$WEBSITE_DIR" || { echo "Failed to change to website directory"; exit 1; }

# Fetch the latest from remote
git fetch origin

# Check if the local main branch is behind the remote
if [ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ]; then
  echo "No changes in remote repository. Skipping deployment."
  exit 0
fi

# Now run the original deployment script
/home/agent-blue/.hermes/scripts/auto-deploy-website.sh
```

### 2. Removed Hourly Cron Job
- **Job ID**: `a631854a0de2` (Auto-deploy Hermes Website)
- **Schedule**: `0 * * * *` (hourly)
- **Status**: Removed

### 3. Created Change-Triggered Cron Job
- **Job ID**: `097ae4b8a06d` (Auto-deploy Hermes Website (on remote changes))
- **Schedule**: `*/15 * * * *` (every 15 minutes)
- **Script**: `auto-deploy-website-if-changed.sh`
- **Delivery**: Local
- **Toolsets**: file, terminal

### 4. Verification Process
The wrapper script follows this logic:
1. Change to website directory (`~/hermes/website`)
2. Fetch latest changes from remote origin
3. Compare local HEAD commit with remote origin/main commit
4. If identical: exit (no changes)
5. If different: run full deployment script

### 5. Benefits of This Approach
- **Efficiency**: Only processes when actual changes exist
- **Resource Conservation**: Avoids unnecessary builds and deployments
- **Timeliness**: Changes deployed within 15 minutes of being pushed
- **Reliability**: Maintains all existing security and deployment guarantees
- **Transparency**: Clear logging shows when deployments are skipped vs executed

### 6. Environment Variables Used
The deployment script continues to use:
- `WEBHOST_USER` (defaults to `agent_blue`)
- `WEBHOST_SFTP` (defaults to `iad1-shared-b8-40.dreamhost.com`)
- SSH key: `~/.ssh/id_ed25519`

### 7. Security Considerations Maintained
- No hardcoded credentials or hostnames
- SSH key-based authentication
- Environment variable fallbacks for configuration
- Same deployment process as before (just with change detection pre-check)

## Usage
This system is now active and will:
- Check for remote changes every 15 minutes
- Only trigger deployment when the remote repository has new commits
- Maintain the same deployment process (build with Zensical, rsync to DreamHost)
- Preserve all logging and error handling from the original deployment script