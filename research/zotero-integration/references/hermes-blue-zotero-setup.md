# Hermes Blue Zotero Setup (Session-specific)

This document captures the specific Zotero configuration discovered during the session with Hermes Blue (Matt from UF Research Computing).

## Environment Details
- **User**: Matt (Manager of Training Team, UF Information Technology, Research Computing)
- **Purpose**: Developing training on AI Agents
- **System**: Personal computer off-campus with access to NaviGator Toolkit (LLM gateway)
- **Zotero Installation**: Located via snap and local installation

## Zotero Setup Discovered

### Installation Paths
1. **Snap Installation**: `/home/agent-blue/snap/zotero-snap/`
   - Contains `.zotero` directory with Zotero binary
   - Data likely stored in `~/snap/zotero-snap/common/.zotero/`

2. **Local Installation**: `/home/agent-blue/Zotero/`
   - **Primary Data Location**: This appears to be the active Zotero library
   - Contains:
     - `zotero.sqlite` (125.1 MB) - Main database
     - `zotero.sqlite-journal` (103 KB) - SQLite journal file
     - `zotero.sqlite.bak` (40.2 MB) - Backup copy
     - `storage/` (12,660 items) - Attachment files (PDFs, etc.)
     - `translators/` (36,864 items) - Zotero translator scripts
     - `styles/` - Citation style files
     - `locate/` - Search indexing data

### Database Access Status
- **SQLite Database**: `/home/agent-blue/Zotero/zotero.sqlite`
- **Access Issue**: Database was reported as "locked" during session (likely because Zotero desktop was running)
- **Size**: 125.1 MB indicating substantial library
- **Tables Present**: items, itemData, itemDataValues, itemCreators, collections, etc.

### Available Tools & Libraries
1. **pyzotero**: Version 1.13.1 installed via UV tools
   - Location: `/home/agent-blue/.local/share/uv/tools/zotero-mcp-server/lib/python3.13/site-packages/pyzotero/`
   - Provides programmatic access to Zotero API

2. **Zotero MCP Server**: 
   - Executable: `/home/agent-blue/.local/share/uv/tools/zotero-mcp-server/bin/zotero-mcp`
   - Had import issues due to path problems (could not find `zotero_mcp` module)
   - Supporting libraries present in same UV environment

3. **Utility Binaries**: 
   - `zotero-cli`, `zotero-mcp`, `pyzotero`, `pyzotero-mcp` available
   - Part of the UV tool installation

### Configuration in Hermes
- **MCP Settings**: Found in `~/.hermes/config.yaml`
  - `mcp_discovery_timeout: 1.5`
  - `inherit_mcp_toolsets: true`
  - MCP section with various auxiliary service configurations
- **No Direct Zotero MCP Config**: No specific Zotero server configured in `mcp_servers`

## Recommendations for Matt's Use Case

### For AI Agent Training Development
1. **Library Analysis**: Use the Zotero library to find papers on:
   - AI agents and autonomous systems
   - Educational technology and training methodologies
   - Human-AI interaction and collaboration
   - Prompt engineering and LLM applications

2. **Training Material Creation**:
   - Extract key papers for reading lists
   - Generate bibliographies for training modules
   - Create examples of good research practices from the library
   - Develop exercises around evaluating AI agent research

3. **Integration Strategies**:
   - **Option A**: Use direct SQLite access when Zotero is closed
   - **Option B**: Configure pyzotero with API credentials for live access
   - **Option C**: Fix MCP server integration for real-time tool access

### Immediate Next Steps
1. Verify Zotero desktop status (close if needed for direct DB access)
2. Test pyzotero API access with credentials from Zotero account settings
3. Explore library structure to understand research domains covered
4. Consider creating a "AI Agents Training" collection or tag for organizing relevant materials

### Sample Queries for Exploration
```sql
-- Count items by type
SELECT it.typeName as itemType, COUNT(*) as count
FROM items i
JOIN itemData id ON i.itemID = id.itemID
JOIN itemDataValues v ON id.valueID = v.valueID
JOIN itemFields f ON id.fieldID = f.fieldID
JOIN itemTypes it ON i.itemTypeID = it.itemTypeID
WHERE f.fieldName = 'itemType'
GROUP BY it.typeName
ORDER BY count DESC;

-- Recent items (last 6 months)
SELECT i.itemID, v.value as title
FROM items i
JOIN itemData id ON i.itemID = id.itemID
JOIN itemDataValues v ON id.valueID = v.valueID
JOIN itemFields f ON id.fieldID = f.fieldID
WHERE f.fieldName = 'title'
AND i.dateAdded >= datetime('now', '-6 months')
ORDER BY i.dateAdded DESC
LIMIT 20;
```