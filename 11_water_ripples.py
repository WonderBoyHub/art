#!/usr/bin/env python3
"""
Interactive Water Ripples - Wave physics simulation with cyberpunk aesthetics
Perfect for Raspberry Pi 5 with 3.5" display
RETRO CYBERPUNK PIXEL ART VERSION
"""

import pygame
import math
import time
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions (optimized for 3.5" Pi display)
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("◉ RIPPLES.EXE - CYBERPUNK MODE ◉")

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

class Ripple:
    def __init__(self, x, y, max_radius=150, ripple_type=0):
        self.x = x
        self.y = y
        self.radius = 0
        self.max_radius = max_radius
        self.ripple_type = ripple_type
        self.speed = 2.0
        self.strength = 1.0
        self.frequency = 0.3
        self.decay = 0.02
        self.color_phase = random.uniform(0, 2 * math.pi)
    
    def update(self, wave_speed, amplitude):
        """Update ripple expansion"""
        self.radius += self.speed * wave_speed
        self.strength *= (1 - self.decay)
        
        # Slow down as it expands
        self.speed *= 0.995
        
        # Adjust strength based on amplitude
        self.strength *= amplitude
    
    def get_wave_height(self, x, y, time_val):
        """Calculate wave height at given position"""
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        
        if distance > self.radius or distance < self.radius - 30:
            return 0
        
        # Different wave types
        if self.ripple_type == 0:  # Classic
            wave_phase = (distance - self.radius) * self.frequency
            wave_height = self.strength * math.sin(wave_phase) * math.exp(-abs(distance - self.radius) * 0.1)
        elif self.ripple_type == 1:  # Square
            wave_phase = (distance - self.radius) * self.frequency
            wave_height = self.strength * (1 if math.sin(wave_phase) > 0 else -1) * math.exp(-abs(distance - self.radius) * 0.1)
        elif self.ripple_type == 2:  # Sawtooth
            wave_phase = (distance - self.radius) * self.frequency
            wave_height = self.strength * (2 * (wave_phase % (2 * math.pi)) / (2 * math.pi) - 1) * math.exp(-abs(distance - self.radius) * 0.1)
        else:  # Interference
            wave_phase = (distance - self.radius) * self.frequency
            wave_height = self.strength * math.sin(wave_phase) * math.sin(wave_phase * 0.5 + time_val) * math.exp(-abs(distance - self.radius) * 0.1)
        
        return wave_height
    
    def draw(self, surface, color_mode, time_val):
        """Draw ripple circles"""
        if self.strength > 0.1 and self.radius < self.max_radius:
            # Draw multiple concentric circles for wave effect
            for i in range(3):
                radius = int(self.radius + i * 8)
                if radius > 0:
                    alpha = int(self.strength * 150)
                    
                    # Color based on mode
                    if color_mode == 0:  # Cyberpunk
                        color = (100, 150 + alpha, 255)
                    elif color_mode == 1:  # Neon
                        hue = (time_val * 100 + self.color_phase) % 360
                        color = (
                            int(255 * abs(math.sin(hue * math.pi / 180))),
                            int(255 * abs(math.sin((hue + 120) * math.pi / 180))),
                            int(255 * abs(math.sin((hue + 240) * math.pi / 180)))
                        )
                    elif color_mode == 2:  # Matrix
                        color = (50, 255, 50)
                    elif color_mode == 3:  # Synthwave
                        color = (255, 100, 255)
                    else:  # Retro
                        color = (255, 255, 100)
                    
                    # Draw circle outline
                    if radius < self.max_radius:
                        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), radius, 2)
    
    def is_dead(self):
        """Check if ripple should be removed"""
        return self.strength < 0.05 or self.radius > self.max_radius

