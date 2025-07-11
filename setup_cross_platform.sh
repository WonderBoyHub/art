#!/bin/bash

# Cross-Platform Pixel Art Collection Setup Script
# Detects the operating system and runs the appropriate setup

echo "🎨 Pixel Art Collection - Cross-Platform Setup"
echo "=============================================="

# Detect operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if [ -f /proc/cpuinfo ] && grep -q "Raspberry Pi" /proc/cpuinfo; then
        echo "🍓 Detected: Raspberry Pi (Linux)"
        echo "Running Raspberry Pi setup..."
        ./setup.sh
    else
        echo "🐧 Detected: Linux (not Raspberry Pi)"
        echo "⚠️  This collection is optimized for Raspberry Pi 5"
        echo "   but will attempt to install on Linux..."
        ./setup.sh
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "🍎 Detected: macOS"
    echo "Running macOS setup..."
    ./setup_macos.sh
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "🪟 Detected: Windows"
    echo "❌ Windows setup not yet implemented."
    echo "   Please use WSL (Windows Subsystem for Linux) and run:"
    echo "   ./setup.sh"
    exit 1
else
    # Unknown
    echo "❓ Unknown operating system: $OSTYPE"
    echo "   Please run the appropriate setup script manually:"
    echo "   - Raspberry Pi / Linux: ./setup.sh"
    echo "   - macOS: ./setup_macos.sh"
    exit 1
fi 