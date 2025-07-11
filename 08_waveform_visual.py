#!/usr/bin/env python3
"""
Interactive Waveform Visualizer - Audio-responsive wave patterns
Perfect for Raspberry Pi 5 with 3.5" display
PIXEL ART INTERACTIVE VERSION
"""

import pygame
import random
import math
import time
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Waveform Visualizer")

# Fullscreen support
fullscreen = False

clock = pygame.time.Clock()
start_time = time.time()

def toggle_fullscreen():
    """Toggle fullscreen mode"""
    global screen, fullscreen
    
    if fullscreen:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        fullscreen = False
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        fullscreen = True

def return_to_launcher():
    """Return to the main launcher"""
    pygame.quit()
    try:
        subprocess.run([sys.executable, "run_art.py"], check=True)
    except Exception as e:
        print(f"Could not return to launcher: {e}")
    finally:
        sys.exit(0)

# Cyberpunk color palette
NEON_CYAN = (0, 255, 255)
NEON_PINK = (255, 20, 147)
NEON_GREEN = (57, 255, 20)
NEON_PURPLE = (191, 64, 191)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 165, 0)
CYBER_BLACK = (10, 10, 25)
CYBER_DARK = (25, 25, 50)
CYBER_BLUE = (0, 100, 200)

# Load or create pixel font
def create_pixel_font(size):
    """Create or load pixel-style font"""
    try:
        # Try to load a pixel font if available
        font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'pixel.ttf')
        if os.path.exists(font_path):
            return pygame.font.Font(font_path, size)
    except:
        pass
    
    # Fallback to system font with pixel-like appearance
    return pygame.font.Font(None, size)

# Colors and timing
clock = pygame.time.Clock()
start_time = time.time()