class InteractiveRipples:
    def __init__(self):
        # Wave parameters
        self.wave_speed = 1.0
        self.amplitude = 1.0
        self.interference_strength = 0.5
        self.auto_mode = True
        self.ripple_type = 0  # 0: Classic, 1: Square, 2: Sawtooth, 3: Interference
        self.color_mode = 0   # 0: Cyberpunk, 1: Neon, 2: Matrix, 3: Synthwave, 4: Retro
        self.brightness = 1.0
        self.pixel_size = 4   # Water surface pixel size
        
        # UI system
        self.ui = CyberpunkUI()
        
        # Ripple types
        self.ripple_types = {
            0: "CLASSIC.WAVE",
            1: "SQUARE.WAVE",
            2: "SAWTOOTH.WAVE",
            3: "INTERFERENCE.WAVE"
        }
        
        # Color palettes
        self.color_modes = {
            0: "CYBERPUNK.CORE",
            1: "NEON.DREAMS", 
            2: "MATRIX.CODE",
            3: "SYNTHWAVE.80s",
            4: "RETRO.FUTURE"
        }
        
        # Ripple management
        self.ripples = []
        self.max_ripples = 10
        
        # Water surface cache
        self.surface_cache = {}
        self.cache_lifetime = 0.1
        self.last_cache_time = 0
    
    def get_water_color(self, height, base_color, time_val):
        """Get water color based on height and color mode"""
        effective_brightness = self.brightness
        
        if self.color_mode == 0:  # Cyberpunk
            base_blue = int(50 * effective_brightness)
            wave_intensity = int(100 * abs(height) * effective_brightness)
            
            if height > 0:
                # Positive waves - lighter blue
                color = (base_blue, base_blue + wave_intensity, 200 + wave_intensity)
            else:
                # Negative waves - darker blue
                color = (base_blue - wave_intensity//2, base_blue, 150 - wave_intensity//2)
        elif self.color_mode == 1:  # Neon
            hue = (time_val * 50 + height * 500) % 360
            intensity = (0.5 + 0.5 * abs(height)) * effective_brightness
            color = (
                int(255 * abs(math.sin(hue * math.pi / 180)) * intensity),
                int(255 * abs(math.sin((hue + 120) * math.pi / 180)) * intensity),
                int(255 * abs(math.sin((hue + 240) * math.pi / 180)) * intensity)
            )
        elif self.color_mode == 2:  # Matrix
            intensity = (0.3 + 0.7 * abs(height)) * effective_brightness
            color = (0, int(255 * intensity), 0)
        elif self.color_mode == 3:  # Synthwave
            intensity = (0.4 + 0.6 * abs(height)) * effective_brightness
            color = (int(255 * intensity), int(100 * intensity), int(255 * intensity))
        else:  # Retro
            intensity = (0.3 + 0.7 * abs(height)) * effective_brightness
            color = (int(255 * intensity), int(255 * intensity), int(100 * intensity))
        
        # Clamp color values
        return tuple(max(0, min(255, c)) for c in color)
    
    def calculate_water_surface(self, time_val):
        """Calculate combined water surface from all ripples"""
        # Use cache if recent
        if time_val - self.last_cache_time < self.cache_lifetime:
            return self.surface_cache
        
        surface_map = {}
        
        for x in range(0, WIDTH, self.pixel_size):
            for y in range(0, HEIGHT, self.pixel_size):
                total_height = 0
                
                # Base water movement
                base_wave = 0.1 * math.sin(x * 0.01 + time_val * 0.5) * math.cos(y * 0.01 + time_val * 0.3)
                total_height += base_wave
                
                # Add contribution from all ripples
                for ripple in self.ripples:
                    wave_height = ripple.get_wave_height(x, y, time_val)
                    total_height += wave_height * self.interference_strength
                
                # Apply amplitude scaling
                total_height *= self.amplitude
                
                surface_map[(x, y)] = total_height
        
        self.surface_cache = surface_map
        self.last_cache_time = time_val
        return surface_map
    
    def draw_water_surface(self, surface, surface_map, time_val):
        """Draw water surface with height-based coloring"""
        for (x, y), height in surface_map.items():
            color = self.get_water_color(height, CYBER_BLUE, time_val)
            
            # Draw water pixel
            pygame.draw.rect(surface, color, (x, y, self.pixel_size, self.pixel_size))
    
    def draw_water_background(self, surface, time_val):
        """Draw base water texture"""
        for x in range(0, WIDTH, 8):
            for y in range(0, HEIGHT, 8):
                # Base water color with subtle movement
                wave = 0.1 * math.sin(x * 0.02 + time_val * 0.8) * math.cos(y * 0.02 + time_val * 0.6)
                base_color = int(60 + 20 * wave * self.brightness)
                
                if self.color_mode == 0:  # Cyberpunk
                    water_color = (base_color // 2, base_color, base_color + 100)
                elif self.color_mode == 1:  # Neon
                    hue = (time_val * 30 + x + y) % 360
                    water_color = (
                        int(base_color * abs(math.sin(hue * math.pi / 180))),
                        int(base_color * abs(math.sin((hue + 120) * math.pi / 180))),
                        int(base_color * abs(math.sin((hue + 240) * math.pi / 180)))
                    )
                elif self.color_mode == 2:  # Matrix
                    water_color = (0, base_color, 0)
                elif self.color_mode == 3:  # Synthwave
                    water_color = (base_color, base_color // 2, base_color)
                else:  # Retro
                    water_color = (base_color, base_color, base_color // 2)
                
                pygame.draw.rect(surface, water_color, (x, y, 8, 8))
    
    def draw_particles(self, surface, surface_map, time_val):
        """Draw floating particles affected by waves"""
        for i in range(int(20 * self.amplitude)):
            base_x = (i * 37) % WIDTH
            base_y = (i * 71) % HEIGHT
            
            # Find nearest water surface point
            nearest_key = None
            min_dist = float('inf')
            for (x, y) in surface_map.keys():
                dist = abs(x - base_x) + abs(y - base_y)
                if dist < min_dist:
                    min_dist = dist
                    nearest_key = (x, y)
            
            if nearest_key:
                wave_height = surface_map[nearest_key]
                particle_y = base_y + wave_height * 10
                
                if 0 <= particle_y < HEIGHT:
                    brightness = 0.5 + 0.5 * abs(wave_height)
                    color = self.get_water_color(wave_height, NEON_CYAN, time_val)
                    size = 1 if brightness < 0.7 else 2
                    pygame.draw.circle(surface, color, (int(base_x), int(particle_y)), size)
    
    def handle_input(self, keys):
        """Handle keyboard input for interactivity"""
        # Wave speed controls
        if keys[pygame.K_UP]:
            self.wave_speed = min(self.wave_speed + 0.05, 3.0)
        if keys[pygame.K_DOWN]:
            self.wave_speed = max(self.wave_speed - 0.05, 0.1)
        
        # Amplitude controls
        if keys[pygame.K_LEFT]:
            self.amplitude = max(self.amplitude - 0.05, 0.1)
        if keys[pygame.K_RIGHT]:
            self.amplitude = min(self.amplitude + 0.05, 2.0)
        
        # Interference strength controls
        if keys[pygame.K_w]:
            self.interference_strength = min(self.interference_strength + 0.05, 2.0)
        if keys[pygame.K_s]:
            self.interference_strength = max(self.interference_strength - 0.05, 0.0)
        
        # Pixel size controls
        if keys[pygame.K_a]:
            self.pixel_size = max(self.pixel_size - 1, 2)
            self.surface_cache = {}  # Clear cache
        if keys[pygame.K_d]:
            self.pixel_size = min(self.pixel_size + 1, 8)
            self.surface_cache = {}  # Clear cache
        
        # Brightness controls
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.brightness = min(self.brightness + 0.05, 2.0)
        if keys[pygame.K_MINUS]:
            self.brightness = max(self.brightness - 0.05, 0.2)
    
    def cycle_ripple_type(self):
        """Cycle to next ripple type"""
        self.ripple_type = (self.ripple_type + 1) % len(self.ripple_types)
    
    def cycle_color_mode(self):
        """Cycle to next color mode"""
        self.color_mode = (self.color_mode + 1) % len(self.color_modes)
    
    def add_ripple(self, x, y):
        """Add a new ripple at position"""
        if len(self.ripples) >= self.max_ripples:
            self.ripples.pop(0)  # Remove oldest
        
        self.ripples.append(Ripple(x, y, 150, self.ripple_type))
    
    def reset(self):
        """Reset to initial state"""
        self.wave_speed = 1.0
        self.amplitude = 1.0
        self.interference_strength = 0.5
        self.ripple_type = 0
        self.color_mode = 0
        self.brightness = 1.0
        self.pixel_size = 4
        self.ripples.clear()
        self.surface_cache = {}
    
    def draw_ui(self, surface):
        """Draw cyberpunk UI interface"""
        # Main control panel
        panel_rect = pygame.Rect(10, 10, 300, 140)
        self.ui.draw_cyber_panel(surface, panel_rect, "WAVE.PHYSICS.ENGINE")
        
        # Status indicators
        y_offset = 35
        x_offset = 20
        
        # Wave speed with progress bar
        speed_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, speed_rect, self.wave_speed, 3.0, NEON_GREEN)
        self.ui.draw_cyber_text(surface, f"SPEED: {self.wave_speed:.1f}", 
                               (x_offset + 210, y_offset - 2), NEON_GREEN, self.ui.font_tiny)
        y_offset += 20
        
        # Amplitude with progress bar
        amp_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, amp_rect, self.amplitude, 2.0, NEON_CYAN)
        self.ui.draw_cyber_text(surface, f"AMP: {self.amplitude:.1f}", 
                               (x_offset + 210, y_offset - 2), NEON_CYAN, self.ui.font_tiny)
        y_offset += 20
        
        # Interference with progress bar
        inter_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, inter_rect, self.interference_strength, 2.0, NEON_PURPLE)
        self.ui.draw_cyber_text(surface, f"INTER: {self.interference_strength:.1f}", 
                               (x_offset + 210, y_offset - 2), NEON_PURPLE, self.ui.font_tiny)
        y_offset += 20
        
        # Pixel size with progress bar
        pixel_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, pixel_rect, self.pixel_size, 8, NEON_YELLOW)
        self.ui.draw_cyber_text(surface, f"PIXEL: {self.pixel_size}", 
                               (x_offset + 210, y_offset - 2), NEON_YELLOW, self.ui.font_tiny)
        y_offset += 25
        
        # Current modes
        self.ui.draw_cyber_text(surface, f"◆ {self.ripple_types[self.ripple_type]}", 
                               (x_offset, y_offset), NEON_PINK, self.ui.font_small)
        y_offset += 18
        
        self.ui.draw_cyber_text(surface, f"◇ {self.color_modes[self.color_mode]}", 
                               (x_offset, y_offset), NEON_ORANGE, self.ui.font_small)
        
        # Status panel
        status_rect = pygame.Rect(WIDTH - 120, 10, 110, 60)
        self.ui.draw_cyber_panel(surface, status_rect, "STATUS")
        
        ripple_count = len(self.ripples)
        self.ui.draw_cyber_text(surface, f"RIPPLES: {ripple_count}", 
                               (WIDTH - 110, 35), NEON_CYAN, self.ui.font_tiny)
        
        mode_text = "AUTO" if self.auto_mode else "MANUAL"
        self.ui.draw_cyber_text(surface, f"MODE: {mode_text}", 
                               (WIDTH - 110, 50), NEON_GREEN, self.ui.font_tiny)
        
        # Controls panel
        controls_rect = pygame.Rect(10, HEIGHT - 90, 460, 80)
        self.ui.draw_cyber_panel(surface, controls_rect, "NEURAL.INTERFACE")
        
        # Control instructions
        controls = [
            "↑↓ WAVE.SPEED ◇ ←→ AMPLITUDE ◇ WS INTERFERENCE ◇ AD PIXEL.SIZE",
            "+/- BRIGHTNESS ◇ [T] WAVE.TYPE ◇ [C] COLOR ◇ [SPACE] AUTO.MODE",
            "CLICK CREATE.RIPPLE ◇ [R] RESET ◇ [H] HIDE.GUI ◇ [ESC] EXIT"
        ]
        
        y_start = HEIGHT - 75
        for i, control in enumerate(controls):
            color = [NEON_CYAN, NEON_GREEN, NEON_YELLOW][i]
            self.ui.draw_cyber_text(surface, control, 
                                   (20, y_start + i * 16), color, self.ui.font_tiny, False)

