---
name: zotero-integration
description: "Integrate with Zotero reference manager for academic research workflows"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, zotero, references, bibliography, academic]
    related_skills: [arxiv, llm-wiki, blogwatcher, ocr-and-documents]
---

# Zotero Integration

Work with your Zotero reference manager to enhance academic research workflows. This skill covers accessing your Zotero library, searching collections, extracting bibliographic data, and integrating with other research tools.

## Why This Matters

Zotero is a powerful reference manager that helps researchers collect, organize, cite, and share research sources. Integrating Zotero with AI agents enables:

- **Automated literature reviews**: Search and extract insights from your personal library
- **Citation management**: Generate formatted bibliographies and in-text citations
- **Research organization**: Tag, categorize, and relate items in your library
- **Knowledge synthesis**: Connect ideas across your collected sources
- **Training material creation**: Use your library as a source for educational content

## Prerequisites

1. **Zotero Installed**: You need Zotero desktop installed and running (or at least have your library data accessible)
2. **Python Dependencies**: `pyzotero` library for API access (may already be installed via MCP tools)
3. **Library Access**: Either:
   - Direct access to your Zotero SQLite database (`~/Zotero/zotero.sqlite`)
   - Zotero API credentials (User ID + API Key) for remote access

See `references/hermes-blue-zotero-setup.md` for session-specific details about Matt's Zotero configuration at UF Research Computing.

## Quick Start

### Option 1: Direct Database Access (No API Needed)
If you have access to your Zotero SQLite file:

```bash
# Check if your Zotero database is accessible
ls -la ~/Zotero/zotero.sqlite

# If accessible, you can query it directly with SQLite
sqlite3 ~/Zotero/zotero.sqlite "SELECT * FROM items LIMIT 5;"
```

### Option 2: API Access (Requires Credentials)
Get your credentials from Zotero:
1. Go to https://www.zotero.org/settings
2. Find your **User ID** under Feeds/API
3. Generate a **private key** (API key) if needed

Then use pyzotero:
```python
from pyzotero import zotero

# Initialize with your credentials
zot = zotero.Zotero(user_id='YOUR_USER_ID', library_type='user', api_key='YOUR_API_KEY')

# Get recent items
items = zot.items(limit=10)
for item in items:
    print(f"{item['data']['itemType']}: {item['data'].get('title', 'No title')}")
```

## Core Capabilities

### 1. Library Exploration
- Browse collections and subcollections
- View item types (journal articles, books, web pages, etc.)
- See tags and relationships between items
- Check attachment files (PDFs, supplements, etc.)

### 2. Search & Retrieval
- Search by title, author, keywords, or tags
- Filter by item type, date, or collection
- Search within notes and annotations
- Retrieve full metadata for items

### 3. Data Extraction
- Export bibliographic data in various formats (BibTeX, RIS, JSON)
- Extract abstracts, authors, publication details
- Get attachment information and file paths
- Access personal notes and tags

### 4. Integration Patterns
- Combine with arXiv search for literature discovery
- Use with note-taking systems (Obsidian, Notion) for knowledge management
- Feed into writing assistance for citation generation
- Create training examples from your research library

## Common Workflows

See `references/hermes-blue-zotero-setup.md` for session-specific details about Matt's Zotero configuration at UF Research Computing.

### Literature Review Assistance
```python
# 1. Search for papers on a topic
search_results = zot.items(q='machine learning education', limit=20)

# 2. Extract key information
papers = []
for item in search_results:
    data = item['data']
    papers.append({
        'title': data.get('title'),
        'authors': [creator.get('lastName') + ', ' + creator.get('firstName') 
                   for creator in data.get('creators', [])],
        'year': data.get('date', '')[:4] if data.get('date') else None,
        'abstract': data.get('abstractNote'),
        'tags': [tag.get('tag') for tag in data.get('tags', [])],
        'itemType': data.get('itemType')
    })

# 3. Analyze patterns (year distribution, common tags, etc.)
```

### Citation Generation
```python
# Get items for a specific collection or search
collection_items = zot.collection_items('COLLECTION_KEY')

# Generate BibTeX entries
bibtex_entries = []
for item in collection_items:
    # Use zotero utilities or custom formatting to create BibTeX
    pass  # Implementation depends on your needs
```

### Research Knowledge Mapping
```python
# Extract tags and relations to build a knowledge graph
tags = set()
relations = []

for item in zot.items():
    data = item['data']
    # Collect tags
    for tag in data.get('tags', []):
        tags.add(tag.get('tag'))
    
    # Look for relations (if using Zotero's relation feature)
    # This would require checking relation tables in the database
```

## Advanced Techniques

### Direct SQLite Access (When API Not Available)
If you can't use the API (e.g., database locked, no internet), you can query the SQLite database directly:

