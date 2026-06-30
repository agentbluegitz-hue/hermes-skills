# Hermes Automation Patterns

## Working with Hermes .env Files

Hermes Agent stores configuration and API keys in `~/.hermes/.env`. When automating tasks that need to access these values, follow these patterns:

### Extracting Values Safely

```bash
# Extract a value from .env file (handles quoted values correctly)
TOKEN=*** '^GH_ACCESS_TOKEN' /home/agent-blue/.hermes/.env | cut -d= -f2)

# For values that might contain special characters, use sed:
VALUE=*** -n 's/^KEY_NAME=*** //p' /home/agent-blue/.hermes/.env)
```

### Common .env Values in Hermes

- `GH_ACCESS_TOKEN` - GitHub personal access token
- `WEBHOST_URL` - Web hosting domain (e.g., agent-blue.gitz.us)
- `WEBHOST_USER` - SSH/SFTP username
- `WEBHOST_SFTP` - SSH/SFTP host
- `ZOTERO_API_KEY` - Zotero API key for library access

## Automation Script Patterns

### Directory Structure Awareness

When writing automation scripts for Hermes, be aware of the standard directory structure:

```
~/.hermes/
├── .env                 # Environment variables and secrets
├── config.yaml          # Main configuration
├── skills/              # Installed skills directory
├── scripts/             # Automation scripts
├── sessions/            # Session history
└── website/             # Website content (if applicable)
```

### Safe File Operations

When modifying files in Hermes automation, always follow the correct read-modify-write pattern to avoid file-mutation verifier warnings:

1. Use `read_file` to get content (returns LINE|CONTENT format)
2. Parse to extract actual content (split on '|', take second part)
3. Process the clean content
4. Use `write_file` with pure content (no line numbers or prefixes)

See the main hermes-file-operations skill for detailed patterns.

### Cron Job Integration

For periodic automation tasks:

1. Place scripts in `~/.hermes/scripts/`
2. Make them executable: `chmod +x ~/.hermes/scripts/script-name.sh`
3. Schedule via `hermes cron create` or the cronjob tool
4. Use appropriate delivery options (local, origin, all, etc.)

Example hourly skill synchronization:
```bash
#!/bin/bash
cd /home/agent-blue/.hermes/skills || exit 1
if ! git diff-index --quiet HEAD --; then
  git add .
  git commit -m "Auto-sync skills: $(date '+%Y-%m-%d %H:%M:%S')"
  git push origin main
fi
```

## Verification Patterns

After file operations in automation scripts:

1. Check exit codes of commands
2. Verify file contents when appropriate
3. Log success/failure for debugging
4. Consider using temporary files for atomic updates

```bash
# Example verification pattern
if git push origin main; then
  echo "Successfully pushed skills to GitHub"
else
  echo "Failed to push skills to GitHub" >&2
  exit 1
fi
```

## Related Tools

- `read_file` / `write_file` - Safe file read/write with verifier protection
- `patch` - Targeted file edits using fuzzy matching
- `execute_code` - Complex file processing logic
- `terminal` - Shell command execution
- `cronjob` - Scheduled task management