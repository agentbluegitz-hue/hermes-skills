# Arxiv Paper Filing from AI Briefings - Lessons Learned

## Overview
This document captures the specific implementation details and lessons learned for automatically filing Arxiv papers mentioned in AI daily briefings into Zotero, particularly in cron environments where user interaction is not possible.

## Cron Environment Challenges
1. **No user interaction**: Cannot use interactive tools or wait for approvals
2. **File path issues**: Complex output from find commands can cause parsing errors
3. **Tool restrictions**: execute_code is blocked in cron mode for security
4. **Environment limitations**: May lack pip or have restricted package installation

## Refined Implementation

### Step 1: Find Most Recent Briefing
```bash
# Primary method - check /tmp first (where briefings are typically generated)
latest=$(ls -t /tmp/ai_briefing_*.md 2>/dev/null | head -1)

# Fallback to home directory if not found in /tmp
if [ -z "$latest" ]; then
    latest=$(ls -t /home/agent-blue/ai_briefing_*.md 2>/dev/null | head -1)
fi

# Exit if no briefing found
if [ -z "$latest" ]; then
    echo "No AI briefing file found."
    exit 1
fi
echo "Processing $latest"
```

### Step 2: Extract and Filter URLs
```bash
# Extract HTTP/HTTPS URLs
urls=$(grep -oE 'https?://[^[:space:]]+' "$latest")

# Extract DOIs and convert to full URLs
dois=$(grep -oE '10\\.[0-9]{4,9}/[-._;()/:A-Z0-9]+' "$latest" -i)
doi_urls=""
for doi in $dois; do
    doi_urls="$doi_urls https://doi.org/$doi"
done

# Combine all URLs
all_urls="$urls $doi_urls"

# Filter for target domains and deduplicate
echo "$all_urls" | tr ' ' '\\n' | grep -E '(arxiv\\.org|biorxiv\\.org|medrxiv\\.org|ssrn\\.com|^https://doi\\.org/)' | sort -u > /home/agent-blue/.hermes/arxiv_to_check.txt

# Report results
count=$(wc -l < /home/agent-blue/.hermes/arxiv_to_check.txt)
echo "Saved $count URLs/DOIs to /home/agent-blue/.hermes/arxiv_to_check.txt"
```

### Step 3: Execute Filing Script
```bash
script_path="/home/agent-blue/.hermes/skills/zotero-library-organizer/scripts/file_missing_arxiv.py"
if [ -f "$script_path" ]; then
    echo "Running $script_path"
    python3 "$script_path"
else
    echo "Script not found: $script_path"
    exit 1
fi
```

## Key Fixes and Improvements

### 1. File Path Handling
**Problem**: Using `find` with `-printf '%T@ %p\\n'` produced output with timestamps that, when used as input to grep, created invalid file paths like:
```
/tmp/ai_briefing_2026-07-01.md 1782904196.0982274230
```
This caused grep to fail with "No such file or directory" errors.

**Solution**: Use `ls -t` instead, which outputs clean filenames without timestamps.

### 2. DOI Extraction Robustness
**Problem**: Simple DOI patterns missed version numbers or had issues with special characters.

**Solution**: Use robust regex pattern `10\\.[0-9]{4,9}/[-._;()/:A-Z0-9]+` with case-insensitive flag.

### 3. Environment Adaptation
**Problem**: Cron jobs cannot use `execute_code` or interactive tools due to security restrictions.

**Solution**: Use pure bash/file I/O approaches that work within cron constraints.

### 4. Error Handling
**Problem**: Silent failures when no briefings are found or when scripts are missing.

**Solution**: Explicit error checking and informative exit messages.

## Verification Steps
1. Confirm briefing file exists and is readable
2. Verify extracted URLs match expected patterns
3. Check that output file contains valid Arxiv/biorxiv/medrxiv/ssrn/doi URLs
4. Ensure filing script executes without errors
5. Validate that any new papers are properly added to Zotero (or skipped if duplicates)

## Maintenance Notes
- This implementation assumes briefings follow the naming pattern `ai_briefing_YYYY-MM-DD.md`
- The fallback to home directory covers cases where briefings might be stored elsewhere
- Output file path (`/home/agent-blue/.hermes/arxiv_to_check.txt`) should be consistent with what the filing script expects
- Consider adding logging for audit purposes in production environments