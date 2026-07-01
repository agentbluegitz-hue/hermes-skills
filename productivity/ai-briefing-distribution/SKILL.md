---
name: ai-briefing-distribution
description: "Use when generating AI briefings that need to be distributed via Telegram rather than left on disk."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [briefing, automation, telegram, distribution]
    related_skills: [hermes-file-operations, plan]
---

# AI Briefing Distribution Skill

## Overview

This skill ensures AI-generated briefings are properly distributed via Telegram rather than left on disk files, addressing the common issue where briefing files are generated but not delivered to the user.

## When to Use

- When setting up automated AI briefing systems
- When creating cron jobs that generate briefing files
- When you need to ensure briefing content reaches the user via Telegram
- When updating existing briefing automation to improve delivery

## Step-by-Step Process

### 1. Generate Briefing Content
Follow your normal briefing generation process (web search, Arxiv search, etc.)

### 2. Save to Temporary Location
Save the briefing to a temporary file (e.g., `/tmp/ai_briefing_[date].md`)

### 3. Distribute via Telegram
In your response, include: `MEDIA:/tmp/ai_briefing_[date].md`

### 4. Clean Up Temporary Files (Optional)
Optionally remove temporary files after distribution if they contain sensitive information

### 5. Update Tracking Files
Update any seen/tracking files to avoid duplicate content in future briefings

## Correct File Handling Patterns

### Reading Tracking Files
```python
# Correctly read seen files (handle LINE|CONTENT format)
result = read_file(path=SEEN_FILE)
seen = set()
if result['content'].strip():
    for line in result['content'].split('\\n'):
        if line and '|' in line:
            _, content = line.split('|', 1)
            seen.add(content.strip())
```

### Writing Tracking Files
```python
# Write clean content (no line numbers)
with open(SEEN_FILE, 'w') as f:
    for item in sorted(seen):
        f.write(item + '\\n')
```

## Telegram Distribution

To send a file via Telegram in Hermes Agent:
- Include `MEDIA:/absolute/path/to/file` in your response
- The system automatically handles the file delivery
- Supported formats: images (.png, .jpg, .webp), audio (.ogg), videos (.mp4)
- For documents like Markdown, they will be sent as readable files

## Example Cron Job Update

When updating an AI briefing cron job:
1. Add step to save briefing to `/tmp/ai_briefing_[current_date].md`
2. Add step to send via Telegram (by including MEDIA: path in response)
3. Keep existing steps for updating seen files
4. Remove any steps that leave briefing files in permanent storage

## Verification Checklist

- [ ] Briefing content is generated correctly
- [ ] Briefing is saved to temporary location
- [ ] MEDIA: path is included in final response
- [ ] User receives file via Telegram
- [ ] Tracking files are updated correctly
- [ ] No briefing files left in permanent storage locations
- [ ] Temporary files cleaned up if needed

## Common Pitfalls

- Forgetting to include MEDIA: path in response (file generated but not sent)
- Using read_file output directly in write_file (causes file-mutation verifier errors)
- Leaving briefing files in /home/agent-blue/.hermes/ or other permanent locations
- Not properly parsing read_file output when updating tracking files
- Sending sensitive information in briefings without considering privacy

## Related Tools

- `read_file` - Returns LINE|CONTENT format requiring parsing
- `write_file` - Expects raw content only
- `web_search` - For gathering briefing content
- `web_extract` - For extracting article content
- `execute_code` - For complex briefing generation logic

## Example: AI Briefing Cron Job

From the AI Daily Briefing cron job (Job ID: 08db831129d5):

1. Read seen file with proper parsing
2. Search for news and Arxiv papers
3. Generate briefing markdown
4. Save to `/tmp/ai_briefing_[current_date].md`
5. Update seen file with new URLs (clean format)
6. **Include** `MEDIA:/tmp/ai_briefing_[current_date].md` in response
7. Output confirmation statistics

This ensures the briefing is delivered to the user via Telegram rather than left on disk.