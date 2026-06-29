#!/usr/bin/env python3
"""
Merge duplicate Zotero items, combining notes.
Process in batches with delays to avoid timeout.
"""

import json
import re
import sys
import time
from pyzotero import zotero

def load_config():
    config_path = "/home/agent-blue/.config/zotero-mcp/config.json"
    with open(config_path, 'r') as f:
        config = json.load(f)
    client_env = config.get('client_env', {})
    return {
        'ZOTERO_API_KEY': client_env.get('ZOTERO_API_KEY'),
        'ZOTERO_LIBRARY_ID': client_env.get('ZOTERO_LIBRARY_ID'),
        'ZOTERO_LIBRARY_TYPE': client_env.get('ZOTERO_LIBRARY_TYPE', 'user')
    }

def normalize_title(title):
    if not title:
        return ""
    title = title.lower().strip()
    title = re.sub(r'\s+', ' ', title)
    title = re.sub(r'[:\-_\.]', '', title)
    return title

def get_arxiv_id(url):
    if not url:
        return None
    match = re.search(r'arxiv\.org/(?:abs|pdf)/([^/\s]+)', url)
    if match:
        return match.group(1)
    return None

def deduplicate_key(item):
    data = item.get('data', {})
    title = data.get('title', '')
    url = data.get('url', '')
    arxiv = get_arxiv_id(url)
    if arxiv:
        return f'arxiv:{arxiv}'
    norm_title = normalize_title(title)
    if norm_title:
        return f'title:{norm_title}'
    return item.get('key', '')

def main():
    config = load_config()
    zot = zotero.Zotero(
        config['ZOTERO_LIBRARY_ID'],
        config['ZOTERO_LIBRARY_TYPE'],
        config['ZOTERO_API_KEY']
    )
    
    print("Fetching all items from Zotero library...")
    all_items = []
    start = 0
    limit = 200
    while True:
        print(f"  Fetching batch starting at {start}...")
        batch = zot.items(limit=limit, start=start)
        if not batch:
            break
        all_items.extend(batch)
        if len(batch) < limit:
            break
        start += limit
        time.sleep(0.2)  # be gentle on the API
    
    print(f"Total items retrieved: {len(all_items)}")
    
    # Group by dedup key
    print("Grouping items by duplicate key...")
    groups = {}
    for item in all_items:
        key = deduplicate_key(item)
        groups.setdefault(key, []).append(item)
    
    # Filter groups with duplicates
    dup_groups = {k: v for k, v in groups.items() if len(v) > 1}
    total_dup_items = sum(len(v)-1 for v in dup_groups.values())
    print(f"Found {len(dup_groups)} groups with duplicates (total duplicate items: {total_dup_items})")
    
    if not dup_groups:
        print("No duplicates found. Exiting.")
        return 0
    
    # Process each duplicate group
    merged_count = 0
    updated_count = 0
    failed_count = 0
    processed_groups = 0
    
    print("\nProcessing duplicate groups...")
    for key, items in dup_groups.items():
        processed_groups += 1
        # Choose the item to keep: prefer one with a note, or longer note, or newer dateModified
        def score(item):
            data = item.get('data', {})
            note_len = len(data.get('note', ''))
            return (note_len, data.get('dateModified', ''))
        items_sorted = sorted(items, key=score, reverse=True)
        keeper = items_sorted[0]
        duplicates = items_sorted[1:]
        
        # Combine notes from all items in the group (using the data we have, but we'll get current versions later)
        notes_list = []
        for it in items:
            note = it.get('data', {}).get('note', '')
            if note:
                notes_list.append(note.strip())
        combined_note = "\n\n---\n\n".join(notes_list) if notes_list else ""
        
        # --- Update the keeper ---
        # Get current version of keeper
        try:
            keeper_current = zot.item(keeper.get('key'))
            keeper_data = keeper_current.get('data', {})
            keeper_version = keeper_data.get('version')
            current_note = keeper_data.get('note', '')
            if combined_note != current_note:
                updated_data = keeper_data.copy()
                updated_data['note'] = combined_note
                update_payload = {
                    'key': keeper.get('key'),
                    'version': keeper_version,
                    'data': updated_data
                }
                result = zot.update_item(update_payload)
                updated_count += 1
                # print(f"  Updated keeper {keeper.get('key')} with merged note.")
            # else:
            #     print(f"  Keeper {keeper.get('key')} note already matches combined.")
        except Exception as e:
            print(f"  Failed to update keeper {keeper.get('key')}: {e}")
            failed_count += 1
            # If we can't update the keeper, we still might want to delete duplicates? 
            # But without updating notes, we risk losing notes. Let's skip deleting duplicates for this group if update fails.
            continue
        
        # --- Delete duplicates ---
        for dup in duplicates:
            try:
                # Get current version of duplicate
                dup_current = zot.item(dup.get('key'))
                dup_version = dup_current.get('data', {}).get('version')
                delete_payload = {
                    'key': dup.get('key'),
                    'version': dup_version
                }
                result = zot.delete_item(delete_payload)
                merged_count += 1
                # print(f"  Deleted duplicate {dup.get('key')}")
            except Exception as e:
                print(f"  Failed to delete duplicate {dup.get('key')}: {e}")
                failed_count += 1
        
        # Progress indicator every 10 groups
        if processed_groups % 10 == 0:
            print(f"  Processed {processed_groups}/{len(dup_groups)} groups: {merged_count} duplicates deleted, {updated_count} items updated, {failed_count} failed")
        
        # Delay between groups to avoid rate limiting
        time.sleep(0.5)
    
    print(f"\nMerge complete.")
    print(f"  Duplicate items deleted: {merged_count}")
    print(f"  Items updated with combined notes: {updated_count}")
    print(f"  Failed operations: {failed_count}")
    
    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())