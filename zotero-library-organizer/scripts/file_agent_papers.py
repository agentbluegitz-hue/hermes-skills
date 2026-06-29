#!/usr/bin/env python3
"""
File specific Arxiv papers related to AI agents into Zotero library
"""

import json
import sys
from datetime import datetime
from pyzotero import zotero

def load_config():
    """Load Zotero credentials from MCP config"""
    config_path = "/home/agent-blue/.config/zotero-mcp/config.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        client_env = config.get('client_env', {})
        return {
            'ZOTERO_API_KEY': client_env.get('ZOTERO_API_KEY'),
            'ZOTERO_LIBRARY_ID': client_env.get('ZOTERO_LIBRARY_ID'),
            'ZOTERO_LIBRARY_TYPE': client_env.get('ZOTERO_LIBRARY_TYPE', 'user')
        }
    except Exception as e:
        print(f"Error loading MCP config: {e}")
        return None

def init_zotero(config):
    """Initialize Zotero API connection"""
    try:
        zot = zotero.Zotero(
            config['ZOTERO_LIBRARY_ID'],
            config['ZOTERO_LIBRARY_TYPE'],
            config['ZOTERO_API_KEY']
        )
        # Test connection
        zot.items(limit=1)
        return zot
    except Exception as e:
        print(f"Failed to initialize Zotero API: {e}")
        return None

def file_arxiv_paper(zot, arxiv_id, title, tags=None):
    """File an Arxiv paper by ID into Zotero"""
    if tags is None:
        tags = []
    
    # Add standard tags for AI agent papers
    if 'agent' in title.lower() or 'agents' in title.lower():
        tags.append('AI Agents')
    if 'llm' in title.lower():
        tags.append('LLM')
    if 'multi' in title.lower() or 'agent' in title.lower():
        tags.append('Multi-Agent Systems')
    
    # Prepare item data - removed notes field which is no longer supported
    item_data = {
        'itemType': 'blogPost',  # Using blogPost as Arxiv doesn't have exact match
        'title': title,
        'url': f'https://arxiv.org/abs/{arxiv_id}',
        'accessDate': datetime.now().strftime('%Y-%m-%d'),
        'tags': [{'tag': tag} for tag in tags]
    }
    
    try:
        # Check if item already exists by URL
        existing = zot.items(q=title[:50])  # Search by partial title
        existing_urls = [item.get('data', {}).get('url', '') for item in existing]
        
        if f'https://arxiv.org/abs/{arxiv_id}' not in existing_urls:
            # Create new item
            response = zot.create_items([item_data])
            if response['success']:
                print(f"✓ Successfully filed: {title} (Arxiv:{arxiv_id})")
                return True
            else:
                print(f"✗ Failed to file {title}: {response}")
                return False
        else:
            print(f"○ Skipped (already exists): {title} (Arxiv:{arxiv_id})")
            return True
    except Exception as e:
        print(f"✗ Error filing {title}: {e}")
        return False

def main():
    """Main function to file AI agent papers"""
    print("=== Filing AI Agent Arxiv Papers to Zotero ===")
    
    # Load configuration
    config = load_config()
    if not config:
        print("ERROR: Could not load Zotero configuration")
        return 1
    
    # Initialize Zotero
    zot = init_zotero(config)
    if not zot:
        print("ERROR: Could not initialize Zotero connection")
        return 1
    
    print(f"Connected to Zotero library {config['ZOTERO_LIBRARY_ID']}")
    
    # List of papers to file from today's briefing
    papers_to_file = [
        {
            'id': '2606.05608',
            'title': 'Agentic Software: How AI Agents Are Restructuring the Software Paradigm',
            'tags': ['AI Agents', 'Software Engineering', 'Paradigm Shift']
        },
        {
            'id': '2606.01801',
            'title': 'MetaForge: A Self-Evolving Multimodal Agent that Retrieves, Adapts, and Forges Tools On Demand',
            'tags': ['AI Agents', 'Multimodal', 'Tool Use', 'Self-Evolving']
        },
        {
            'id': '2606.24775',
            'title': 'Are We Ready For An Agent-Native Memory System?',
            'tags': ['AI Agents', 'Memory Systems', 'MemoryAgentBench', 'Evaluation']
        }
    ]
    
    # File each paper
    success_count = 0
    for paper in papers_to_file:
        print(f"\nProcessing: {paper['title']}")
        if file_arxiv_paper(zot, paper['id'], paper['title'], paper['tags']):
            success_count += 1
    
    print(f"\n=== Summary ===")
    print(f"Successfully filed: {success_count}/{len(papers_to_file)} papers")
    
    if success_count == len(papers_to_file):
        print("All papers filed successfully! 🎉")
        return 0
    else:
        print("Some papers failed to file. Check errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())