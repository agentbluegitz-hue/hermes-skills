---
name: zotero-library-organizer
description: "Analyze and organize personal Zotero libraries using content-based topic modeling and automated filing"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [zotero, library, organization, research, academic]
    related_skills: [hermes-academic-research, hermes-agent, zotero-integration]
---
# Zotero Library Organizer

This skill provides methodologies for analyzing personal Zotero libraries to discover topical structure and automate organization into meaningful collections. It addresses the common challenge of large, unfiled research libraries where users know they have valuable content but struggle to find and organize it.

## Why This Matters

Personal research libraries (like Zotero) often accumulate thousands of items over time, with significant portions remaining unfiled or poorly organized. This creates inefficiencies in research workflows where users cannot easily discover relevant materials for new projects, literature reviews, or training material development.

The Zotero Library Organizer skill helps users:
- Discover hidden topical structure in their libraries
- Identify significant research domains they may have forgotten about
- Automatically organize unfiled items into meaningful collections
- Create a browsable knowledge base that enhances research productivity
- Prepare libraries for use with AI research assistants

## Core Workflow

### Phase 1: Library Assessment
```markdown
## Library Assessment Process

1. **Connection Verification**
   - Test API access to Zotero library (direct pyzotero or MCP server)
   - Verify credentials and permissions
   - Check total item count and collection structure

2. **Sampling Strategy**
   - Determine appropriate sample size for initial analysis
   - Consider library size when choosing sample (e.g., 100-500 items for libraries >1000 items)
   - Ensure sample includes various item types (journal articles, attachments, notes, etc.)

3. **Initial Content Analysis**
   - Extract titles, abstracts, tags, and item types
   - Perform basic topic modeling (keyword frequency analysis)
   - Identify dominant themes and potential gaps
   - Note format distribution (what percentage are substantive vs. annotations/attachments)
```

### Phase 2: Targeted Domain Discovery
```markdown
## Targeted Domain Discovery

When initial analysis suggests missing domains or when users suspect specific content exists:

1. **Hypothesis Formation**
   - Based on user statements ("I know I have papers about X")
   - Based on collection names that suggest domains
   - Based on known research interests

2. **Domain-Specific Search Terms**
   - Create targeted search queries for suspected domains
   - Examples:
     * Plant biology: ['plant phylogeny', 'evolution', 'botany', 'clade', 'polyploidy']
     * Machine learning: ['neural network', 'deep learning', 'transformer', 'CNN', 'RNN']
     * Medical imaging: ['radiology', 'MRI', 'CT scan', 'diagnosis', 'pathology']
     * Education: ['pedagogy', 'curriculum', 'assessment', 'learning outcomes']

3. **Broad Search Execution**
   - Execute searches for each term
   - Deduplicate results across search terms
   - Analyze result types and quality
   - Estimate domain size in library

4. **Result Validation**
   - Examine actual titles and content of search results
   - Verify relevance to suspected domain
   - Check for false positives and refine search terms
```

### Phase 3: Organization Planning
```markdown
## Organization Planning Process

1. **Topic Definition**
   - Based on discovered domains and user preferences
   - Create clear definitions for each proposed collection
   - Establish inclusion/exclusion criteria
   - Consider hierarchical organization (broad topics with subcollections)

2. **Item Assignment Strategy**
   - Develop rules for assigning items to topics
   - Options:
     * Keyword matching (title, abstract, tags)
     * Machine learning classification (if sufficient training data)
     * Hybrid approach (keywords + ML)
     * Manual review for borderline cases

3. **Collection Planning**
   - Decide which existing collections to keep, rename, or merge
   - Plan new collections to create
   - Estimate item distribution across collections
   - Identify items that may fit multiple collections (needing tie-breaker rules)
```

### Phase 4: Implementation & Verification
```markdown
## Implementation Process

1. **Preview Generation**
   - Create detailed plan showing:
     * Which items would go to each collection
     * Sample items for verification
     * Conflicts or ambiguous assignments
     * Estimates for full library based on sample

2. **User Review & Approval**
   - Present plan to user for feedback
   - Allow adjustments to topics, keywords, or assignments
   - Incorporate user expertise and domain knowledge
   - Get final approval before proceeding

3. **Batch Processing**
   - Process library in batches to avoid API limits
   - Create missing collections in Zotero
   - File items according to plan
   - Maintain detailed logs for potential rollback

4. **Verification & Reporting**
   - Post-implementation audit
   - Before/after statistics
   - Sample of newly organized library
   - Suggestions for next steps (further refinement, subcollection creation)
```

## Key Lessons Learned

## Key Lessons Learned

