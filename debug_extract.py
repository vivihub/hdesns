#!/usr/bin/env python3
"""Debug script to examine file content structure."""
import json
import re
import os

filepath = "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964274613.txt"

if not os.path.exists(filepath):
    print("FILE NOT FOUND!")
    exit(1)

with open(filepath, 'r', encoding='utf-8') as f:
    raw = f.read()

print(f"Raw file size: {len(raw)} bytes")
print(f"\nFirst 200 chars of raw:")
print(repr(raw[:200]))

data = json.loads(raw)
content = data.get('fileContent', '')

print(f"\nContent length: {len(content)}")
print(f"\nFirst 500 chars of content:")
print(repr(content[:500]))

# Check for literal \n vs actual newlines
literal_newlines = content.count('\\n')
actual_newlines = content.count('\n')
print(f"\nLiteral \\\\n count (2-char sequence): {literal_newlines}")
print(f"Actual newline (\\n) count: {actual_newlines}")

# Find first occurrence of 'instagram'
idx = content.lower().find('instagram')
if idx >= 0:
    print(f"\nFirst 'instagram' at index {idx}")
    print(f"Context: {repr(content[max(0,idx-100):idx+200])}")
else:
    print("\nNo 'instagram' found in content!")

# Try to find the section split pattern
import re
sections = re.split(r'\|\s*\|\s*instagram\s*\|', content)
print(f"\nSplit by '|  | instagram |' -> {len(sections)} sections")

# Try actual newline split
sections2 = re.split(r'\n\|\s*\|\s*instagram\s*\|', content)
print(f"Split by '\\n|  | instagram |' -> {len(sections2)} sections")

if len(sections) > 1:
    # Show first section
    print(f"\nFirst section (first 300 chars):")
    print(repr(sections[1][:300]))
