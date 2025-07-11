#!/bin/bash

# Universal Pixel Art Collection Launcher
# Works on both macOS and Raspberry Pi

echo "🎨 Starting Pixel Art Collection..."

# Check if virtual environment exists (macOS setup)
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if Python3 and pygame are available
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "❌ pygame not found. Please run setup first:"
    echo ""
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  ./setup_macos.sh"
    else
        echo "  ./setup.sh"
    fi
    echo ""
    echo "Or use the cross-platform setup:"
    echo "  ./setup_cross_platform.sh"
    exit 1
fi

# Launch the art collection
echo "🚀 Launching art collection..."
python3 run_art.py 