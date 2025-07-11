#!/usr/bin/env python3
"""
Interactive Particle Fire Effect - Simulated fire with keyboard controls
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
pygame.display.set_caption("Interactive Particle Fire")

clock = pygame.time.Clock()

class FireParticle:
    def __init__(self, x, y, intensity=1.0, wind=0.0):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-1, 1) + wind
        self.vel_y = random.uniform(-3, -1) * intensity
        self.life = 255
        self.decay = random.uniform(2, 5) / intensity
        self.size = random.uniform(1, 3) * intensity
        self.intensity = intensity
        self.spark_chance = 0.02
        
    def update(self, gravity=0.1, wind=0.0):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y -= gravity  # Gravity effect
        self.life -= self.decay
        
        # Add wind effect
        self.vel_x += wind * 0.1
        
        # Add some randomness to movement
        self.vel_x += random.uniform(-0.2, 0.2)
        self.vel_y += random.uniform(-0.1, 0.1)
        
        # Limit horizontal velocity
        self.vel_x = max(-3, min(3, self.vel_x))
    
    def draw(self, surface, pixel_size=1):
        if self.life > 0:
            # Pixel art style colors
            if self.life > 200:
                # Hot core - white/yellow
                color = (255, 255, int(255 * (255 - self.life) / 55))
            elif self.life > 150:
                # Bright flame - yellow/orange
                color = (255, int(255 * (200 - self.life) / 50), 0)
            elif self.life > 100:
                # Orange flame
                color = (255, int(140 * (150 - self.life) / 50), 0)
            elif self.life > 50:
                # Red flame
                color = (int(255 * (self.life / 50)), 0, 0)
            else:
                # Dying embers - dark red
                alpha = int(self.life * 3)
                color = (alpha, 0, 0)
            
            # Draw particle as pixel art block
            size = max(1, int(self.size * pixel_size))
            pygame.draw.rect(surface, color, 
                           (int(self.x), int(self.y), size, size))

class InteractiveFire:
    def __init__(self):
        self.particles = []
        self.intensity = 1.0
        self.wind = 0.0
        self.gravity = 0.1
        self.spawn_rate = 5
        self.pixel_size = 2
        self.fire_mode = 0  # 0: Normal, 1: Torch, 2: Campfire, 3: Inferno
        self.color_mode = 0  # 0: Classic, 1: Blue, 2: Green, 3: Purple
        self.spark_mode = True
        
        self.fire_modes = {
            0: "Normal Fire",
            1: "Torch Flame", 
            2: "Campfire",
            3: "Inferno"
        }
        
        self.color_modes = {
            0: "Classic Fire",
            1: "Blue Flame",
            2: "Green Flame", 
            3: "Purple Flame"
        }
    
    def get_spawn_area(self):
        """Get spawn area based on fire mode"""
        if self.fire_mode == 0:  # Normal
            return (WIDTH//4, 3*WIDTH//4, HEIGHT - 10, HEIGHT - 10)
        elif self.fire_mode == 1:  # Torch
            return (WIDTH//2 - 20, WIDTH//2 + 20, HEIGHT - 10, HEIGHT - 10)
        elif self.fire_mode == 2:  # Campfire
            return (WIDTH//3, 2*WIDTH//3, HEIGHT - 15, HEIGHT - 5)
        else:  # Inferno
            return (WIDTH//6, 5*WIDTH//6, HEIGHT - 20, HEIGHT - 5)
    
    def create_particles(self):
        """Create new particles based on spawn rate and mode"""
        x1, x2, y1, y2 = self.get_spawn_area()
        
        for _ in range(int(self.spawn_rate)):
            x = random.randint(x1, x2)
            y = random.randint(y1, y2)
            
            # Adjust particle properties based on fire mode
            if self.fire_mode == 1:  # Torch - more upward velocity
                particle = FireParticle(x, y, self.intensity, self.wind)
                particle.vel_y *= 1.5
            elif self.fire_mode == 2:  # Campfire - more spread
                particle = FireParticle(x, y, self.intensity, self.wind)
                particle.vel_x *= 1.5
            elif self.fire_mode == 3:  # Inferno - more intense
                particle = FireParticle(x, y, self.intensity * 1.5, self.wind)
                particle.life *= 1.3
            else:  # Normal
                particle = FireParticle(x, y, self.intensity, self.wind)
            
            self.particles.append(particle)
    
    def create_sparks(self):
        """Create spark effects"""
        if self.spark_mode:
            for _ in range(int(self.spawn_rate // 2)):
                x = random.randint(WIDTH//3, 2*WIDTH//3)
                y = random.randint(HEIGHT//2, HEIGHT)
                
                # Create spark particle
                spark = FireParticle(x, y, 0.5, self.wind)
                spark.vel_y = random.uniform(-5, -2)
                spark.vel_x = random.uniform(-2, 2)
                spark.life = random.randint(50, 100)
                spark.decay = random.uniform(3, 6)
                spark.size = random.uniform(0.5, 2)
                
                self.particles.append(spark)
    
    def update_particles(self):
        """Update all particles"""
        # Remove dead particles
        self.particles = [p for p in self.particles if p.life > 0]
        
        # Update existing particles
        for particle in self.particles:
            particle.update(self.gravity, self.wind)
    
    def draw_particles(self, surface):
        """Draw all particles with color mode"""
        for particle in self.particles:
            if particle.life > 0:
                # Apply color mode
                if self.color_mode == 0:  # Classic
                    particle.draw(surface, self.pixel_size)
                else:
                    # Modify colors for different modes
                    original_color = self.get_original_color(particle)
                    modified_color = self.apply_color_mode(original_color)
                    
                    size = max(1, int(particle.size * self.pixel_size))
                    pygame.draw.rect(surface, modified_color, 
                                   (int(particle.x), int(particle.y), size, size))
    
    def get_original_color(self, particle):
        """Get original particle color"""
        if particle.life > 200:
            return (255, 255, int(255 * (255 - particle.life) / 55))
        elif particle.life > 150:
            return (255, int(255 * (200 - particle.life) / 50), 0)
        elif particle.life > 100:
            return (255, int(140 * (150 - particle.life) / 50), 0)
        elif particle.life > 50:
            return (int(255 * (particle.life / 50)), 0, 0)
        else:
            alpha = int(particle.life * 3)
            return (alpha, 0, 0)
    
    def apply_color_mode(self, color):
        """Apply color mode transformation"""
        r, g, b = color
        brightness = (r + g + b) / 3
        
        if self.color_mode == 1:  # Blue
            return (0, int(brightness * 0.5), int(brightness))
        elif self.color_mode == 2:  # Green
            return (0, int(brightness), int(brightness * 0.3))
        elif self.color_mode == 3:  # Purple
            return (int(brightness * 0.8), 0, int(brightness))
        else:
            return color
    
    def handle_input(self, keys):
        """Handle keyboard input"""
        # Wind controls
        if keys[pygame.K_LEFT]:
            self.wind = max(self.wind - 0.1, -2.0)
        if keys[pygame.K_RIGHT]:
            self.wind = min(self.wind + 0.1, 2.0)
        
        # Intensity controls
        if keys[pygame.K_UP]:
            self.intensity = min(self.intensity + 0.1, 3.0)
        if keys[pygame.K_DOWN]:
            self.intensity = max(self.intensity - 0.1, 0.2)
        
        # Spawn rate controls
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.spawn_rate = min(self.spawn_rate + 1, 15)
        if keys[pygame.K_MINUS]:
            self.spawn_rate = max(self.spawn_rate - 1, 1)
    
    def cycle_fire_mode(self):
        """Cycle fire mode"""
        self.fire_mode = (self.fire_mode + 1) % len(self.fire_modes)
    
    def cycle_color_mode(self):
        """Cycle color mode"""
        self.color_mode = (self.color_mode + 1) % len(self.color_modes)
    
    def toggle_sparks(self):
        """Toggle spark effects"""
        self.spark_mode = not self.spark_mode
    
    def draw_ui(self, surface):
        """Draw UI information"""
        font = pygame.font.Font(None, 20)
        y_offset = 10
        
        # Current settings
        intensity_text = font.render(f"Intensity: {self.intensity:.1f}", True, (255, 255, 255))
        surface.blit(intensity_text, (10, y_offset))
        y_offset += 25
        
        wind_text = font.render(f"Wind: {self.wind:.1f}", True, (255, 255, 255))
        surface.blit(wind_text, (10, y_offset))
        y_offset += 25
        
        spawn_text = font.render(f"Spawn Rate: {self.spawn_rate}", True, (255, 255, 255))
        surface.blit(spawn_text, (10, y_offset))
        y_offset += 25
        
        fire_text = font.render(f"Mode: {self.fire_modes[self.fire_mode]}", True, (255, 255, 255))
        surface.blit(fire_text, (10, y_offset))
        y_offset += 25
        
        color_text = font.render(f"Color: {self.color_modes[self.color_mode]}", True, (255, 255, 255))
        surface.blit(color_text, (10, y_offset))
        y_offset += 25
        
        sparks_text = font.render(f"Sparks: {'ON' if self.spark_mode else 'OFF'}", True, (255, 255, 255))
        surface.blit(sparks_text, (10, y_offset))
        
        # Controls
        controls_font = pygame.font.Font(None, 16)
        controls = [
            "↑↓ Intensity  ←→ Wind  +/- Spawn Rate",
            "F: Fire Mode  C: Color  S: Sparks  R: Reset",
            "ESC: Exit"
        ]
        
        for i, control in enumerate(controls):
            control_text = controls_font.render(control, True, (200, 200, 200))
            surface.blit(control_text, (10, HEIGHT - 60 + i * 18))

def main():
    fire = InteractiveFire()
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
                elif event.key == pygame.K_f:
                    fire.cycle_fire_mode()
                elif event.key == pygame.K_c:
                    fire.cycle_color_mode()
                elif event.key == pygame.K_s:
                    fire.toggle_sparks()
                elif event.key == pygame.K_r:
                    # Reset to defaults
                    fire.intensity = 1.0
                    fire.wind = 0.0
                    fire.spawn_rate = 5
                    fire.fire_mode = 0
                    fire.color_mode = 0
                    fire.spark_mode = True
                elif event.key == pygame.K_h:
                    show_ui = not show_ui
        
        # Handle continuous input
        fire.handle_input(keys)
        
        # Clear screen with black
        screen.fill((0, 0, 0))
        
        # Create new particles
        fire.create_particles()
        fire.create_sparks()
        
        # Update particles
        fire.update_particles()
        
        # Draw particles
        fire.draw_particles(screen)
        
        # Draw UI if enabled
        if show_ui:
            # Semi-transparent background for UI
            ui_surface = pygame.Surface((250, 180))
            ui_surface.set_alpha(180)
            ui_surface.fill((0, 0, 0))
            screen.blit(ui_surface, (5, 5))
            
            fire.draw_ui(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main() 