### Lesson 1: Small Samples Can Miss Significant Content
- Initial topic modeling from small samples (e.g., 100 items) may miss domain-specific content
- Specialized terminology may not surface in top keyword lists from limited samples
- Always validate with targeted searches for suspected domains
- **Session Reference**: See `references/zotero-api-authentication-lessons.md` for detailed authentication workflow and MCP server troubleshooting discovered during session with Matt
- **Session Reference**: See `references/optimized-batch-processing-lessons.md` for lessons learned about eliminating script timeouts through optimized batch processing strategies

### Lesson 2: Format Matters for Content Discovery
- Attachments often have generic titles ("Full Text PDF", "Snapshot")
- Annotations frequently lack meaningful titles
- Substantive content (journal articles, books, preprints) is more discoverable via title/abstract analysis
- Different strategies needed for different item types

### Lesson 3: Iterative Refinement Beats One-Shot Analysis
- Start broad, then refine based on results
- Use deduplication across multiple search terms
- Check actual content, not just metadata
- Verify with collection membership when possible

### Lesson 4: User Domain Knowledge is Essential
- Users know their research interests better than any algorithm
- Incorporate user feedback at every stage
- Allow users to override algorithmic suggestions
- Use user collections as ground truth for validation

### Lesson 5: Enhanced Classification Improves Domain Discovery
- Generic keyword lists may miss specialized domain content
- Adding domain-specific terminology (e.g., plant biology terms like "clade", "polyploidy", "phylogenetic") significantly improves classification accuracy
- Consider creating enhanced keyword lists for known research domains
- Test classification on sample items before full deployment
- **Iterative Enhancement**: Start with broad classification, then refine with domain-specific terms when initial results suggest missing content (as discovered when plant biology content was missed in initial sampling but found via targeted search)

### Lesson 6: Batch Processing Enables Efficient Library Organization
- Processing large libraries in batches prevents API overload and allows progress tracking
- Skip non-substantive items (annotations, attachments) during initial organization passes for efficiency
- Tag preprint items during processing to mark them for easy identification
- Handle version conflicts gracefully by retrieving fresh item data when needed
- Maintain detailed logs for verification and potential rollback
- **Enhanced Technique**: Use small batch sizes (10-20 items) with strategic delays (1-2 seconds) to prevent API timeouts, as detailed in `references/optimized-batch-processing-lessons.md`

### Lesson 7: Correct API Usage for Collection Operations
- The `zot.addto_collection()` method requires the full item dictionary (as returned by `zot.item()` or `zot.items()`), not just the item key
## Key Lessons Learned

## Key Lessons Learned

### Lesson 8: Automated Arxiv Paper Filing from AI Briefings
- AI news briefings often contain links to recent Arxiv papers relevant to specific domains
- Implement automated detection of Arxiv links in briefing content
- File these papers directly into Zotero with appropriate tags
- **Workflow**: 
  1. Generate daily AI briefing with Arxiv paper detection
  2. Extract Arxiv IDs/URLs from briefing
  3. For each paper: get metadata, prepare Zotero item, file with relevant tags
  4. Avoid duplicates by checking existing items
  5. Use small batches and appropriate delays to prevent API overload
- **Reference**: See `references/arxiv-paper-filing-lessons.md` for detailed workflow and implementation discovered during session with Matt
  2. Use direct API approach (requires credentials, works when desktop open)
  3. Use read-only copy of database
  ## Key Lessons Learned

  ### Lesson 9: Duplicate Merging Preserves Research Context
  - Duplicate items in Zotero libraries often contain complementary notes, tags, and metadata
  - Merging duplicates while combining notes preserves valuable research context
  - The merging process:
    1. Identifies duplicates using multiple strategies (Arxiv ID, normalized title)
    2. Selects the item with the richest note as the "keeper"
    3. Combines notes from all duplicates with clear separators
    4. Updates the keeper with the combined note
    5. Safely deletes duplicate items
  - **Session Reference**: See `scripts/merge_zotero_duplicates.py` for the implementation that resolved duplicate management issues during the session with Matt

  ### Lesson 10: RAG Systems Enable Semantic Library Search
  - Traditional keyword search misses semantic relationships (e.g., "AI agent" vs "LLM assistant")
  - Retrieval-Augmented Generation (RAG) transforms libraries into searchable knowledge bases
  - **Implementation**: 
    * Extract text from title+abstract+notes+tags for each item
    * Create embeddings using sentence-transformers (all-MiniLM-L6-v2)
    * Build FAISS index for millisecond-scale similarity search
    * Query with semantic understanding rather than exact keyword matching
  - **Benefits**: 
    * Finds conceptually related items even with different terminology
    * Provides relevance scoring (0-1) for result ranking
    * Enables natural language questioning of your library
    * Complements traditional organization with discovery capabilities
  - **Session Reference**: See `references/rag-system-lessons.md` for detailed implementation and lessons learned from building a RAG system for Matt's Zotero library
  - **Storage Efficient**: ~20-30 MB for a ~5,000 item library
  - **Performance**: <1 second query times after index loading

