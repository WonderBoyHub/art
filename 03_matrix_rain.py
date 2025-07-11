#!/usr/bin/env python3
"""
Interactive Matrix Rain Effect - Digital rain with keyboard controls
Perfect for Raspberry Pi 5 with 3.5" display
PIXEL ART INTERACTIVE VERSION
"""

import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Matrix Rain")

clock = pygame.time.Clock()

# Font for characters
font = pygame.font.Font(None, 18)

# Character sets for different modes
CHARACTER_SETS = {
    0: "アィウェオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789",
    1: "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[]{}|;:,.<>?",
    2: "01", 
    3: "アィウェオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン",
    4: "░▒▓█▄▀▐▌■□▪▫◆◇○●◊◈",
    5: "!@#$%^&*()_+-=[]{}|;:,.<>?~`"
}

CHARACTER_SET_NAMES = {
    0: "Classic Matrix",
    1: "ASCII Digital",
    2: "Binary Code",
    3: "Japanese Only",
    4: "Block Art",
    5: "Symbols"
}

class MatrixStream:
    def __init__(self, x, char_set=0):
        self.x = x
        self.y = random.randint(-HEIGHT, 0)
        self.speed = random.uniform(2, 6)
        self.length = random.randint(5, 15)
        self.char_set = char_set
        self.chars = [random.choice(CHARACTER_SETS[char_set]) for _ in range(self.length)]
        self.change_rate = random.uniform(0.1, 0.5)
        self.glow_intensity = random.uniform(0.5, 1.0)
        
    def update(self, speed_multiplier=1.0):
        self.y += self.speed * speed_multiplier
        
        # Randomly change characters
        if random.random() < self.change_rate:
            idx = random.randint(0, len(self.chars) - 1)
            self.chars[idx] = random.choice(CHARACTER_SETS[self.char_set])
    
    def draw(self, surface, color_mode=0, pixel_size=1):
        for i, char in enumerate(self.chars):
            char_y = self.y + i * 20
            if 0 <= char_y < HEIGHT:
                # Color based on position in stream and color mode
                color = self.get_color(i, color_mode)
                
                # Render character
                text = font.render(char, True, color)
                
                # Draw with pixel art scaling if needed
                if pixel_size > 1:
                    # Scale the character for pixel art effect
                    char_rect = text.get_rect()
                    scaled_surface = pygame.transform.scale(text, 
                                                          (char_rect.width * pixel_size, 
                                                           char_rect.height * pixel_size))
                    surface.blit(scaled_surface, (self.x * pixel_size, char_y * pixel_size))
                else:
                    surface.blit(text, (self.x, char_y))
    
    def get_color(self, position, color_mode):
        """Get color based on position and color mode"""
        if color_mode == 0:  # Classic Green
            if position == 0:  # Head - bright white
                return (255, 255, 255)
            elif position < 3:  # Bright green
                return (0, 255, 0)
            elif position < 6:  # Medium green
                return (0, 200, 0)
            else:  # Dark green
                return (0, 100, 0)
        elif color_mode == 1:  # Blue Digital
            if position == 0:
                return (255, 255, 255)
            elif position < 3:
                return (100, 200, 255)
            elif position < 6:
                return (50, 150, 255)
            else:
                return (0, 100, 200)
        elif color_mode == 2:  # Red Alert
            if position == 0:
                return (255, 255, 255)
            elif position < 3:
                return (255, 100, 100)
            elif position < 6:
                return (200, 50, 50)
            else:
                return (150, 0, 0)
        elif color_mode == 3:  # Purple Neon
            if position == 0:
                return (255, 255, 255)
            elif position < 3:
                return (255, 100, 255)
            elif position < 6:
                return (200, 50, 200)
            else:
                return (150, 0, 150)
        elif color_mode == 4:  # Gold
            if position == 0:
                return (255, 255, 255)
            elif position < 3:
                return (255, 215, 0)
            elif position < 6:
                return (218, 165, 32)
            else:
                return (184, 134, 11)
        else:  # Rainbow
            import math
            hue = (position * 60) % 360
            # Simple HSV to RGB conversion
            c = 255
            x = int(c * (1 - abs((hue / 60) % 2 - 1)))
            if hue < 60:
                return (c, x, 0)
            elif hue < 120:
                return (x, c, 0)
            elif hue < 180:
                return (0, c, x)
            elif hue < 240:
                return (0, x, c)
            elif hue < 300:
                return (x, 0, c)
            else:
                return (c, 0, x)
    
    def is_off_screen(self):
        return self.y > HEIGHT + self.length * 20