```sql
-- Find all journal articles from 2023-2024
SELECT itemID, itemTypeID FROM itemTypes WHERE typeName = 'journalArticle';
-- Then join with items table to get the actual items

-- Search items by title containing specific keywords
SELECT i.itemID, i.value 
FROM itemData i 
JOIN itemDataValues v ON i.valueID = v.valueID 
WHERE i.fieldID = (SELECT fieldID FROM itemFields WHERE fieldName = 'title') 
AND v.value LIKE '%machine learning%';

-- Get creators (authors) for items
SELECT i.itemID, v.value as author_name
FROM itemData i 
JOIN itemDataValues v ON i.valueID = v.valueID 
JOIN itemCreators ic ON i.itemID = ic.itemID 
JOIN creatorTypes ct ON ic.creatorTypeID = ct.creatorTypeID 
WHERE i.fieldID = (SELECT fieldID FROM itemFields WHERE fieldName = 'author') 
AND ct.creatorType = 'author';
```

### Working with Attachments
Zotero stores attachments (PDFs, etc.) in the `storage` folder:
- Location: `~/Zotero/storage/`
- Files are named with item keys (e.g., `ABCD1234.pdf`)
- You can link items to their attachments via the database

### Handling Groups vs Personal Library
- Personal library: `library_type='user'`
- Group libraries: `library_type='group'` with group ID instead of user ID

## Best Practices

### Performance
- Limit results when browsing large libraries (`limit=50` or similar)
- Use specific searches rather than retrieving all items
- Consider caching frequent queries if doing repeated analysis

### Data Quality
- Check for missing fields (some items may lack abstracts or authors)
- Handle different item types appropriately (book vs article vs webpage)
- Normalize date formats for consistent analysis

### Privacy & Security
- Your Zotero library contains potentially sensitive research data
- Be careful when sharing extracts or analyses that might reveal unpublished work
- Consider using local processing only for sensitive materials

## Integration with Other Hermes Skills

### With arXiv Search
1. Search arXiv for recent papers on your topic
2. Check if those papers are already in your Zotero library
3. Add new ones to Zotero for long-term tracking
4. Use your Zotero library as the primary source for literature review

### With Note-Taking Systems
- Export Zotero notes and annotations to Obsidian/Notion
- Create bidirectional links between your reference manager and knowledge base
- Use Zotero tags to structure your note-taking system

### For Training Material Development
- Extract examples of good/bad research practices from your library
- Create exercises around evaluating different study methodologies
- Generate reading lists for specific topics or methods
- Demonstrate citation management techniques

## Troubleshooting

### "Database is locked" Error
This means Zotero desktop is running and has the database open:
- Close Zotero desktop temporarily for direct access
- Or use the API approach instead (doesn't require direct DB access)
- Consider making a read-only copy of the database for analysis

### Missing pyzotero Library
Install it:
```bash
pip install pyzotero
# or if using uv:
uv pip install pyzotero
```

### Permission Issues
Ensure you have read access to:
- `~/Zotero/zotero.sqlite` (the database)
- `~/Zotero/storage/` (attachment files)
- `~/Zotero/` (the main directory)

### API Connection Problems
- Double-check your User ID and API Key
- Verify your internet connection (for API access)
- Check if Zotero sync is working properly in desktop client
- Try regenerating your API key if having persistent issues

## Example: Building a Research Training Module

Here's how you might use this skill to create training content:

```python
# 1. Explore your library for examples
research_methods = zot.items(q='mixed methods', limit=10)
case_studies = zot.items(q='case study', itemType='journalArticle')

# 2. Extract teaching examples
examples = []
for item in case_studies:
    data = item['data']
    if data.get('abstractNote'):
        examples.append({
            'citation': f"{data.get('creators', [{}])[0].get('lastName', 'Unknown')} et al. ({data.get('date', 'XXXX')[:4]})",
            'title': data.get('title'),
            'abstract': data.get('abstractNote')[:200] + '...',
            'methodology_indicators': ['case study' in data.get('abstractNote', '').lower()]
        })

# 3. Create training slides or handouts
# Use the examples to illustrate different research approaches
# Show how to evaluate methodology sections
# Demonstrate proper citation of case study research

# 4. Generate bibliography for training materials
# Export the examples in APA/MLA/Chicago format as needed
```

## Next Steps

1. **Verify your setup**: Check if you can access your Zotero library via either method
2. **Explore your collections**: See what research areas you have material on
3. **Try a focused search**: Look for papers on a specific topic you're teaching
4. **Build a simple extraction**: Pull titles, authors, and years for a subset of items
5. **Consider automation**: Think about how this could save time in your research workflow

This skill provides the foundation for using your Zotero library as a dynamic research assistant rather than just a static reference manager.