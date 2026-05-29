#!/usr/bin/env python3
"""
Extract historical follower data from Google Sheets tool-result files.
Run on Mac: python3 /Users/shusuzuki/Documents/Claude/Projects/社内タレント情報/extract_historical.py
"""
import json
import re
import os
import sys

# Complete mapping of month keys to tool-result file paths
FILES = {
    "2023/1":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964274613.txt",
    "2023/2":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964277814.txt",
    "2023/3":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964281125.txt",
    "2023/4":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964284915.txt",
    "2023/5":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964287748.txt",
    "2023/6":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964290594.txt",
    "2023/7":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964533255.txt",
    "2023/8":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964535605.txt",
    "2023/9":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964538962.txt",
    "2023/10": "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964541975.txt",
    "2023/11": "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964545048.txt",
    "2023/12": "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964547997.txt",
    "2024/1":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964556205.txt",
    "2024/2":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964558583.txt",
    "2024/3":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964560907.txt",
    "2024/4":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964563425.txt",
    "2024/5":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964566249.txt",
    "2024/6":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964569744.txt",
    "2024/7":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964578235.txt",
    "2024/8":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964580710.txt",
    "2024/9":  "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964583744.txt",
    "2024/10": "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964586267.txt",
    "2024/11": "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964589099.txt",
    "2024/12": "/var/folders/nx/v50228gx65qfjv29k33rdxj80000gn/T/claude-hostloop-plugins/06b9ad9a48135d4b/projects/-Users-shusuzuki-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-86114aaf-b580-4d14-83f6-526045d5a223-outpu-j49j83/85184203-45e9-4085-beb5-2d8bda2e9b85/tool-results/mcp-48a54925-3d04-4d80-a294-73a9c752f445-read_file_content-1779964591636.txt",
}

# Mapping Instagram account username -> canonical talent name
# Identified from the file content analysis
IG_TO_TALENT = {
    "fantique_": "湯上響花",        # fantique\_/ normalized to fantique_
    "fantique": "湯上響花",         # fallback without trailing underscore
    "eito.konishi": "小西詠斗",
    "kagei_hina": "景井ひな",       # kagei\_hina
    "kagei": "景井ひな",            # fallback
    "moe_nobori": "のぼりもえ",     # moe\_nobori
    "moe.nobori": "のぼりもえ",
    "mi_smile25": "花山瑞貴",       # mi\_smile25
    "saayagram0101": "水瀬紗彩耶",
    "saaya_0101": "水瀬紗彩耶",     # possible variant
    "bgirlcocoa": "七瀬恋彩",       # COCOA
    "mao.6454": "まお",
    "mao6454": "まお",
    "shoya___4008": "坂田秀晃",     # shoya\_\_\_4008
    "shoya__4008": "坂田秀晃",
    "sora.kaito0520": "皆藤空良",
    "lindow_ozaki": "せきぐちりさ",  # lindow\_ozaki
    "lindow": "せきぐちりさ",        # fallback
}

# Also try Twitter-based identification as fallback
TW_TO_TALENT = {
    "higuys_iamkyoka": "湯上響花",
    "higuys": "湯上響花",
    "Eightkns": "小西詠斗",
    "hinatter0219": "景井ひな",
    "_mme16": "のぼりもえ",
    "saaya112233": "水瀬紗彩耶",
    "bgirlcocoa": "七瀬恋彩",
    "mao0504_": "まお",
    "mao0504": "まお",
    "sora_kaito0520": "皆藤空良",
    "sora": "皆藤空良",  # might be ambiguous
}

TARGET_TALENTS = {
    "湯上響花", "小西詠斗", "景井ひな", "花山瑞貴", "水瀬紗彩耶",
    "七瀬恋彩", "皆藤空良", "まお", "せきぐちりさ", "坂田秀晃",
    "中本大賀", "宮本廉也", "永田聖一朗", "のぼりもえ"
}

def parse_number(s):
    """Convert number strings like '1.5万', '10.4万', '1,234', '1.2M' to integers."""
    if s is None:
        return None
    s = str(s).strip()
    # Clean up escape artifacts
    s = s.replace('\\', '').replace('-', '').strip()
    if not s or s in ('', '—', '---', '失敗', 'N/A'):
        return None
    # Remove commas
    s = s.replace(',', '')
    # Handle 万 (10000)
    if '万' in s:
        s2 = s.replace('万', '').strip()
        try:
            return int(round(float(s2) * 10000))
        except:
            return None
    # Handle M (million)
    m = re.match(r'^([\d.]+)\s*[Mm]$', s)
    if m:
        try:
            return int(round(float(m.group(1)) * 1000000))
        except:
            return None
    # Handle K (thousand)
    m = re.match(r'^([\d.]+)\s*[Kk]$', s)
    if m:
        try:
            return int(round(float(m.group(1)) * 1000))
        except:
            return None
    # Handle negative numbers (skip them - we only want positive counts)
    if s.startswith('-'):
        return None
    # Plain integer or float
    try:
        val = float(s)
        if val < 0:
            return None
        return int(val)
    except:
        return None

