#!/bin/bash
cd "$(dirname "$0")"
python3 debug2024.py 2>&1 | tee debug2024_output.log
echo "Done! Press Enter to close."
read
