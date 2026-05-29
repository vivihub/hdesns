#!/usr/bin/env python3
"""Find all Instagram/Twitter accounts in the spreadsheet files with correct regex."""
import json
import re
import os

FILES = {
    "2023/1":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964274613.txt",
    "2024/1":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964556205.txt",
    "2024/12": "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964591636.txt",
}

def extract_accounts(content):
    """Extract all sections with their account info."""
    sections_raw = re.split(r'\|\s*\|\s*instagram\s*\|', content)
    results = []
    for i, section in enumerate(sections_raw[1:], 1):
        full_section = '|  | instagram |' + section
        lines = full_section.split('\n')

        # Line 2 should be the URL row
        url_line = lines[2] if len(lines) > 2 else ''
        # Normalize backslash escapes
        normalized = url_line.replace('\\_', '_').replace('\\-', '-')

        ig_m = re.search(r'instagram\.com/([^/?&#\s|]+)', normalized)
        tw_m = re.search(r'twitter\.com/([^/?&#\s|]+)', normalized)

        ig = ig_m.group(1).strip('/').lower() if ig_m else None
        tw = tw_m.group(1).strip('/') if tw_m else None

        # Also show the raw URL for debugging
        ig_raw = re.search(r'instagram\.com/[^\s|]+', url_line)
        tw_raw = re.search(r'twitter\.com/[^\s|]+', url_line)
        results.append({
            'section': i,
            'ig': ig,
            'tw': tw,
            'ig_raw': ig_raw.group(0) if ig_raw else None,
            'tw_raw': tw_raw.group(0) if tw_raw else None,
        })
    return results

for month_key, filepath in FILES.items():
    if not os.path.exists(filepath):
        print(f"{month_key}: FILE NOT FOUND")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()
    data = json.loads(raw)
    content = data.get('fileContent', '')

    results = extract_accounts(content)
    print(f"\n=== {month_key} ({len(results)} sections) ===")
    for r in results:
        print(f"  Sec {r['section']}: ig={r['ig']!r}, tw={r['tw']!r}")
        if r['ig_raw']:
            print(f"    raw ig URL: {r['ig_raw']}")
