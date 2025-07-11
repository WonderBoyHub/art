#!/bin/bash

# Cyberpunk Art Collection - Setup & Launch Script
# Perfect for Raspberry Pi 5 with 3.5" display
# Auto-setup dependencies and launch the interactive art collection

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Art Collection Info
COLLECTION_NAME="◉ CYBERPUNK ART COLLECTION ◉"
VERSION="v2.0"
AUTHOR="Enhanced for Raspberry Pi 5"

echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                                                              ║${NC}"
echo -e "${PURPLE}║${CYAN}    ◉ CYBERPUNK ART COLLECTION SETUP & LAUNCHER ◉${PURPLE}         ║${NC}"
echo -e "${PURPLE}║                                                              ║${NC}"
echo -e "${PURPLE}║${GREEN}    Advanced Interactive Art & Simulations ${VERSION}${PURPLE}            ║${NC}"
echo -e "${PURPLE}║${YELLOW}    Optimized for Raspberry Pi 5 + 3.5\" Display${PURPLE}           ║${NC}"
echo -e "${PURPLE}║                                                              ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to print status messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║ $1${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
}

# Check if running on Raspberry Pi
check_raspberry_pi() {
    if grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
        PI_MODEL=$(grep "Model" /proc/cpuinfo | cut -d ':' -f 2 | xargs)
        print_success "Detected: $PI_MODEL"
        return 0
    else
        print_warning "Not running on Raspberry Pi - desktop mode"
        return 1
    fi
}

# Check if package is installed
is_package_installed() {
    dpkg -l | grep -q "^ii  $1 " 2>/dev/null
}

# Check if Python package is installed
is_python_package_installed() {
    python3 -c "import $1" 2>/dev/null
}

