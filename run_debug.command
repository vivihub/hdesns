#!/bin/bash
cd "$(dirname "$0")"
python3 debug_extract.py 2>&1 | tee debug_output.log
echo "Done! Press Enter to close."
read
