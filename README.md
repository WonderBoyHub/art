# 🎮 Cyberpunk Pixel Art Collection

> **Retro-futuristic interactive art programs optimized for Raspberry Pi 5 with 3.5" displays**

A stunning collection of **12 interactive pixel art programs** featuring retro-cyberpunk aesthetics, CRT scanlines, neon colors, and immersive GUI elements. Designed for both **Raspberry Pi 5** and **Mac systems**.

## ✨ Features

### 🖥️ Retro-Cyberpunk GUI
- **CRT scanlines** and holographic effects
- **Neon glowing borders** with animated colors
- **Matrix-style background** with digital rain
- **Pixel art typography** and cyberpunk styling
- **Interactive progress bars** and real-time system monitoring

### 🎨 Enhanced Art Programs
- **12 fully interactive** pixel art experiences
- **Keyboard-only controls** for easy navigation
- **Cross-platform compatibility** (Pi 5 + Mac)
- **60 FPS performance** optimized for 3.5" displays
- **Multiple visual modes** and real-time parameter adjustment

### 🎛️ Interactive Controls
Each program features extensive customization:
- **Color palettes** (5-6 modes per program)
- **Pattern variations** and visual effects
- **Speed/intensity controls** with live adjustment
- **Pixel art sizing** for authentic retro feel
- **Easy exit** back to launcher (ESC key)

## 🚀 Quick Start

### Raspberry Pi 5 Setup
```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-pygame

# Clone or download the collection
git clone <repository-url>
cd art

# Install Python packages
pip3 install -r requirements.txt

# Test compatibility
python3 test_compatibility.py

# Launch cyberpunk terminal
python3 run_art.py
```

### Mac Setup
```bash
# Install dependencies
pip3 install -r requirements.txt

# Test compatibility
python3 test_compatibility.py

# Launch cyberpunk terminal
python3 run_art.py
```

## 🎮 Program Gallery

### 🌀 PLASMA.EXE
**Neural pattern simulation with 5 color modes**
- **Controls:** ↑↓ Speed, ←→ Pixel Size, C: Color Mode, P: Pattern
- **Modes:** Cyberpunk, Neon Dreams, Matrix Code, Synthwave, Retro Future
- **Patterns:** Classic Wave, Ripple Scan, Sine Dance, Spiral Vortex

### 🔥 PYRO.SIM  
**Thermal dynamics engine with wind control**
- **Controls:** ↑↓ Intensity, ←→ Wind Force, F: Fire Type, C: Color
- **Types:** Normal Fire, Torch Flame, Campfire, Inferno
- **Colors:** Classic Fire, Blue Flame, Green Flame, Purple Flame

### 💚 MATRIX.TERM
**Data stream visualizer with 6 character encodings**
- **Controls:** ↑↓ Speed, ←→ Density, S: Character Set, C: Color
- **Character Sets:** Classic Matrix, ASCII Digital, Binary Code, Japanese, Block Art, Symbols
- **Rain Patterns:** Random, Wave Pattern, Cascade, Pulse Mode

### 🌌 WARP.DRIVE
**Hyperspace navigator with 4 warp modes**
- **Controls:** ↑↓ Warp Speed, WASD: Navigation, C: Color, M: Mode
- **Warp Modes:** Forward, Spiral Travel, Orbital Motion, Hyperspace
- **Colors:** White Stars, Colorful, Blue Nebula, Red Giant, Green Space, Purple Void

### 🧬 LIFE.SIM
**Cellular automaton lab with 4 rule sets**
- **Controls:** Space: Play/Pause, Mouse: Draw, L: Rules, V: Color
- **Rule Sets:** Classic Conway, HighLife, Maze, Coral
- **Patterns:** Random Fill, Glider Pattern, Oscillators, Still Lifes

### ⚡ TESLA.LAB
**Electrical discharge simulation with 6 colors**
- **Controls:** ↑↓ Frequency, ←→ Intensity, C: Color, B: Type
- **Bolt Types:** Classic, Jagged, Smooth, Chaotic
- **Storm Modes:** Random Storm, Continuous, Directed

## 🎯 Launcher Features

### 🖥️ Cyberpunk Terminal Interface
- **Boot sequence** with animated loading
- **Matrix rain background** and circuit patterns
- **System monitoring** with CPU/Memory displays
- **Glowing UI elements** and neon color cycling
- **Program selection** with hex addresses

