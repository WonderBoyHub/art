# ◉ CYBERPUNK ART COLLECTION ◉

**Advanced Interactive Art & Simulations for Raspberry Pi 5**

A collection of 12 mesmerizing, interactive cyberpunk-themed art programs optimized for Raspberry Pi 5 with 3.5" displays. Features advanced simulations, realistic physics, genetic algorithms, and immersive visual experiences.

![Cyberpunk Art Collection](https://img.shields.io/badge/Cyberpunk-Art%20Collection-purple?style=for-the-badge&logo=raspberry-pi)
![Raspberry Pi 5](https://img.shields.io/badge/Raspberry%20Pi-5-red?style=for-the-badge&logo=raspberry-pi)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)

---

## 🚀 **ONE-COMMAND INSTALLATION**

### **For Raspberry Pi:**
```bash
wget -O setup.sh https://raw.githubusercontent.com/WonderBoyHub/art/main/setup_and_launch.sh && chmod +x setup.sh && ./setup.sh
```

### **Or clone and setup:**
```bash
git clone https://github.com/WonderBoyHub/art.git
cd art
chmod +x setup_and_launch.sh
./setup_and_launch.sh
```

The setup script automatically:
- ✅ Detects Raspberry Pi hardware
- ✅ Installs all dependencies (Python, pygame, numpy)
- ✅ Optimizes performance settings
- ✅ Creates desktop shortcuts
- ✅ Configures display settings
- ✅ Launches the art collection

---

## 🎨 **FEATURED ART PROGRAMS**

### **🛸 Advanced Warp Drive Simulator**
- **Complete space navigation simulation**
- Multiple warp drive systems (Quantum, Hyperspace, Wormhole)
- Fuel management, hull integrity, environmental hazards
- Navigation computer with galactic coordinates
- Emergency systems and auto pilot

### **🧬 Advanced Ecosystem Simulator** 
- **Multi-species life simulation with evolution**
- 5 species with predator-prey dynamics
- Genetic algorithms with 6 inheritable traits
- Environmental simulation (climate, seasons, disasters)
- Population dynamics and ecosystem balance

### **🔥 Interactive Particle Fire**
- Realistic fire physics with wind effects
- 4 fire modes (Normal, Torch, Campfire, Inferno)
- 4 color palettes with spark effects
- Interactive intensity and wind controls

### **🌊 Interactive Water Ripples**
- Advanced wave physics simulation
- Mouse-interactive ripple creation
- 4 wave types with interference patterns
- Real-time parameter adjustment

### **🧬 Interactive DNA Helix**
- Double helix visualization
- Genetic base pair simulation
- Complementary strand logic
- Statistical analysis display

### **🌌 Interactive Spiral Galaxy**
- Rotating galaxy with multiple stellar types
- Gravitational physics simulation
- Nebula effects and galactic center
- Variable star density and properties

### **🎵 Interactive Waveform Visualizer**
- Audio-responsive wave patterns
- 5 wave types with spectrum analyzer
- Floating particle effects
- Dynamic color cycling

### **Plus 5 More Interactive Art Programs:**
- Plasma Effect with 5 color modes
- Matrix Rain with 6 character sets
- Mandelbrot Zoom with navigation
- Rainbow Tunnel with rotation effects
- Lightning Effect with storm modes

---

## 🎮 **UNIVERSAL CONTROLS**

**All Programs Support:**
- **F11**: Toggle Fullscreen
- **ESC**: Return to Launcher
- **H**: Toggle UI/Help Display

**Program-Specific Controls:**
- **Arrow Keys**: Navigation/Speed Control
- **WASD**: Advanced Navigation (where applicable)
- **Mouse**: Interactive Drawing/Effects
- **Space**: Play/Pause or Special Functions
- **T/C/V/M**: Mode Cycling (Type/Color/View/Mode)
- **R**: Reset to Defaults

---

## 🔧 **TECHNICAL SPECIFICATIONS**

### **System Requirements:**
- **Raspberry Pi 5** (recommended) or Pi 4
- **3.5" Display** (480x320) or any HDMI display
- **1GB RAM** minimum, 2GB+ recommended
- **microSD Card** 16GB+ (Class 10)
- **Raspbian OS** (Bullseye or newer)

### **Performance Optimizations:**
- **60 FPS** target with dynamic scaling
- **Multi-threaded** particle systems
- **Memory-efficient** object pooling
- **GPU acceleration** where available
- **CPU governor** optimization
- **Cache-friendly** algorithms

### **Dependencies:**
- Python 3.8+
- pygame 2.0+
- numpy 1.19+
- psutil (for system monitoring)

---

## 📦 **INSTALLATION OPTIONS**

### **Option 1: Automated Setup (Recommended)**
```bash
./setup_and_launch.sh                    # Full setup and launch
./setup_and_launch.sh --setup-only       # Setup only
./setup_and_launch.sh --launch-only      # Launch only
./setup_and_launch.sh --enable-autostart # Setup with autostart
./setup_and_launch.sh --verify           # Verify installation
```

### **Option 2: Manual Installation**
```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-pygame python3-numpy git

# Install Python packages
pip3 install pygame numpy psutil

# Clone and run
git clone https://github.com/WonderBoyHub/art.git
cd art
python3 run_art.py
```

### **Option 3: Virtual Environment**
```bash
python3 -m venv cyberpunk-art
source cyberpunk-art/bin/activate
pip install -r requirements.txt
python3 run_art.py
```

---

## 🖥️ **DISPLAY CONFIGURATION**

### **3.5" TFT Display Setup:**
```bash
# Add to /boot/config.txt
hdmi_group=2
hdmi_mode=87
hdmi_cvt=480 320 60 6 0 0 0
hdmi_drive=1
```

### **Auto-start on Boot:**
```bash
# Enable with setup script
./setup_and_launch.sh --enable-autostart

# Or manually add to ~/.config/autostart/
```

### **Performance Tuning:**
```bash
# GPU memory split
sudo raspi-config -> Advanced Options -> Memory Split -> 128

# CPU governor
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

---

## 🎯 **USAGE SCENARIOS**

### **🏠 Home Entertainment:**
- **Ambient Art Display**: Continuous visual entertainment
- **Interactive Learning**: Educational simulations for all ages
- **Party Mode**: Engaging visuals for gatherings

### **🏫 Educational:**
- **Physics Demonstrations**: Wave propagation, particle dynamics
- **Biology Simulations**: Ecosystem dynamics, genetic algorithms
- **Computer Science**: Cellular automata, emergent behavior

### **🎨 Artistic Installation:**
- **Gallery Display**: Automated art exhibition
- **Interactive Kiosk**: Touch-free interaction via sensors
- **Digital Signage**: Eye-catching displays

---

## 🛠️ **TROUBLESHOOTING**

### **Common Issues:**

**Display Problems:**
```bash
# Check display connection
tvservice -s

# Test HDMI output
raspi-config -> Display Options
```

**Performance Issues:**
```bash
# Check system resources
htop
free -h

# Optimize GPU memory
sudo raspi-config -> Advanced Options -> Memory Split
```

**Python Module Errors:**
```bash
# Reinstall dependencies
./setup_and_launch.sh --verify
pip3 install --upgrade pygame numpy
```

### **Debug Mode:**
```bash
# Run with debug output
python3 run_art.py --debug

# Check system compatibility
python3 test_compatibility.py
```

---

## 🤝 **CONTRIBUTING**

Contributions welcome! Areas for enhancement:
- **New Art Programs**: Additional visual effects and simulations
- **Performance Optimization**: Faster algorithms and rendering
- **Platform Support**: Additional device compatibility
- **Educational Content**: Tutorials and documentation

### **Development Setup:**
```bash
git clone https://github.com/WonderBoyHub/art.git
cd art
python3 -m venv dev-env
source dev-env/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

---

## 📄 **LICENSE**

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 **ACKNOWLEDGMENTS**

- **Raspberry Pi Foundation** for amazing single-board computers
- **pygame Community** for excellent multimedia library
- **NumPy Team** for high-performance computing tools
- **Cyberpunk Aesthetic** inspired by retro-futuristic design

---

## 🔗 **LINKS**

- **GitHub Repository**: [https://github.com/WonderBoyHub/art](https://github.com/WonderBoyHub/art)
- **Issues & Support**: [GitHub Issues](https://github.com/WonderBoyHub/art/issues)
- **Raspberry Pi Guide**: [Official Documentation](https://www.raspberrypi.org/documentation/)
- **pygame Documentation**: [pygame.org](https://www.pygame.org/docs/)

---

**🎮 Ready to dive into the cyberpunk art experience? Run the setup script and let the simulations begin! 🚀** 