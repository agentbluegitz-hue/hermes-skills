---
name: process-ai-briefing-for-zotero
description: Extract academic publication links from AI briefing markdown files and prepare them for Zotero ingestion
version: 1.0.0
---
# Process AI Briefing for Zotero

This skill outlines the process for extracting academic publication links from AI briefing markdown files and saving them for Zotero ingestion.

## When to Use

Use this skill when:
- You have generated or received an AI daily briefing in markdown format
- You need to identify academic papers (arXiv, biorxiv, medrxiv, SSRN, DOI) mentioned in the briefing
- You want to prepare these papers for addition to a Zotero reference library

## Steps

1. **Locate the most recent briefing file**
   ```bash
   ls -t /tmp/ai_briefing_*.md /home/agent-blue/ai_briefing_*.md 2>/dev/null | head -1
   ```
   Alternative using find:
   ```bash
   find /tmp /home/agent-blue -name "ai_briefing_*.md" -type f -printf '%T@ %p\\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-
   ```

2. **Extract URLs from the briefing**
   ```bash
   grep -oE 'https?://[^[:space:]]+' "$LATEST_FILE"
   ```

3. **Clean trailing punctuation from URLs**
   ```bash
   # Remove common trailing punctuation that is not part of URLs
   sed 's/[.,:;!?\"'\''\)\]\}+$//g'
   ```

4. **Filter for academic publication links**
   ```bash
   grep -E 'arxiv\.org|biorxiv\.org|medrxiv\.org|ssrn\.com|doi\.org'
   ```

5. **Remove duplicates and sort**
   ```bash
   sort -u
   ```

6. **Save filtered links to the tracking file**
   ```bash
   mkdir -p /home/agent-blue/.hermes
   echo "$FILTERED_LINKS" > /home/agent-blue/.hermes/arxiv_to_check.txt
   ```

7. **Run the processing script (if available)**
   ```bash
   if [ -f "/home/agent-blue/file_papers_from_briefing.py" ]; then
       python3 "/home/agent-blue/file_papers_from_briefing.py"
   else
       echo "Warning: file_papers_from_briefing.py not found. Links prepared for manual processing."
   fi
   ```

8. **Output summary**
   Report the number of links found and any issues encountered.

## Example Complete Script

```bash
#!/bin/bash
set -e

# Step 1: Find the most recent briefing file
latest_file=$(ls -t /tmp/ai_briefing_*.md /home/agent-blue/ai_briefing_*.md 2>/dev/null | head -1)

if [ -z "$latest_file" ]; then
    echo "No briefing file found."
    exit 0
fi

echo "Found briefing file: $latest_file"

# Step 2: Extract URLs and clean trailing punctuation
urls=$(grep -oE 'https?://[^[:space:]]+' "$latest_file")
cleaned=$(echo "$urls" | sed 's/[.,:;!?\"'\''\)\]\}+$//g')

# Step 3: Filter for Arxiv, biorxiv, medrxiv, ssrn, and DOI
filtered=$(echo "$cleaned" | grep -E 'arxiv\.org|biorxiv\.org|medrxiv\.org|ssrn\.com|doi\.org' | sort -u)

# Step 4: Write to file
output_file="/home/agent-blue/.hermes/arxiv_to_check.txt"
mkdir -p "$(dirname "$output_file")"
echo "$filtered" > "$output_file"

count=$(echo "$filtered" | grep -c .)
echo "Found $count Arxiv/DOI links in the briefing."

# Step 5: Run the script and capture output
script_path="/home/agent-blue/file_papers_from_briefing.py"
if [ -f "$script_path" ]; then
    echo "Running file_papers_from_briefing.py..."
    script_output=$(python3 "$script_path" 2>&1)
    script_exit=$?
    echo "Script output:"
    echo "$script_output"
    if [ $script_exit -ne 0 ]; then
        echo "Script exited with code $script_exit"
    fi
else
    echo "Warning: file_papers_from_briefing.py not found in /home/agent-blue"
fi
```

## Pitfalls

- **URL extraction can include trailing punctuation**: Always clean URLs after extraction to remove trailing periods, commas, quotes, etc. that are not part of the actual URL.
- **The briefing file may not exist**: Always check if the file was found before proceeding.
- **The processing script may not exist**: Handle the case where `file_papers_from_briefing.py` is missing gracefully.
- **Duplicate URLs**: Use `sort -u` to eliminate duplicate links that may appear multiple times in the briefing.
- **Empty results**: It's normal to find 0 links in some briefings - don't treat this as an error.

## Verification

After running this skill, verify that:
- `/home/agent-blue/.hermes/arxiv_to_check.txt` exists and contains the expected URLs
- Each line in the file is a valid URL matching one of the target domains
- The script executed successfully (or gave an appropriate warning if missing)

## References

See `references/briefing-processing-details.md` for additional details about URL patterns and edge cases encountered from actual processing sessions.