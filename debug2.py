#!/usr/bin/env python3
"""Debug script to test the parsing after the fix."""
import json
import re
import os

filepath = "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964274613.txt"

with open(filepath, 'r', encoding='utf-8') as f:
    raw = f.read()

data = json.loads(raw)
content = data.get('fileContent', '')

# Split into sections
sections_raw = re.split(r'\|\s*\|\s*instagram\s*\|', content)
print(f"Total sections: {len(sections_raw)}")

# Get first real section
section = sections_raw[1]
full_section = '|  | instagram |' + section
print(f"\nFull section first 600 chars:")
print(repr(full_section[:600]))

# Split into lines
lines = full_section.split('\n')
print(f"\nNumber of lines: {len(lines)}")
print(f"\nFirst 5 lines:")
for i, line in enumerate(lines[:5]):
    print(f"  [{i}]: {repr(line)}")

# Test Instagram URL extraction from lines
import re
for i, line in enumerate(lines[:5]):
    ig_match = re.search(r'instagram\.com/([^/?&#\s\\|]+)', line)
    if ig_match:
        username = ig_match.group(1).replace('\\', '').lower().strip('/')
        print(f"\nFound IG username in line {i}: '{username}'")

# Test day rows parsing
print("\n\nDay rows found:")
for line in lines:
    cells = [p.strip() for p in line.split('|')[1:-1]] if line.startswith('|') else None
    if cells and len(cells) >= 3:
        label = cells[0].strip().replace('\\', '')
        m = re.match(r'^(\d+)', label)
        if m:
            day = int(m.group(1))
            ig_cell = cells[2]
            # Parse number
            ig_cell_clean = ig_cell.strip().replace(',', '')
            try:
                val = int(float(ig_cell_clean))
                if val > 0:
                    print(f"  Day {day}: ig={val} (from '{ig_cell}')")
            except:
                pass
