#!/usr/bin/env python3
"""Debug the 2024 file structure."""
import json
import re
import os

filepath = "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964591636.txt"

with open(filepath, 'r', encoding='utf-8') as f:
    raw = f.read()
data = json.loads(raw)
content = data.get('fileContent', '')

print(f"Content length: {len(content)}")
print(f"First 500 chars:")
print(repr(content[:500]))
print()

# Find all instagram.com occurrences
ig_positions = [m.start() for m in re.finditer(r'instagram\.com', content)]
print(f"Total instagram.com occurrences: {len(ig_positions)}")
for pos in ig_positions[:5]:
    ctx = content[max(0,pos-50):pos+150]
    print(f"\nAt pos {pos}:")
    print(repr(ctx))

# Find the section split pattern
sections_raw = re.split(r'\|\s*\|\s*instagram\s*\|', content)
print(f"\nSections: {len(sections_raw) - 1}")

# Look at first section in detail
if len(sections_raw) > 1:
    section = sections_raw[1]
    full = '|  | instagram |' + section
    lines = full.split('\n')
    print(f"\nFirst section lines 0-5:")
    for i, line in enumerate(lines[:6]):
        print(f"  [{i}]: {repr(line[:200])}")