def main():
    ripples = InteractiveRipples()
    running = True
    show_ui = True
    
    while running:
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_t:
                    ripples.cycle_ripple_type()
                elif event.key == pygame.K_c:
                    ripples.cycle_color_mode()
                elif event.key == pygame.K_SPACE:
                    ripples.auto_mode = not ripples.auto_mode
                elif event.key == pygame.K_r:
                    ripples.reset()
                elif event.key == pygame.K_h:
                    show_ui = not show_ui
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Create ripple at mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                ripples.add_ripple(mouse_x, mouse_y)
        
        # Handle continuous input
        ripples.handle_input(keys)
        
        # Calculate time-based animation
        current_time = time.time() - start_time
        
        # Auto-generate ripples
        if ripples.auto_mode and random.random() < 0.02:  # 2% chance per frame
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            ripples.add_ripple(x, y)
        
        # Clear screen
        screen.fill(CYBER_BLACK)
        
        # Draw water background
        ripples.draw_water_background(screen, current_time)
        
        # Update ripples
        ripples.ripples = [ripple for ripple in ripples.ripples if not ripple.is_dead()]
        
        for ripple in ripples.ripples:
            ripple.update(ripples.wave_speed, ripples.amplitude)
        
        # Calculate and draw water surface
        if ripples.ripples:
            surface_map = ripples.calculate_water_surface(current_time)
            ripples.draw_water_surface(screen, surface_map, current_time)
            
            # Draw particles
            ripples.draw_particles(screen, surface_map, current_time)
        
        # Draw ripple circles
        for ripple in ripples.ripples:
            ripple.draw(screen, ripples.color_mode, current_time)
        
        # Draw CRT scanlines
        ripples.ui.draw_scanlines(screen)
        
        # Draw UI if enabled
        if show_ui:
            ripples.draw_ui(screen)
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS for smooth animation
    
    pygame.quit()

if __name__ == "__main__":
    main() 