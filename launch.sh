#!/bin/bash
# Suno Prompt Hub Launcher (Mac/Linux)
# On Mac: right-click → Open With → Terminal
# Or: chmod +x launch.sh && ./launch.sh

cd "$(dirname "$0")"

if command -v python3 &>/dev/null; then
    python3 launch.py
elif command -v python &>/dev/null; then
    python launch.py
else
    echo "Python not found. Install from https://www.python.org"
    read -p "Press Enter to exit..."
fi