class CyberpunkUI:
    """Retro-cyberpunk UI elements"""
    
    def __init__(self):
        self.font_large = create_pixel_font(24)
        self.font_medium = create_pixel_font(18)
        self.font_small = create_pixel_font(14)
        self.font_tiny = create_pixel_font(12)
        
        # Animation variables
        self.glow_phase = 0
        self.scanline_offset = 0
        
    def draw_scanlines(self, surface):
        """Draw CRT-style scanlines"""
        self.scanline_offset = (self.scanline_offset + 1) % 4
        
        for y in range(self.scanline_offset, HEIGHT, 4):
            pygame.draw.line(surface, (0, 0, 0, 30), (0, y), (WIDTH, y))
            
        # Add subtle horizontal blur lines
        for y in range(0, HEIGHT, 2):
            alpha = 10 + 5 * math.sin(time.time() * 2 + y * 0.1)
            color = (*CYBER_DARK, int(alpha))
            pygame.draw.line(surface, color[:3], (0, y), (WIDTH, y))
    
    def draw_glowing_border(self, surface, rect, color, thickness=2):
        """Draw a glowing neon border"""
        self.glow_phase += 0.1
        
        # Multiple border layers for glow effect
        for i in range(thickness, 0, -1):
            alpha = int(100 + 50 * math.sin(self.glow_phase) * (thickness - i + 1) / thickness)
            glow_color = (*color, min(255, alpha))
            
            # Draw the border rectangle
            border_rect = pygame.Rect(rect.x - i, rect.y - i, 
                                    rect.width + 2*i, rect.height + 2*i)
            pygame.draw.rect(surface, glow_color[:3], border_rect, 1)
    
    def draw_cyber_panel(self, surface, rect, title="", alpha=200):
        """Draw a cyberpunk-style panel"""
        # Main panel background
        panel_surface = pygame.Surface((rect.width, rect.height))
        panel_surface.set_alpha(alpha)
        panel_surface.fill(CYBER_BLACK)
        surface.blit(panel_surface, rect)
        
        # Glowing border
        self.draw_glowing_border(surface, rect, NEON_CYAN, 3)
        
        # Corner decorations
        corner_size = 8
        corners = [
            (rect.x, rect.y),
            (rect.x + rect.width - corner_size, rect.y),
            (rect.x, rect.y + rect.height - corner_size),
            (rect.x + rect.width - corner_size, rect.y + rect.height - corner_size)
        ]
        
        for corner_x, corner_y in corners:
            pygame.draw.rect(surface, NEON_PINK, 
                           (corner_x, corner_y, corner_size, corner_size))
            pygame.draw.rect(surface, NEON_CYAN, 
                           (corner_x + 2, corner_y + 2, corner_size - 4, corner_size - 4))
        
        # Title bar if provided
        if title:
            title_rect = pygame.Rect(rect.x + 10, rect.y - 15, rect.width - 20, 20)
            title_surface = pygame.Surface((title_rect.width, title_rect.height))
            title_surface.fill(CYBER_BLACK)
            title_surface.set_alpha(240)
            surface.blit(title_surface, title_rect)
            
            title_text = self.font_small.render(f"▶ {title} ◀", True, NEON_GREEN)
            title_pos = (title_rect.x + 5, title_rect.y + 2)
            surface.blit(title_text, title_pos)
    
    def draw_cyber_text(self, surface, text, pos, color=NEON_CYAN, font=None, glow=True):
        """Draw text with cyberpunk styling"""
        if font is None:
            font = self.font_small
            
        if glow:
            # Draw glow effect
            for offset in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                glow_pos = (pos[0] + offset[0], pos[1] + offset[1])
                glow_text = font.render(text, True, (color[0]//4, color[1]//4, color[2]//4))
                surface.blit(glow_text, glow_pos)
        
        # Main text
        main_text = font.render(text, True, color)
        surface.blit(main_text, pos)
    
    def draw_progress_bar(self, surface, rect, value, max_value, color=NEON_GREEN):
        """Draw a cyberpunk-style progress bar"""
        # Background
        pygame.draw.rect(surface, CYBER_DARK, rect)
        self.draw_glowing_border(surface, rect, color, 1)
        
        # Fill
        if max_value > 0:
            fill_width = int((value / max_value) * (rect.width - 4))
            fill_rect = pygame.Rect(rect.x + 2, rect.y + 2, fill_width, rect.height - 4)
            pygame.draw.rect(surface, color, fill_rect)
            
            # Animated fill effect
            for i in range(0, fill_width, 4):
                alpha = int(100 + 50 * math.sin(time.time() * 10 + i * 0.1))
                bright_color = tuple(min(255, c + alpha//3) for c in color)
                pygame.draw.line(surface, bright_color, 
                               (rect.x + 2 + i, rect.y + 2), 
                               (rect.x + 2 + i, rect.y + rect.height - 2))

class InteractiveWaveform:
    def __init__(self):
        # Wave parameters
        self.frequency = 1.0
        self.amplitude = 1.0
        self.wave_speed = 1.0
        self.wave_type = 0  # 0: Sine, 1: Saw, 2: Square, 3: Triangle, 4: Noise
        self.color_mode = 0  # 0: Cyberpunk, 1: Neon, 2: Matrix, 3: Synthwave, 4: Retro
        self.num_waves = 4
        self.brightness = 1.0
        self.glow_intensity = 0.5
        
        # UI system
        self.ui = CyberpunkUI()
        
        # Wave types
        self.wave_types = {
            0: "SINE.WAVE",
            1: "SAW.WAVE",
            2: "SQUARE.WAVE",
            3: "TRIANGLE.WAVE",
            4: "NOISE.WAVE"
        }
        
        # Color palettes
        self.color_modes = {
            0: "CYBERPUNK.CORE",
            1: "NEON.DREAMS", 
            2: "MATRIX.CODE",
            3: "SYNTHWAVE.80s",
            4: "RETRO.FUTURE"
        }
        
        # Create wave layers
        self.waves = []
        self.regenerate_waves()
        
        # Spectrum analyzer
        self.spectrum_bars = 32
        self.spectrum_data = [0] * self.spectrum_bars
    
    def regenerate_waves(self):
        """Regenerate wave layers"""
        self.waves = []
        for i in range(self.num_waves):
            wave = {
                'frequency': 0.02 + i * 0.005,
                'amplitude': 40 - i * 5,
                'phase': i * 0.5,
                'color_offset': i * 60,
                'y_offset': -60 + i * 40
            }
            self.waves.append(wave)
    
    def get_color_palette(self, hue, intensity, wave_index):
        """Get color based on selected cyberpunk palette"""
        base_intensity = intensity * self.brightness
        
        if self.color_mode == 0:  # Cyberpunk
            if wave_index % 4 == 0:
                r = int(255 * min(1.0, base_intensity + 0.3))
                g = int(100 * max(0, base_intensity - 0.2))
                b = int(255 * max(0.3, base_intensity))
            elif wave_index % 4 == 1:
                r = int(255 * base_intensity)
                g = int(20 * base_intensity)
                b = int(147 * base_intensity)
            elif wave_index % 4 == 2:
                r = int(57 * base_intensity)
                g = int(255 * base_intensity)
                b = int(20 * base_intensity)
            else:
                r = int(255 * base_intensity)
                g = int(255 * base_intensity)
                b = int(0 * base_intensity)
        elif self.color_mode == 1:  # Neon
            r = int(255 * abs(math.sin(hue * math.pi / 180)) * base_intensity)
            g = int(255 * abs(math.sin((hue + 120) * math.pi / 180)) * base_intensity)
            b = int(255 * abs(math.sin((hue + 240) * math.pi / 180)) * base_intensity)
        elif self.color_mode == 2:  # Matrix
            r = int(50 * max(0, base_intensity - 0.5))
            g = int(255 * min(1.0, base_intensity + 0.2))
            b = int(50 * max(0, base_intensity - 0.7))
        elif self.color_mode == 3:  # Synthwave
            r = int(255 * (0.8 + 0.2 * math.sin(hue * math.pi / 180)) * base_intensity)
            g = int(100 * (0.5 + 0.5 * math.sin((hue + 90) * math.pi / 180)) * base_intensity)
            b = int(255 * (0.9 + 0.1 * math.sin((hue + 180) * math.pi / 180)) * base_intensity)
        else:  # Retro Future
            # Quantize to 8-bit palette
            val = int(base_intensity * 15) / 15
            r = int(255 * (val if val > 0.4 else 0.1))
            g = int(255 * (val if 0.2 < val < 0.9 else 0.1))
            b = int(255 * (val if val < 0.7 else 0.1))
        
        return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    def calculate_wave_value(self, x, time_val, wave_params):
        """Calculate wave value based on wave type"""
        phase = wave_params['phase'] + time_val * self.wave_speed
        freq = wave_params['frequency'] * self.frequency
        
        if self.wave_type == 0:  # Sine
            return math.sin(x * freq + phase)
        elif self.wave_type == 1:  # Saw
            return 2 * ((x * freq + phase) % (2 * math.pi)) / (2 * math.pi) - 1
        elif self.wave_type == 2:  # Square
            return 1 if math.sin(x * freq + phase) > 0 else -1
        elif self.wave_type == 3:  # Triangle
            saw = 2 * ((x * freq + phase) % (2 * math.pi)) / (2 * math.pi) - 1
            return 2 * abs(saw) - 1
        else:  # Noise
            random.seed(int(x * freq + phase * 100))
            return random.uniform(-1, 1)
    
    def draw_waveforms(self, surface, time_val):
        """Draw waveform with pixel art style"""
        for wave_index, wave in enumerate(self.waves):
            # Calculate wave points
            points = []
            for x in range(0, WIDTH, 2):
                wave_val = self.calculate_wave_value(x, time_val, wave)
                y = HEIGHT // 2 + wave['y_offset'] + int(wave_val * wave['amplitude'] * self.amplitude)
                if 0 <= y < HEIGHT:
                    points.append((x, y))
            
            if len(points) > 1:
                # Calculate color
                hue = (wave['color_offset'] + time_val * 50) % 360
                intensity = 0.8 + 0.2 * math.sin(time_val * 2 + wave_index)
                color = self.get_color_palette(hue, intensity, wave_index)
                
                # Draw main wave line
                pygame.draw.lines(surface, color, False, points, 3)
                
                # Draw glow effect
                if self.glow_intensity > 0:
                    glow_color = tuple(int(c * self.glow_intensity) for c in color)
                    pygame.draw.lines(surface, glow_color, False, points, 6)
    
    def update_spectrum(self, time_val):
        """Update spectrum analyzer data"""
        for i in range(self.spectrum_bars):
            # Simulate spectrum data with multiple harmonics
            freq = (i + 1) * 0.2
            amplitude = 0
            
            # Add multiple harmonics
            for harmonic in range(1, 4):
                amplitude += (1 / harmonic) * abs(math.sin(time_val * freq * harmonic * self.frequency))
            
            # Add some randomness
            amplitude += random.uniform(-0.1, 0.1)
            
            # Smooth the transition
            target = max(0, min(1, amplitude))
            self.spectrum_data[i] = self.spectrum_data[i] * 0.7 + target * 0.3
    
    def draw_spectrum_analyzer(self, surface, time_val):
        """Draw spectrum analyzer bars"""
        bar_width = WIDTH // self.spectrum_bars
        
        for i in range(self.spectrum_bars):
            x = i * bar_width
            height = int(self.spectrum_data[i] * HEIGHT // 3)
            
            # Color based on frequency
            hue = (i * 11 + time_val * 50) % 360
            intensity = self.spectrum_data[i] * 0.8 + 0.2
            color = self.get_color_palette(hue, intensity, i)
            
            # Draw bar
            if height > 0:
                rect = pygame.Rect(x, HEIGHT - height, bar_width - 2, height)
                pygame.draw.rect(surface, color, rect)
                
                # Draw reflection
                if self.glow_intensity > 0:
                    reflection_color = tuple(int(c * self.glow_intensity * 0.3) for c in color)
                    reflection_rect = pygame.Rect(x, HEIGHT - height - 10, bar_width - 2, 10)
                    pygame.draw.rect(surface, reflection_color, reflection_rect)

    def draw_center_line(self, surface):
        """Draw center reference line"""
        pygame.draw.line(surface, CYBER_DARK, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)
    
    def draw_particles(self, surface, time_val):
        """Draw floating particles"""
        for i in range(int(20 * self.amplitude)):
            x = (time_val * 50 + i * 37) % WIDTH
            y = (time_val * 30 + i * 71) % HEIGHT
            
            # Particle movement based on waves
            wave_influence = 0
            for wave in self.waves:
                wave_val = self.calculate_wave_value(x, time_val, wave)
                wave_influence += wave_val * 0.1
            
            particle_y = y + wave_influence * 10
            
            if 0 <= particle_y < HEIGHT:
                brightness = 0.3 + 0.7 * abs(math.sin(time_val * 2 + i * 0.5))
                color = self.get_color_palette(i * 20, brightness, i)
                size = 1 if brightness < 0.7 else 2
                pygame.draw.circle(surface, color, (int(x), int(particle_y)), size)
    
    def handle_input(self, keys):
        """Handle keyboard input for interactivity"""
        # Frequency controls
        if keys[pygame.K_UP]:
            self.frequency = min(self.frequency + 0.05, 3.0)
        if keys[pygame.K_DOWN]:
            self.frequency = max(self.frequency - 0.05, 0.1)
        
        # Amplitude controls
        if keys[pygame.K_LEFT]:
            self.amplitude = max(self.amplitude - 0.05, 0.1)
        if keys[pygame.K_RIGHT]:
            self.amplitude = min(self.amplitude + 0.05, 2.0)
        
        # Wave speed controls
        if keys[pygame.K_w]:
            self.wave_speed = min(self.wave_speed + 0.05, 3.0)
        if keys[pygame.K_s]:
            self.wave_speed = max(self.wave_speed - 0.05, 0.1)
        
        # Number of waves
        if keys[pygame.K_a]:
            self.num_waves = max(self.num_waves - 1, 1)
            self.regenerate_waves()
        if keys[pygame.K_d]:
            self.num_waves = min(self.num_waves + 1, 8)
            self.regenerate_waves()
        
        # Brightness controls
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.brightness = min(self.brightness + 0.05, 2.0)
        if keys[pygame.K_MINUS]:
            self.brightness = max(self.brightness - 0.05, 0.2)
        
        # Glow intensity
        if keys[pygame.K_PAGEUP]:
            self.glow_intensity = min(self.glow_intensity + 0.05, 1.0)
        if keys[pygame.K_PAGEDOWN]:
            self.glow_intensity = max(self.glow_intensity - 0.05, 0.0)
    
    def cycle_wave_type(self):
        """Cycle to next wave type"""
        self.wave_type = (self.wave_type + 1) % len(self.wave_types)
    
    def cycle_color_mode(self):
        """Cycle to next color mode"""
        self.color_mode = (self.color_mode + 1) % len(self.color_modes)
    
    def reset(self):
        """Reset to initial state"""
        self.frequency = 1.0
        self.amplitude = 1.0
        self.wave_speed = 1.0
        self.wave_type = 0
        self.color_mode = 0
        self.num_waves = 4
        self.brightness = 1.0
        self.glow_intensity = 0.5
        self.regenerate_waves()
    
    def draw_ui(self, surface):
        """Draw cyberpunk UI interface"""
        # Main control panel
        panel_rect = pygame.Rect(10, 10, 300, 140)
        self.ui.draw_cyber_panel(surface, panel_rect, "WAVEFORM.ANALYZER")
        
        # Status indicators
        y_offset = 35
        x_offset = 20
        
        # Frequency with progress bar
        freq_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, freq_rect, self.frequency, 3.0, NEON_GREEN)
        self.ui.draw_cyber_text(surface, f"FREQ: {self.frequency:.1f}", 
                               (x_offset + 210, y_offset - 2), NEON_GREEN, self.ui.font_tiny)
        y_offset += 20
        
        # Amplitude with progress bar
        amp_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, amp_rect, self.amplitude, 2.0, NEON_CYAN)
        self.ui.draw_cyber_text(surface, f"AMP: {self.amplitude:.1f}", 
                               (x_offset + 210, y_offset - 2), NEON_CYAN, self.ui.font_tiny)
        y_offset += 20
        
        # Wave speed with progress bar
        speed_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, speed_rect, self.wave_speed, 3.0, NEON_PURPLE)
        self.ui.draw_cyber_text(surface, f"SPEED: {self.wave_speed:.1f}", 
                               (x_offset + 210, y_offset - 2), NEON_PURPLE, self.ui.font_tiny)
        y_offset += 20
        
        # Number of waves with progress bar
        waves_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, waves_rect, self.num_waves, 8, NEON_YELLOW)
        self.ui.draw_cyber_text(surface, f"WAVES: {self.num_waves}", 
                               (x_offset + 210, y_offset - 2), NEON_YELLOW, self.ui.font_tiny)
        y_offset += 25
        
        # Current modes
        self.ui.draw_cyber_text(surface, f"◆ {self.wave_types[self.wave_type]}", 
                               (x_offset, y_offset), NEON_PINK, self.ui.font_small)
        y_offset += 18
        
        self.ui.draw_cyber_text(surface, f"◇ {self.color_modes[self.color_mode]}", 
                               (x_offset, y_offset), NEON_ORANGE, self.ui.font_small)
        
        # Controls panel
        controls_rect = pygame.Rect(10, HEIGHT - 90, 460, 80)
        self.ui.draw_cyber_panel(surface, controls_rect, "NEURAL.INTERFACE")
        
        # Control instructions
        controls = [
            "↑↓ FREQUENCY ◇ ←→ AMPLITUDE ◇ WS SPEED ◇ AD WAVES",
            "+/- BRIGHTNESS ◇ PGUP/PGDN GLOW ◇ [T] WAVE.TYPE ◇ [C] COLOR",
            "[R] RESET ◇ [H] HIDE.GUI ◇ [ESC] EXIT.PROGRAM"
        ]
        
        y_start = HEIGHT - 75
        for i, control in enumerate(controls):
            color = [NEON_CYAN, NEON_GREEN, NEON_YELLOW][i]
            self.ui.draw_cyber_text(surface, control, 
                                   (20, y_start + i * 16), color, self.ui.font_tiny, False)

def main():
    waveform = InteractiveWaveform()
    running = True
    show_ui = True
    
    while running:
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return_to_launcher()
                elif event.key == pygame.K_F11:
                    toggle_fullscreen()
                elif event.key == pygame.K_h:
                    show_ui = not show_ui
                elif event.key == pygame.K_r:
                    waveform.reset()
                elif event.key == pygame.K_t:
                    waveform.cycle_wave_type()
                elif event.key == pygame.K_c:
                    waveform.cycle_color_mode()
        
        # Handle continuous input
        waveform.handle_input(keys)
        
        # Calculate time-based animation
        current_time = time.time() - start_time
        
        # Update spectrum analyzer
        waveform.update_spectrum(current_time)
        
        # Clear screen
        screen.fill(CYBER_BLACK)
        
        # Draw spectrum analyzer (background)
        waveform.draw_spectrum_analyzer(screen, current_time)
        
        # Draw center reference line
        waveform.draw_center_line(screen)
        
        # Draw waveforms
        waveform.draw_waveforms(screen, current_time)
        
        # Draw particles
        waveform.draw_particles(screen, current_time)
        
        # Draw CRT scanlines
        waveform.ui.draw_scanlines(screen)
        
        # Draw UI if enabled
        if show_ui:
            waveform.draw_ui(screen)
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS for smooth animation
    
    pygame.quit()

if __name__ == "__main__":
    main() 