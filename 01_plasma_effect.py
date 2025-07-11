#!/usr/bin/env python3
"""
Interactive Plasma Effect - Psychedelic color patterns with keyboard controls
Perfect for Raspberry Pi 5 with 3.5" display
RETRO CYBERPUNK PIXEL ART VERSION
"""

import pygame
import numpy as np
import math
import time
import os

# Initialize Pygame
pygame.init()

# Screen dimensions (optimized for 3.5" Pi display)
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("◉ PLASMA.EXE - CYBERPUNK MODE ◉")

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

class InteractivePlasma:
    def __init__(self):
        self.speed = 1.0
        self.color_mode = 0  # 0: Cyberpunk, 1: Neon, 2: Matrix, 3: Synthwave, 4: Retro
        self.pattern_mode = 0  # 0: Classic, 1: Ripples, 2: Waves, 3: Spiral
        self.pixel_size = 2  # Pixel art block size
        self.brightness = 1.0
        self.contrast = 1.0
        
        # UI system
        self.ui = CyberpunkUI()
        
        # Color palettes for cyberpunk aesthetic
        self.color_modes = {
            0: "CYBERPUNK.CORE",
            1: "NEON.DREAMS", 
            2: "MATRIX.CODE",
            3: "SYNTHWAVE.80s",
            4: "RETRO.FUTURE"
        }
        
        self.pattern_modes = {
            0: "CLASSIC.WAVE",
            1: "RIPPLE.SCAN",
            2: "SINE.DANCE", 
            3: "SPIRAL.VORTEX"
        }
    
    def get_color_palette(self, value, time_val):
        """Get color based on selected cyberpunk palette"""
        if self.color_mode == 0:  # Cyberpunk
            r = int(255 * min(1.0, value + 0.3))
            g = int(100 * max(0, value - 0.2))
            b = int(255 * max(0.3, value))
        elif self.color_mode == 1:  # Neon
            r = int(255 * abs(math.sin(value * math.pi + time_val * 0.1)))
            g = int(255 * abs(math.sin(value * math.pi + time_val * 0.2 + math.pi/3)))
            b = int(255 * abs(math.sin(value * math.pi + time_val * 0.3 + 2*math.pi/3)))
        elif self.color_mode == 2:  # Matrix
            r = int(50 * max(0, value - 0.5))
            g = int(255 * min(1.0, value + 0.2))
            b = int(50 * max(0, value - 0.7))
        elif self.color_mode == 3:  # Synthwave
            r = int(255 * (0.8 + 0.2 * math.sin(value * 2 + time_val * 0.5)))
            g = int(100 * (0.5 + 0.5 * math.sin(value * 3 + time_val * 0.3)))
            b = int(255 * (0.9 + 0.1 * math.sin(value * 4 + time_val * 0.7)))
        else:  # Retro Future
            # Quantize to 8-bit palette with neon enhancement
            val = int(value * 15) / 15
            r = int(255 * (val if val > 0.4 else 0.1))
            g = int(255 * (val if 0.2 < val < 0.9 else 0.1))
            b = int(255 * (val if val < 0.7 else 0.1))
        
        # Apply brightness and contrast with cyberpunk enhancement
        r = min(255, int(r * self.brightness * self.contrast))
        g = min(255, int(g * self.brightness * self.contrast))
        b = min(255, int(b * self.brightness * self.contrast))
        
        return (r, g, b)
    
    def calculate_plasma_value(self, x, y, time_val):
        """Calculate plasma value based on pattern mode"""
        if self.pattern_mode == 0:  # Classic
            value = math.sin(x * 0.04 + time_val * self.speed)
            value += math.sin(y * 0.03 + time_val * 0.7 * self.speed)
            value += math.sin((x + y) * 0.02 + time_val * 0.5 * self.speed)
            value += math.sin(math.sqrt(x*x + y*y) * 0.02 + time_val * 0.3 * self.speed)
        elif self.pattern_mode == 1:  # Ripples
            cx, cy = WIDTH // 2, HEIGHT // 2
            dist = math.sqrt((x - cx)**2 + (y - cy)**2)
            value = math.sin(dist * 0.05 + time_val * self.speed * 2)
            value += math.sin(dist * 0.02 + time_val * self.speed * 1.5)
            value += math.sin(x * 0.03 + time_val * self.speed)
            value += math.sin(y * 0.03 + time_val * self.speed)
        elif self.pattern_mode == 2:  # Waves
            value = math.sin(x * 0.06 + time_val * self.speed)
            value += math.sin(y * 0.04 + time_val * self.speed * 0.8)
            value += math.sin((x + y) * 0.03 + time_val * self.speed * 0.6)
            value += math.sin((x - y) * 0.02 + time_val * self.speed * 0.4)
        else:  # Spiral
            cx, cy = WIDTH // 2, HEIGHT // 2
            angle = math.atan2(y - cy, x - cx)
            dist = math.sqrt((x - cx)**2 + (y - cy)**2)
            value = math.sin(angle * 3 + dist * 0.02 + time_val * self.speed)
            value += math.sin(angle * 2 + dist * 0.01 + time_val * self.speed * 0.7)
            value += math.sin(dist * 0.03 + time_val * self.speed * 0.5)
            value += math.sin(angle * 4 + time_val * self.speed * 0.3)
        
        # Normalize to 0-1 range
        return (value + 4) / 8
    
    def draw(self, surface, time_val):
        """Draw the plasma effect with pixel art style"""
        # Create pixel art blocks
        for x in range(0, WIDTH, self.pixel_size):
            for y in range(0, HEIGHT, self.pixel_size):
                # Sample from center of pixel block
                sample_x = x + self.pixel_size // 2
                sample_y = y + self.pixel_size // 2
                
                plasma_value = self.calculate_plasma_value(sample_x, sample_y, time_val)
                color = self.get_color_palette(plasma_value, time_val)
                
                # Draw pixel block
                pygame.draw.rect(surface, color, (x, y, self.pixel_size, self.pixel_size))
    
    def handle_input(self, keys):
        """Handle keyboard input for interactivity"""
        # Speed controls
        if keys[pygame.K_UP]:
            self.speed = min(self.speed + 0.05, 3.0)
        if keys[pygame.K_DOWN]:
            self.speed = max(self.speed - 0.05, 0.1)
        
        # Pixel size controls
        if keys[pygame.K_LEFT]:
            self.pixel_size = max(self.pixel_size - 1, 1)
        if keys[pygame.K_RIGHT]:
            self.pixel_size = min(self.pixel_size + 1, 8)
        
        # Brightness controls
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.brightness = min(self.brightness + 0.05, 2.0)
        if keys[pygame.K_MINUS]:
            self.brightness = max(self.brightness - 0.05, 0.2)
    
    def cycle_color_mode(self):
        """Cycle to next color mode"""
        self.color_mode = (self.color_mode + 1) % len(self.color_modes)
    
    def cycle_pattern_mode(self):
        """Cycle to next pattern mode"""
        self.pattern_mode = (self.pattern_mode + 1) % len(self.pattern_modes)
    
    def draw_ui(self, surface):
        """Draw cyberpunk UI interface"""
        # Main control panel
        panel_rect = pygame.Rect(10, 10, 280, 140)
        self.ui.draw_cyber_panel(surface, panel_rect, "PLASMA.CONTROL.MATRIX")
        
        # Status indicators
        y_offset = 35
        x_offset = 20
        
        # Current settings with progress bars
        speed_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, speed_rect, self.speed, 3.0, NEON_GREEN)
        self.ui.draw_cyber_text(surface, f"SPEED: {self.speed:.1f}", 
                               (x_offset + 210, y_offset - 2), NEON_GREEN, self.ui.font_tiny)
        y_offset += 20
        
        pixel_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, pixel_rect, self.pixel_size, 8, NEON_CYAN)
        self.ui.draw_cyber_text(surface, f"PIXEL: {self.pixel_size}", 
                               (x_offset + 210, y_offset - 2), NEON_CYAN, self.ui.font_tiny)
        y_offset += 20
        
        bright_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, bright_rect, self.brightness, 2.0, NEON_YELLOW)
        self.ui.draw_cyber_text(surface, f"BRIGHT: {self.brightness:.1f}", 
                               (x_offset + 210, y_offset - 2), NEON_YELLOW, self.ui.font_tiny)
        y_offset += 25
        
        # Mode displays
        self.ui.draw_cyber_text(surface, f"◆ {self.color_modes[self.color_mode]}", 
                               (x_offset, y_offset), NEON_PINK, self.ui.font_small)
        y_offset += 18
        
        self.ui.draw_cyber_text(surface, f"◇ {self.pattern_modes[self.pattern_mode]}", 
                               (x_offset, y_offset), NEON_PURPLE, self.ui.font_small)
        
        # Controls panel
        controls_rect = pygame.Rect(10, HEIGHT - 90, 460, 80)
        self.ui.draw_cyber_panel(surface, controls_rect, "NEURAL.INTERFACE")
        
        # Control instructions
        controls = [
            "↑↓ PLASMA.SPEED ◇ ←→ PIXEL.SIZE ◇ +/- BRIGHTNESS",
            "[C] COLOR.MODE ◇ [P] PATTERN.MODE ◇ [R] RESET.SYS",
            "[H] HIDE.GUI ◇ [ESC] EXIT.PROGRAM"
        ]
        
        y_start = HEIGHT - 75
        for i, control in enumerate(controls):
            color = [NEON_CYAN, NEON_GREEN, NEON_YELLOW][i]
            self.ui.draw_cyber_text(surface, control, 
                                   (20, y_start + i * 16), color, self.ui.font_tiny, False)

def main():
    plasma = InteractivePlasma()
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
                elif event.key == pygame.K_c:
                    plasma.cycle_color_mode()
                elif event.key == pygame.K_p:
                    plasma.cycle_pattern_mode()
                elif event.key == pygame.K_r:
                    # Reset to defaults
                    plasma.speed = 1.0
                    plasma.pixel_size = 2
                    plasma.brightness = 1.0
                    plasma.color_mode = 0
                    plasma.pattern_mode = 0
                elif event.key == pygame.K_h:
                    show_ui = not show_ui
        
        # Handle continuous input
        plasma.handle_input(keys)
        
        # Calculate time-based animation
        current_time = time.time() - start_time
        
        # Clear screen
        screen.fill(CYBER_BLACK)
        
        # Draw plasma effect
        plasma.draw(screen, current_time)
        
        # Draw CRT scanlines
        plasma.ui.draw_scanlines(screen)
        
        # Draw UI if enabled
        if show_ui:
            plasma.draw_ui(screen)
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS for smooth interaction
    
    pygame.quit()

if __name__ == "__main__":
    main() 