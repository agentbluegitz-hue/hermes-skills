# Environment Variable Usage in Hermes Automation

This document provides best practices for using environment variables in Hermes Agent automation to avoid hard-coded values and improve flexibility.

## Overview

Hard-coding values like usernames, hosts, or URLs in automation scripts creates several problems:
- IP blocking from repeated failed connection attempts
- Inflexibility when deployment targets change
- Security risks if sensitive information is committed to version control
- Difficulty maintaining multiple environments (dev/staging/prod)

## Best Practices

### 1. Use Environment Variables for Configuration

Instead of hard-coding values in scripts, use environment variables with sensible fallbacks:

```bash
# Good: Use environment variables with fallbacks
USER="${WEBHOST_USER:-agent_blue}"
HOST="${WEBHOST_SFTP:-iad1-shared-b8-40.dreamhost.com}"
URL="${WEBHOST_URL:-https://agent-blue.gitz.us/}"

# Test before using
if [ -n "$USER" ] && [ -n "$HOST" ]; then
    echo "Using $USER@$HOST"
else
    echo "Missing required configuration"
    exit 1
fi
```

### 2. Source Environment Files Properly

When working with `.env` files, source them correctly in bash scripts:

```bash
# Source the environment file if it exists
if [ -f "/home/agent-blue/.hermes/.env" ]; then
    # Export variables so they're available to subprocesses
    set -o allexport
    source /home/agent-blue/.hermes/.env
    set +o allexport
fi
```

### 3. Validate Required Variables

Check that required environment variables are set before proceeding:

```bash
validate_env() {
    local missing=()
    
    [[ -z "$WEBHOST_USER" ]] && missing+=("WEBHOST_USER")
    [[ -z "$WEBHOST_SFTP" ]] && missing+=("WEBHOST_SFTP")
    
    if [ ${#missing[@]} -gt 0 ]; then
        echo "Error: Missing required environment variables: ${missing[*]}"
        echo "Please set these in your .env file or environment"
        return 1
    fi
    
    return 0
}
```

### 4. Use Proper Variable Expansion

Always use quotes around variable expansions to prevent word splitting and globbing:

```bash
# Good
rsync -avz --delete site/ "$USER@$HOST:~/public_html/"

# Bad (can break if username or host contains spaces)
rsync -avz --delete site/ $USER@$HOST:~/public_html/
```

### 5. Implement Connection Testing

Before attempting operations that depend on network connectivity, test the connection first:

```bash
# Test SSH connection before deploying
if ssh -i ~/.ssh/id_ed25519 -o BatchMode=yes -o PreferredAuthentications=publickey "$USER@$HOST" true 2>/dev/null; then
    echo "SSH connection successful"
    # Proceed with deployment
else
    echo "SSH connection failed - skipping deployment"
    echo "Please verify:"
    echo "  - Host $HOST is reachable"
    echo "  - SSH service is running on port 22"
    echo "  - User $USER has valid SSH key configured"
    echo "  - Firewall allows outbound SSH connections"
    return 1
fi
```

## Application to Website Deployment

In the Hermes website deployment automation, these practices are implemented as follows:

1. **Environment Variable Usage**: The `auto-deploy-website.sh` script uses `WEBHOST_USER`, `WEBHOST_SFTP`, and `WEBHOST_URL` with appropriate fallbacks.

2. **Connection Testing**: Before attempting rsync deployment, the script tests SSH connectivity to avoid wasting time on failed connections.

3. **Graceful Degradation**: If environment variables aren't set or SSH fails, the script continues with GitHub-only deployment (which always succeeds if the repository is accessible).

4. **Verification**: After deployment, the script verifies success and provides clear error messages when things go wrong.

## Benefits

1. **Prevents IP Blocking**: By testing connections before attempting operations, we avoid repeated failed attempts that could trigger security blocks.
2. **Configuration Flexibility**: Easy to change deployment targets by updating environment variables rather than modifying scripts.
3. **Improved Reliability**: Connection testing prevents wasting time on operations that are destined to fail.
4. **Better Error Handling**: Clear error messages help users understand what went wrong and how to fix it.
5. **Security**: Keeps configuration out of version control when using `.env` files appropriately.

## Example from Hermes Website Deployment

Here's how the updated deployment script implements these practices:

```bash
# Deploy to DreamHost via rsync if environment variables are set
if [ -n "$WEBHOST_USER" ] && [ -n "$WEBHOST_SFTP" ]; then
  echo "Deploying to DreamHost via rsync..."
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
else
  echo "WEBHOST_USER or WEBHOST_SFTP not set. Skipping DreamHost deployment."
  echo "Website built and pushed to GitHub only."
fi
```

This approach ensures that:
- The script only attempts DreamHost deployment when credentials are available
- It verifies SSH connectivity before attempting the potentially slow rsync operation
- It provides clear feedback when deployment is skipped
- It always ensures the website is updated in GitHub (for GitHub Pages)