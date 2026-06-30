# RAG System for Zotero Libraries: Lessons Learned

## Overview
During this session, I built a complete Retrieval-Augmented Generation (RAG) system for querying Matt's Zotero library. This system transforms the library into a searchable knowledge base that understands semantic meaning rather than just keywords.

## System Architecture
```
Zotero Library → [API Fetch] → [Text Extraction] → [Embedding Model] → [FAISS Index]
                                   ↑                                          ↓
                          [User Question] ← [Query Embedding] ← [Similarity Search] ← [Results]
```

## Key Components

### 1. Text Extraction Strategy
For each Zotero item, we combine:
- **Title** (primary identifier)
- **Abstract** (core content)
- **Note** (user's personal annotations)
- **Tags** (user-generated categorization)

This approach maximizes semantic coverage per item while respecting the user's own organization.

### 2. Embedding Model Selection
Used `sentence-transformers/all-MiniLM-L6-v2`:
- 384-dimensional vectors
- Excellent balance of speed/quality for general text
- Open-source and CPU-efficient
- Produces meaningful semantic representations where similar concepts have similar vectors

### 3. FAISS Index Implementation
- Index type: `IndexFlatIP` (Inner Product) with L2-normalized vectors → **Cosine Similarity**
- Enables millisecond-scale similarity search even for large libraries
- Storage efficient: ~1.5KB per item for vectors alone

### 4. Batch Processing for Large Libraries
To handle libraries of 5,000+ items without timeouts:
- **Fetch batches**: 200 items/request from Zotero API
- **Encode batches**: 32 items for embedding generation
- **Strategic delays**: 50ms between API batches to prevent rate limiting
- **Progress tracking**: Regular updates during long operations

## Storage Characteristics
Based on testing with Matt's library (~5,292 items):
- **Vector storage**: ~8 MB (384 dimensions × 4 bytes × 5,292 items)
- **Metadata storage**: ~15-20 MB (item data, extracted text, metadata)
- **Total estimate**: **20-30 MB** for complete library index
- **Per-item cost**: ~4-6 KB including overhead

This is very lightweight - equivalent to 4-10 photos or 4-8 songs.

## Implementation Patterns

### Resilient API Handling
```python
# Fetch with retry and backoff
def fetch_with_retry(zot, params, max_retries=3):
    for attempt in range(max_retries):
        try:
            return zot.items(**params)
            break
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Memory-Efficient Processing
```python
# Process in batches to avoid memory issues
def process_in_batches(items, batch_size=100):
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]
```

### Incremental Index Updates
For libraries that change frequently:
1. Save timestamp of last index build
2. On update, fetch items modified since last build
3. Add new vectors to existing index (requires index type that supports additions)
4. Or rebuild entirely if changes are extensive

## Integration with Organization Workflows
The RAG system complements traditional library organization:

1. **Discovery Tool**: Find items on specific topics even if misfiled
2. **Validation Aid**: Check if proposed collections make semantic sense
3. **Gap Identification**: Discover missing areas in your collection
4. **Recommendation Engine**: Suggest related items when filing new papers

## Performance Characteristics
- **Index build time**: ~5-10 minutes for 5,000 items (mostly model loading and API fetching)
- **Query time**: <1 second after index is loaded
- **Memory usage**: ~100-200 MB during build, ~50 MB during querying
- **Scalability**: Linear scaling with library size

## Lessons Specific to Matt's Setup
1. **MCP Configuration Works Well**: Using the Zotero MCP server credentials provided reliable API access
2. **Virtual Environment Essential**: Created `zotero_venv` with `uv` to manage dependencies cleanly
3. **Batch Sizes Critical**: Initial attempts timed out until batch processing was optimized
4. **Model Caching Benefits**: Sentence transformer model cached after first load for faster subsequent queries
5. **Storage Location**: Using `/home/agent-blue/.hermes/rag_storage/` kept index files organized and backed up with skills

## Future Enhancements
1. **Incremental Updates**: Add new items without full rebuild
2. **Hybrid Search**: Combine vector search with keyword matching for best results
3. **Metadata Enrichment**: Extract additional fields like DOI, journal, citations
4. **Temporal Analysis**: Track how research interests evolve over time
5. **Multi-Language Support**: Handle non-English abstracts and titles effectively