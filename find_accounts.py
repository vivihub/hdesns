#!/usr/bin/env python3
"""Find all Instagram/Twitter accounts in the spreadsheet files."""
import json
import re
import os

# Check all files, look for unrecognized accounts
FILES = {
    "2023/1":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964274613.txt",
    "2024/12": "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964591636.txt",
}

KNOWN = {
    "fantique", "eito.konishi", "kagei_hina", "kagei", "moe_nobori", "moe.nobori",
    "mi_smile25", "saayagram0101", "bgirlcocoa", "mao.6454", "mao6454",
    "shoya___4008", "shoya__4008", "sora.kaito0520", "lindow_ozaki", "lindow",
}

for month_key, filepath in FILES.items():
    if not os.path.exists(filepath):
        print(f"{month_key}: FILE NOT FOUND")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()
    data = json.loads(raw)
    content = data.get('fileContent', '')

    # Find all instagram.com URLs in header lines (line 2 of each section)
    sections_raw = re.split(r'\|\s*\|\s*instagram\s*\|', content)
    print(f"\n=== {month_key} ===")
    print(f"Sections: {len(sections_raw) - 1}")

    for i, section in enumerate(sections_raw[1:], 1):
        full_section = '|  | instagram |' + section
        lines = full_section.split('\n')

        # Line 0 is header, line 1 is separator, line 2 should be URLs
        ig_url = None
        tw_url = None
        for j, line in enumerate(lines[:5]):
            ig_m = re.search(r'instagram\.com/([^/?&#\s\\|]+)', line)
            tw_m = re.search(r'twitter\.com/([^/?&#\s\\|]+)', line)
            if ig_m and not ig_url:
                ig_url = ig_m.group(1).replace('\\', '').lower().strip('/')
            if tw_m and not tw_url:
                tw_url = tw_m.group(1).replace('\\', '')

        known = ig_url in KNOWN if ig_url else False
        print(f"  Section {i}: ig={ig_url!r}, tw={tw_url!r}, known={known}")