# Install system dependencies
install_system_dependencies() {
    print_header "INSTALLING SYSTEM DEPENDENCIES"
    
    # Update package list
    print_status "Updating package list..."
    sudo apt update -qq
    
    # Required packages
    PACKAGES=(
        "python3"
        "python3-pip" 
        "python3-dev"
        "python3-pygame"
        "git"
        "curl"
        "htop"
    )
    
    # Optional packages for Pi optimization
    PI_PACKAGES=(
        "python3-numpy"
        "python3-psutil"
        "fonts-dejavu-core"
        "xserver-xorg"
        "xinit"
    )
    
    INSTALL_NEEDED=()
    
    # Check required packages
    for package in "${PACKAGES[@]}"; do
        if ! is_package_installed "$package"; then
            INSTALL_NEEDED+=("$package")
            print_status "Will install: $package"
        else
            print_success "Already installed: $package"
        fi
    done
    
    # Check Pi-specific packages
    if check_raspberry_pi; then
        for package in "${PI_PACKAGES[@]}"; do
            if ! is_package_installed "$package"; then
                INSTALL_NEEDED+=("$package")
                print_status "Will install (Pi): $package"
            fi
        done
    fi
    
    # Install missing packages
    if [ ${#INSTALL_NEEDED[@]} -gt 0 ]; then
        print_status "Installing ${#INSTALL_NEEDED[@]} packages..."
        sudo apt install -y "${INSTALL_NEEDED[@]}"
        print_success "System packages installed successfully"
    else
        print_success "All system packages already installed"
    fi
}

# Install Python dependencies
install_python_dependencies() {
    print_header "INSTALLING PYTHON DEPENDENCIES"
    
    PYTHON_PACKAGES=(
        "pygame"
        "numpy" 
        "psutil"
    )
    
    PIP_INSTALL_NEEDED=()
    
    for package in "${PYTHON_PACKAGES[@]}"; do
        if ! is_python_package_installed "$package"; then
            PIP_INSTALL_NEEDED+=("$package")
            print_status "Will install: python3-$package"
        else
            print_success "Already installed: python3-$package"
        fi
    done
    
    if [ ${#PIP_INSTALL_NEEDED[@]} -gt 0 ]; then
        print_status "Installing Python packages via pip..."
        
        # Upgrade pip first
        python3 -m pip install --upgrade pip --user
        
        # Install packages
        for package in "${PIP_INSTALL_NEEDED[@]}"; do
            print_status "Installing $package..."
            python3 -m pip install "$package" --user
        done
        
        print_success "Python packages installed successfully"
    else
        print_success "All Python packages already installed"
    fi
}

# Setup display configuration for Pi
setup_pi_display() {
    if ! check_raspberry_pi; then
        return 0
    fi
    
    print_header "OPTIMIZING DISPLAY FOR RASPBERRY PI"
    
    # Check if running in GUI environment
    if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
        print_success "GUI environment detected"
    else
        print_status "Setting up minimal X11 environment..."
        
        # Create basic xinitrc if it doesn't exist
        if [ ! -f "$HOME/.xinitrc" ]; then
            cat > "$HOME/.xinitrc" << 'EOF'
#!/bin/bash
# Basic X11 setup for art collection
xset -dpms     # Disable DPMS (Energy Star) features
xset s off     # Disable screen saver
xset s noblank # Don't blank the video device
exec python3 /home/pi/art/run_art.py
EOF
            chmod +x "$HOME/.xinitrc"
            print_success "Created ~/.xinitrc for auto-launch"
        fi
    fi
    
    # GPU memory split optimization
    GPU_MEM=$(vcgencmd get_mem gpu | cut -d= -f2 | cut -d= -f1)
    if [ "${GPU_MEM%M}" -lt 128 ]; then
        print_warning "GPU memory is ${GPU_MEM}, consider increasing to 128M"
        print_status "Run: sudo raspi-config -> Advanced Options -> Memory Split -> 128"
    else
        print_success "GPU memory: $GPU_MEM (sufficient)"
    fi
}

# Create desktop launcher
create_desktop_launcher() {
    print_header "CREATING DESKTOP INTEGRATION"
    
    # Create desktop shortcut
    DESKTOP_DIR="$HOME/Desktop"
    if [ -d "$DESKTOP_DIR" ]; then
        cat > "$DESKTOP_DIR/Cyberpunk Art Collection.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Cyberpunk Art Collection
Comment=Interactive Art & Simulations
Exec=$PWD/setup_and_launch.sh --launch-only
Icon=$PWD/icon.png
Terminal=false
Categories=Graphics;Education;Game;
StartupNotify=true
EOF
        chmod +x "$DESKTOP_DIR/Cyberpunk Art Collection.desktop"
        print_success "Desktop shortcut created"
    fi
    
    # Create application menu entry
    APPS_DIR="$HOME/.local/share/applications"
    mkdir -p "$APPS_DIR"
    cat > "$APPS_DIR/cyberpunk-art.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Cyberpunk Art Collection
Comment=Interactive Art & Simulations for Raspberry Pi
Exec=$PWD/setup_and_launch.sh --launch-only
Icon=$PWD/icon.png
Terminal=false
Categories=Graphics;Education;Game;
Keywords=art;animation;simulation;cyberpunk;pi;
StartupNotify=true
EOF
    print_success "Application menu entry created"
}

# Setup autostart (optional)
setup_autostart() {
    if [ "$1" != "--enable-autostart" ]; then
        return 0
    fi
    
    print_header "SETTING UP AUTOSTART"
    
    # Create autostart entry
    AUTOSTART_DIR="$HOME/.config/autostart"
    mkdir -p "$AUTOSTART_DIR"
    
    cat > "$AUTOSTART_DIR/cyberpunk-art.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Cyberpunk Art Collection
Exec=$PWD/setup_and_launch.sh --launch-only
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF
    
    print_success "Autostart configured - will launch on login"
    print_warning "Disable with: rm ~/.config/autostart/cyberpunk-art.desktop"
}

# Verify installation
verify_installation() {
    print_header "VERIFYING INSTALLATION"
    
    # Check Python
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 --version 2>&1)
        print_success "Python: $PYTHON_VERSION"
    else
        print_error "Python3 not found!"
        return 1
    fi
    
    # Check required Python modules
    REQUIRED_MODULES=("pygame" "numpy" "psutil")
    for module in "${REQUIRED_MODULES[@]}"; do
        if python3 -c "import $module" 2>/dev/null; then
            print_success "Python module: $module ✓"
        else
            print_error "Python module missing: $module"
            return 1
        fi
    done
    
    # Check art files
    REQUIRED_FILES=("run_art.py" "requirements.txt")
    for file in "${REQUIRED_FILES[@]}"; do
        if [ -f "$file" ]; then
            print_success "Art file: $file ✓"
        else
            print_error "Missing file: $file"
            return 1
        fi
    done
    
    print_success "Installation verification complete!"
    return 0
}

# Launch the art collection
launch_art_collection() {
    print_header "LAUNCHING CYBERPUNK ART COLLECTION"
    
    # Change to script directory
    cd "$(dirname "$0")"
    
    # Check if we're in a GUI environment
    if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
        if check_raspberry_pi; then
            print_status "Starting X11 session..."
            startx
            return $?
        else
            print_warning "No display environment detected"
            print_status "Attempting to run in current terminal..."
        fi
    fi
    
    # Launch the main art program
    print_status "Starting interactive art collection..."
    print_status "Press Ctrl+C to exit, or use ESC in programs to return to launcher"
    echo ""
    
    # Run with nice priority for better performance
    nice -n -10 python3 run_art.py
}

# Performance optimization
optimize_performance() {
    if ! check_raspberry_pi; then
        return 0
    fi
    
    print_header "OPTIMIZING PERFORMANCE"
    
    # CPU governor
    if [ -f /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor ]; then
        CURRENT_GOV=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor)
        print_status "Current CPU governor: $CURRENT_GOV"
        
        if [ "$CURRENT_GOV" != "performance" ]; then
            print_status "Setting CPU governor to performance..."
            echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor >/dev/null
        fi
    fi
    
    # Disable swap for better performance (optional)
    if [ "$(swapon --show)" ]; then
        print_status "Swap is enabled (may impact performance)"
        print_status "Consider disabling: sudo dphys-swapfile swapoff"
    fi
    
    print_success "Performance optimization complete"
}

# Create installation summary
create_summary() {
    SUMMARY_FILE="INSTALLATION_SUMMARY.txt"
    cat > "$SUMMARY_FILE" << EOF
CYBERPUNK ART COLLECTION - INSTALLATION SUMMARY
============================================

Installation Date: $(date)
System: $(uname -a)
Python Version: $(python3 --version 2>&1)

INSTALLED PROGRAMS:
- Advanced Warp Drive Simulator (05_starfield.py)
- Advanced Ecosystem Simulator (06_game_of_life.py) 
- Interactive Particle Fire (02_particle_fire.py)
- Interactive Water Ripples (11_water_ripples.py)
- Interactive DNA Helix (12_dna_helix.py)
- Interactive Spiral Galaxy (09_spiral_galaxy.py)
- Interactive Waveform Visual (08_waveform_visual.py)
- Plus 5 more interactive art programs!

FEATURES:
✓ Fullscreen support (F11)
✓ ESC navigation back to launcher
✓ Advanced simulations with realistic physics
✓ Multiple interactive modes and controls
✓ Cyberpunk retro aesthetic
✓ Optimized for Raspberry Pi 5 + 3.5" display

USAGE:
- Run: ./setup_and_launch.sh
- Or: python3 run_art.py
- Navigate with arrow keys, ESC to return to launcher
- F11 for fullscreen mode

CONTROLS:
- Launcher: Arrow keys, Enter to select, ESC to quit
- Programs: ESC returns to launcher, F11 toggles fullscreen
- Each program has unique controls (see on-screen help)

For support or updates, visit:
https://github.com/WonderBoyHub/art
EOF
    
    print_success "Installation summary saved to: $SUMMARY_FILE"
}

# Main setup function
main_setup() {
    print_status "Starting setup process..."
    
    # Run setup steps
    install_system_dependencies
    install_python_dependencies
    setup_pi_display
    optimize_performance
    create_desktop_launcher
    setup_autostart "$@"
    
    if verify_installation; then
        create_summary
        print_success "Setup completed successfully!"
        echo ""
        print_status "You can now run the art collection with:"
        echo -e "  ${GREEN}./setup_and_launch.sh --launch-only${NC}"
        echo -e "  ${GREEN}python3 run_art.py${NC}"
        echo ""
        return 0
    else
        print_error "Setup verification failed!"
        return 1
    fi
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "Cyberpunk Art Collection Setup & Launcher"
        echo ""
        echo "Usage:"
        echo "  $0                    # Full setup and launch"
        echo "  $0 --setup-only      # Setup only, don't launch"
        echo "  $0 --launch-only     # Launch only, skip setup"
        echo "  $0 --enable-autostart # Setup with autostart enabled"
        echo "  $0 --verify          # Verify installation only"
        echo "  $0 --help            # Show this help"
        echo ""
        exit 0
        ;;
    --setup-only)
        main_setup "$@"
        exit $?
        ;;
    --launch-only)
        launch_art_collection
        exit $?
        ;;
    --verify)
        verify_installation
        exit $?
        ;;
    --enable-autostart)
        main_setup "$@"
        if [ $? -eq 0 ]; then
            echo ""
            read -p "Launch the art collection now? (y/N): " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                launch_art_collection
            fi
        fi
        exit $?
        ;;
    "")
        # Default: setup and launch
        main_setup "$@"
        if [ $? -eq 0 ]; then
            echo ""
            read -p "Launch the art collection now? (Y/n): " -n 1 -r
            echo ""
            if [[ ! $REPLY =~ ^[Nn]$ ]]; then
                launch_art_collection
            fi
        fi
        exit $?
        ;;
    *)
        print_error "Unknown option: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac 