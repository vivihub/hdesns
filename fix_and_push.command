#!/bin/bash
cd "/Users/shusuzuki/Library/Mobile Documents/com~apple~CloudDocs/Claude/Projects/社内タレント情報"
rm -f .git/index.lock
git add -A
git commit -m "Add all files: debug scripts, SNS data, and update talent_manager.html"
git push origin main
echo "✅ Done!"
