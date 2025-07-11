#!/usr/bin/env python3
"""
Interactive Lightning Effect - Electric discharge simulation with controls
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
pygame.display.set_caption("Interactive Lightning Effect")

clock = pygame.time.Clock()

class LightningBolt:
    def __init__(self, start_x, start_y, end_x, end_y, bolt_type=0, intensity=1.0):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.points = []
        self.life = int(255 * intensity)
        self.max_life = int(255 * intensity)
        self.thickness = random.randint(2, max(3, int(5 * intensity)))
        self.color_offset = random.randint(0, 60)
        self.bolt_type = bolt_type
        self.intensity = intensity
        self.branches = []
        self.generate_lightning()
    
    def generate_lightning(self):
        """Generate jagged lightning path"""
        self.points = [(self.start_x, self.start_y)]
        
        current_x = self.start_x
        current_y = self.start_y
        
        steps = 15 + int(10 * self.intensity)
        for i in range(1, steps):
            # Linear interpolation with random offset
            progress = i / steps
            target_x = self.start_x + (self.end_x - self.start_x) * progress
            target_y = self.start_y + (self.end_y - self.start_y) * progress
            
            # Add random deviation based on bolt type
            if self.bolt_type == 0:  # Classic
                deviation = 30 * (1 - abs(progress - 0.5) * 2) * self.intensity
            elif self.bolt_type == 1:  # Jagged
                deviation = 50 * self.intensity
            elif self.bolt_type == 2:  # Smooth
                deviation = 15 * (1 - abs(progress - 0.5) * 2) * self.intensity
            else:  # Chaotic
                deviation = 40 * random.uniform(0.5, 1.5) * self.intensity
            
            offset_x = random.uniform(-deviation, deviation)
            offset_y = random.uniform(-deviation, deviation)
            
            new_x = target_x + offset_x
            new_y = target_y + offset_y
            
            self.points.append((new_x, new_y))
            current_x, current_y = new_x, new_y
        
        self.points.append((self.end_x, self.end_y))
        
        # Generate branches
        self.generate_branches()
    
    def generate_branches(self):
        """Generate lightning branches"""
        self.branches = []
        branch_chance = 0.3 * self.intensity
        
        for i in range(1, len(self.points) - 1):
            if random.random() < branch_chance:
                branch_length = random.randint(20, int(60 * self.intensity))
                branch_angle = random.uniform(-math.pi/2, math.pi/2)
                
                start_x, start_y = self.points[i]
                end_x = start_x + branch_length * math.cos(branch_angle)
                end_y = start_y + branch_length * math.sin(branch_angle)
                
                # Create branch points
                branch_points = [(start_x, start_y)]
                branch_steps = random.randint(3, 8)
                
                for j in range(1, branch_steps):
                    progress = j / branch_steps
                    target_x = start_x + (end_x - start_x) * progress
                    target_y = start_y + (end_y - start_y) * progress
                    
                    deviation = 10 * self.intensity
                    offset_x = random.uniform(-deviation, deviation)
                    offset_y = random.uniform(-deviation, deviation)
                    
                    branch_points.append((target_x + offset_x, target_y + offset_y))
                
                branch_points.append((end_x, end_y))
                self.branches.append(branch_points)
    
    def update(self, flicker_rate=0.3):
        """Update lightning bolt"""
        self.life -= 3
        
        # Occasionally regenerate path for flickering effect
        if random.random() < flicker_rate:
            self.generate_lightning()
    
    def draw(self, surface, color_mode=0, pixel_size=1):
        """Draw lightning bolt"""
        if self.life > 0 and len(self.points) > 1:
            # Calculate color based on life
            alpha = self.life / self.max_life
            
            # Get colors based on mode
            main_color, glow_color = self.get_colors(color_mode, alpha)
            
            # Draw glow first (thicker, darker)
            if self.thickness > 1:
                self.draw_lightning_line(surface, self.points, glow_color, 
                                       self.thickness + 4, pixel_size)
            
            # Draw main bolt
            self.draw_lightning_line(surface, self.points, main_color, 
                                   self.thickness, pixel_size)
            
            # Draw branches
            for branch_points in self.branches:
                branch_color = tuple(int(c * 0.8) for c in main_color)
                self.draw_lightning_line(surface, branch_points, branch_color, 
                                       max(1, self.thickness - 1), pixel_size)
    
    def get_colors(self, color_mode, alpha):
        """Get colors based on mode"""
        if color_mode == 0:  # Classic Blue-White
            main_color = (int(255 * alpha), int(255 * alpha), int(255 * alpha))
            glow_color = (int(100 * alpha), int(150 * alpha), int(255 * alpha))
        elif color_mode == 1:  # Red Lightning
            main_color = (int(255 * alpha), int(100 * alpha), int(100 * alpha))
            glow_color = (int(200 * alpha), int(50 * alpha), int(50 * alpha))
        elif color_mode == 2:  # Green Lightning
            main_color = (int(100 * alpha), int(255 * alpha), int(100 * alpha))
            glow_color = (int(50 * alpha), int(200 * alpha), int(50 * alpha))
        elif color_mode == 3:  # Purple Lightning
            main_color = (int(255 * alpha), int(100 * alpha), int(255 * alpha))
            glow_color = (int(150 * alpha), int(50 * alpha), int(200 * alpha))
        elif color_mode == 4:  # Orange Lightning
            main_color = (int(255 * alpha), int(180 * alpha), int(100 * alpha))
            glow_color = (int(200 * alpha), int(100 * alpha), int(50 * alpha))
        else:  # Rainbow
            hue = (time.time() * 2) % 1
            main_color = self.hsv_to_rgb(hue, 1, alpha)
            glow_color = self.hsv_to_rgb(hue, 0.8, alpha * 0.7)
        
        return main_color, glow_color
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB"""
        i = int(h * 6.0)
        f = h * 6.0 - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q
        
        return (int(r * 255), int(g * 255), int(b * 255))
    
    def draw_lightning_line(self, surface, points, color, thickness, pixel_size):
        """Draw lightning line with pixel art style"""
        if pixel_size > 1:
            # Pixel art style - draw as rectangles
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                
                # Draw line as connected rectangles
                steps = max(1, int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2) / pixel_size))
                for j in range(steps + 1):
                    progress = j / max(1, steps)
                    x = x1 + (x2 - x1) * progress
                    y = y1 + (y2 - y1) * progress
                    
                    rect_size = thickness * pixel_size
                    pygame.draw.rect(surface, color, 
                                   (int(x), int(y), rect_size, rect_size))
        else:
            # Normal line drawing
            if len(points) > 1:
                pygame.draw.lines(surface, color, False, points, thickness)
    
    def is_dead(self):
        """Check if lightning bolt is dead"""
        return self.life <= 0

