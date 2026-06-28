---
name: hermes-file-operations
description: "Patterns for safe file read-modify-write workflows in Hermes Agent"
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [files, automation, workflow, patterns]
    related_skills: [systematic-debugging, plan]
---

# Hermes File Operations Patterns

## Overview

When working with files in Hermes Agent, special care must be taken to avoid the file-mutation verifier blocking writes. This skill documents the correct patterns for file read-modify-write cycles.

## The Core Issue

Hermes Agent's `read_file` tool returns content formatted for display in the chat interface, not raw file bytes. This format includes line-number prefixes:

```
1|https://example.com
2|https://test.com
3|https://another.com
```

If this display-formatted string is passed directly to `write_file`, the file-mutation verifier will block the write to prevent accidentally writing chat-display artifacts (like "|" prefixes and line numbers) into actual files.

## Correct File Round-Trip Pattern

To safely read-modify-write files in Hermes, follow this pattern:

### 1. Read File and Extract REAL Content

```python
from hermes_tools import read_file, write_file

# Read file
result = read_file(path="/path/to/file.txt")

# Parse the "LINE|CONTENT" format to get just the content lines
lines = []
for line in result['content'].split('\n'):
    if line and '|' in line:
        _, content = line.split('|', 1)  # Split on first '|'
        lines.append(content)
actual_content = '\n'.join(lines)
```

### 2. Process the Actual Content

```python
# Example: add new items to a list
new_lines = actual_content.split('\n') if actual_content else []
new_lines.extend([new_item1, new_item2])  # Add your new items
updated_content = '\n'.join(new_lines)
```

### 3. Write BACK the Clean Content

```python
# Write pure content, ready for file storage
write_file(
    path="/path/to/file.txt",
    content=updated_content  # This is pure content, no line numbers
)
```

## Alternative: Using execute_code with Proper Parsing

When using `execute_code` for file operations:

```python
code = """
import os
from hermes_tools import read_file, write_file

SEEN_FILE = "/home/agent-blue/.hermes/ai_briefing_seen.txt"

# Read and extract real content
result = read_file(path=SEEN_FILE)
seen = set()
if result['content'].strip():
    for line in result['content'].split('\n'):
        if line and '|' in line:
            _, url = line.split('|', 1)
            seen.add(url.strip())

# Process (add new URLs)
new_urls = ["https://example1.com", "https://example2.com"]
seen.update(new_urls)

# Write clean content
with open(SEEN_FILE, 'w') as f:
    for url in seen:
        f.write(url + '\n')
"""

from hermes_tools import execute_code
result = execute_code(code=code)
```

## Common Patterns

### Tracking Seen Items (for deduplication)

Many automation workflows need to track which items have been processed to avoid duplicates:

```python
# Read seen items
result = read_file(path=SEEN_FILE)
seen = set()
if result['content'].strip():
    for line in result['content'].split('\n'):
        if line and '|' in line:
            _, item = line.split('|', 1)
            seen.add(item.strip())

# Process new items
new_items = get_new_items()  # Your logic here
seen.update(new_items)

# Write back clean list
with open(SEEN_FILE, 'w') as f:
    for item in seen:
        f.write(item + '\n')
```

### Updating Configuration Files

When updating JSON, YAML, or other config files:

```python
# Read and parse
result = read_file(path=CONFIG_FILE)
config_content = ''
if result['content'].strip():
    for line in result['content'].split('\n'):
        if line and '|' in line:
            _, content = line.split('|', 1)
            config_content += content + '\n'

# Parse as JSON/YAML/etc
import json
config = json.loads(config_content) if config_content.strip() else {}

# Modify
config['new_key'] = 'new_value'

# Write back
with open(CONFIG_FILE, 'w') as f:
    f.write(json.dumps(config, indent=2))
```

## Verification

After writing files, you can verify the content was written correctly:

```python
# Read back to verify
verify_result = read_file(path=FILE_PATH)
# Check that content doesn't contain line-number prefixes
if '|' in verify_result['content'] and not verify_result['content'].startswith('1|'):
    # Might indicate incorrect format - investigate
    pass
```

## Automation Integration

This pattern works seamlessly with cron jobs and other automation:

1. **Cron Jobs**: Use this pattern in your cron job scripts
2. **Background Processes**: Apply in long-running file processing workflows
3. **Delegation Tasks**: Subagents should use this pattern when modifying files

## Related Tools

- `read_file` - Reads file with line-number prefixes for display
- `write_file` - Expects raw content without formatting
- `patch` - Alternative for targeted file edits (uses fuzzy matching)
- `execute_code` - For complex file processing logic

## Error Prevention

This pattern prevents:
- File corruption from chat-display artifacts
- Silent failures where files appear updated but contain garbage
- The "File-mutation verifier: 1 file(s) were NOT modified" warning

## Best Practices

1. **Always parse** `read_file` output before processing
2. **Never assume** file content is ready for direct reuse after `read_file`
3. **Write pure content** - no extra formatting, line numbers, or prefixes
4. **Verify critical writes** by reading back and checking format
5. **Use temporary variables** to keep display-format and raw-content separate

## Example: AI Briefing Seen File Update

```python
# Correct pattern used in AI briefing automation
from hermes_tools import read_file, write_file, web_search

SEEN_FILE = "/home/agent-blue/.hermes/ai_briefing_seen.txt"

# 1. Read and extract real URLs
result = read_file(path=SEEN_FILE)
seen = set()
if result['content'].strip():
    for line in result['content'].split('\n'):
        if line and '|' in line:
            _, url = line.split('|', 1)
            seen.add(url.strip())

# 2. Get new articles
results = web_search(query='AI news', limit=20)
items = results.get('data', {}).get('web', [])
new_items = []
for it in items:
    url = it.get('url')
    if url and url not in seen:
        new_items.append(it)

# 3. Take up to 6 new items
selected = new_items[:6]

# 4. Generate briefing (output to user)
# ... briefing generation logic ...

# 5. Update seen file with NEW URLs only
new_urls = [it.get('url') for it in selected if it.get('url')]
seen.update(new_urls)

# 6. Write CLEAN content (URLs only, one per line)
with open(SEEN_FILE, 'w') as f:
    for url in seen:
        f.write(url + '\n')
```

This ensures the seen file contains only clean URLs, ready for the next read cycle.