#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract follower data from Google Drive spreadsheet temp files.
These files are saved by the Claude agent when files are too large to return inline.
"""

import json
import re
import os
import glob
import sys

TMPDIR = '/var/folders/l6/gjrf_52n1p73my_ltflp2mjh0000gn/T/claude-hostloop-plugins/5c021dfa83b84fdb/projects/-Users-shuosakapc-Library-Application-Support-Claude-local-agent-mode-sessions-a59ed77e-4b6c-4f14-8402-dbe7c66ed45f-e867c526-6e59-45b0-992d-bc7992b984b0-local-8463bb6c-882e-4534-9e5b-940f6e42a74f-outp-krvsm4/e07e34de-2dc3-40df-826d-0d1f383e2a16/tool-results'

# Timestamp -> month mapping for this session's requests
# Order of requests: 2024/1, 2024/2, ..., 2024/12, 2025/1, ..., 2025/11
timestamp_to_month = {
    '1779084347284': '2024/1',
    '1779084351852': '2024/2',
    '1779084356828': '2024/3',
    '1779084362126': '2024/4',
    '1779084367205': '2024/5',
    '1779084372053': '2024/6',
    '1779084377228': '2024/7',
    '1779084381886': '2024/8',
    '1779084386429': '2024/9',
    '1779084391399': '2024/10',
    '1779084396366': '2024/11',
    '1779084401394': '2024/12',
    '1779084406318': '2025/1',
    '1779084410894': '2025/2',
    '1779084415341': '2025/3',
    '1779084420155': '2025/4',
    '1779084425587': '2025/5',
    '1779084430155': '2025/6',
    '1779084435251': '2025/7',
    '1779084440468': '2025/8',
    '1779084449122': '2025/9',
    '1779084454352': '2025/10',
    '1779084459482': '2025/11',
}

TARGETS = [
    '湯上響花', '小西詠斗', '景井ひな', '花山瑞貴', '水瀬紗彩耶',
    '七瀬恋彩', '皆藤空良', 'まお', 'せきぐちりさ', '坂田秀晃',
    '中本大賀', '宮本廉也', '永田聖一朗', 'のぼりもえ', 'SUMOMO'
]

TALENT_ALIASES = {
    '真波みお': 'まお',
    'まお\\*mao': 'まお',
    'まお': 'まお',
    '七瀬恋彩/ COCOA': '七瀬恋彩',
    '七瀬恋彩': '七瀬恋彩',
    '湯上響花 / きょうきょう': '湯上響花',
    '湯上響花': '湯上響花',
    'せきぐちりさ': 'せきぐちりさ',
    '皆藤空良': '皆藤空良',
    '景井ひな': '景井ひな',
    '花山瑞貴': '花山瑞貴',
    '水瀬紗彩耶': '水瀬紗彩耶',
    '小西詠斗': '小西詠斗',
    '坂田秀晃': '坂田秀晃',
    '中本大賀': '中本大賀',
    '宮本廉也': '宮本廉也',
    '永田聖一朗': '永田聖一朗',
    'のぼりもえ': 'のぼりもえ',
    'SUMOMO': 'SUMOMO',
}


def parse_number(s):
    """Parse a number string like '42,548' or '#REF!' etc."""
    if not s:
        return None
    s = s.strip()
    if s in ('#REF!', '', '0', '\\#REF\\!', '-', 'N/A'):
        return None
    # Remove commas, backslashes, plus signs
    s = s.replace(',', '').replace('\\', '').replace('+', '').replace(' ', '')
    try:
        val = int(float(s))
        return val if val > 0 else None
    except:
        return None


def parse_spreadsheet_content(content, month_key):
    """Parse a spreadsheet markdown content and extract follower data."""
    results = {}
    lines = content.split('\\n')

    i = 0
    current_talent = None

    while i < len(lines):
        line = lines[i]

        # Check if this line is a talent header row
        if line.startswith('| ') and line.count('|') >= 5:
            parts = [p.strip() for p in line.split('|')]
            first_cell = parts[1] if len(parts) > 1 else ''

            # Skip non-talent rows
            skip_values = ('instagram', 'Twitter', 'TikTok', 'YouTube', 'Youtube', 'Twiiter', 'X',
                           '月初', '月末', '月次増減', 'フォロワー数', '投稿URL', '実数', '前日比', ':-:')
            if (first_cell and
                not first_cell.startswith('http') and
                first_cell not in skip_values and
                not re.match(r'^\d+日$', first_cell) and
                not re.match(r'^\d+$', first_cell)):

                # Check if it's a known talent or alias
                matched = None
                for alias, canonical in TALENT_ALIASES.items():
                    if alias in first_cell or first_cell in alias:
                        matched = canonical
                        break

                if matched is None:
                    for t in TARGETS:
                        if t in first_cell:
                            matched = t
                            break

                if matched:
                    current_talent = matched

        # If we have a current talent, look for フォロワー数
        if current_talent and 'フォロワー数' in line:
            parts = [p.strip() for p in line.split('|')]
            data_parts = []
            for p in parts:
                if p and p != 'フォロワー数' and p != ':-:':
                    data_parts.append(p)

            if current_talent not in results:
                results[current_talent] = {}

            # Get platform order by looking back for platform header
            platforms = []
            for back in range(i - 1, max(i - 10, 0), -1):
                bline = lines[back].lower()
                if 'instagram' in bline or 'twitter' in bline or 'tiktok' in bline or 'youtube' in bline:
                    bparts = [p.strip() for p in lines[back].split('|')]
                    for p in bparts:
                        pl = p.lower().strip()
                        if pl == 'instagram':
                            platforms.append('instagram')
                        elif pl in ('twitter', 'twiiter', 'x'):
                            platforms.append('twitter')
                        elif pl == 'tiktok':
                            platforms.append('tiktok')
                        elif pl in ('youtube',):
                            platforms.append('youtube')
                    break

            if not platforms:
                platforms = ['instagram', 'twitter', 'tiktok', 'youtube']

            # Extract 月初 values (indices 0, 3, 6, 9 in data_parts)
            for idx, plat in enumerate(platforms[:4]):
                j = idx * 3
                if j < len(data_parts):
                    val_str = data_parts[j]
                    val = parse_number(val_str)
                    if val and val > 0:
                        if plat not in results[current_talent]:
                            results[current_talent][plat] = {}
                        results[current_talent][plat][month_key] = val

            # For #REF! cases, look at 1日 row for actual start-of-month values
            for fwd in range(i + 1, min(i + 60, len(lines))):
                fwd_line = lines[fwd]
                fwd_parts = [p.strip() for p in fwd_line.split('|')]
                if len(fwd_parts) > 1 and fwd_parts[1].strip() == '1日':
                    # Format: | 1日 | URL | real_val | prev | URL | real_val | prev | ...
                    day1_vals = []
                    for k in range(2, len(fwd_parts), 3):
                        if k < len(fwd_parts):
                            day1_vals.append(fwd_parts[k])

                    for idx, plat in enumerate(platforms[:4]):
                        current_plat_data = results.get(current_talent, {}).get(plat, {})
                        if month_key not in current_plat_data:
                            if idx < len(day1_vals):
                                val = parse_number(day1_vals[idx])
                                if val and val > 0:
                                    if current_talent not in results:
                                        results[current_talent] = {}
                                    if plat not in results[current_talent]:
                                        results[current_talent][plat] = {}
                                    results[current_talent][plat][month_key] = val
                    break

        i += 1

    return results


def main():
    # Find all temp files for this session
    files = sorted(glob.glob(os.path.join(TMPDIR, 'mcp-48a54925*read_file_content*.txt')))
    print(f"Found {len(files)} temp files", file=sys.stderr)

    all_results = {}

    for fpath in files:
        fname = os.path.basename(fpath)
        ts_match = re.search(r'read_file_content-(\d+)\.txt', fname)
        if not ts_match:
            continue
        ts = ts_match.group(1)

        if ts not in timestamp_to_month:
            print(f"Unknown timestamp: {ts} ({fname})", file=sys.stderr)
            continue

        month_key = timestamp_to_month[ts]
        print(f"Processing {month_key} from {fname[-30:]}", file=sys.stderr)

        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            content = data.get('fileContent', '')
        except Exception as e:
            print(f"Error reading {fname}: {e}", file=sys.stderr)
            continue

        month_results = parse_spreadsheet_content(content, month_key)
        print(f"  Extracted {len(month_results)} talents", file=sys.stderr)
        for talent, platforms in month_results.items():
            summary = {p: list(v.values())[0] for p, v in platforms.items() if v}
            print(f"    {talent}: {summary}", file=sys.stderr)

        for talent, platforms in month_results.items():
            if talent not in all_results:
                all_results[talent] = {}
            for plat, months in platforms.items():
                if plat not in all_results[talent]:
                    all_results[talent][plat] = {}
                all_results[talent][plat].update(months)

    # Build final output in requested format
    output = {}
    for talent in TARGETS:
        data = all_results.get(talent, {})
        output[talent] = {
            'instagram': data.get('instagram', {}),
            'twitter': data.get('twitter', {}),
            'tiktok': data.get('tiktok', {}),
            'youtube': data.get('youtube', {}),
        }

    # Print summary
    print("\n--- Results Summary ---")
    for talent in TARGETS:
        months_with_data = set()
        for plat in ['instagram', 'twitter', 'tiktok', 'youtube']:
            months_with_data.update(output[talent][plat].keys())
        print(f"{talent}: {sorted(months_with_data)}")

    # Save to JSON (both locations)
    output_path1 = '/Users/shuosakapc/Documents/Claude/Projects/社内タレント情報/follower_data.json'
    output_path2 = '/Users/shuosakapc/Library/Application Support/Claude/local-agent-mode-sessions/a59ed77e-4b6c-4f14-8402-dbe7c66ed45f/e867c526-6e59-45b0-992d-bc7992b984b0/local_8463bb6c-882e-4534-9e5b-940f6e42a74f/outputs/follower_data.json'
    for output_path in [output_path1, output_path2]:
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print(f"Saved to {output_path}", file=sys.stderr)
        except Exception as e:
            print(f"Error saving to {output_path}: {e}", file=sys.stderr)

    # Also print full JSON
    print("\n--- Full JSON Output ---")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
