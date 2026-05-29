#!/bin/bash
cd "$(dirname "$0")"
python3 debug2.py 2>&1 | tee debug2_output.log
echo "Done! Press Enter to close."
read
