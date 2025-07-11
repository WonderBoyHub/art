#!/usr/bin/env python3
"""
Advanced Starfield Warp Drive Simulator - Complete space navigation simulation
Perfect for Raspberry Pi 5 with 3.5" display
ENHANCED WARP DRIVE SIMULATOR VERSION
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
pygame.display.set_caption("Advanced Warp Drive Simulator")

# Fullscreen support
fullscreen = False
original_screen = screen

clock = pygame.time.Clock()
start_time = time.time()

# Enhanced colors
CYBER_BLACK = (10, 10, 15)
NEON_BLUE = (50, 150, 255)
NEON_GREEN = (50, 255, 150)
NEON_CYAN = (50, 255, 255)
NEON_YELLOW = (255, 255, 50)
NEON_RED = (255, 50, 50)
NEON_PURPLE = (150, 50, 255)
NEON_ORANGE = (255, 150, 50)
WARP_BLUE = (100, 200, 255)
QUANTUM_PURPLE = (200, 100, 255)
DANGER_RED = (255, 100, 100)

class QuantumParticle:
    def __init__(self):
        self.x = random.uniform(-2, 2)
        self.y = random.uniform(-2, 2)
        self.z = random.uniform(0.1, 1)
        self.quantum_phase = random.uniform(0, 2 * math.pi)
        self.energy = random.uniform(0.5, 1.0)
        self.color_shift = random.uniform(0, 360)
        
    def update(self, quantum_field_strength):
        # Quantum tunneling effect
        tunnel_chance = quantum_field_strength * 0.01
        if random.random() < tunnel_chance:
            self.x += random.uniform(-0.5, 0.5)
            self.y += random.uniform(-0.5, 0.5)
            
        # Quantum phase evolution
        self.quantum_phase += quantum_field_strength * 0.1
        self.energy *= 0.99  # Quantum decay
        
        # Recharge if energy too low
        if self.energy < 0.1:
            self.energy = random.uniform(0.5, 1.0)
            
    def draw(self, surface, center_x, center_y):
        if self.z > 0:
            screen_x = self.x / self.z * WIDTH/4 + center_x
            screen_y = self.y / self.z * HEIGHT/4 + center_y
            
            if 0 <= screen_x < WIDTH and 0 <= screen_y < HEIGHT:
                # Quantum glow effect
                intensity = int(self.energy * 255)
                phase_color = (
                    max(0, min(255, int(intensity * abs(math.sin(self.quantum_phase))))),
                    max(0, min(255, int(intensity * abs(math.sin(self.quantum_phase + 2.1))))),
                    max(0, min(255, int(intensity * abs(math.sin(self.quantum_phase + 4.2)))))
                )
                
                size = max(1, int(self.energy * 3))
                pygame.draw.circle(surface, phase_color, (int(screen_x), int(screen_y)), size)

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
        self.stellar_type = random.choice(['main', 'giant', 'dwarf', 'neutron', 'pulsar'])
        self.luminosity = random.uniform(0.3, 1.0)
        
    def update(self, speed, direction_x=0, direction_y=0, warp_distortion=0):
        self.prev_x = self.get_screen_x()
        self.prev_y = self.get_screen_y()
        
        # Warp distortion effects
        if warp_distortion > 0:
            distortion_x = math.sin(time.time() * 2 + self.x * 10) * warp_distortion * 0.1
            distortion_y = math.cos(time.time() * 2 + self.y * 10) * warp_distortion * 0.1
            self.x += distortion_x
            self.y += distortion_y
        
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
            self.stellar_type = random.choice(['main', 'giant', 'dwarf', 'neutron', 'pulsar'])
            self.luminosity = random.uniform(0.3, 1.0)
    
    def get_screen_x(self):
        return (self.x + self.center_x) / self.z * WIDTH/2 + WIDTH/2
    
    def get_screen_y(self):
        return (self.y + self.center_y) / self.z * HEIGHT/2 + HEIGHT/2
    
    def draw(self, surface, color_mode=0, pixel_size=1, twinkle=False, time_val=0):
        if self.z > 0:
            screen_x = self.get_screen_x()
            screen_y = self.get_screen_y()
            
            # Check if star is on screen
            if 0 <= screen_x < WIDTH and 0 <= screen_y < HEIGHT:
                # Calculate star size based on distance and stellar type
                base_size = max(1, int((1 - self.z) * 4))
                if self.stellar_type == 'giant':
                    base_size *= 2
                elif self.stellar_type == 'neutron':
                    base_size = max(1, base_size // 2)
                elif self.stellar_type == 'pulsar':
                    base_size = max(1, int(base_size * (1 + 0.5 * math.sin(time_val * 10))))
                
                size = base_size * pixel_size
                
                # Calculate brightness based on distance and luminosity
                base_brightness = int(255 * (1 - self.z) * self.luminosity)
                
                # Apply twinkle effect
                if twinkle:
                    twinkle_factor = 0.7 + 0.3 * math.sin(time_val * 5 + self.twinkle_phase)
                    brightness = int(base_brightness * twinkle_factor)
                else:
                    brightness = base_brightness
                
                # Get color based on mode and stellar type
                color = self.get_color(color_mode, brightness, time_val)
                
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
                        trail_color = tuple(max(0, min(255, c//3)) for c in color)
                        pygame.draw.line(surface, trail_color, 
                                       (int(self.prev_x), int(self.prev_y)), 
                                       (int(screen_x), int(screen_y)), 
                                       max(1, pixel_size))
    
    def get_color(self, color_mode, brightness, time_val):
        """Get star color based on mode and stellar type"""
        if self.stellar_type == 'neutron':
            return (brightness, brightness, max(0, min(255, brightness + 50)))
        elif self.stellar_type == 'pulsar':
            pulse = abs(math.sin(time_val * 10))
            return (max(0, min(255, int(brightness * pulse))), 
                    max(0, min(255, int(brightness * pulse * 0.5))), 
                    max(0, min(255, brightness)))
        elif self.stellar_type == 'giant':
            return (brightness, max(0, min(255, brightness//2)), max(0, min(255, brightness//4)))
        elif self.stellar_type == 'dwarf':
            return (max(0, min(255, brightness//2)), max(0, min(255, brightness//2)), brightness)
        
        # Normal stellar colors based on mode
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
            
            return (max(0, min(255, int((r + m) * 255))), 
                    max(0, min(255, int((g + m) * 255))), 
                    max(0, min(255, int((b + m) * 255))))
        elif color_mode == 2:  # Blue nebula
            return (max(0, min(255, brightness//4)), max(0, min(255, brightness//2)), brightness)
        elif color_mode == 3:  # Red giant
            return (brightness, max(0, min(255, brightness//4)), max(0, min(255, brightness//8)))
        elif color_mode == 4:  # Green space
            return (max(0, min(255, brightness//8)), brightness, max(0, min(255, brightness//4)))
        else:  # Purple void
            return (max(0, min(255, brightness//2)), max(0, min(255, brightness//8)), brightness)

class AdvancedWarpDrive:
    def __init__(self):
        self.stars = []
        self.quantum_particles = []
        self.star_count = 200
        self.speed = 0.01
        self.direction_x = 0
        self.direction_y = 0
        self.color_mode = 0
        self.pixel_size = 1
        self.twinkle = False
        self.warp_mode = 0  # 0: Normal, 1: Quantum, 2: Hyperspace, 3: Wormhole, 4: Emergency
        self.show_trails = True
        self.show_hud = True
        
        # Advanced systems
        self.fuel_level = 100.0
        self.energy_level = 100.0
        self.quantum_field_strength = 0.0
        self.hull_integrity = 100.0
        self.navigation_computer = True
        self.emergency_mode = False
        self.auto_pilot = False
        self.warp_core_temp = 0.0
        
        # Galactic coordinates
        self.galactic_x = 0.0
        self.galactic_y = 0.0
        self.galactic_z = 0.0
        self.sector = "Alpha"
        self.quadrant = "001"
        
        # Hazards and events
        self.solar_storm = False
        self.asteroid_field = False
        self.quantum_anomaly = False
        self.time_distortion = False
        
        self.color_mode_names = {
            0: "STELLAR.STANDARD",
            1: "SPECTRAL.ANALYSIS", 
            2: "NEBULA.FILTER",
            3: "RED.GIANT.MODE",
            4: "QUANTUM.SPACE",
            5: "VOID.DETECTION"
        }
        
        self.warp_mode_names = {
            0: "IMPULSE.DRIVE",
            1: "QUANTUM.DRIVE",
            2: "HYPERSPACE.JUMP",
            3: "WORMHOLE.TRANSIT",
            4: "EMERGENCY.POWER"
        }
        
        self.initialize_systems()
    
    def initialize_systems(self):
        """Initialize all ship systems"""
        self.stars = [Star() for _ in range(self.star_count)]
        self.quantum_particles = [QuantumParticle() for _ in range(50)]
        
    def update_systems(self, time_val):
        """Update all ship systems"""
        # Fuel consumption based on speed and warp mode
        base_consumption = self.speed * 0.1
        if self.warp_mode == 1:  # Quantum drive
            base_consumption *= 1.5
        elif self.warp_mode == 2:  # Hyperspace
            base_consumption *= 2.0
        elif self.warp_mode == 3:  # Wormhole
            base_consumption *= 3.0
        elif self.warp_mode == 4:  # Emergency
            base_consumption *= 0.5
            
        self.fuel_level = max(0, self.fuel_level - base_consumption)
        
        # Energy consumption for navigation and systems
        energy_consumption = 0.02
        if self.navigation_computer:
            energy_consumption += 0.01
        if abs(self.direction_x) > 0 or abs(self.direction_y) > 0:
            energy_consumption += 0.03
            
        self.energy_level = max(0, self.energy_level - energy_consumption)
        
        # Warp core temperature
        target_temp = self.speed * 100
        if self.warp_mode >= 2:
            target_temp *= 1.5
        self.warp_core_temp += (target_temp - self.warp_core_temp) * 0.1
        
        # Hull integrity degradation in hazardous conditions
        if self.solar_storm or self.asteroid_field or self.quantum_anomaly:
            self.hull_integrity = max(0, self.hull_integrity - 0.1)
        else:
            self.hull_integrity = min(100, self.hull_integrity + 0.05)
        
        # Update galactic coordinates
        self.galactic_x += self.direction_x * self.speed * 1000
        self.galactic_y += self.direction_y * self.speed * 1000
        self.galactic_z += self.speed * 1000
        
        # Update sector and quadrant
        sector_num = int(abs(self.galactic_x) // 10000) % 26
        self.sector = chr(ord('A') + sector_num)
        self.quadrant = f"{int(abs(self.galactic_y) // 5000) % 1000:03d}"
        
        # Random hazard generation
        if random.random() < 0.001:  # 0.1% chance per frame
            self.generate_hazard()
        
        # Clear hazards randomly
        if random.random() < 0.01:  # 1% chance per frame
            self.clear_hazards()
        
        # Emergency mode activation
        if self.fuel_level < 10 or self.energy_level < 10 or self.hull_integrity < 20:
            self.emergency_mode = True
            self.warp_mode = 4  # Emergency power
        else:
            self.emergency_mode = False
        
        # Quantum field strength for quantum drive
        if self.warp_mode == 1:
            self.quantum_field_strength = min(self.quantum_field_strength + 0.1, 1.0)
        else:
            self.quantum_field_strength = max(self.quantum_field_strength - 0.05, 0.0)
            
    def generate_hazard(self):
        """Generate random space hazards"""
        hazard_type = random.choice(['solar_storm', 'asteroid_field', 'quantum_anomaly', 'time_distortion'])
        if hazard_type == 'solar_storm':
            self.solar_storm = True
        elif hazard_type == 'asteroid_field':
            self.asteroid_field = True
        elif hazard_type == 'quantum_anomaly':
            self.quantum_anomaly = True
        elif hazard_type == 'time_distortion':
            self.time_distortion = True
            
    def clear_hazards(self):
        """Clear random hazards"""
        self.solar_storm = False
        self.asteroid_field = False
        self.quantum_anomaly = False
        self.time_distortion = False
        
    def update_stars(self, time_val):
        """Update all stars based on warp mode"""
        warp_distortion = 0
        
        for star in self.stars:
            if self.warp_mode == 0:  # Normal impulse
                star.update(self.speed, self.direction_x, self.direction_y)
            elif self.warp_mode == 1:  # Quantum drive
                warp_distortion = self.quantum_field_strength
                star.update(self.speed * 1.5, self.direction_x, self.direction_y, warp_distortion)
            elif self.warp_mode == 2:  # Hyperspace
                hyper_time = time_val * 2
                hyper_x = math.cos(hyper_time) * 0.1
                hyper_y = math.sin(hyper_time) * 0.1
                star.update(self.speed * 2, hyper_x, hyper_y)
            elif self.warp_mode == 3:  # Wormhole
                wormhole_time = time_val * 3
                wormhole_x = math.cos(wormhole_time) * 0.2
                wormhole_y = math.sin(wormhole_time) * 0.2
                star.update(self.speed * 3, wormhole_x, wormhole_y, 0.5)
            else:  # Emergency power
                star.update(self.speed * 0.5, self.direction_x * 0.5, self.direction_y * 0.5)
        
        # Update quantum particles
        for particle in self.quantum_particles:
            particle.update(self.quantum_field_strength)
    
    def draw_stars(self, surface, time_val):
        """Draw all stars"""
        for star in self.stars:
            star.draw(surface, self.color_mode, self.pixel_size, self.twinkle, time_val)
    
    def draw_quantum_field(self, surface):
        """Draw quantum field effects"""
        if self.quantum_field_strength > 0:
            for particle in self.quantum_particles:
                particle.draw(surface, WIDTH//2, HEIGHT//2)
    
    def draw_warp_tunnel(self, surface, time_val):
        """Draw warp tunnel effects"""
        if self.warp_mode >= 2:
            center_x, center_y = WIDTH//2, HEIGHT//2
            tunnel_rings = 8
            
            for i in range(tunnel_rings):
                progress = (time_val * 2 + i * 0.5) % 4
                radius = int(20 + progress * 50)
                
                if radius < 200:
                    alpha = int(255 * (1 - progress / 4))
                    if self.warp_mode == 2:  # Hyperspace
                        color = (alpha, alpha//2, alpha)
                    else:  # Wormhole
                        color = (alpha//2, alpha, alpha)
                    
                    pygame.draw.circle(surface, color, (center_x, center_y), radius, 2)
    
    def draw_hazard_effects(self, surface, time_val):
        """Draw hazard visual effects"""
        if self.solar_storm:
            # Solar storm effect
            for i in range(20):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                intensity = int(100 + 155 * abs(math.sin(time_val * 8 + i)))
                color = (intensity, intensity//2, 0)
                pygame.draw.circle(surface, color, (x, y), 2)
        
        if self.asteroid_field:
            # Asteroid field effect
            for i in range(15):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                size = random.randint(2, 6)
                color = (100, 80, 60)
                pygame.draw.circle(surface, color, (x, y), size)
        
        if self.quantum_anomaly:
            # Quantum anomaly effect
            center_x, center_y = WIDTH//2, HEIGHT//2
            anomaly_radius = int(50 + 30 * math.sin(time_val * 4))
            colors = [(255, 0, 255), (0, 255, 255), (255, 255, 0)]
            
            for i, color in enumerate(colors):
                offset_angle = time_val * 2 + i * 2.1
                offset_x = int(center_x + math.cos(offset_angle) * 20)
                offset_y = int(center_y + math.sin(offset_angle) * 20)
                pygame.draw.circle(surface, color, (offset_x, offset_y), anomaly_radius, 3)
    
    def draw_advanced_hud(self, surface):
        """Draw advanced HUD elements"""
        if self.show_hud:
            # Main crosshair
            crosshair_color = NEON_GREEN if not self.emergency_mode else DANGER_RED
            pygame.draw.line(surface, crosshair_color, 
                           (WIDTH//2 - 15, HEIGHT//2), 
                           (WIDTH//2 + 15, HEIGHT//2), 2)
            pygame.draw.line(surface, crosshair_color, 
                           (WIDTH//2, HEIGHT//2 - 15), 
                           (WIDTH//2, HEIGHT//2 + 15), 2)
            
            # Navigation compass
            if self.direction_x != 0 or self.direction_y != 0:
                radar_x = WIDTH - 60
                radar_y = 60
                pygame.draw.circle(surface, NEON_CYAN, (radar_x, radar_y), 25, 2)
                
                # Direction indicator
                dir_length = 20
                end_x = radar_x + self.direction_x * dir_length * 100
                end_y = radar_y + self.direction_y * dir_length * 100
                pygame.draw.line(surface, NEON_GREEN, 
                               (radar_x, radar_y), 
                               (int(end_x), int(end_y)), 3)
                
                # Compass markings
                for angle in range(0, 360, 45):
                    mark_x = radar_x + math.cos(math.radians(angle)) * 22
                    mark_y = radar_y + math.sin(math.radians(angle)) * 22
                    pygame.draw.circle(surface, NEON_CYAN, (int(mark_x), int(mark_y)), 2)
            
            # System status indicators
            status_y = HEIGHT - 80
            
            # Fuel gauge
            fuel_width = int(60 * (self.fuel_level / 100))
            fuel_color = NEON_GREEN if self.fuel_level > 30 else NEON_YELLOW if self.fuel_level > 10 else DANGER_RED
            pygame.draw.rect(surface, fuel_color, (10, status_y, fuel_width, 8))
            pygame.draw.rect(surface, NEON_CYAN, (10, status_y, 60, 8), 1)
            
            # Energy gauge
            energy_width = int(60 * (self.energy_level / 100))
            energy_color = NEON_GREEN if self.energy_level > 30 else NEON_YELLOW if self.energy_level > 10 else DANGER_RED
            pygame.draw.rect(surface, energy_color, (10, status_y + 12, energy_width, 8))
            pygame.draw.rect(surface, NEON_CYAN, (10, status_y + 12, 60, 8), 1)
            
            # Hull integrity
            hull_width = int(60 * (self.hull_integrity / 100))
            hull_color = NEON_GREEN if self.hull_integrity > 50 else NEON_YELLOW if self.hull_integrity > 20 else DANGER_RED
            pygame.draw.rect(surface, hull_color, (10, status_y + 24, hull_width, 8))
            pygame.draw.rect(surface, NEON_CYAN, (10, status_y + 24, 60, 8), 1)
            
            # Warp core temperature
            temp_width = int(60 * (self.warp_core_temp / 100))
            temp_color = NEON_BLUE if self.warp_core_temp < 70 else NEON_YELLOW if self.warp_core_temp < 90 else DANGER_RED
            pygame.draw.rect(surface, temp_color, (10, status_y + 36, temp_width, 8))
            pygame.draw.rect(surface, NEON_CYAN, (10, status_y + 36, 60, 8), 1)
            
            # Emergency indicators
            if self.emergency_mode:
                warning_text = "⚠ EMERGENCY MODE ⚠"
                font = pygame.font.Font(None, 24)
                text_surface = font.render(warning_text, True, DANGER_RED)
                surface.blit(text_surface, (WIDTH//2 - 80, 10))
            
            # Hazard warnings
            warning_y = 40
            if self.solar_storm:
                font = pygame.font.Font(None, 20)
                text = font.render("⚡ SOLAR STORM", True, NEON_YELLOW)
                surface.blit(text, (WIDTH//2 - 50, warning_y))
                warning_y += 20
            
            if self.asteroid_field:
                font = pygame.font.Font(None, 20)
                text = font.render("🌑 ASTEROID FIELD", True, NEON_ORANGE)
                surface.blit(text, (WIDTH//2 - 60, warning_y))
                warning_y += 20
            
            if self.quantum_anomaly:
                font = pygame.font.Font(None, 20)
                text = font.render("🌀 QUANTUM ANOMALY", True, QUANTUM_PURPLE)
                surface.blit(text, (WIDTH//2 - 70, warning_y))
    
    def draw_navigation_computer(self, surface):
        """Draw navigation computer display"""
        if self.navigation_computer:
            # Navigation panel
            nav_rect = pygame.Rect(WIDTH - 150, 10, 140, 100)
            pygame.draw.rect(surface, CYBER_BLACK, nav_rect)
            pygame.draw.rect(surface, NEON_CYAN, nav_rect, 2)
            
            font = pygame.font.Font(None, 18)
            
            # Coordinates
            coord_text = font.render(f"SECTOR: {self.sector}", True, NEON_GREEN)
            surface.blit(coord_text, (WIDTH - 145, 20))
            
            quad_text = font.render(f"QUAD: {self.quadrant}", True, NEON_GREEN)
            surface.blit(quad_text, (WIDTH - 145, 35))
            
            # Position
            pos_text = font.render(f"X: {self.galactic_x:.1f}", True, NEON_BLUE)
            surface.blit(pos_text, (WIDTH - 145, 55))
            
            pos_text = font.render(f"Y: {self.galactic_y:.1f}", True, NEON_BLUE)
            surface.blit(pos_text, (WIDTH - 145, 70))
            
            pos_text = font.render(f"Z: {self.galactic_z:.1f}", True, NEON_BLUE)
            surface.blit(pos_text, (WIDTH - 145, 85))
    
    def draw_system_status(self, surface):
        """Draw detailed system status"""
        font = pygame.font.Font(None, 16)
        y_offset = 10
        
        # System labels
        labels = ["FUEL", "ENERGY", "HULL", "CORE"]
        values = [f"{self.fuel_level:.1f}%", f"{self.energy_level:.1f}%", 
                 f"{self.hull_integrity:.1f}%", f"{self.warp_core_temp:.1f}°C"]
        
        for i, (label, value) in enumerate(zip(labels, values)):
            color = NEON_GREEN if i < 3 else NEON_BLUE
            if i == 0 and self.fuel_level < 20:
                color = DANGER_RED
            elif i == 1 and self.energy_level < 20:
                color = DANGER_RED
            elif i == 2 and self.hull_integrity < 30:
                color = DANGER_RED
            elif i == 3 and self.warp_core_temp > 80:
                color = DANGER_RED
            
            text = font.render(f"{label}: {value}", True, color)
            surface.blit(text, (85, y_offset + i * 15))
        
        # Current settings
        speed_text = font.render(f"WARP: {self.speed:.3f}", True, NEON_CYAN)
        surface.blit(speed_text, (85, y_offset + 70))
        
        stars_text = font.render(f"STARS: {self.star_count}", True, NEON_CYAN)
        surface.blit(stars_text, (85, y_offset + 85))
        
        mode_text = font.render(f"MODE: {self.warp_mode_names[self.warp_mode]}", True, NEON_PURPLE)
        surface.blit(mode_text, (85, y_offset + 100))
        
        color_text = font.render(f"SCAN: {self.color_mode_names[self.color_mode]}", True, NEON_YELLOW)
        surface.blit(color_text, (85, y_offset + 115))
    
    def draw_controls_help(self, surface):
        """Draw control instructions"""
        font = pygame.font.Font(None, 14)
        controls = [
            "FLIGHT CONTROLS:",
            "↑↓ Warp Speed", "WASD Navigation", "+/- Star Density",
            "",
            "SYSTEMS:",
            "M: Warp Mode", "C: Scanner Mode", "T: Stellar Twinkle",
            "N: Nav Computer", "H: HUD Toggle", "A: Auto Pilot",
            "",
            "EMERGENCY:",
            "E: Emergency Systems", "R: Full Reset",
            "F11: Fullscreen", "ESC: Return to Launcher"
        ]
        
        y_start = HEIGHT - 200
        for i, control in enumerate(controls):
            color = NEON_GREEN if control.endswith(":") else NEON_CYAN
            if "EMERGENCY" in control:
                color = DANGER_RED
            
            text = font.render(control, True, color)
            surface.blit(text, (10, y_start + i * 12))
    
    def handle_input(self, keys):
        """Handle keyboard input"""
        # Speed controls
        if keys[pygame.K_UP]:
            max_speed = 0.05 if self.warp_mode < 2 else 0.1
            self.speed = min(self.speed + 0.002, max_speed)
        if keys[pygame.K_DOWN]:
            self.speed = max(self.speed - 0.002, 0.001)
        
        # Navigation controls
        if keys[pygame.K_w]:
            self.direction_y = max(self.direction_y - 0.02, -0.8)
        if keys[pygame.K_s]:
            self.direction_y = min(self.direction_y + 0.02, 0.8)
        if keys[pygame.K_a]:
            self.direction_x = max(self.direction_x - 0.02, -0.8)
        if keys[pygame.K_d]:
            self.direction_x = min(self.direction_x + 0.02, 0.8)
        
        # Star density controls
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.star_count = min(self.star_count + 5, 800)
            if len(self.stars) < self.star_count:
                self.stars.extend([Star() for _ in range(self.star_count - len(self.stars))])
        if keys[pygame.K_MINUS]:
            self.star_count = max(self.star_count - 5, 50)
            if len(self.stars) > self.star_count:
                self.stars = self.stars[:self.star_count]
        
        # Auto pilot
        if self.auto_pilot:
            # Automatically navigate to avoid hazards
            if self.solar_storm or self.asteroid_field or self.quantum_anomaly:
                self.direction_x += random.uniform(-0.01, 0.01)
                self.direction_y += random.uniform(-0.01, 0.01)
            
            # Maintain optimal speed
            if self.fuel_level > 50:
                self.speed = min(self.speed + 0.001, 0.03)
            else:
                self.speed = max(self.speed - 0.001, 0.01)
    
    def cycle_color_mode(self):
        """Cycle scanner mode"""
        self.color_mode = (self.color_mode + 1) % len(self.color_mode_names)
    
    def cycle_warp_mode(self):
        """Cycle warp mode"""
        if not self.emergency_mode:
            self.warp_mode = (self.warp_mode + 1) % (len(self.warp_mode_names) - 1)  # Exclude emergency
        else:
            self.warp_mode = 4  # Force emergency mode
    
    def toggle_twinkle(self):
        """Toggle stellar twinkle effect"""
        self.twinkle = not self.twinkle
    
    def toggle_hud(self):
        """Toggle HUD display"""
        self.show_hud = not self.show_hud
    
    def toggle_nav_computer(self):
        """Toggle navigation computer"""
        self.navigation_computer = not self.navigation_computer
    
    def toggle_auto_pilot(self):
        """Toggle auto pilot"""
        self.auto_pilot = not self.auto_pilot
    
    def emergency_stop(self):
        """Emergency stop all systems"""
        self.emergency_mode = True
        self.speed = 0.005
        self.direction_x = 0
        self.direction_y = 0
        self.warp_mode = 4
    
    def reset_navigation(self):
        """Reset navigation to center"""
        self.direction_x = 0
        self.direction_y = 0
    
    def full_reset(self):
        """Full system reset"""
        self.speed = 0.01
        self.star_count = 200
        self.color_mode = 0
        self.warp_mode = 0
        self.twinkle = False
        self.fuel_level = 100.0
        self.energy_level = 100.0
        self.hull_integrity = 100.0
        self.warp_core_temp = 0.0
        self.emergency_mode = False
        self.auto_pilot = False
        self.reset_navigation()
        self.initialize_systems()
        self.clear_hazards()

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

def main():
    warp_drive = AdvancedWarpDrive()
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
                elif event.key == pygame.K_c:
                    warp_drive.cycle_color_mode()
                elif event.key == pygame.K_m:
                    warp_drive.cycle_warp_mode()
                elif event.key == pygame.K_t:
                    warp_drive.toggle_twinkle()
                elif event.key == pygame.K_h:
                    warp_drive.toggle_hud()
                elif event.key == pygame.K_n:
                    warp_drive.toggle_nav_computer()
                elif event.key == pygame.K_z:
                    warp_drive.toggle_auto_pilot()
                elif event.key == pygame.K_e:
                    warp_drive.emergency_stop()
                elif event.key == pygame.K_r:
                    warp_drive.full_reset()
                elif event.key == pygame.K_SPACE:
                    warp_drive.reset_navigation()
                elif event.key == pygame.K_F1:
                    show_ui = not show_ui
        
        # Handle continuous input
        warp_drive.handle_input(keys)
        
        # Calculate time-based animation
        current_time = time.time() - start_time
        
        # Update all systems
        warp_drive.update_systems(current_time)
        
        # Clear screen
        screen.fill(CYBER_BLACK)
        
        # Draw hazard effects first
        warp_drive.draw_hazard_effects(screen, current_time)
        
        # Draw warp tunnel effects
        warp_drive.draw_warp_tunnel(screen, current_time)
        
        # Update and draw stars
        warp_drive.update_stars(current_time)
        warp_drive.draw_stars(screen, current_time)
        
        # Draw quantum field
        warp_drive.draw_quantum_field(screen)
        
        # Draw advanced HUD
        warp_drive.draw_advanced_hud(screen)
        
        # Draw navigation computer
        warp_drive.draw_navigation_computer(screen)
        
        # Draw UI if enabled
        if show_ui:
            # Semi-transparent background for UI
            ui_surface = pygame.Surface((400, 250))
            ui_surface.set_alpha(200)
            ui_surface.fill(CYBER_BLACK)
            screen.blit(ui_surface, (5, 5))
            
            warp_drive.draw_system_status(screen)
            warp_drive.draw_controls_help(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main() 