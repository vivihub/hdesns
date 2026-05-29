#!/usr/bin/env python3
"""Show full URL line for each section to identify usernames correctly."""
import json
import re
import os

filepath = "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964274613.txt"

with open(filepath, 'r', encoding='utf-8') as f:
    raw = f.read()
data = json.loads(raw)
content = data.get('fileContent', '')

sections_raw = re.split(r'\|\s*\|\s*instagram\s*\|', content)
print(f"Total sections: {len(sections_raw) - 1}")

for i, section in enumerate(sections_raw[1:], 1):
    full_section = '|  | instagram |' + section
    lines = full_section.split('\n')

    # Line 2 (index 2) should be the URL row
    url_line = lines[2] if len(lines) > 2 else ''
    print(f"\nSection {i} URL line:")
    print(f"  {url_line}")

    # Also try with normalized backslashes
    normalized = url_line.replace('\\_', '_')
    ig_m = re.search(r'instagram\.com/([^/?&#\s|]+)', normalized)
    if ig_m:
        print(f"  -> IG username: {ig_m.group(1).strip('/')}")