class InteractiveLightning:
    def __init__(self):
        self.lightning_bolts = []
        self.frequency = 0.05  # Lightning spawn rate
        self.intensity = 1.0
        self.color_mode = 0
        self.bolt_type = 0
        self.pixel_size = 1
        self.show_rain = True
        self.show_clouds = True
        self.show_flash = True
        self.storm_mode = 0  # 0: Random, 1: Continuous, 2: Directed
        self.auto_lightning = True
        
        self.color_modes = {
            0: "Classic Blue",
            1: "Red Lightning",
            2: "Green Lightning",
            3: "Purple Lightning",
            4: "Orange Lightning",
            5: "Rainbow"
        }
        
        self.bolt_types = {
            0: "Classic",
            1: "Jagged",
            2: "Smooth",
            3: "Chaotic"
        }
        
        self.storm_modes = {
            0: "Random Storm",
            1: "Continuous",
            2: "Directed"
        }
    
    def create_lightning(self, start_x=None, start_y=None, end_x=None, end_y=None):
        """Create a new lightning bolt"""
        if start_x is None:
            start_x = random.randint(0, WIDTH)
        if start_y is None:
            start_y = random.randint(0, HEIGHT // 4)
        if end_x is None:
            end_x = random.randint(0, WIDTH)
        if end_y is None:
            end_y = random.randint(HEIGHT // 2, HEIGHT)
        
        bolt = LightningBolt(start_x, start_y, end_x, end_y, 
                           self.bolt_type, self.intensity)
        self.lightning_bolts.append(bolt)
    
    def update_lightning(self):
        """Update all lightning bolts"""
        # Remove dead bolts
        self.lightning_bolts = [bolt for bolt in self.lightning_bolts if not bolt.is_dead()]
        
        # Update existing bolts
        for bolt in self.lightning_bolts:
            bolt.update(0.2 + self.intensity * 0.3)
        
        # Create new lightning based on storm mode
        if self.auto_lightning:
            if self.storm_mode == 0:  # Random
                if random.random() < self.frequency:
                    self.create_lightning()
            elif self.storm_mode == 1:  # Continuous
                if random.random() < self.frequency * 3:
                    self.create_lightning()
            elif self.storm_mode == 2:  # Directed
                if random.random() < self.frequency * 2:
                    # Lightning towards center
                    start_x = random.randint(0, WIDTH)
                    start_y = random.randint(0, HEIGHT // 4)
                    end_x = WIDTH // 2 + random.randint(-50, 50)
                    end_y = HEIGHT // 2 + random.randint(-50, 50)
                    self.create_lightning(start_x, start_y, end_x, end_y)
    
    def draw_storm_clouds(self, surface, time_val):
        """Draw storm clouds background"""
        if not self.show_clouds:
            return
        
        cloud_color = (20, 20, 30)
        
        for i in range(10):
            x = (i * 60 + time_val * 10) % (WIDTH + 100) - 50
            y = 30 + 20 * math.sin(time_val * 0.5 + i)
            
            # Multiple overlapping circles for cloud effect
            for j in range(5):
                offset_x = random.randint(-15, 15)
                offset_y = random.randint(-10, 10)
                radius = random.randint(20, 40)
                
                if self.pixel_size > 1:
                    # Pixel art clouds
                    pygame.draw.rect(surface, cloud_color, 
                                   (int(x + offset_x), int(y + offset_y), 
                                    radius * 2, radius))
                else:
                    pygame.draw.circle(surface, cloud_color, 
                                     (int(x + offset_x), int(y + offset_y)), radius)
    
    def draw_rain(self, surface):
        """Draw rain effect"""
        if not self.show_rain:
            return
        
        rain_intensity = int(20 * self.intensity)
        for _ in range(rain_intensity):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            rain_color = (50, 50, 80)
            
            if self.pixel_size > 1:
                # Pixel art rain
                pygame.draw.rect(surface, rain_color, 
                               (x, y, self.pixel_size, self.pixel_size * 3))
            else:
                pygame.draw.line(surface, rain_color, (x, y), (x + 2, y + 10), 1)
    
    def draw_flash(self, surface):
        """Draw lightning flash effect"""
        if not self.show_flash or len(self.lightning_bolts) == 0:
            return
        
        if random.random() < 0.1:
            flash_overlay = pygame.Surface((WIDTH, HEIGHT))
            flash_overlay.set_alpha(int(30 * self.intensity))
            flash_overlay.fill((255, 255, 255))
            surface.blit(flash_overlay, (0, 0))
    
    def draw_lightning_bolts(self, surface):
        """Draw all lightning bolts"""
        for bolt in self.lightning_bolts:
            bolt.draw(surface, self.color_mode, self.pixel_size)
    
    def handle_input(self, keys):
        """Handle keyboard input"""
        # Frequency controls
        if keys[pygame.K_UP]:
            self.frequency = min(self.frequency + 0.005, 0.5)
        if keys[pygame.K_DOWN]:
            self.frequency = max(self.frequency - 0.005, 0.01)
        
        # Intensity controls
        if keys[pygame.K_LEFT]:
            self.intensity = max(self.intensity - 0.05, 0.2)
        if keys[pygame.K_RIGHT]:
            self.intensity = min(self.intensity + 0.05, 3.0)
        
        # Pixel size controls
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.pixel_size = min(self.pixel_size + 1, 4)
        if keys[pygame.K_MINUS]:
            self.pixel_size = max(self.pixel_size - 1, 1)
    
    def cycle_color_mode(self):
        """Cycle color mode"""
        self.color_mode = (self.color_mode + 1) % len(self.color_modes)
    
    def cycle_bolt_type(self):
        """Cycle bolt type"""
        self.bolt_type = (self.bolt_type + 1) % len(self.bolt_types)
    
    def cycle_storm_mode(self):
        """Cycle storm mode"""
        self.storm_mode = (self.storm_mode + 1) % len(self.storm_modes)
    
    def toggle_auto_lightning(self):
        """Toggle automatic lightning"""
        self.auto_lightning = not self.auto_lightning
    
    def toggle_effects(self):
        """Toggle visual effects"""
        self.show_rain = not self.show_rain
        self.show_clouds = not self.show_clouds
        self.show_flash = not self.show_flash
    
    def draw_ui(self, surface):
        """Draw UI information"""
        font = pygame.font.Font(None, 20)
        y_offset = 10
        
        # Current settings
        freq_text = font.render(f"Frequency: {self.frequency:.3f}", True, (255, 255, 255))
        surface.blit(freq_text, (10, y_offset))
        y_offset += 25
        
        intensity_text = font.render(f"Intensity: {self.intensity:.1f}", True, (255, 255, 255))
        surface.blit(intensity_text, (10, y_offset))
        y_offset += 25
        
        color_text = font.render(f"Color: {self.color_modes[self.color_mode]}", True, (255, 255, 255))
        surface.blit(color_text, (10, y_offset))
        y_offset += 25
        
        bolt_text = font.render(f"Type: {self.bolt_types[self.bolt_type]}", True, (255, 255, 255))
        surface.blit(bolt_text, (10, y_offset))
        y_offset += 25
        
        storm_text = font.render(f"Storm: {self.storm_modes[self.storm_mode]}", True, (255, 255, 255))
        surface.blit(storm_text, (10, y_offset))
        y_offset += 25
        
        bolts_text = font.render(f"Bolts: {len(self.lightning_bolts)}", True, (255, 255, 255))
        surface.blit(bolts_text, (10, y_offset))
        
        # Controls
        controls_font = pygame.font.Font(None, 16)
        controls = [
            "↑↓ Frequency  ←→ Intensity  +/- Pixel Size",
            "C: Color  B: Bolt Type  S: Storm Mode",
            "A: Auto Toggle  E: Effects  R: Reset",
            "Click: Manual Lightning  ESC: Exit"
        ]
        
        for i, control in enumerate(controls):
            control_text = controls_font.render(control, True, (200, 200, 200))
            surface.blit(control_text, (10, HEIGHT - 80 + i * 16))

def main():
    lightning = InteractiveLightning()
    running = True
    show_ui = True
    start_time = time.time()
    
    while running:
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_c:
                    lightning.cycle_color_mode()
                elif event.key == pygame.K_b:
                    lightning.cycle_bolt_type()
                elif event.key == pygame.K_s:
                    lightning.cycle_storm_mode()
                elif event.key == pygame.K_a:
                    lightning.toggle_auto_lightning()
                elif event.key == pygame.K_e:
                    lightning.toggle_effects()
                elif event.key == pygame.K_r:
                    # Reset to defaults
                    lightning.frequency = 0.05
                    lightning.intensity = 1.0
                    lightning.color_mode = 0
                    lightning.bolt_type = 0
                    lightning.storm_mode = 0
                    lightning.lightning_bolts = []
                elif event.key == pygame.K_h:
                    show_ui = not show_ui
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Create lightning bolt to mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                start_x = random.randint(0, WIDTH)
                start_y = random.randint(0, HEIGHT // 3)
                lightning.create_lightning(start_x, start_y, mouse_x, mouse_y)
        
        # Handle continuous input
        lightning.handle_input(keys)
        
        current_time = time.time() - start_time
        
        # Clear screen with dark storm background
        screen.fill((5, 5, 15))
        
        # Draw storm effects
        lightning.draw_storm_clouds(screen, current_time)
        lightning.draw_rain(screen)
        
        # Update and draw lightning
        lightning.update_lightning()
        lightning.draw_lightning_bolts(screen)
        
        # Draw flash effect
        lightning.draw_flash(screen)
        
        # Draw UI if enabled
        if show_ui:
            # Semi-transparent background for UI
            ui_surface = pygame.Surface((280, 180))
            ui_surface.set_alpha(180)
            ui_surface.fill((0, 0, 0))
            screen.blit(ui_surface, (5, 5))
            
            lightning.draw_ui(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main() 