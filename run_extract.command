#!/bin/bash
# Double-click this file in Finder to run on Mac
cd "$(dirname "$0")"
python3 extract_historical.py 2>&1 | tee extract_output.log
echo "Done! Press Enter to close."
read
