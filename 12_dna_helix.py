#!/usr/bin/env python3
"""
Interactive DNA Helix - Genetic visualization with cyberpunk aesthetics
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
pygame.display.set_caption("◉ DNA.EXE - CYBERPUNK MODE ◉")

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

class InteractiveDNA:
    def __init__(self):
        # DNA parameters
        self.rotation_speed = 1.0
        self.helix_stretch = 2.0
        self.helix_radius = 25
        self.color_mode = 0  # 0: Cyberpunk, 1: Neon, 2: Matrix, 3: Synthwave, 4: Retro
        self.brightness = 1.0
        self.glow_intensity = 0.5
        self.pixel_style = True
        
        # UI system
        self.ui = CyberpunkUI()
        
        # Color palettes
        self.color_modes = {
            0: "CYBERPUNK.CORE",
            1: "NEON.DREAMS", 
            2: "MATRIX.CODE",
            3: "SYNTHWAVE.80s",
            4: "RETRO.FUTURE"
        }
        
        # DNA bases and pairs
        self.base_pairs = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        
        # Create DNA strands
        self.strand1 = self.create_strand(WIDTH // 2 - 30, HEIGHT // 2, self.helix_radius, 0)
        self.strand2 = self.create_strand(WIDTH // 2 + 30, HEIGHT // 2, self.helix_radius, math.pi)
        
        # Statistics
        self.base_count = {'A': 0, 'T': 0, 'G': 0, 'C': 0}
        self.update_base_count()
    
    def create_strand(self, center_x, center_y, radius, phase_offset):
        """Create a DNA strand with random bases"""
        strand = {
            'center_x': center_x,
            'center_y': center_y,
            'radius': radius,
            'phase_offset': phase_offset,
            'bases': []
        }
        
        # Generate random DNA bases
        base_types = ['A', 'T', 'G', 'C']
        for i in range(60):
            base = random.choice(base_types)
            strand['bases'].append(base)
        
        return strand
    
    def update_base_count(self):
        """Update base pair statistics"""
        self.base_count = {'A': 0, 'T': 0, 'G': 0, 'C': 0}
        
        for base in self.strand1['bases']:
            self.base_count[base] += 1
        for base in self.strand2['bases']:
            self.base_count[base] += 1
    
    def get_base_colors(self, base, time_val):
        """Get cyberpunk colors for DNA bases"""
        if self.color_mode == 0:  # Cyberpunk
            base_colors = {
                'A': (255, 100, 100),  # Adenine - Red
                'T': (100, 255, 100),  # Thymine - Green
                'G': (100, 100, 255),  # Guanine - Blue
                'C': (255, 255, 100),  # Cytosine - Yellow
            }
        elif self.color_mode == 1:  # Neon
            hue_offset = {'A': 0, 'T': 120, 'G': 240, 'C': 60}
            hue = (time_val * 100 + hue_offset[base]) % 360
            base_colors = {
                'A': (int(255 * abs(math.sin(hue * math.pi / 180))), 
                      int(255 * abs(math.sin((hue + 120) * math.pi / 180))), 
                      int(255 * abs(math.sin((hue + 240) * math.pi / 180)))),
                'T': (int(255 * abs(math.sin(hue * math.pi / 180))), 
                      int(255 * abs(math.sin((hue + 120) * math.pi / 180))), 
                      int(255 * abs(math.sin((hue + 240) * math.pi / 180)))),
                'G': (int(255 * abs(math.sin(hue * math.pi / 180))), 
                      int(255 * abs(math.sin((hue + 120) * math.pi / 180))), 
                      int(255 * abs(math.sin((hue + 240) * math.pi / 180)))),
                'C': (int(255 * abs(math.sin(hue * math.pi / 180))), 
                      int(255 * abs(math.sin((hue + 120) * math.pi / 180))), 
                      int(255 * abs(math.sin((hue + 240) * math.pi / 180))))
            }
        elif self.color_mode == 2:  # Matrix
            base_colors = {
                'A': (50, 255, 50),
                'T': (100, 255, 100),
                'G': (150, 255, 150),
                'C': (200, 255, 200)
            }
        elif self.color_mode == 3:  # Synthwave
            base_colors = {
                'A': (255, 100, 255),  # Magenta
                'T': (100, 255, 255),  # Cyan
                'G': (255, 255, 100),  # Yellow
                'C': (255, 150, 100),  # Orange
            }
        else:  # Retro Future
            base_colors = {
                'A': (255, 255, 100),
                'T': (255, 100, 255),
                'G': (100, 255, 255),
                'C': (255, 255, 255)
            }
        
        color = base_colors[base]
        # Apply brightness
        return tuple(int(c * self.brightness) for c in color)
    
    def get_strand_position(self, strand, index, time_val):
        """Calculate 3D position of base along helix"""
        # Vertical position
        y = strand['center_y'] - 100 + (index * self.helix_stretch)
        
        # Helix angle
        angle = (index * 0.4 + time_val * self.rotation_speed + strand['phase_offset']) % (2 * math.pi)
        
        # Horizontal position
        x = strand['center_x'] + strand['radius'] * math.cos(angle)
        z = strand['radius'] * math.sin(angle)  # Depth for 3D effect
        
        return (x, y, z, angle)
    
    def draw_strand(self, surface, strand, time_val):
        """Draw DNA strand with pixel art style"""
        points = []
        
        for i, base in enumerate(strand['bases']):
            x, y, z, angle = self.get_strand_position(strand, i, time_val)
            
            # Only draw if within screen bounds
            if 0 <= y < HEIGHT and 0 <= x < WIDTH:
                # Size based on depth (z-position)
                if self.pixel_style:
                    size = 4 if z > 0 else 3  # Pixel art style
                else:
                    size = int(3 + 2 * (z / strand['radius'] + 1))
                
                # Color intensity based on depth
                depth_factor = (z / strand['radius'] + 1) / 2
                base_color = self.get_base_colors(base, time_val)
                shaded_color = tuple(int(c * depth_factor) for c in base_color)
                
                # Draw base with pixel art style
                if self.pixel_style:
                    pygame.draw.rect(surface, shaded_color, (int(x - size//2), int(y - size//2), size, size))
                else:
                pygame.draw.circle(surface, shaded_color, (int(x), int(y)), size)
                
                # Add glow effect
                if self.glow_intensity > 0:
                    glow_color = tuple(int(c * self.glow_intensity) for c in base_color)
                    if self.pixel_style:
                        pygame.draw.rect(surface, glow_color, (int(x - size//2 - 1), int(y - size//2 - 1), size + 2, size + 2))
                    else:
                        pygame.draw.circle(surface, glow_color, (int(x), int(y)), size + 1)
                
                # Store point for backbone
                points.append((x, y, z))
        
        # Draw backbone (connecting line)
        backbone_points = []
        for x, y, z in points:
            if 0 <= y < HEIGHT:
                depth_factor = (z / strand['radius'] + 1) / 2
                backbone_color = tuple(int(100 * depth_factor * self.brightness) for _ in range(3))
                backbone_points.append((int(x), int(y)))
        
        if len(backbone_points) > 1:
            pygame.draw.lines(surface, backbone_color, False, backbone_points, 2)
        
        return points

    def draw_base_pairs(self, surface, strand1_points, strand2_points, time_val):
    """Draw connections between base pairs"""
    min_len = min(len(strand1_points), len(strand2_points))
    
    for i in range(min_len):
        x1, y1, z1 = strand1_points[i]
        x2, y2, z2 = strand2_points[i]
        
        # Only draw if both points are visible
        if (0 <= y1 < HEIGHT and 0 <= x1 < WIDTH and 
            0 <= y2 < HEIGHT and 0 <= x2 < WIDTH):
            
            # Color based on average depth
            avg_depth = (z1 + z2) / 2
            depth_factor = (avg_depth / 50 + 1) / 2
            
            # Pulsing effect
            pulse = 0.5 + 0.5 * math.sin(time_val * 3 + i * 0.1)
                intensity = int(100 * depth_factor * pulse * self.brightness)
            
                if self.color_mode == 0:  # Cyberpunk
            pair_color = (intensity, intensity, intensity)
                elif self.color_mode == 1:  # Neon
                    hue = (time_val * 100 + i * 20) % 360
                    pair_color = (
                        int(intensity * abs(math.sin(hue * math.pi / 180))),
                        int(intensity * abs(math.sin((hue + 120) * math.pi / 180))),
                        int(intensity * abs(math.sin((hue + 240) * math.pi / 180)))
                    )
                elif self.color_mode == 2:  # Matrix
                    pair_color = (0, intensity, 0)
                elif self.color_mode == 3:  # Synthwave
                    pair_color = (intensity, intensity // 2, intensity)
                else:  # Retro
                    pair_color = (intensity, intensity, intensity // 2)
            
            # Draw connection line
                if self.pixel_style:
                    # Pixel art style connection
                    steps = int(abs(x2 - x1) + abs(y2 - y1))
                    if steps > 0:
                        for step in range(0, steps, 2):
                            t = step / steps
                            px = int(x1 + t * (x2 - x1))
                            py = int(y1 + t * (y2 - y1))
                            pygame.draw.rect(surface, pair_color, (px, py, 2, 2))
                else:
            pygame.draw.line(surface, pair_color, (int(x1), int(y1)), (int(x2), int(y2)), 1)
    
    def draw_molecular_background(self, surface, time_val):
    """Draw molecular background effects"""
    # Draw floating molecules
        for i in range(15):
        x = (i * 47 + time_val * 20) % WIDTH
        y = (i * 71 + time_val * 15) % HEIGHT
        
        # Twinkling effect
        brightness = 0.3 + 0.7 * abs(math.sin(time_val * 1.5 + i * 0.3))
            
            if self.color_mode == 0:  # Cyberpunk
        color = (int(brightness * 50), int(brightness * 50), int(brightness * 100))
            elif self.color_mode == 1:  # Neon
                hue = (time_val * 50 + i * 60) % 360
                color = (
                    int(brightness * 255 * abs(math.sin(hue * math.pi / 180))),
                    int(brightness * 255 * abs(math.sin((hue + 120) * math.pi / 180))),
                    int(brightness * 255 * abs(math.sin((hue + 240) * math.pi / 180)))
                )
            elif self.color_mode == 2:  # Matrix
                color = (0, int(brightness * 100), 0)
            elif self.color_mode == 3:  # Synthwave
                color = (int(brightness * 100), int(brightness * 50), int(brightness * 100))
            else:  # Retro
                color = (int(brightness * 100), int(brightness * 100), int(brightness * 50))
            
            size = 2 if brightness > 0.6 else 1
            if self.pixel_style:
                pygame.draw.rect(surface, color, (int(x), int(y), size, size))
            else:
                pygame.draw.circle(surface, color, (int(x), int(y)), size)
    
    def handle_input(self, keys):
        """Handle keyboard input for interactivity"""
        # Rotation speed controls
        if keys[pygame.K_UP]:
            self.rotation_speed = min(self.rotation_speed + 0.1, 3.0)
        if keys[pygame.K_DOWN]:
            self.rotation_speed = max(self.rotation_speed - 0.1, 0.2)
        
        # Helix stretch controls
        if keys[pygame.K_LEFT]:
            self.helix_stretch = max(self.helix_stretch - 0.1, 0.5)
        if keys[pygame.K_RIGHT]:
            self.helix_stretch = min(self.helix_stretch + 0.1, 4.0)
        
        # Helix radius controls
        if keys[pygame.K_w]:
            self.helix_radius = min(self.helix_radius + 1, 40)
            self.strand1['radius'] = self.helix_radius
            self.strand2['radius'] = self.helix_radius
        if keys[pygame.K_s]:
            self.helix_radius = max(self.helix_radius - 1, 15)
            self.strand1['radius'] = self.helix_radius
            self.strand2['radius'] = self.helix_radius
        
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
    
    def cycle_color_mode(self):
        """Cycle to next color mode"""
        self.color_mode = (self.color_mode + 1) % len(self.color_modes)
    
    def regenerate_sequence(self):
        """Regenerate DNA sequences"""
        base_types = ['A', 'T', 'G', 'C']
        
        # Regenerate strand 1
        self.strand1['bases'] = []
        for i in range(60):
            base = random.choice(base_types)
            self.strand1['bases'].append(base)
        
        # Regenerate strand 2 with complementary bases
        self.strand2['bases'] = []
        for base in self.strand1['bases']:
            complement = self.base_pairs[base]
            self.strand2['bases'].append(complement)
        
        self.update_base_count()
    
    def toggle_pixel_style(self):
        """Toggle pixel art style"""
        self.pixel_style = not self.pixel_style
    
    def reset(self):
        """Reset to initial state"""
        self.rotation_speed = 1.0
        self.helix_stretch = 2.0
        self.helix_radius = 25
        self.color_mode = 0
        self.brightness = 1.0
        self.glow_intensity = 0.5
        self.pixel_style = True
        self.strand1['radius'] = self.helix_radius
        self.strand2['radius'] = self.helix_radius
        self.regenerate_sequence()
    
    def draw_ui(self, surface):
        """Draw cyberpunk UI interface"""
        # Main control panel
        panel_rect = pygame.Rect(10, 10, 300, 140)
        self.ui.draw_cyber_panel(surface, panel_rect, "DNA.SEQUENCER")
        
        # Status indicators
        y_offset = 35
        x_offset = 20
        
        # Rotation speed with progress bar
        rot_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, rot_rect, self.rotation_speed, 3.0, NEON_GREEN)
        self.ui.draw_cyber_text(surface, f"SPEED: {self.rotation_speed:.1f}", 
                               (x_offset + 210, y_offset - 2), NEON_GREEN, self.ui.font_tiny)
        y_offset += 20
        
        # Helix stretch with progress bar
        stretch_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, stretch_rect, self.helix_stretch, 4.0, NEON_CYAN)
        self.ui.draw_cyber_text(surface, f"STRETCH: {self.helix_stretch:.1f}", 
                               (x_offset + 210, y_offset - 2), NEON_CYAN, self.ui.font_tiny)
        y_offset += 20
        
        # Radius with progress bar
        radius_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, radius_rect, self.helix_radius, 40, NEON_PURPLE)
        self.ui.draw_cyber_text(surface, f"RADIUS: {self.helix_radius}", 
                               (x_offset + 210, y_offset - 2), NEON_PURPLE, self.ui.font_tiny)
        y_offset += 20
        
        # Brightness with progress bar
        bright_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, bright_rect, self.brightness, 2.0, NEON_YELLOW)
        self.ui.draw_cyber_text(surface, f"BRIGHT: {self.brightness:.1f}", 
                               (x_offset + 210, y_offset - 2), NEON_YELLOW, self.ui.font_tiny)
        y_offset += 25
        
        # Current mode
        self.ui.draw_cyber_text(surface, f"◆ {self.color_modes[self.color_mode]}", 
                               (x_offset, y_offset), NEON_PINK, self.ui.font_small)
        y_offset += 18
        
        style_text = "PIXEL.ART" if self.pixel_style else "SMOOTH.RENDER"
        self.ui.draw_cyber_text(surface, f"◇ {style_text}", 
                               (x_offset, y_offset), NEON_ORANGE, self.ui.font_small)
        
        # Base count panel
        base_rect = pygame.Rect(WIDTH - 120, 10, 110, 100)
        self.ui.draw_cyber_panel(surface, base_rect, "BASE.COUNT")
        
        y_start = 35
        for base, count in self.base_count.items():
            color = self.get_base_colors(base, time.time())
            self.ui.draw_cyber_text(surface, f"{base}: {count}", 
                                   (WIDTH - 110, y_start), color, self.ui.font_tiny)
            y_start += 15
        
        # Controls panel
        controls_rect = pygame.Rect(10, HEIGHT - 90, 460, 80)
        self.ui.draw_cyber_panel(surface, controls_rect, "NEURAL.INTERFACE")
        
        # Control instructions
        controls = [
            "↑↓ SPEED ◇ ←→ STRETCH ◇ WS RADIUS ◇ +/- BRIGHTNESS",
            "PGUP/PGDN GLOW ◇ [C] COLOR ◇ [G] GENERATE ◇ [P] PIXEL.MODE",
            "[R] RESET ◇ [H] HIDE.GUI ◇ [ESC] EXIT.PROGRAM"
        ]
        
        y_start = HEIGHT - 75
        for i, control in enumerate(controls):
            color = [NEON_CYAN, NEON_GREEN, NEON_YELLOW][i]
            self.ui.draw_cyber_text(surface, control, 
                                   (20, y_start + i * 16), color, self.ui.font_tiny, False)

def main():
    dna = InteractiveDNA()
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
                    dna.cycle_color_mode()
                elif event.key == pygame.K_g:
                    dna.regenerate_sequence()
                elif event.key == pygame.K_p:
                    dna.toggle_pixel_style()
                elif event.key == pygame.K_r:
                    dna.reset()
                elif event.key == pygame.K_h:
                    show_ui = not show_ui
        
        # Handle continuous input
        dna.handle_input(keys)
        
        # Calculate time-based animation
        current_time = time.time() - start_time
        
        # Clear screen with dark background
        screen.fill(CYBER_BLACK)
        
        # Draw molecular background
        dna.draw_molecular_background(screen, current_time)
        
        # Draw DNA strands
        strand1_points = dna.draw_strand(screen, dna.strand1, current_time)
        strand2_points = dna.draw_strand(screen, dna.strand2, current_time)
        
        # Draw base pair connections
        dna.draw_base_pairs(screen, strand1_points, strand2_points, current_time)
        
        # Draw helix axis
        axis_color = tuple(int(50 * dna.brightness) for _ in range(3))
        pygame.draw.line(screen, axis_color, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)
        
        # Draw CRT scanlines
        dna.ui.draw_scanlines(screen)
        
        # Draw UI if enabled
        if show_ui:
            dna.draw_ui(screen)
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS for smooth animation
    
    pygame.quit()

if __name__ == "__main__":
    main() 