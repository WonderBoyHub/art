#!/usr/bin/env python3
"""
Interactive Spiral Galaxy - Space simulation with cyberpunk aesthetics
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
pygame.display.set_caption("◉ GALAXY.EXE - CYBERPUNK MODE ◉")

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

class Particle:
    def __init__(self, angle, distance, spiral_arm, star_type=0):
        self.angle = angle
        self.distance = distance
        self.spiral_arm = spiral_arm
        self.star_type = star_type
        self.size = random.uniform(0.5, 3.0)
        self.brightness = random.uniform(0.3, 1.0)
        self.color_offset = random.uniform(0, 60)
        self.twinkle_phase = random.uniform(0, 2 * math.pi)
        self.orbital_speed = 1.0 / (self.distance * 0.01 + 1)
    
    def update(self, time_val, rotation_speed, gravitational_strength):
        # Rotate the particle
        self.angle += rotation_speed * self.orbital_speed
        
        # Add gravitational effects
        if gravitational_strength > 0:
            # Orbital motion with gravitational influence
            self.angle += math.sin(time_val * 0.5 + self.distance * 0.1) * 0.002 * gravitational_strength
            
            # Slight distance variation due to gravitational waves
            self.distance += math.sin(time_val * 0.3 + self.angle) * 0.1 * gravitational_strength
    
    def get_position(self, center_x, center_y, time_val):
        # Calculate spiral position
        spiral_angle = self.angle + self.spiral_arm * (2 * math.pi / 3)
        
        # Spiral equation with time-based variation
        x = center_x + self.distance * math.cos(spiral_angle + self.distance * 0.02)
        y = center_y + self.distance * math.sin(spiral_angle + self.distance * 0.02)
        
        return (int(x), int(y))
    
    def get_color(self, time_val, color_mode):
        # Calculate twinkle effect
        twinkle = 0.8 + 0.2 * math.sin(time_val * 3 + self.twinkle_phase)
        effective_brightness = self.brightness * twinkle
        
        # Color based on star type and distance
        if color_mode == 0:  # Cyberpunk
            if self.star_type == 0:  # Main sequence
                r = int(255 * min(1.0, effective_brightness + 0.3))
                g = int(100 * max(0, effective_brightness - 0.2))
                b = int(255 * max(0.3, effective_brightness))
            elif self.star_type == 1:  # Giant
                r = int(255 * effective_brightness)
                g = int(20 * effective_brightness)
                b = int(147 * effective_brightness)
            else:  # Dwarf
                r = int(57 * effective_brightness)
                g = int(255 * effective_brightness)
                b = int(20 * effective_brightness)
        elif color_mode == 1:  # Neon
            hue = (self.distance * 2 + time_val * 20 + self.color_offset) % 360
            r = int(255 * abs(math.sin(hue * math.pi / 180)) * effective_brightness)
            g = int(255 * abs(math.sin((hue + 120) * math.pi / 180)) * effective_brightness)
            b = int(255 * abs(math.sin((hue + 240) * math.pi / 180)) * effective_brightness)
        elif color_mode == 2:  # Matrix
            r = int(50 * max(0, effective_brightness - 0.5))
            g = int(255 * min(1.0, effective_brightness + 0.2))
            b = int(50 * max(0, effective_brightness - 0.7))
        elif color_mode == 3:  # Synthwave
            hue = (self.distance * 2 + time_val * 20 + self.color_offset) % 360
            r = int(255 * (0.8 + 0.2 * math.sin(hue * math.pi / 180)) * effective_brightness)
            g = int(100 * (0.5 + 0.5 * math.sin((hue + 90) * math.pi / 180)) * effective_brightness)
            b = int(255 * (0.9 + 0.1 * math.sin((hue + 180) * math.pi / 180)) * effective_brightness)
        else:  # Retro Future
            # Quantize to 8-bit palette
            val = int(effective_brightness * 15) / 15
            r = int(255 * (val if val > 0.4 else 0.1))
            g = int(255 * (val if 0.2 < val < 0.9 else 0.1))
            b = int(255 * (val if val < 0.7 else 0.1))
        
        return (min(255, r), min(255, g), min(255, b))

class InteractiveGalaxy:
    def __init__(self):
        # Galaxy parameters
        self.rotation_speed = 0.005
        self.gravitational_strength = 0.5
        self.star_density = 1.0
        self.spiral_arms = 3
        self.color_mode = 0  # 0: Cyberpunk, 1: Neon, 2: Matrix, 3: Synthwave, 4: Retro
        self.brightness = 1.0
        self.glow_intensity = 0.5
        
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
        
        # Create galaxy particles
        self.particles = []
        self.regenerate_galaxy()
        
        # Background stars
        self.background_stars = []
        self.generate_background_stars()
    
    def regenerate_galaxy(self):
        """Regenerate galaxy particles based on current parameters"""
        self.particles = []
        
        # Calculate number of particles based on density
        base_particles = int(150 * self.star_density)
    
    # Create multiple spiral arms
        for arm in range(self.spiral_arms):
            particles_per_arm = base_particles // self.spiral_arms
            for i in range(particles_per_arm):
            angle = random.uniform(0, 4 * math.pi)
            distance = random.uniform(10, 150)
                star_type = random.randint(0, 2)  # 0: Main, 1: Giant, 2: Dwarf
                self.particles.append(Particle(angle, distance, arm, star_type))
    
        # Add some central particles (galactic core)
        for i in range(int(50 * self.star_density)):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(5, 30)
            star_type = 1  # Giants in the core
            self.particles.append(Particle(angle, distance, 0, star_type))
    
    def generate_background_stars(self):
        """Generate background stars"""
        self.background_stars = []
        for i in range(50):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            brightness = random.uniform(0.2, 0.8)
            twinkle_phase = random.uniform(0, 2 * math.pi)
            self.background_stars.append({'x': x, 'y': y, 'brightness': brightness, 'phase': twinkle_phase})
    
    def get_galaxy_color(self, hue, brightness, star_type):
        """Get color based on selected cyberpunk palette"""
        effective_brightness = brightness * self.brightness
        
        if self.color_mode == 0:  # Cyberpunk
            if star_type == 0:  # Main sequence
                r = int(255 * min(1.0, effective_brightness + 0.3))
                g = int(100 * max(0, effective_brightness - 0.2))
                b = int(255 * max(0.3, effective_brightness))
            elif star_type == 1:  # Giant
                r = int(255 * effective_brightness)
                g = int(20 * effective_brightness)
                b = int(147 * effective_brightness)
            else:  # Dwarf
                r = int(57 * effective_brightness)
                g = int(255 * effective_brightness)
                b = int(20 * effective_brightness)
        elif self.color_mode == 1:  # Neon
            r = int(255 * abs(math.sin(hue * math.pi / 180)) * effective_brightness)
            g = int(255 * abs(math.sin((hue + 120) * math.pi / 180)) * effective_brightness)
            b = int(255 * abs(math.sin((hue + 240) * math.pi / 180)) * effective_brightness)
        elif self.color_mode == 2:  # Matrix
            r = int(50 * max(0, effective_brightness - 0.5))
            g = int(255 * min(1.0, effective_brightness + 0.2))
            b = int(50 * max(0, effective_brightness - 0.7))
        elif self.color_mode == 3:  # Synthwave
            r = int(255 * (0.8 + 0.2 * math.sin(hue * math.pi / 180)) * effective_brightness)
            g = int(100 * (0.5 + 0.5 * math.sin((hue + 90) * math.pi / 180)) * effective_brightness)
            b = int(255 * (0.9 + 0.1 * math.sin((hue + 180) * math.pi / 180)) * effective_brightness)
        else:  # Retro Future
            # Quantize to 8-bit palette
            val = int(effective_brightness * 15) / 15
            r = int(255 * (val if val > 0.4 else 0.1))
            g = int(255 * (val if 0.2 < val < 0.9 else 0.1))
            b = int(255 * (val if val < 0.7 else 0.1))
        
        return (min(255, r), min(255, g), min(255, b))
    
    def draw_background_stars(self, surface, time_val):
        """Draw background stars for space effect"""
        for star in self.background_stars:
            # Twinkling effect
            brightness = star['brightness'] * (0.3 + 0.7 * abs(math.sin(time_val * 2 + star['phase'])))
            color = self.get_galaxy_color(0, brightness, 0)
            
            size = 1 if brightness < 0.7 else 2
            pygame.draw.circle(surface, color, (star['x'], star['y']), size)
    
    def draw_galactic_center(self, surface, time_val):
        """Draw the galactic center (black hole and accretion disk)"""
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        
        # Draw black hole
        black_hole_size = int(8 + 3 * math.sin(time_val * 2))
        pygame.draw.circle(surface, (0, 0, 0), (center_x, center_y), black_hole_size)
        
        # Draw accretion disk
        for radius in range(black_hole_size + 2, black_hole_size + 15, 2):
            intensity = 1 - (radius - black_hole_size) / 15
            color = self.get_galaxy_color(time_val * 50, intensity, 1)
            pygame.draw.circle(surface, color, (center_x, center_y), radius, 1)
    
    def draw_nebula_effects(self, surface, time_val):
        """Draw nebula clouds"""
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        
        for i in range(3):
            nebula_x = center_x + int(100 * math.cos(time_val * 0.3 + i * 2))
            nebula_y = center_y + int(100 * math.sin(time_val * 0.3 + i * 2))
            
            if 0 <= nebula_x < WIDTH and 0 <= nebula_y < HEIGHT:
                nebula_hue = (time_val * 30 + i * 120) % 360
                nebula_brightness = 0.3 + 0.2 * math.sin(time_val + i)
                nebula_color = self.get_galaxy_color(nebula_hue, nebula_brightness, 2)
                
                pygame.draw.circle(surface, nebula_color, (nebula_x, nebula_y), 10)
    
    def handle_input(self, keys):
        """Handle keyboard input for interactivity"""
        # Rotation speed controls
        if keys[pygame.K_UP]:
            self.rotation_speed = min(self.rotation_speed + 0.0005, 0.02)
        if keys[pygame.K_DOWN]:
            self.rotation_speed = max(self.rotation_speed - 0.0005, -0.02)
        
        # Gravitational strength controls
        if keys[pygame.K_LEFT]:
            self.gravitational_strength = max(self.gravitational_strength - 0.05, 0.0)
        if keys[pygame.K_RIGHT]:
            self.gravitational_strength = min(self.gravitational_strength + 0.05, 2.0)
        
        # Star density controls
        if keys[pygame.K_w]:
            self.star_density = min(self.star_density + 0.1, 2.0)
            self.regenerate_galaxy()
        if keys[pygame.K_s]:
            self.star_density = max(self.star_density - 0.1, 0.2)
            self.regenerate_galaxy()
        
        # Spiral arms controls
        if keys[pygame.K_a]:
            self.spiral_arms = max(self.spiral_arms - 1, 1)
            self.regenerate_galaxy()
        if keys[pygame.K_d]:
            self.spiral_arms = min(self.spiral_arms + 1, 6)
            self.regenerate_galaxy()
        
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
    
    def reset(self):
        """Reset to initial state"""
        self.rotation_speed = 0.005
        self.gravitational_strength = 0.5
        self.star_density = 1.0
        self.spiral_arms = 3
        self.color_mode = 0
        self.brightness = 1.0
        self.glow_intensity = 0.5
        self.regenerate_galaxy()
    
    def draw_ui(self, surface):
        """Draw cyberpunk UI interface"""
        # Main control panel
        panel_rect = pygame.Rect(10, 10, 300, 140)
        self.ui.draw_cyber_panel(surface, panel_rect, "GALAXY.SIMULATOR")
        
        # Status indicators
        y_offset = 35
        x_offset = 20
        
        # Rotation speed with progress bar
        rot_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        rot_display = abs(self.rotation_speed) * 1000  # Scale for display
        self.ui.draw_progress_bar(surface, rot_rect, rot_display, 20, NEON_GREEN)
        self.ui.draw_cyber_text(surface, f"ROT: {self.rotation_speed:.3f}", 
                               (x_offset + 210, y_offset - 2), NEON_GREEN, self.ui.font_tiny)
        y_offset += 20
        
        # Gravitational strength with progress bar
        grav_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, grav_rect, self.gravitational_strength, 2.0, NEON_CYAN)
        self.ui.draw_cyber_text(surface, f"GRAV: {self.gravitational_strength:.1f}", 
                               (x_offset + 210, y_offset - 2), NEON_CYAN, self.ui.font_tiny)
        y_offset += 20
        
        # Star density with progress bar
        density_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, density_rect, self.star_density, 2.0, NEON_PURPLE)
        self.ui.draw_cyber_text(surface, f"DENSITY: {self.star_density:.1f}", 
                               (x_offset + 210, y_offset - 2), NEON_PURPLE, self.ui.font_tiny)
        y_offset += 20
        
        # Spiral arms with progress bar
        arms_rect = pygame.Rect(x_offset, y_offset, 200, 12)
        self.ui.draw_progress_bar(surface, arms_rect, self.spiral_arms, 6, NEON_YELLOW)
        self.ui.draw_cyber_text(surface, f"ARMS: {self.spiral_arms}", 
                               (x_offset + 210, y_offset - 2), NEON_YELLOW, self.ui.font_tiny)
        y_offset += 25
        
        # Current mode and particle count
        self.ui.draw_cyber_text(surface, f"◆ {self.color_modes[self.color_mode]}", 
                               (x_offset, y_offset), NEON_PINK, self.ui.font_small)
        y_offset += 18
        
        particle_count = len(self.particles)
        self.ui.draw_cyber_text(surface, f"◇ STARS: {particle_count}", 
                               (x_offset, y_offset), NEON_ORANGE, self.ui.font_small)
        
        # Controls panel
        controls_rect = pygame.Rect(10, HEIGHT - 90, 460, 80)
        self.ui.draw_cyber_panel(surface, controls_rect, "NEURAL.INTERFACE")
        
        # Control instructions
        controls = [
            "↑↓ ROTATION ◇ ←→ GRAVITY ◇ WS DENSITY ◇ AD ARMS",
            "+/- BRIGHTNESS ◇ PGUP/PGDN GLOW ◇ [C] COLOR.MODE",
            "[R] RESET ◇ [H] HIDE.GUI ◇ [ESC] EXIT.PROGRAM"
        ]
        
        y_start = HEIGHT - 75
        for i, control in enumerate(controls):
            color = [NEON_CYAN, NEON_GREEN, NEON_YELLOW][i]
            self.ui.draw_cyber_text(surface, control, 
                                   (20, y_start + i * 16), color, self.ui.font_tiny, False)

def main():
    galaxy = InteractiveGalaxy()
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
                    galaxy.cycle_color_mode()
                elif event.key == pygame.K_r:
                    galaxy.reset()
                elif event.key == pygame.K_h:
                    show_ui = not show_ui
        
        # Handle continuous input
        galaxy.handle_input(keys)
        
        # Calculate time-based animation
        current_time = time.time() - start_time
        
        # Clear screen with space background
        screen.fill(CYBER_BLACK)
        
        # Draw background stars
        galaxy.draw_background_stars(screen, current_time)
        
        # Draw nebula effects
        galaxy.draw_nebula_effects(screen, current_time)
        
        # Update and draw galaxy particles
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        
        for particle in galaxy.particles:
            particle.update(current_time, galaxy.rotation_speed, galaxy.gravitational_strength)
            pos = particle.get_position(center_x, center_y, current_time)
            
            # Only draw particles within screen bounds
            if 0 <= pos[0] < WIDTH and 0 <= pos[1] < HEIGHT:
                color = particle.get_color(current_time, galaxy.color_mode)
                size = int(particle.size)
                
                if size > 0:
                    pygame.draw.circle(screen, color, pos, size)
                    
                    # Add glow effect for brighter particles
                    if particle.brightness > 0.7 and galaxy.glow_intensity > 0:
                        glow_color = tuple(int(c * galaxy.glow_intensity) for c in color)
                        pygame.draw.circle(screen, glow_color, pos, size + 1)
        
        # Draw galactic center
        galaxy.draw_galactic_center(screen, current_time)
        
        # Draw CRT scanlines
        galaxy.ui.draw_scanlines(screen)
        
        # Draw UI if enabled
        if show_ui:
            galaxy.draw_ui(screen)
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS for smooth animation
    
    pygame.quit()

if __name__ == "__main__":
    main() 