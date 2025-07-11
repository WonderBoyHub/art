#!/bin/bash

# Pixel Art Collection Setup Script for Raspberry Pi 5
# This script installs dependencies and sets up the art collection

echo "🎨 Setting up Pixel Art Collection for Raspberry Pi 5..."

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo; then
    echo "⚠️  Warning: This setup is optimized for Raspberry Pi 5"
    echo "   It may work on other systems but performance may vary."
fi

# Update package list
echo "📦 Updating package list..."
sudo apt-get update

# Install Python3 and pip if not already installed
echo "🐍 Installing Python3 and pip..."
sudo apt-get install -y python3 python3-pip

# Install pygame dependencies
echo "🎮 Installing pygame dependencies..."
sudo apt-get install -y python3-pygame

# Install required Python packages
echo "📚 Installing Python packages..."
pip3 install -r requirements.txt

# Make all Python files executable
echo "🔧 Making Python files executable..."
chmod +x *.py

# Create desktop shortcut (optional)
echo "🖥️  Creating desktop shortcut..."
cat > ~/Desktop/PixelArt.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Pixel Art Collection
Comment=Beautiful code art for Raspberry Pi 5
Exec=python3 $(pwd)/run_art.py
Icon=applications-graphics
Terminal=false
Categories=Graphics;Education;
EOF

chmod +x ~/Desktop/PixelArt.desktop

# Enable GPU memory split for better performance
echo "🚀 Optimizing GPU memory split..."
sudo raspi-config nonint do_memory_split 128

# Test installation
echo "🧪 Testing installation..."
python3 -c "import pygame; print('✅ pygame imported successfully')"
python3 -c "import numpy; print('✅ numpy imported successfully')"

echo ""
echo "🎉 Setup complete! 🎉"
echo ""
echo "To run the art collection:"
echo "  python3 run_art.py"
echo ""
echo "Or double-click the desktop shortcut."
echo ""
echo "For best performance:"
echo "  - Use in a dark room"
echo "  - Ensure good ventilation for your Pi"
echo "  - Close unnecessary programs"
echo ""
echo "Enjoy your pixel art experience! 🎨✨" 