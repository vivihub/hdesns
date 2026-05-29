#!/bin/bash
cd "$(dirname "$0")"
python3 check_sections.py 2>&1 | tee check_output.log
echo "Done! Press Enter to close."
read
