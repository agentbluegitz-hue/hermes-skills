# Quota Optimization Lessons for Zotero Library

## Overview
This document captures lessons learned from optimizing Zotero library sync quota usage, specifically targeting the reduction of online storage consumption while maintaining library functionality.

## Key Discoveries from Session

### 1. Trash Items Consume Significant Quota
- **Discovery**: 100 items in trash were consuming measurable quota space
- **Impact**: Emptying trash provided immediate quota reduction
- **Lesson**: Regularly emptying trash is a high-impact, low-effort optimization
- **Action**: Zotero → Right-click Trash → "Empty Trash"

### 2. Tag Proliferation Increases Metadata Overhead
- **Discovery**: Analysis showed 175 tags used only 1-2 times in the library
- **Examples**: Highly specific tags like "Coalescence", "Cytonuclear discordance", "Hybridization" each used once
- **Impact**: Each tag adds metadata overhead to the sync quota
- **Lesson**: Periodic tag cleanup reduces quota usage without losing meaningful organization
- **Action**: Review and delete tags used 2 times or less (except for intentional sparse tags)

### 3. Annotations Can Contain Unexpected Bloat
- **Discovery**: 18 annotation items found in sample analysis
- **Potential Issues**: 
  - Very long highlighted selections stored in annotations
  - Extensive annotation notes
  - Duplicate annotations on same item
- **Lesson**: Annotations should be reviewed periodically for bloat
- **Action**: Search `itemType:annotation` and review for excessive content

### 4. Database Maintenance Affects Local Efficiency
- **Discovery**: Local zotero.sqlite was ~125MB with multiple backup files
- **Lesson**: While database vacuuming primarily helps local performance, it contributes to overall library health
- **Action**: Periodic VACUUM operations (with Zotero closed):
  ```bash
  sqlite3 zotero.sqlite "VACUUM;"
  ```

### 5. Understanding What Consumes Sync Quota
With file syncing disabled, quota stores:
- Item metadata (titles, creators, dates, DOIs, URLs, etc.)
- Notes and annotations (text content)
- Tags and collections (organizational structure)
- Item relations (connections between items)
- **Not stored**: File attachments (when file syncing is off)

### 6. Verification and Monitoring Process
- **Wait 10-15 minutes** after changes for sync to update
- **Check quota**: https://www.zotero.org/settings/storage
- **API verification**: https://api.zotero.org/users/{userID}/storage (requires auth)
- **Trend tracking**: Monitor quota changes over time to identify optimization effectiveness

### 7. Batch-Aware Optimization Strategies
When implementing quota reduction:
- Process library in small batches (10-20 items) to prevent API timeouts
- Include progress reporting for long-running operations
- Maintain detailed logs for verification and potential rollback
- Handle version conflicts by retrieving fresh item data when needed

### 8. When Standard Optimization Isn't Enough
If quota remains above limit after standard optimizations:
- Consider creating a secondary Zotero library for less-active items
- Sync only primary working library, keep archives/reference local-only
- Evaluate whether specific collections can be excluded from sync
- Review attachment usage patterns even with file syncing off (local copies still exist)

## Practical Workflow for Quota Reduction

```markdown
## Zotero Quota Optimization Process

### Phase 1: Immediate High-Impact Actions
1. Empty trash (check item count first)
2. Wait 5-10 minutes, check quota change
3. If still over limit, proceed to Phase 2

### Phase 2: Metadata Optimization
1. Review tags used 1-2 times, consider deletion
2. Check annotations for bloat (search itemType:annotation)
3. Wait 10-15 minutes, check quota change
4. If still over limit, proceed to Phase 3

### Phase 3: Database and Advanced Optimization
1. Perform database VACUUM (Zotero closed)
2. Consider library splitting if appropriate
3. Wait for sync, verify quota
```

## Session-Specific Context
- **Library Size**: ~5,292 items (as referenced in user profile)
- **Initial State**: 380MB attachment storage + database = 770MB total local
- **After File Sync Off**: 293MB quota usage (primarily metadata)
- **Target**: Further reduction below 293MB through metadata optimization
- **Key Insight**: Even with file syncing off, metadata optimization can yield meaningful quota savings

## References to Other Lessons
- See `references/optimized-batch-processing-lessons.md` for batch processing strategies
- See `references/rag-system-lessons.md` for semantic search approaches that complement organization
- See `references/arxiv-paper-filing-lessons.md` for automated paper filing workflows