### Issue: Poor Search Results
- **Cause**: Overly broad or narrow search terms
- **Solutions**:
  1. Start with broad terms, then add specificity
  2. Use field-specific searches when available (title vs. abstract vs. tags)
  3. Consider synonyms and related terms
  4. Examine result quality and adjust accordingly

### Issue: Performance Problems with Large Libraries
- **Cause**: API limits, processing time
- **Solutions**:
  1. Batch processing (e.g., 100 items at a time)
  2. Use caching for repeated queries
  3. Focus on substantive items first
  4. Consider exporting library for local analysis if needed

### Issue: Ambiguous Item Assignment
- **Cause**: Items fitting multiple topics
- **Solutions**:
  1. Create tie-breaker rules (e.g., prefer newer items, prefer specific over general)
  2. Allow dual filing when appropriate (tags can indicate multiple topics)
  3. Create "interdisciplinary" collections for borderline cases
  4. Manual review for high-value ambiguous items

## Best Practices

### For Initial Analysis
- Always start with a connection test
- Use multiple approaches: sampling + targeted searches
- Check existing collections as ground truth
- Consider library size when choosing methods
- **User Preference**: Provide analysis and plans, then request confirmation before acting (proactive but permission-based)

### For Topic Definition
- Create mutually exclusive and collectively exhaustive topics when possible
- Use clear, descriptive names that users will understand
- Provide examples of what belongs in each topic
- Consider both broad fields and specific subtopics
- **User Preference**: Use markdown formatting and code blocks for clarity

### For Implementation
- Process in batches with progress reporting
- Maintain detailed logs for rollback capability
- Verify after each batch if possible
- Provide clear before/after comparisons
- **User Preference**: Provide regular progress updates during long-running processes
- **Optimization**: Use small batch sizes (10-20 items) with appropriate delays (1-2 seconds) to prevent API timeouts
- **Error Handling**: Handle version conflicts gracefully by retrieving fresh item data when needed
- **User Preference**: Be transparent about limitations and errors rather than pretending they don't exist

### For User Collaboration
- Present plans in clear, understandable formats
- Use visualizations when helpful (charts, tables)
- Explain reasoning behind recommendations
- Be ready to adapt based on user expertise
- **Security Note**: API keys should be stored in secure credential stores (like ~/.hermes/.env for Hermes) rather than exposed in logs or memory
- **User Preference**: Be transparent about limitations and errors rather than pretending they don't exist
- **Security Note**: API keys should be stored in secure credential stores (like ~/.hermes/.env for Hermes) rather than exposed in logs or memory

## Example: Plant Biology Discovery (from session with Matt)

During analysis of Matt's Zotero library (5,292 items):
- Initial sample (100 items) via topic modeling suggested limited plant content
- Targeted search using plant evolution terms revealed:
  - 858 unique items (~16.2% of library) matching plant/botany/evolution terms
  - Core phylogenetics work: APG classifications, plastid phylogenomics
  - Multiple plant groups: bryophytes, gymnosperms, angiosperms
  - Various methodologies: DNA barcoding, phylogenomics, molecular dating
- **Reason for initial miss**: Many items were attachments with generic titles, annotations without meaningful titles, and specialized terminology not surfacing in initial keyword analysis

This led to adding "Plant Biology & Evolution" and "Phylogenetics & Systematics" to the organization plan.

## Integration with Research Workflows

Once organized, the library can power:
- **AI Research Assistants**: Agents that can search, summarize, and synthesize from your library
- **Literature Review Automation**: Generate reviews on specific topics from your actual collections
- **Training Material Development**: Create exercises and examples from your research
- **Project Support**: Quickly find background literature for new projects
- **Knowledge Discovery**: See connections between related works in your library

## Next Steps for Enhancement

1. **Machine Learning Enhancement**: Train classifiers on user-provided examples for better accuracy
2. **Hierarchical Organization**: Create broad topics with subcollections for granularity
3. **Temporal Analysis**: Track how research interests evolve over time
4. **Collaboration Features**: Enable sharing organizational schemes with colleagues
5. **Maintenance Mode**: Set up periodic checks to keep new items organized
6. **Optimized Processing**: Implement the batch processing strategies from `references/optimized-batch-processing-lessons.md` for all large-scale library operations
7. **User Preference Integration**: Formalize the proactive-but-permission-based approach and regular progress reporting as core principles of the skill
8. **Arxiv Integration**: Implement automated workflows to file new Arxiv papers from AI briefings into relevant Zotero collections (see `references/arxiv-paper-filing-lessons.md` as starting point)
9. **RAG System Enhancement**: Develop the semantic search capabilities further with hybrid search, metadata enrichment, and incremental updates (see `references/rag-system-lessons.md` as foundation)