# Zotero MCP Server Troubleshooting
## Session-Specific Fixes for Matt's Setup (UF Research Computing)

Based on the session with Hermes Blue (Matt from UF Information Technology, Research Computing), here are specific solutions to the Zotero MCP server issues encountered:

## Problem 1: ModuleNotFoundError: No module named 'zotero_mcp'
**Error**: When running `/home/agent-blue/.local/share/uv/tools/zotero-mcp-server/bin/zotero-mcp`, got:
```
Traceback (most recent call last):
  File ".../bin/zotero-mcp", line 4, in <module>
    from zotero_mcp.cli import main
ModuleNotFoundError: No module named 'zotero_mcp'
```

**Root Cause**: The executable script cannot find the zotero_mcp module because the Python path doesn't include the installation's site-packages directory.

**Solution**: Set PYTHONPATH explicitly before running:
```bash
cd /home/agent-blue/.local/share/uv/tools/zotero-mcp-server
PYTHONPATH=/home/agent-blue/.local/share/uv/tools/zotero-mcp-server/lib/python3.13/site-packages:$PYTHONPATH \
  /home/agent-blue/.local/share/uv/tools/zotero-mcp-server/bin/python -m zotero_mcp.cli [command]
```

**Verification**: Test with setup-info command:
```bash
PYTHONPATH=/home/agent-blue/.local/share/uv/tools/zotero-mcp-server/lib/python3.13/site-packages:$PYTHONPATH \
  /home/agent-blue/.local/share/uv/tools/zotero-mcp-server/bin/python -m zotero_mcp.cli setup-info
```

## Problem 2: ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'
**Error**: After fixing the first issue, got:
```
ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'
```

**Root Cause**: The pydantic-core package installed in the uv tool environment is corrupted or incomplete.

**Solution**: Reinstall pydantic and pydantic-core using uv:
```bash
cd /home/agent-blue/.local/share/uv/tools/zotero-mcp-server
/home/agent-blue/.local/bin/uv pip install --force-reinstall pydantic pydantic-core
```

## Problem 3: Configuration Discovery
The MCP server was actually configured but the setup wasn't being recognized due to the above issues.

**Working Configuration Discovery** (after fixing paths):
```bash
PYTHONPATH=/home/agent-blue/.local/share/uv/tools/zotero-mcp-server/lib/python3.13/site-packages:$PYTHONPATH \
  /home/agent-blue/.local/share/uv/tools/zotero-mcp-server/bin/python -m zotero_mcp.cli setup-info
```

**Output showed**:
- Command path: `/home/agent-blue/.local/bin/zotero-mcp`
- Environment variables including:
  - `ZOTERO_API_KEY`: "WCM4********************" (obfuscated)
  - `ZOTERO_LIBRARY_ID`: "****" (obfuscated)  
  - `ZOTERO_DB_PATH`: "/home/agent-blue/snap/zotero-snap/common/Zotero/zotero.sqlite"
  - `OPENAI_BASE_URL`: "https://api.ai.it.ufl.edu/"
  - `OPENAI_API_KEY`: "sk-vn_...ZasA" (obfuscated)
  - `ZOTERO_LOCAL`: "true"

## Problem 4: Direct Database Access Issues
**Error**: When trying to access `/home/agent-blue/Zotero/zotero.sqlite` directly:
```
Error accessing database: database is locked
```

**Root Cause**: Zotero desktop application was running and had the database open.

