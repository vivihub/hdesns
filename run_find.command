#!/bin/bash
cd "$(dirname "$0")"
python3 find_accounts.py 2>&1 | tee find_output.log
echo "Done! Press Enter to close."
read
