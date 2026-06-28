# Zotero API Authentication Lessons from Session

## Key Discoveries

1. **API Key Security**: The user's Zotero API key is intentionally NOT stored in accessible memory or environment variables for security reasons. The memory only notes that an API key was "provided" without storing the actual value.

2. **Memory Structure**: User information is stored in `/home/agent-blue/.hermes/memories/USER.md` (not `/home/agent-blue/.hermes/memory/user.md` as initially assumed). This file uses `§` as section separators.

3. **MCP Server Configuration**: The Zotero MCP server configuration is located at `/home/agent-blue/.config/zotero-mcp/config.json` and contains semantic search settings but does NOT store API credentials for security.

4. **Dependency Issues**: The Zotero MCP server has dependency problems with `pydantic_core` missing, preventing normal operation.

5. **Alternative Access Methods**: 
   - Direct pyzotero API access works when credentials are available
   - MCP server can be made to work with proper PYTHONPATH setup
   - Local SQLite database access is possible when Zotero desktop is closed (to unlock the database)

## Technical Workflow Discovered

### Successful pyzotero Import Path
```python
import sys
sys.path.insert(0, '/home/agent-blue/.local/share/uv/tools/zotero-mcp-server/lib/python3.13/site-packages')
from pyzotero import zotero
```

### MCP Server Usage Pattern
```bash
PYTHONPATH="/home/agent-blue/.local/share/uv/tools/zotero-mcp-server/lib/python3.13/site-packages" \
/home/agent-blue/.local/share/uv/tools/zotero-mcp-server/bin/zotero-mcp setup --help
```

### Database Location and Status
- Path: `/home/agent-blue/Zotero/zotero.sqlite`
- Size: ~131MB
- Status: Locked when Zotero desktop is running

## Classification Enhancement Technique

When initial topic modeling misses suspected content:
1. Start with broad sampling (100-500 items)
2. Perform keyword frequency analysis
3. When user indicates missing domains (e.g., "I know I have plant biology papers")
4. Execute targeted searches with domain-specific terminology
5. Deduplicate results across search terms
6. Enhance classification keywords with discovered effective terms
7. Validate with sample items before full deployment

## Plant Biology Keywords Discovered
Through targeted search, these terms proved effective for finding plant biology content:
- Plant groups: bryophytes, pteridophyta, gymnosperms, angiosperms, monocot, dicot
- Specific species: Arabidopsis, rice, maize, wheat, soybean, tomato
- Evolutionary concepts: speciation, divergence, convergence, radiation, diversification
- Methodological: phylogeny, phylogenetic, cladistics, cladogram, molecular clock
- Taxonomic: taxon, taxonomy, classification, nomenclature, systematics

## Session-Specific Workflow Adjustments

Based on the interaction pattern:
1. **Proactive but Permission-Based**: Provide analysis and plans, then request confirmation before acting
2. **Progress Reporting**: Provide regular updates during long-running processes
3. **Error Transparency**: Be open about limitations (like missing API key) rather than pretending
4. **Iterative Refinement**: Start with broad approaches, then enhance based on discovered gaps
5. **Evidence-Based Planning**: Show actual data samples and counts to justify recommendations
