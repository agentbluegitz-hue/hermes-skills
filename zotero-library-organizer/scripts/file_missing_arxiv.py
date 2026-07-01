#!/usr/bin/env python3
"""
File specific missing Arxiv papers into Zotero library
"""

import os
import sys
import json
from pyzotero import zotero
import urllib.request
import xml.etree.ElementTree as ET
import re

def load_config():
    """Load Zotero credentials from MCP config"""
    config_path = '/home/agent-blue/.config/zotero-mcp/config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        client_env = config.get('client_env', {})
        return {
            'ZOTERO_API_KEY': client_env.get('ZOTERO_API_KEY'),
            'ZOTERO_LIBRARY_ID': client_env.get('ZOTERO_LIBRARY_ID'),
            'ZOTERO_LIBRARY_TYPE': client_env.get('ZOTERO_LIBRARY_TYPE', 'user')
        }
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

def get_arxiv_metadata(arxiv_id):
    """Get metadata for an Arxiv paper from the Arxiv API"""
    try:
        # Clean the ID (remove version if present for API call)
        clean_id = arxiv_id.split('v')[0] if 'v' in arxiv_id else arxiv_id
        url = f"http://export.arxiv.org/api/query?id_list={clean_id}"
        
        with urllib.request.urlopen(url) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        entry = root.find('atom:entry', ns)
        if entry is None:
            return None
        
        title_elem = entry.find('atom:title', ns)
        title = title_elem.text.strip() if title_elem is not None else "Unknown Title"
        title = re.sub(r'\s+', ' ', title)  # Clean whitespace
        
        # Get authors
        authors = []
        for author in entry.findall('atom:author', ns):
            name_elem = author.find('atom:name', ns)
            if name_elem is not None:
                authors.append(name_elem.text.strip())
        
        # Get published date
        published_elem = entry.find('atom:published', ns)
        published = published_elem.text.strip() if published_elem is not None else ""
        
        # Get summary/abstract
        summary_elem = entry.find('atom:summary', ns)
        summary = summary_elem.text.strip() if summary_elem is not None else ""
        summary = re.sub(r'\s+', ' ', summary)  # Clean whitespace
        
        return {
            'id': arxiv_id,
            'clean_id': clean_id,
            'title': title,
            'authors': authors,
            'published': published,
            'summary': summary,
            'url': f'https://arxiv.org/abs/{clean_id}'
        }
    except Exception as e:
        print(f"Error fetching metadata for Arxiv:{arxiv_id}: {e}")
        return None

def file_arxiv_paper(zot, metadata):
    """File an Arxiv paper into Zotero"""
    if not metadata:
        return False
    
    # Prepare tags
    tags = ['Arxiv', 'AI Research']
    title_lower = metadata['title'].lower()
    if 'agent' in title_lower or 'agents' in title_lower:
        tags.append('AI Agents')
    if 'llm' in title_lower or 'language model' in title_lower:
        tags.append('LLM')
    if 'multi' in title_lower or 'agent' in title_lower:
        tags.append('Multi-Agent Systems')
    
    # Prepare item data - using journalArticle type which is more appropriate for papers
    item_data = {
        'itemType': 'journalArticle',
        'title': metadata['title'],
        'url': metadata['url'],
        'accessDate': metadata['published'][:10] if metadata['published'] else '',
        'date': metadata['published'][:10] if metadata['published'] else '',
        'abstractNote': metadata['summary'],
        'tags': [{'tag': tag} for tag in tags],
        'creators': []
    }
    
    # Add authors as creators
    for author in metadata['authors']:
        # Split author name into first and last
        parts = author.strip().split()
        if len(parts) >= 2:
            last_name = parts[-1]
            first_name = ' '.join(parts[:-1])
            item_data['creators'].append({
                'creatorType': 'author',
                'firstName': first_name,
                'lastName': last_name
            })
        else:
            # If we can't split, put everything in last name
            item_data['creators'].append({
                'creatorType': 'author',
                'lastName': author
            })
    
    try:
        # Check if item already exists by URL
        existing = zot.items(q=metadata['title'][:50])  # Search by partial title
        existing_urls = [item.get('data', {}).get('url', '') for item in existing]
        
        if metadata['url'] not in existing_urls:
            # Create new item
            response = zot.create_items([item_data])
            if response['success']:
                print(f"✓ Successfully filed: {metadata['title'][:60]}... (Arxiv:{metadata['id']})")
                return True
            else:
                print(f"✗ Failed to file {metadata['title']}: {response}")
                return False
        else:
            print(f"○ Skipped (already exists): {metadata['title'][:60]}... (Arxiv:{metadata['id']})")
            return True
    except Exception as e:
        print(f"✗ Error filing {metadata['title']}: {e}")
        return False

def main():
    """Main function to file missing Arxiv papers"""
    print("=== Filing Missing Arxiv Papers to Zotero ===")
    
    # Load configuration
    config = load_config()
    if not config:
        print("ERROR: Could not load Zotero configuration")
        return 1
    
    print(f"Loaded config for library {config['ZOTERO_LIBRARY_ID']} ({config['ZOTERO_LIBRARY_TYPE']})")
    
    # Initialize Zotero
    zot = init_zotero(config)
    if not zot:
        print("ERROR: Could not initialize Zotero connection")
        return 1
    
    print(f"Connected to Zotero library successfully")
    
    # Specific Arxiv IDs user mentioned as missing
    missing_ids = [
        '2602.17753',
        '2606.02080',
        '2606.22902',
        '2606.26859',
        '2606.31935'
    ]
    
    print(f"\nProcessing {len(missing_ids)} missing Arxiv papers:")
    
    # Process each paper
    success_count = 0
    for arxiv_id in missing_ids:
        print(f"\n--- Processing Arxiv:{arxiv_id} ---")
        
        # Get paper metadata
        metadata = get_arxiv_metadata(arxiv_id)
        if not metadata:
            print(f"✗ Could not get metadata for Arxiv:{arxiv_id}")
            continue
        
        print(f"Title: {metadata['title'][:60]}...")
        print(f"Authors: {', '.join(metadata['authors'][:3])}{'...' if len(metadata['authors']) > 3 else ''}")
        
        # File the paper
        if file_arxiv_paper(zot, metadata):
            success_count += 1
    
    print(f"\n=== Summary ===")
    print(f"Successfully filed: {success_count}/{len(missing_ids)} papers")
    
    if success_count == len(missing_ids):
        print("All missing papers filed successfully! 🎉")
        return 0
    else:
        print("Some papers failed to file. Check errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())