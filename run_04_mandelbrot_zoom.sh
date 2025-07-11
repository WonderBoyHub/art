#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 "04_mandelbrot_zoom.py"
