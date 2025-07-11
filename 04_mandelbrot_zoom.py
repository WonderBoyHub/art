#!/usr/bin/env python3
"""
Interactive Mandelbrot Zoom - Fractal exploration with cyberpunk aesthetics
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
pygame.display.set_caption("◉ MANDELBROT.EXE - CYBERPUNK MODE ◉")

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

class InteractiveMandelbrot:
    def __init__(self):
        # Navigation parameters
        self.center_x = -0.7269
        self.center_y = 0.1889
        self.zoom = 1.0
        self.zoom_speed = 1.02
        self.auto_zoom = True
        
        # Rendering parameters
        self.max_iterations = 50
        self.color_mode = 0  # 0: Cyberpunk, 1: Neon, 2: Matrix, 3: Synthwave, 4: Retro
        self.pixel_size = 2  # Pixel art block size
        self.brightness = 1.0
        
        # UI system
        self.ui = CyberpunkUI()
        
        # Create pixel array for faster drawing
        self.pixel_array = pygame.surfarray.array3d(screen)
        
        # Color palettes
        self.color_modes = {
            0: "CYBERPUNK.CORE",
            1: "NEON.DREAMS", 
            2: "MATRIX.CODE",
            3: "SYNTHWAVE.80s",
            4: "RETRO.FUTURE"
        }
        
        # Famous Mandelbrot coordinates
        self.famous_points = [
            (-0.7269, 0.1889, "SEAHORSE.VALLEY"),
            (-0.8, 0.156, "ELEPHANT.TRUNK"),
            (-0.74529, 0.11307, "LIGHTNING.BOLT"),
            (-1.25066, 0.02012, "MINI.MANDELBROT"),
            (-0.160, 1.0407, "FRACTAL.SPIRAL"),
            (-0.7453, 0.1127, "DOUBLE.SPIRAL")
        ]
        self.current_point = 0
    
    def mandelbrot(self, c, max_iter=None):
        """Calculate Mandelbrot set value for complex number c"""
        if max_iter is None:
            max_iter = self.max_iterations
            
        z = 0
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return max_iter
    
    def get_color_palette(self, iterations, max_iter, time_offset=0):
        """Get color based on selected cyberpunk palette"""
        if iterations == max_iter:
            return (0, 0, 0)  # Black for points in the set
        
        ratio = iterations / max_iter
        
        if self.color_mode == 0:  # Cyberpunk
            r = int(255 * min(1.0, ratio + 0.3))
            g = int(100 * max(0, ratio - 0.2))
            b = int(255 * max(0.3, ratio))
        elif self.color_mode == 1:  # Neon
            hue = (ratio + time_offset) % 1.0
            r = int(255 * abs(math.sin(hue * math.pi * 2)))
            g = int(255 * abs(math.sin(hue * math.pi * 2 + math.pi/3)))
            b = int(255 * abs(math.sin(hue * math.pi * 2 + 2*math.pi/3)))
        elif self.color_mode == 2:  # Matrix
            r = int(50 * max(0, ratio - 0.5))
            g = int(255 * min(1.0, ratio + 0.2))
            b = int(50 * max(0, ratio - 0.7))
        elif self.color_mode == 3:  # Synthwave
            r = int(255 * (0.8 + 0.2 * math.sin(ratio * 2 + time_offset)))
            g = int(100 * (0.5 + 0.5 * math.sin(ratio * 3 + time_offset)))
            b = int(255 * (0.9 + 0.1 * math.sin(ratio * 4 + time_offset)))
        else:  # Retro Future
            # Quantize to 8-bit palette
            val = int(ratio * 15) / 15
            r = int(255 * (val if val > 0.4 else 0.1))
            g = int(255 * (val if 0.2 < val < 0.9 else 0.1))
            b = int(255 * (val if val < 0.7 else 0.1))
        
        # Apply brightness
        r = min(255, int(r * self.brightness))
        g = min(255, int(g * self.brightness))
        b = min(255, int(b * self.brightness))
        
        return (r, g, b)
    
    def calculate_fractal(self, time_offset=0):
        """Calculate Mandelbrot set with pixel art style"""
        # Clear pixel array
        self.pixel_array.fill(0)
        
        # Calculate in pixel blocks for performance
        for x in range(0, WIDTH, self.pixel_size):
            for y in range(0, HEIGHT, self.pixel_size):
                # Map pixel to complex plane
                real = self.center_x + (x - WIDTH/2) / (WIDTH/2) / self.zoom
                imag = self.center_y + (y - HEIGHT/2) / (HEIGHT/2) / self.zoom
                
                c = complex(real, imag)
                iterations = self.mandelbrot(c)
                color = self.get_color_palette(iterations, self.max_iterations, time_offset)
                
                # Fill pixel block
                for px in range(x, min(x + self.pixel_size, WIDTH)):
                    for py in range(y, min(y + self.pixel_size, HEIGHT)):
                        if px < WIDTH and py < HEIGHT:
                            self.pixel_array[px][py] = color
    
    def handle_input(self, keys):
        """Handle keyboard input for interactivity"""
        move_speed = 0.1 / self.zoom
        
        # Navigation controls
        if keys[pygame.K_w]:
            self.center_y -= move_speed
        if keys[pygame.K_s]:
            self.center_y += move_speed
        if keys[pygame.K_a]:
            self.center_x -= move_speed
        if keys[pygame.K_d]:
            self.center_x += move_speed
        
        # Zoom controls
        if keys[pygame.K_UP]:
            self.zoom *= 1.1
        if keys[pygame.K_DOWN]:
            self.zoom /= 1.1
        
        # Zoom speed controls
        if keys[pygame.K_LEFT]:
            self.zoom_speed = max(self.zoom_speed - 0.005, 1.001)
        if keys[pygame.K_RIGHT]:
            self.zoom_speed = min(self.zoom_speed + 0.005, 1.1)
        
        # Iteration controls
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.max_iterations = min(self.max_iterations + 5, 200)
        if keys[pygame.K_MINUS]:
            self.max_iterations = max(self.max_iterations - 5, 10)
        
        # Pixel size controls
        if keys[pygame.K_COMMA]:
            self.pixel_size = max(self.pixel_size - 1, 1)
        if keys[pygame.K_PERIOD]:
            self.pixel_size = min(self.pixel_size + 1, 8)
        
        # Brightness controls
        if keys[pygame.K_PAGEUP]:
            self.brightness = min(self.brightness + 0.05, 2.0)
        if keys[pygame.K_PAGEDOWN]:
            self.brightness = max(self.brightness - 0.05, 0.2)
    
    def cycle_color_mode(self):
        """Cycle to next color mode"""
        self.color_mode = (self.color_mode + 1) % len(self.color_modes)
    
    def goto_famous_point(self):
        """Navigate to famous Mandelbrot coordinates"""
        self.current_point = (self.current_point + 1) % len(self.famous_points)
        x, y, name = self.famous_points[self.current_point]
        self.center_x = x
        self.center_y = y
        self.zoom = 1.0
    
    def reset(self):
        """Reset to initial state"""
        self.center_x = -0.7269
        self.center_y = 0.1889
        self.zoom = 1.0
        self.zoom_speed = 1.02
        self.max_iterations = 50
        self.pixel_size = 2
        self.brightness = 1.0
        self.color_mode = 0
        self.auto_zoom = True
    
    def draw_ui(self, surface):
        """Draw cyberpunk UI interface"""
        # Main control panel
        panel_rect = pygame.Rect(10, 10, 300, 160)
        self.ui.draw_cyber_panel(surface, panel_rect, "FRACTAL.ANALYZER")
        
        # Status indicators
        y_offset = 35
        x_offset = 20
        
        # Coordinates
        self.ui.draw_cyber_text(surface, f"X: {self.center_x:.6f}", 
                               (x_offset, y_offset), NEON_CYAN, self.ui.font_tiny)
        y_offset += 15
        self.ui.draw_cyber_text(surface, f"Y: {self.center_y:.6f}", 
                               (x_offset, y_offset), NEON_CYAN, self.ui.font_tiny)
        y_offset += 20
        
        # Zoom level with progress bar
        zoom_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        zoom_display = min(self.zoom, 1e6)  # Cap for display
        self.ui.draw_progress_bar(surface, zoom_rect, math.log10(zoom_display + 1), 6, NEON_GREEN)
        self.ui.draw_cyber_text(surface, f"ZOOM: {self.zoom:.2e}", 
                               (x_offset + 210, y_offset - 2), NEON_GREEN, self.ui.font_tiny)
        y_offset += 20
        
        # Iterations with progress bar
        iter_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, iter_rect, self.max_iterations, 200, NEON_YELLOW)
        self.ui.draw_cyber_text(surface, f"ITER: {self.max_iterations}", 
                               (x_offset + 210, y_offset - 2), NEON_YELLOW, self.ui.font_tiny)
        y_offset += 20
        
        # Pixel size with progress bar
        pixel_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, pixel_rect, self.pixel_size, 8, NEON_PURPLE)
        self.ui.draw_cyber_text(surface, f"PIXEL: {self.pixel_size}", 
                               (x_offset + 210, y_offset - 2), NEON_PURPLE, self.ui.font_tiny)
        y_offset += 25
        
        # Current mode and famous point
        self.ui.draw_cyber_text(surface, f"◆ {self.color_modes[self.color_mode]}", 
                               (x_offset, y_offset), NEON_PINK, self.ui.font_small)
        y_offset += 18
        
        current_point_name = self.famous_points[self.current_point][2]
        self.ui.draw_cyber_text(surface, f"◇ {current_point_name}", 
                               (x_offset, y_offset), NEON_ORANGE, self.ui.font_small)
        
        # Controls panel
        controls_rect = pygame.Rect(10, HEIGHT - 110, 460, 100)
        self.ui.draw_cyber_panel(surface, controls_rect, "NEURAL.INTERFACE")
        
        # Control instructions
        controls = [
            "WASD NAVIGATE ◇ ↑↓ ZOOM ◇ ←→ ZOOM.SPEED ◇ +/- ITERATIONS",
            ",/. PIXEL.SIZE ◇ PGUP/PGDN BRIGHTNESS ◇ [C] COLOR.MODE", 
            "[F] FAMOUS.POINTS ◇ [T] TOGGLE.AUTO ◇ [R] RESET ◇ [H] HIDE.GUI",
            "[ESC] EXIT.PROGRAM"
        ]
        
        y_start = HEIGHT - 95
        for i, control in enumerate(controls):
            color = [NEON_CYAN, NEON_GREEN, NEON_YELLOW, NEON_ORANGE][i]
            self.ui.draw_cyber_text(surface, control, 
                                   (20, y_start + i * 16), color, self.ui.font_tiny, False)
        
        # Auto-zoom indicator
        if self.auto_zoom:
            auto_rect = pygame.Rect(WIDTH - 120, 10, 100, 25)
            self.ui.draw_cyber_panel(surface, auto_rect, "AUTO.ZOOM")

def main():
    mandelbrot = InteractiveMandelbrot()
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
                    mandelbrot.cycle_color_mode()
                elif event.key == pygame.K_f:
                    mandelbrot.goto_famous_point()
                elif event.key == pygame.K_t:
                    mandelbrot.auto_zoom = not mandelbrot.auto_zoom
                elif event.key == pygame.K_r:
                    mandelbrot.reset()
                elif event.key == pygame.K_h:
                    show_ui = not show_ui
        
        # Handle continuous input
        mandelbrot.handle_input(keys)
        
        # Auto-zoom if enabled
        if mandelbrot.auto_zoom:
            mandelbrot.zoom *= mandelbrot.zoom_speed
            
            # Reset zoom when it gets too deep
            if mandelbrot.zoom > 1e10:
                mandelbrot.zoom = 1.0
        
        # Calculate time-based animation
        current_time = time.time() - start_time
        time_offset = current_time * 0.1
        
        # Clear screen
        screen.fill(CYBER_BLACK)
        
        # Calculate and draw fractal
        mandelbrot.calculate_fractal(time_offset)
        
        # Update display
        pygame.surfarray.blit_array(screen, mandelbrot.pixel_array)
        
        # Draw CRT scanlines
        mandelbrot.ui.draw_scanlines(screen)
        
        # Draw UI if enabled
        if show_ui:
            mandelbrot.draw_ui(screen)
        
        pygame.display.flip()
        clock.tick(30)  # 30 FPS for complex calculations
    
    pygame.quit()

if __name__ == "__main__":
    main() 