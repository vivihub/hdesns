#!/bin/bash
cd "$(dirname "$0")"
python3 find_accounts2.py 2>&1 | tee find2_output.log
echo "Done! Press Enter to close."
read