def extract_ig_username(url):
    """Extract Instagram username from URL."""
    # Remove backslash escapes
    url = url.replace('\\', '')
    m = re.search(r'instagram\.com/([^/?&#\s]+)', url)
    if m:
        username = m.group(1).strip('/')
        return username.lower()
    return None

def extract_tw_username(url):
    """Extract Twitter username from URL."""
    url = url.replace('\\', '')
    m = re.search(r'twitter\.com/([^/?&#\s]+)', url)
    if m:
        return m.group(1).strip('/')
    return None

def parse_table_row(line):
    """Parse a markdown table row into cells."""
    line = line.strip()
    if not line.startswith('|'):
        return None
    # Split by | and strip each cell
    parts = line.split('|')
    # Remove first empty (before first |) and last empty (after last |)
    cells = [p.strip() for p in parts[1:-1]]
    return cells

def parse_number_cell(cell):
    """Try to parse a cell as a follower count."""
    cell = cell.strip()
    # Remove URL artifacts
    if 'http' in cell or 'www.' in cell:
        return None
    # Remove markdown formatting
    cell = cell.replace('\\', '').replace('*', '').strip()
    # Handle empty or dash
    if not cell or cell in ('-', '—', '\\-', 'N/A', '失敗'):
        return None
    return parse_number(cell)

def identify_talent_from_section(section_text):
    """
    Identify talent from a section's header text.
    Returns canonical talent name or None.
    """
    # Normalize markdown escapes: \_ -> _, \\ -> \ etc.
    normalized = section_text.replace('\\_', '_').replace('\\-', '-').replace('\\&', '&')

    # Look for Instagram URL
    ig_match = re.search(r'instagram\.com/([^/?&#\s|]+)', normalized)
    if ig_match:
        username = ig_match.group(1).strip('/').lower()
        # Remove trailing slashes and path components
        username = username.split('/')[0]
        # Check exact match
        if username in IG_TO_TALENT:
            talent = IG_TO_TALENT[username]
            if talent.startswith('?'):
                return None
            return talent if talent in TARGET_TALENTS else None
        # Check partial match (key is contained in username)
        for key, talent in IG_TO_TALENT.items():
            if talent.startswith('?'):
                continue
            if key == username or username.startswith(key + '_') or username.startswith(key + '.'):
                return talent if talent in TARGET_TALENTS else None

    # Try Twitter URL as fallback
    tw_match = re.search(r'twitter\.com/([^/?&#\s|]+)', normalized)
    if tw_match:
        username = tw_match.group(1).strip('/')
        if username in TW_TO_TALENT:
            talent = TW_TO_TALENT[username]
            return talent if talent in TARGET_TALENTS else None

    return None

def parse_day_label(label):
    """Parse day label like '1日', '15日', '31日' -> int or None."""
    label = label.strip().replace('\\', '')
    m = re.match(r'^(\d+)', label)
    if m:
        return int(m.group(1))
    return None

def parse_section(section_text, month_key):
    """
    Parse a single talent section.
    Returns (talent_name, monthly_snapshot, daily_data) or None if not a target.

    Section structure (split by \n):
    Line 0: |  | instagram |  |  | Twitter |  |  | TikTok |  |  | YouTube (or LINELIVE) |  |  |
    Line 1: | :-: | :-: | ... |
    Line 2: |  | IG_URL |  |  | TW_URL |  |  | TT_URL |  |  | YT_URL |  |  |
    Line 3: |  | 投稿URL | 実数 | 前日比 | 投稿URL | 実数 | 前日比 | 投稿URL | 実数 | 前日比 | 投稿URL | 実数 | 前日比 |
    Lines 4+: | Nday | URL/- | IG_count | diff | URL/- | TW_count | diff | URL/- | TT_count | diff | URL/- | YT_count | diff |
    Last line: |  |  |  | -total_ig |  |  | -total_tw |  |  | -total_tt |  |  | -total_yt |
    """
    year_str, month_str = month_key.split('/')
    year = int(year_str)
    month = int(month_str)

    lines = section_text.split('\n')

    # Find the talent from line 2 (URL row)
    # But first, we need to identify which URL row we're looking at
    talent = None
    for line in lines[:5]:
        talent = identify_talent_from_section(line)
        if talent:
            break

    if not talent:
        return None

    # Parse daily data rows
    daily_data = {}  # day_int -> {ig, tw, tt, yt}
    last_day_with_data = None
    last_day_data = None

    for line in lines:
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = parse_table_row(line)
        if not cells or len(cells) < 4:
            continue

        # Check if first cell is a day label (Nday format)
        day = parse_day_label(cells[0])
        if day is None:
            continue

        # Extract counts from cells
        # Format: | day_label | URL/- | IG_count | diff | URL/- | TW_count | diff | URL/- | TT_count | diff | URL/- | YT_count | diff |
        # Cells:    [0]          [1]     [2]        [3]    [4]     [5]        [6]    [7]     [8]        [9]    [10]    [11]       [12]

        ig_count = None
        tw_count = None
        tt_count = None
        yt_count = None

        if len(cells) >= 3:
            ig_count = parse_number_cell(cells[2])
        if len(cells) >= 6:
            tw_count = parse_number_cell(cells[5])
        if len(cells) >= 9:
            tt_count = parse_number_cell(cells[8])
        if len(cells) >= 12:
            yt_count = parse_number_cell(cells[11])

        if ig_count is not None or tw_count is not None or tt_count is not None or yt_count is not None:
            daily_data[day] = {
                'ig': ig_count,
                'tw': tw_count,
                'tt': tt_count,
                'yt': yt_count
            }
            last_day_with_data = day
            last_day_data = daily_data[day]

    # Month-end snapshot = last day with data
    monthly_snapshot = None
    if last_day_data:
        monthly_snapshot = {
            'instagram': last_day_data['ig'],
            'twitter': last_day_data['tw'],
            'tiktok': last_day_data['tt'],
            'youtube': last_day_data['yt'],
        }

    # Daily instagram data
    daily_list = []
    for day, data in sorted(daily_data.items()):
        if data['ig'] is not None:
            date_str = f"{year}/{month}/{day}"
            daily_list.append((date_str, talent, data['ig']))

    return talent, monthly_snapshot, daily_list


