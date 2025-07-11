#!/bin/bash
# Activate virtual environment and run the art launcher
cd "$(dirname "$0")"
source venv/bin/activate
python3 run_art.py