### ⌨️ Universal Controls
- **↑↓**: Navigate programs
- **Enter**: Execute program
- **0-9**: Direct program access
- **R**: Random program selection
- **Tab**: Show/hide controls
- **ESC**: Exit system

## 🖼️ Display Optimization

### 3.5" Raspberry Pi Display (480x320)
- **Perfect pixel scaling** for retro aesthetics
- **Optimized UI layout** for small screens
- **Readable fonts** and clear controls
- **Efficient rendering** for smooth 60 FPS

### Cross-Platform Compatibility
- **Automatic display detection**
- **Scalable interface elements**
- **Performance optimization** for different hardware
- **Consistent visual experience** across platforms

## 🔧 Technical Specifications

### System Requirements
- **Python 3.7+** with Pygame 2.5.0+
- **NumPy 1.24.0+** for mathematical operations
- **psutil 5.9.0+** for system monitoring
- **Minimum 512MB RAM** (1GB+ recommended)
- **Hardware acceleration** recommended

### Performance Targets
- **60 FPS** on Raspberry Pi 5
- **Sub-20ms frame times** for responsive controls
- **Cross-platform compatibility** with Mac systems
- **Efficient memory usage** for embedded systems

### File Structure
```
art/
├── 01_plasma_effect.py      # Enhanced plasma with 5 modes
├── 02_particle_fire.py      # Interactive fire simulation  
├── 03_matrix_rain.py        # Matrix code with 6 char sets
├── 04_mandelbrot_zoom.py    # Fractal explorer
├── 05_starfield.py          # Warp drive simulator
├── 06_game_of_life.py       # Cellular automaton lab
├── 07_rainbow_tunnel.py     # Chromatic vortex
├── 08_waveform_visual.py    # Audio spectrum display
├── 09_spiral_galaxy.py      # Stellar formation sim
├── 10_lightning_effect.py   # Tesla laboratory
├── 11_water_ripples.py      # Fluid dynamics
├── 12_dna_helix.py          # Molecular visualization
├── run_art.py               # Cyberpunk launcher
├── test_compatibility.py    # Platform testing
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## 🛠️ Customization

### Adding New Programs
1. Create new Python file following naming convention
2. Implement cyberpunk UI using provided classes
3. Add entry to `ART_PROGRAMS` list in launcher
4. Include control information in `CONTROL_INFO`

### Modifying Visual Themes
- Edit color palettes in individual programs
- Customize UI elements in `CyberpunkUI` classes
- Adjust scanline effects and glow parameters
- Modify background patterns and animations

## 🎨 Visual Examples

### Cyberpunk Aesthetics
- **Neon color schemes** with cyan, pink, green highlights
- **CRT scanlines** for authentic retro feel
- **Glowing borders** with animated pulsing
- **Matrix-style backgrounds** with digital effects
- **Terminal typography** and cyberpunk symbols

### Interactive Elements
- **Real-time parameter adjustment** with visual feedback
- **Animated progress bars** with segmented fills
- **System monitoring** with live CPU/memory display
- **Color-coded status** indicators and mode displays
- **Smooth transitions** between program states

## 🔍 Troubleshooting

### Performance Issues
- Run `python3 test_compatibility.py` for diagnostics
- Increase GPU memory split on Raspberry Pi
- Enable hardware acceleration in system settings
- Reduce pixel sizes for better performance

### Display Problems
- Verify 480x320 resolution support
- Check pygame installation and version
- Test with different display drivers
- Ensure proper hardware connection

### Platform-Specific Issues

#### Raspberry Pi 5
- Enable GPU acceleration: `sudo raspi-config`
- Set GPU memory split: 128MB or higher
- Use performance governor: `sudo cpufreq-set -g performance`
- Consider overclocking for demanding effects

#### Mac Systems  
- Install Xcode command line tools
- Use Homebrew for Python dependencies
- Verify OpenGL acceleration
- Check display scaling settings

## 📝 License

This cyberpunk pixel art collection is designed for educational and artistic purposes. Individual programs may have different licensing terms.

## 🤝 Contributing

Contributions welcome for:
- New interactive art programs
- Enhanced cyberpunk UI elements
- Performance optimizations
- Platform compatibility improvements
- Documentation and examples

---

**◉ CYBER.ART.TERMINAL ◉ - Where retro computing meets pixel art**

*Optimized for Raspberry Pi 5 • Cross-platform compatible • 60 FPS performance* 