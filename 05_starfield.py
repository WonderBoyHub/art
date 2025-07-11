#!/usr/bin/env python3
"""
Interactive Starfield Effect - Stars with navigation and warp drive controls
Perfect for Raspberry Pi 5 with 3.5" display
PIXEL ART INTERACTIVE VERSION
"""

import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Starfield")

clock = pygame.time.Clock()

class Star:
    def __init__(self, center_x=0, center_y=0):
        self.x = random.uniform(-1, 1)
        self.y = random.uniform(-1, 1)
        self.z = random.uniform(0.1, 1)
        self.prev_x = None
        self.prev_y = None
        self.center_x = center_x
        self.center_y = center_y
        self.color_hue = random.randint(0, 360)
        self.twinkle_phase = random.uniform(0, 2 * math.pi)
    
    def update(self, speed, direction_x=0, direction_y=0):
        self.prev_x = self.get_screen_x()
        self.prev_y = self.get_screen_y()
        
        self.z -= speed
        
        # Add directional movement
        self.x += direction_x * speed * 10
        self.y += direction_y * speed * 10
        
        # Reset star if it goes behind viewer or too far away
        if self.z <= 0 or abs(self.x) > 2 or abs(self.y) > 2:
            self.x = random.uniform(-1, 1)
            self.y = random.uniform(-1, 1)
            self.z = 1
            self.prev_x = None
            self.prev_y = None
            self.color_hue = random.randint(0, 360)
            self.twinkle_phase = random.uniform(0, 2 * math.pi)
    
    def get_screen_x(self):
        return (self.x + self.center_x) / self.z * WIDTH/2 + WIDTH/2
    
    def get_screen_y(self):
        return (self.y + self.center_y) / self.z * HEIGHT/2 + HEIGHT/2
    
    def draw(self, surface, color_mode=0, pixel_size=1, twinkle=False):
        if self.z > 0:
            screen_x = self.get_screen_x()
            screen_y = self.get_screen_y()
            
            # Check if star is on screen
            if 0 <= screen_x < WIDTH and 0 <= screen_y < HEIGHT:
                # Calculate star size based on distance
                base_size = max(1, int((1 - self.z) * 4))
                size = base_size * pixel_size
                
                # Calculate brightness based on distance
                base_brightness = int(255 * (1 - self.z))
                
                # Apply twinkle effect
                if twinkle:
                    twinkle_factor = 0.7 + 0.3 * math.sin(time.time() * 5 + self.twinkle_phase)
                    brightness = int(base_brightness * twinkle_factor)
                else:
                    brightness = base_brightness
                
                # Get color based on mode
                color = self.get_color(color_mode, brightness)
                
                # Draw star as pixel art
                if pixel_size > 1:
                    pygame.draw.rect(surface, color, 
                                   (int(screen_x), int(screen_y), size, size))
                else:
                    pygame.draw.circle(surface, color, 
                                     (int(screen_x), int(screen_y)), size)
                
                # Draw trail for warp effect
                if self.prev_x is not None and self.prev_y is not None:
                    if 0 <= self.prev_x < WIDTH and 0 <= self.prev_y < HEIGHT:
                        trail_color = tuple(c//3 for c in color)
                        pygame.draw.line(surface, trail_color, 
                                       (int(self.prev_x), int(self.prev_y)), 
                                       (int(screen_x), int(screen_y)), 
                                       max(1, pixel_size))
    
    def get_color(self, color_mode, brightness):
        """Get star color based on mode"""
        if color_mode == 0:  # White stars
            return (brightness, brightness, brightness)
        elif color_mode == 1:  # Colored stars
            # Convert HSV to RGB
            h = self.color_hue / 360.0
            s = 0.7
            v = brightness / 255.0
            
            c = v * s
            x = c * (1 - abs((h * 6) % 2 - 1))
            m = v - c
            
            if h < 1/6:
                r, g, b = c, x, 0
            elif h < 2/6:
                r, g, b = x, c, 0
            elif h < 3/6:
                r, g, b = 0, c, x
            elif h < 4/6:
                r, g, b = 0, x, c
            elif h < 5/6:
                r, g, b = x, 0, c
            else:
                r, g, b = c, 0, x
            
            return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))
        elif color_mode == 2:  # Blue nebula
            return (brightness//4, brightness//2, brightness)
        elif color_mode == 3:  # Red giant
            return (brightness, brightness//4, brightness//8)
        elif color_mode == 4:  # Green space
            return (brightness//8, brightness, brightness//4)
        else:  # Purple void
            return (brightness//2, brightness//8, brightness)

class InteractiveStarfield:
    def __init__(self):
        self.stars = []
        self.star_count = 200
        self.speed = 0.01
        self.direction_x = 0
        self.direction_y = 0
        self.color_mode = 0
        self.pixel_size = 1
        self.twinkle = False
        self.warp_mode = 0  # 0: Forward, 1: Spiral, 2: Orbit, 3: Hyperspace
        self.show_trails = True
        self.show_hud = True
        
        self.color_mode_names = {
            0: "White Stars",
            1: "Colorful Stars",
            2: "Blue Nebula",
            3: "Red Giant",
            4: "Green Space",
            5: "Purple Void"
        }
        
        self.warp_mode_names = {
            0: "Forward Warp",
            1: "Spiral Travel",
            2: "Orbital Motion",
            3: "Hyperspace"
        }
        
        self.initialize_stars()
    
    def initialize_stars(self):
        """Initialize stars based on current settings"""
        self.stars = [Star() for _ in range(self.star_count)]
    
    def update_stars(self):
        """Update all stars based on warp mode"""
        for star in self.stars:
            if self.warp_mode == 0:  # Forward warp
                star.update(self.speed, self.direction_x, self.direction_y)
            elif self.warp_mode == 1:  # Spiral
                spiral_time = time.time() * 0.5
                spiral_x = math.cos(spiral_time) * 0.1
                spiral_y = math.sin(spiral_time) * 0.1
                star.update(self.speed, spiral_x, spiral_y)
            elif self.warp_mode == 2:  # Orbit
                orbit_time = time.time() * 0.3
                orbit_x = math.cos(orbit_time) * 0.05
                orbit_y = math.sin(orbit_time) * 0.05
                star.update(self.speed * 0.5, orbit_x, orbit_y)
            else:  # Hyperspace
                hyper_speed = self.speed * (2 + math.sin(time.time() * 3))
                star.update(hyper_speed, self.direction_x, self.direction_y)
    
    def draw_stars(self, surface):
        """Draw all stars"""
        for star in self.stars:
            star.draw(surface, self.color_mode, self.pixel_size, self.twinkle)
    
    def draw_hud(self, surface):
        """Draw HUD elements"""
        if self.show_hud:
            # Center crosshair
            crosshair_color = (100, 100, 100)
            pygame.draw.line(surface, crosshair_color, 
                           (WIDTH//2 - 10, HEIGHT//2), 
                           (WIDTH//2 + 10, HEIGHT//2), 2)
            pygame.draw.line(surface, crosshair_color, 
                           (WIDTH//2, HEIGHT//2 - 10), 
                           (WIDTH//2, HEIGHT//2 + 10), 2)
            
            # Radar/compass
            if self.direction_x != 0 or self.direction_y != 0:
                radar_x = WIDTH - 60
                radar_y = 60
                pygame.draw.circle(surface, (50, 50, 50), (radar_x, radar_y), 20, 2)
                
                # Direction indicator
                dir_length = 15
                end_x = radar_x + self.direction_x * dir_length * 100
                end_y = radar_y + self.direction_y * dir_length * 100
                pygame.draw.line(surface, (0, 255, 0), 
                               (radar_x, radar_y), 
                               (int(end_x), int(end_y)), 2)
    
    def draw_ui(self, surface):
        """Draw UI information"""
        font = pygame.font.Font(None, 20)
        y_offset = 10
        
        # Current settings
        speed_text = font.render(f"Warp: {self.speed:.3f}", True, (255, 255, 255))
        surface.blit(speed_text, (10, y_offset))
        y_offset += 25
        
        stars_text = font.render(f"Stars: {self.star_count}", True, (255, 255, 255))
        surface.blit(stars_text, (10, y_offset))
        y_offset += 25
        
        color_text = font.render(f"Color: {self.color_mode_names[self.color_mode]}", True, (255, 255, 255))
        surface.blit(color_text, (10, y_offset))
        y_offset += 25
        
        warp_text = font.render(f"Mode: {self.warp_mode_names[self.warp_mode]}", True, (255, 255, 255))
        surface.blit(warp_text, (10, y_offset))
        y_offset += 25
        
        effects_text = font.render(f"Twinkle: {'ON' if self.twinkle else 'OFF'}", True, (255, 255, 255))
        surface.blit(effects_text, (10, y_offset))
        
        # Navigation info
        if self.direction_x != 0 or self.direction_y != 0:
            nav_text = font.render(f"Nav: {self.direction_x:.2f}, {self.direction_y:.2f}", True, (0, 255, 0))
            surface.blit(nav_text, (10, HEIGHT - 80))
        
        # Controls
        controls_font = pygame.font.Font(None, 16)
        controls = [
            "↑↓ Warp Speed  WASD: Navigation  +/- Star Count",
            "C: Color Mode  M: Warp Mode  T: Twinkle",
            "H: HUD  R: Reset  ESC: Exit"
        ]
        
        for i, control in enumerate(controls):
            control_text = controls_font.render(control, True, (200, 200, 200))
            surface.blit(control_text, (10, HEIGHT - 60 + i * 18))
    
    def handle_input(self, keys):
        """Handle keyboard input"""
        # Speed controls
        if keys[pygame.K_UP]:
            self.speed = min(self.speed + 0.002, 0.2)
        if keys[pygame.K_DOWN]:
            self.speed = max(self.speed - 0.002, 0.001)
        
        # Navigation controls
        if keys[pygame.K_w]:
            self.direction_y = max(self.direction_y - 0.01, -0.5)
        if keys[pygame.K_s]:
            self.direction_y = min(self.direction_y + 0.01, 0.5)
        if keys[pygame.K_a]:
            self.direction_x = max(self.direction_x - 0.01, -0.5)
        if keys[pygame.K_d]:
            self.direction_x = min(self.direction_x + 0.01, 0.5)
        
        # Star count controls
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.star_count = min(self.star_count + 5, 500)
            if len(self.stars) < self.star_count:
                self.stars.extend([Star() for _ in range(self.star_count - len(self.stars))])
        if keys[pygame.K_MINUS]:
            self.star_count = max(self.star_count - 5, 50)
            if len(self.stars) > self.star_count:
                self.stars = self.stars[:self.star_count]
    
    def cycle_color_mode(self):
        """Cycle color mode"""
        self.color_mode = (self.color_mode + 1) % len(self.color_mode_names)
    
    def cycle_warp_mode(self):
        """Cycle warp mode"""
        self.warp_mode = (self.warp_mode + 1) % len(self.warp_mode_names)
    
    def toggle_twinkle(self):
        """Toggle twinkle effect"""
        self.twinkle = not self.twinkle
    
    def toggle_hud(self):
        """Toggle HUD display"""
        self.show_hud = not self.show_hud
    
    def reset_navigation(self):
        """Reset navigation to center"""
        self.direction_x = 0
        self.direction_y = 0

def main():
    starfield = InteractiveStarfield()
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
                    starfield.cycle_color_mode()
                elif event.key == pygame.K_m:
                    starfield.cycle_warp_mode()
                elif event.key == pygame.K_t:
                    starfield.toggle_twinkle()
                elif event.key == pygame.K_h:
                    starfield.toggle_hud()
                elif event.key == pygame.K_r:
                    # Reset to defaults
                    starfield.speed = 0.01
                    starfield.star_count = 200
                    starfield.color_mode = 0
                    starfield.warp_mode = 0
                    starfield.twinkle = False
                    starfield.reset_navigation()
                    starfield.initialize_stars()
                elif event.key == pygame.K_SPACE:
                    starfield.reset_navigation()
                elif event.key == pygame.K_F1:
                    show_ui = not show_ui
        
        # Handle continuous input
        starfield.handle_input(keys)
        
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Update and draw stars
        starfield.update_stars()
        starfield.draw_stars(screen)
        
        # Draw HUD
        starfield.draw_hud(screen)
        
        # Draw UI if enabled
        if show_ui:
            # Semi-transparent background for UI
            ui_surface = pygame.Surface((300, 160))
            ui_surface.set_alpha(180)
            ui_surface.fill((0, 0, 0))
            screen.blit(ui_surface, (5, 5))
            
            starfield.draw_ui(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main() 