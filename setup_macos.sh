#!/bin/bash

# Pixel Art Collection Setup Script for macOS
# This script sets up a virtual environment and installs dependencies

echo "🎨 Setting up Pixel Art Collection for macOS..."

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  This setup is for macOS. For Raspberry Pi, use setup.sh"
    exit 1
fi

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python3 first:"
    echo "   brew install python3"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install pip3 first:"
    echo "   curl https://bootstrap.pypa.io/get-pip.py | python3"
    exit 1
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install required packages
echo "📚 Installing Python packages..."
pip install pygame>=2.5.0 numpy>=1.24.0

# Make all Python files executable
echo "🔧 Making Python files executable..."
chmod +x *.py

# Create activation script
echo "📝 Creating activation script..."
cat > run_with_venv.sh << 'EOF'
#!/bin/bash
# Activate virtual environment and run the art launcher
cd "$(dirname "$0")"
source venv/bin/activate
python3 run_art.py
EOF

chmod +x run_with_venv.sh

# Create individual program runners
echo "🎯 Creating program runners..."
for py_file in *.py; do
    if [[ "$py_file" != "run_art.py" && "$py_file" != "run_with_venv.py" ]]; then
        script_name="run_${py_file%.py}.sh"
        cat > "$script_name" << EOF
#!/bin/bash
cd "\$(dirname "\$0")"
source venv/bin/activate
python3 "$py_file"
EOF
        chmod +x "$script_name"
    fi
done

# Test installation
echo "🧪 Testing installation..."
source venv/bin/activate
python3 -c "import pygame; print('✅ pygame imported successfully')"
python3 -c "import numpy; print('✅ numpy imported successfully')"

echo ""
echo "🎉 macOS Setup complete! 🎉"
echo ""
echo "To run the art collection:"
echo "  ./run_with_venv.sh"
echo ""
echo "Or activate the virtual environment manually:"
echo "  source venv/bin/activate"
echo "  python3 run_art.py"
echo ""
echo "Individual programs can be run with:"
echo "  ./run_01_plasma_effect.sh"
echo "  ./run_02_particle_fire.sh"
echo "  ... etc"
echo ""
echo "Note: These programs are optimized for Raspberry Pi 5 with a 3.5\" display"
echo "but will work on macOS with different resolutions."
echo ""
echo "Enjoy your pixel art experience! 🎨✨" 