def parse_file(filepath, month_key):
    """Parse a tool-result file and extract all talent data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()

    data = json.loads(raw)
    content = data.get('fileContent', '')

    # Split content into talent sections
    # Sections are separated by the pattern: \n\n|  | instagram |  |  | Twitter
    # OR start at the beginning

    # Find all section boundaries - the header pattern
    section_header = '|  | instagram |  |  | Twitter'
    # Also handle variations
    section_header2 = '| instagram |  |  | Twitter'

    # Split content by section headers
    # First, normalize the section header to find boundaries
    sections_raw = re.split(r'\|\s*\|\s*instagram\s*\|', content)

    monthly_snapshot = {}
    daily_list = []

    for i, section in enumerate(sections_raw):
        if i == 0:
            # First part is before first section, skip
            continue

        # Reconstruct the full section (add back the split point)
        full_section = '|  | instagram |' + section

        result = parse_section(full_section, month_key)
        if result:
            talent, snap, daily = result
            if snap:
                monthly_snapshot[talent] = snap
            daily_list.extend(daily)

    return monthly_snapshot, daily_list


def main():
    monthly_snapshots = {}
    daily_instagram_map = {}  # date_str -> {talent: count}
    notes = {}

    for month_key in sorted(FILES.keys()):
        filepath = FILES[month_key]
        print(f"\nProcessing {month_key}...", end='', flush=True)

        if not os.path.exists(filepath):
            print(f" FILE NOT FOUND")
            notes[month_key] = "file not found"
            continue

        try:
            snap, daily = parse_file(filepath, month_key)

            if snap:
                monthly_snapshots[month_key] = snap

            for date_str, talent, ig_count in daily:
                if date_str not in daily_instagram_map:
                    daily_instagram_map[date_str] = {}
                daily_instagram_map[date_str][talent] = ig_count

            print(f" -> {len(snap)} talents, {len(daily)} daily entries")

        except Exception as e:
            import traceback
            print(f" ERROR: {e}")
            traceback.print_exc()
            notes[month_key] = f"error: {str(e)}"

    # Convert daily_instagram_map to list
    daily_instagram = []
    for date_str in sorted(daily_instagram_map.keys(),
                           key=lambda d: [int(x) for x in d.split('/')]):
        daily_instagram.append({
            "date": date_str,
            "talents": daily_instagram_map[date_str]
        })

    result = {
        "monthly_snapshots": monthly_snapshots,
        "daily_instagram": daily_instagram,
        "_notes": notes
    }

    output_path = "/Users/shusuzuki/Documents/Claude/Projects/社内タレント情報/historical_2023_2024.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n\nOutput written to: {output_path}")
    print(f"Months processed: {len(monthly_snapshots)}")
    print(f"Daily entries: {len(daily_instagram)}")

    # Show summary of what was found
    print("\n=== Talent coverage ===")
    talent_months = {}
    for month, talents in monthly_snapshots.items():
        for talent in talents:
            if talent not in talent_months:
                talent_months[talent] = []
            talent_months[talent].append(month)

    for talent in sorted(TARGET_TALENTS):
        months = talent_months.get(talent, [])
        print(f"  {talent}: {len(months)} months")

    return result


if __name__ == '__main__':
    main()