**Solutions**:
1. Close Zotero desktop temporarily for direct database access
2. Use the Zotero API approach instead (doesn't require direct DB access)
3. Make a read-only copy of the database for analysis:
   ```bash
   cp /home/agent-blue/Zotero/zotero.sqlite /tmp/zotero-copy.sqlite
   sqlite3 /tmp/zotero-copy.sqlite "SELECT COUNT(*) FROM items;"
   ```

## Alternative Approach: Direct Zotero API Access
When the MCP server is problematic, direct API access via pyzotero works reliably:

### Finding Credentials
1. Go to Zotero → Settings → Feeds/API
2. Note your User ID (numeric)
3. Generate or note your private key (API Key)
4. Library type is usually "user" for personal libraries

### Python Access Example
```python
import os
from pyzotero import zotero

# Method 1: From environment variables
api_key = os.environ.get('ZOTERO_API_KEY')
library_id = os.environ.get('ZOTERO_LIBRARY_ID') 

# Method 2: From MCP config file (if available)
import json
config_path = os.path.expanduser('~/.config/zotero-mcp/config.json')
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
    client_env = config.get('client_env', {})
    api_key = client_env.get('ZOTERO_API_KEY', api_key)
    library_id = client_env.get('ZOTERO_LIBRARY_ID', library_id)

# Connect if credentials available
if api_key and library_id:
    zot = zotero.Zotero(library_id, 'user', api_key)
    # Test connection
    user_info = zot.user_info()
    print(f"Connected to Zotero library: {user_info}")
    
    # Get recent items
    recent_items = zot.items(limit=5)
    for item in recent_items:
        data = item.get('data', {})
        print(f"- [{data.get('itemType')}] {data.get('title', 'No title')}")
else:
    print("Missing credentials. Check Zotero → Settings → Feeds/API")
```

## Environment Specifics from Matt's Setup
- **Zotero Database**: `/home/agent-blue/Zotero/zotero.sqlite` (125.1 MB)
- **pyzotero**: Version 1.13.1 available via UV tools
- **Zotero MCP Server**: Installed but had path/dependency issues
- **NaviGator Toolkit**: Available at https://api.ai.it.ufl.edu/v1
- **Model**: nemotron-3-super-120b-a12b
- **Operating System**: Linux (Ubuntu-based)

## Recommendation for Research Assistance Workflows
For Matt's use case (developing AI Agent training materials at UF Research Computing):

1. **Use Direct API Access** as primary method:
   - Doesn't require closing Zotero desktop
   - Reliable and straightforward
   - Provides sufficient functionality for most research tasks
   - Works with the existing pyzotero installation

2. **Consider MCP Server** only if:
   - Semantic search capabilities are specifically needed
   - Real-time synchronization with Zotero is required
   - The path/dependency issues are resolved permanently

3. **Direct Database Access** for:
   - Complex queries not possible via API
   - Offline analysis when internet is unavailable
   - Cases where API rate limits are a concern

## Quick Test Script
Save this as `test_zotero_access.py` and run it to verify your setup:
```python
#!/usr/bin/env python3
"""
Test script to verify Zotero access via API
"""
import os
import sys

def test_pyzotero_available():
    try:
        from pyzotero import zotero
        print("✓ pyzotero library available")
        return True
    except ImportError as e:
        print(f"✗ pyzotero not available: {e}")
        return False

def test_credentials():
    api_key = os.environ.get('ZOTERO_API_KEY')
    library_id = os.environ.get('ZOTERO_LIBRARY_ID')
    
    if api_key and library_id:
        print(f"✓ Found credentials in environment")
        print(f"  Library ID: {library_id}")
        print(f"  API Key: {api_key[:4]}...{api_key[-4:] if len(api_key) > 8 else '****'}")
        return api_key, library_id
    else:
        print("✗ No credentials found in environment")
        return None, None

def test_connection(api_key, library_id):
    if not api_key or not library_id:
        return False
        
    try:
        from pyzotero import zotero
        zot = zotero.Zotero(library_id, 'user', api_key)
        user_info = zot.user_info()
        print(f"✓ Successfully connected to Zotero")
        print(f"  User: {user_info.get('username', 'Unknown')}")
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

def main():
    print("=== Zotero Access Test ===")
    
    if not test_pyzotero_available():
        print("\nInstall pyzotero with:")
        print("  uv pip install pyzotero")
        return 1
        
    api_key, library_id = test_credentials()
    if not api_key:
        print("\nTo get credentials:")
        print("  1. Go to https://www.zotero.org/settings")
        print("  2. Navigate to Feeds/API tab")
        print("  3. Note your User ID")
        print("  4. Generate a private key (API Key) if needed")
        return 1
        
    if test_connection(api_key, library_id):
        print("\n🎉 Zotero API access is working!")
        return 0
    else:
        print("\n❌ Zotero API access failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```