class InteractiveMatrix:
    def __init__(self):
        self.streams = []
        self.speed_multiplier = 1.0
        self.char_set = 0
        self.color_mode = 0
        self.density = 0.7
        self.pixel_size = 1
        self.trail_effect = True
        self.glow_effect = False
        self.rain_mode = 0  # 0: Random, 1: Waves, 2: Cascade, 3: Pulse
        
        self.color_mode_names = {
            0: "Classic Green",
            1: "Blue Digital",
            2: "Red Alert",
            3: "Purple Neon",
            4: "Gold",
            5: "Rainbow"
        }
        
        self.rain_mode_names = {
            0: "Random Rain",
            1: "Wave Pattern",
            2: "Cascade",
            3: "Pulse Mode"
        }
        
        self.initialize_streams()
    
    def initialize_streams(self):
        """Initialize streams based on current settings"""
        self.streams = []
        for x in range(0, WIDTH, 25):
            if random.random() < self.density:
                self.streams.append(MatrixStream(x, self.char_set))
    
    def update_streams(self):
        """Update all streams"""
        # Update existing streams
        for stream in self.streams[:]:
            stream.update(self.speed_multiplier)
            
            if stream.is_off_screen():
                self.streams.remove(stream)
        
        # Add new streams based on rain mode
        if self.rain_mode == 0:  # Random
            if random.random() < 0.1 * self.density:
                x = random.choice(range(0, WIDTH, 25))
                self.streams.append(MatrixStream(x, self.char_set))
        elif self.rain_mode == 1:  # Waves
            wave_time = time.time() * 2
            for x in range(0, WIDTH, 25):
                if random.random() < 0.05 * self.density * (1 + 0.5 * math.sin(wave_time + x * 0.01)):
                    self.streams.append(MatrixStream(x, self.char_set))
        elif self.rain_mode == 2:  # Cascade
            if random.random() < 0.15 * self.density:
                # Start cascades from left to right
                cascade_x = int((time.time() * 50) % WIDTH)
                cascade_x = (cascade_x // 25) * 25
                self.streams.append(MatrixStream(cascade_x, self.char_set))
        elif self.rain_mode == 3:  # Pulse
            pulse_time = time.time() * 3
            if abs(math.sin(pulse_time)) > 0.8 and random.random() < 0.2 * self.density:
                for x in range(0, WIDTH, 25):
                    if random.random() < 0.7:
                        self.streams.append(MatrixStream(x, self.char_set))
    
    def draw_streams(self, surface):
        """Draw all streams"""
        for stream in self.streams:
            stream.draw(surface, self.color_mode, self.pixel_size)
    
    def draw_background_effects(self, surface):
        """Draw background effects"""
        if self.trail_effect:
            # Create trail effect
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(20)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
        
        if self.glow_effect:
            # Add subtle glow effect
            for _ in range(10):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                color = (0, random.randint(50, 100), 0)
                pygame.draw.circle(surface, color, (x, y), 1)
    
    def handle_input(self, keys):
        """Handle keyboard input"""
        # Speed controls
        if keys[pygame.K_UP]:
            self.speed_multiplier = min(self.speed_multiplier + 0.1, 5.0)
        if keys[pygame.K_DOWN]:
            self.speed_multiplier = max(self.speed_multiplier - 0.1, 0.1)
        
        # Density controls
        if keys[pygame.K_LEFT]:
            self.density = max(self.density - 0.05, 0.1)
        if keys[pygame.K_RIGHT]:
            self.density = min(self.density + 0.05, 2.0)
        
        # Pixel size controls
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.pixel_size = min(self.pixel_size + 1, 3)
        if keys[pygame.K_MINUS]:
            self.pixel_size = max(self.pixel_size - 1, 1)
    
    def cycle_char_set(self):
        """Cycle character set"""
        self.char_set = (self.char_set + 1) % len(CHARACTER_SETS)
        # Update existing streams
        for stream in self.streams:
            stream.char_set = self.char_set
            stream.chars = [random.choice(CHARACTER_SETS[self.char_set]) for _ in range(stream.length)]
    
    def cycle_color_mode(self):
        """Cycle color mode"""
        self.color_mode = (self.color_mode + 1) % len(self.color_mode_names)
    
    def cycle_rain_mode(self):
        """Cycle rain mode"""
        self.rain_mode = (self.rain_mode + 1) % len(self.rain_mode_names)
    
    def toggle_trail_effect(self):
        """Toggle trail effect"""
        self.trail_effect = not self.trail_effect
    
    def toggle_glow_effect(self):
        """Toggle glow effect"""
        self.glow_effect = not self.glow_effect
    
    def draw_ui(self, surface):
        """Draw UI information"""
        font = pygame.font.Font(None, 20)
        y_offset = 10
        
        # Current settings
        speed_text = font.render(f"Speed: {self.speed_multiplier:.1f}", True, (255, 255, 255))
        surface.blit(speed_text, (10, y_offset))
        y_offset += 25
        
        density_text = font.render(f"Density: {self.density:.1f}", True, (255, 255, 255))
        surface.blit(density_text, (10, y_offset))
        y_offset += 25
        
        char_text = font.render(f"Chars: {CHARACTER_SET_NAMES[self.char_set]}", True, (255, 255, 255))
        surface.blit(char_text, (10, y_offset))
        y_offset += 25
        
        color_text = font.render(f"Color: {self.color_mode_names[self.color_mode]}", True, (255, 255, 255))
        surface.blit(color_text, (10, y_offset))
        y_offset += 25
        
        rain_text = font.render(f"Mode: {self.rain_mode_names[self.rain_mode]}", True, (255, 255, 255))
        surface.blit(rain_text, (10, y_offset))
        y_offset += 25
        
        effects_text = font.render(f"Trail: {'ON' if self.trail_effect else 'OFF'} | Glow: {'ON' if self.glow_effect else 'OFF'}", True, (255, 255, 255))
        surface.blit(effects_text, (10, y_offset))
        
        # Controls
        controls_font = pygame.font.Font(None, 16)
        controls = [
            "↑↓ Speed  ←→ Density  +/- Pixel Size",
            "S: Characters  C: Color  M: Rain Mode",
            "T: Trail  G: Glow  R: Reset  ESC: Exit"
        ]
        
        for i, control in enumerate(controls):
            control_text = controls_font.render(control, True, (200, 200, 200))
            surface.blit(control_text, (10, HEIGHT - 70 + i * 18))

def main():
    import math
    
    matrix = InteractiveMatrix()
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
                elif event.key == pygame.K_s:
                    matrix.cycle_char_set()
                elif event.key == pygame.K_c:
                    matrix.cycle_color_mode()
                elif event.key == pygame.K_m:
                    matrix.cycle_rain_mode()
                elif event.key == pygame.K_t:
                    matrix.toggle_trail_effect()
                elif event.key == pygame.K_g:
                    matrix.toggle_glow_effect()
                elif event.key == pygame.K_r:
                    # Reset to defaults
                    matrix.speed_multiplier = 1.0
                    matrix.density = 0.7
                    matrix.char_set = 0
                    matrix.color_mode = 0
                    matrix.rain_mode = 0
                    matrix.pixel_size = 1
                    matrix.trail_effect = True
                    matrix.glow_effect = False
                    matrix.initialize_streams()
                elif event.key == pygame.K_h:
                    show_ui = not show_ui
        
        # Handle continuous input
        matrix.handle_input(keys)
        
        # Fill screen with dark background
        screen.fill((0, 0, 0))
        
        # Draw background effects
        matrix.draw_background_effects(screen)
        
        # Update and draw streams
        matrix.update_streams()
        matrix.draw_streams(screen)
        
        # Draw UI if enabled
        if show_ui:
            # Semi-transparent background for UI
            ui_surface = pygame.Surface((280, 180))
            ui_surface.set_alpha(180)
            ui_surface.fill((0, 0, 0))
            screen.blit(ui_surface, (5, 5))
            
            matrix.draw_ui(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main() 