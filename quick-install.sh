#!/bin/bash

# Cyberpunk Art Collection - Quick Installer
# Downloads and runs the full setup script from GitHub

echo "◉ CYBERPUNK ART COLLECTION - QUICK INSTALLER ◉"
echo ""
echo "Downloading setup script from GitHub..."

# Download the setup script
curl -L -o cyberpunk-setup.sh https://raw.githubusercontent.com/WonderBoyHub/art/main/setup_and_launch.sh

if [ $? -eq 0 ]; then
    echo "Download successful!"
    chmod +x cyberpunk-setup.sh
    echo ""
    echo "Running setup..."
    ./cyberpunk-setup.sh
else
    echo "Download failed. Please check your internet connection."
    echo ""
    echo "Alternative: Clone the repository manually:"
    echo "git clone https://github.com/WonderBoyHub/art.git"
    echo "cd art"
    echo "./setup_and_launch.sh"
fi 