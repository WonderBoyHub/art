#!/usr/bin/env python3
"""
Advanced Astrophysics Simulator - Complete universe simulation with stellar evolution
Perfect for Raspberry Pi 5 with 3.5" display (480x320)
COMPLETE ASTROPHYSICS SIMULATION WITH STELLAR EVOLUTION AND COSMIC PHENOMENA
"""

import pygame
import numpy as np
import random
import math
import time
import sys
import subprocess
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

# Initialize Pygame
pygame.init()

# Screen dimensions optimized for Pi 5
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Astrophysics Simulator")

# Fullscreen support
fullscreen = False
clock = pygame.time.Clock()
start_time = time.time()

# Enhanced astrophysics color palette
CYBER_BLACK = (2, 2, 8)
NEON_BLUE = (50, 150, 255)
NEON_GREEN = (50, 255, 150)
NEON_CYAN = (50, 255, 255)
NEON_YELLOW = (255, 255, 50)
NEON_RED = (255, 50, 50)
NEON_PURPLE = (150, 50, 255)
NEON_ORANGE = (255, 150, 50)
COSMIC_COLORS = {
    'red_giant': (255, 100, 50),
    'white_dwarf': (255, 255, 255),
    'neutron_star': (150, 150, 255),
    'black_hole': (50, 0, 100),
    'main_sequence': (255, 255, 150),
    'brown_dwarf': (150, 100, 50),
    'supernova': (255, 200, 100),
    'galaxy_core': (255, 150, 255),
    'nebula': (100, 255, 200),
    'dark_matter': (50, 50, 80)
}

class StellarType(Enum):
    MAIN_SEQUENCE = 0
    RED_GIANT = 1
    WHITE_DWARF = 2
    NEUTRON_STAR = 3
    BLACK_HOLE = 4
    BROWN_DWARF = 5
    SUPERNOVA = 6
    PROTOSTAR = 7

class PlanetType(Enum):
    TERRESTRIAL = 0
    GAS_GIANT = 1
    ICE_GIANT = 2
    DWARF_PLANET = 3
    ASTEROID = 4
    COMET = 5

class SimulationMode(Enum):
    SOLAR_SYSTEM = 0
    STELLAR_EVOLUTION = 1
    GALAXY_FORMATION = 2
    COSMIC_PHENOMENA = 3
    GRAVITATIONAL_WAVES = 4
    DARK_MATTER = 5
    EXOPLANET_HUNT = 6
    SUPERNOVA_SIMULATION = 7

@dataclass
class StellarParameters:
    """Stellar physics parameters"""
    mass: float  # Solar masses
    radius: float  # Solar radii
    temperature: float  # Kelvin
    luminosity: float  # Solar luminosities
    age: float  # Millions of years
    metallicity: float  # [Fe/H]
    
    def __post_init__(self):
        # Clamp values to realistic ranges
        self.mass = max(0.08, min(150, self.mass))
        self.temperature = max(1000, min(50000, self.temperature))
        self.age = max(0, min(13700, self.age))

class CelestialBody:
    """Base class for all celestial objects"""
    def __init__(self, x: float, y: float, body_type: str):
        self.x = x
        self.y = y
        self.body_type = body_type
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.mass = 1.0
        self.radius = 1.0
        self.temperature = 5778  # Sun's temperature
        self.age = 0.0
        self.brightness = 1.0
        self.color = COSMIC_COLORS.get(body_type, NEON_YELLOW)
        
    def update_position(self, dt: float):
        """Update position based on velocity"""
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
    def apply_gravity(self, other: 'CelestialBody', dt: float):
        """Apply gravitational force from another body"""
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Gravitational constant (scaled for simulation)
            G = 100.0
            force = G * self.mass * other.mass / (distance * distance)
            
            # Apply force
            force_x = force * dx / distance
            force_y = force * dy / distance
            
            self.velocity_x += force_x / self.mass * dt
            self.velocity_y += force_y / self.mass * dt

class Star(CelestialBody):
    """Advanced star with stellar evolution"""
    def __init__(self, x: float, y: float, stellar_type: StellarType = StellarType.MAIN_SEQUENCE):
        super().__init__(x, y, stellar_type.name.lower())
        self.stellar_type = stellar_type
        self.stellar_params = StellarParameters(
            mass=1.0,
            radius=1.0,
            temperature=5778,
            luminosity=1.0,
            age=0.0,
            metallicity=0.0
        )
        self.fusion_rate = 1.0
        self.convection_cells = []
        self.magnetic_field_strength = 1.0
        self.stellar_wind_speed = 400.0  # km/s
        self.evolutionary_stage = 0
        
        # Generate stellar parameters based on type
        self.generate_stellar_parameters()
        
    def generate_stellar_parameters(self):
        """Generate realistic stellar parameters"""
        if self.stellar_type == StellarType.MAIN_SEQUENCE:
            self.stellar_params.mass = random.uniform(0.1, 20.0)
            self.stellar_params.radius = self.stellar_params.mass ** 0.8
            self.stellar_params.temperature = 5778 * (self.stellar_params.mass ** 0.5)
            self.stellar_params.luminosity = self.stellar_params.mass ** 3.5
            self.color = self.temperature_to_color(self.stellar_params.temperature)
        elif self.stellar_type == StellarType.RED_GIANT:
            self.stellar_params.mass = random.uniform(0.5, 8.0)
            self.stellar_params.radius = random.uniform(10, 100)
            self.stellar_params.temperature = random.uniform(3000, 4000)
            self.stellar_params.luminosity = random.uniform(100, 3000)
            self.color = COSMIC_COLORS['red_giant']
        elif self.stellar_type == StellarType.WHITE_DWARF:
            self.stellar_params.mass = random.uniform(0.3, 1.4)
            self.stellar_params.radius = 0.01  # Very small
            self.stellar_params.temperature = random.uniform(8000, 40000)
            self.stellar_params.luminosity = random.uniform(0.001, 0.1)
            self.color = COSMIC_COLORS['white_dwarf']
        elif self.stellar_type == StellarType.NEUTRON_STAR:
            self.stellar_params.mass = random.uniform(1.4, 3.0)
            self.stellar_params.radius = 0.00001  # Extremely small
            self.stellar_params.temperature = random.uniform(1e6, 1e7)
            self.stellar_params.luminosity = random.uniform(0.1, 10)
            self.color = COSMIC_COLORS['neutron_star']
        elif self.stellar_type == StellarType.BLACK_HOLE:
            self.stellar_params.mass = random.uniform(3.0, 100.0)
            self.stellar_params.radius = 0.000001  # Event horizon
            self.stellar_params.temperature = 0  # Hawking radiation negligible
            self.stellar_params.luminosity = 0
            self.color = COSMIC_COLORS['black_hole']
        
        self.mass = self.stellar_params.mass
        self.radius = max(1, self.stellar_params.radius * 2)  # Display radius
        self.temperature = self.stellar_params.temperature
        
    def temperature_to_color(self, temp: float) -> Tuple[int, int, int]:
        """Convert temperature to RGB color"""
        if temp < 3500:
            return (255, 100, 50)  # Red
        elif temp < 5000:
            return (255, 200, 100)  # Orange
        elif temp < 6000:
            return (255, 255, 150)  # Yellow
        elif temp < 7500:
            return (255, 255, 255)  # White
        elif temp < 10000:
            return (150, 200, 255)  # Blue-white
        else:
            return (100, 150, 255)  # Blue
    
    def evolve(self, dt: float):
        """Simulate stellar evolution"""
        self.stellar_params.age += dt * 100  # Accelerated time
        
        # Main sequence evolution
        if self.stellar_type == StellarType.MAIN_SEQUENCE:
            # Hydrogen burning
            self.fusion_rate = self.stellar_params.mass ** 3.5
            
            # Check for evolution off main sequence
            main_sequence_lifetime = 10000 / (self.stellar_params.mass ** 2.5)
            if self.stellar_params.age > main_sequence_lifetime:
                if self.stellar_params.mass < 8.0:
                    self.stellar_type = StellarType.RED_GIANT
                    self.generate_stellar_parameters()
                else:
                    self.stellar_type = StellarType.SUPERNOVA
                    self.generate_stellar_parameters()
        
        # Red giant evolution
        elif self.stellar_type == StellarType.RED_GIANT:
            # Helium burning
            self.stellar_params.radius += dt * 0.1
            if self.stellar_params.radius > 200:
                self.stellar_type = StellarType.WHITE_DWARF
                self.generate_stellar_parameters()
        
        # Supernova explosion
        elif self.stellar_type == StellarType.SUPERNOVA:
            self.stellar_params.luminosity += dt * 1000
            if self.stellar_params.luminosity > 10000:
                if self.stellar_params.mass < 20:
                    self.stellar_type = StellarType.NEUTRON_STAR
                else:
                    self.stellar_type = StellarType.BLACK_HOLE
                self.generate_stellar_parameters()
        
        # Update visual properties
        self.brightness = min(2.0, self.stellar_params.luminosity * 0.001)
        self.color = self.temperature_to_color(self.stellar_params.temperature)

class Planet(CelestialBody):
    """Planet with orbital mechanics"""
    def __init__(self, x: float, y: float, planet_type: PlanetType = PlanetType.TERRESTRIAL):
        super().__init__(x, y, planet_type.name.lower())
        self.planet_type = planet_type
        self.orbital_radius = 100.0
        self.orbital_velocity = 0.0
        self.orbital_angle = 0.0
        self.axial_tilt = 0.0
        self.rotation_period = 24.0  # hours
        self.atmosphere_thickness = 0.0
        self.surface_temperature = 288.0  # Kelvin
        self.has_life = False
        
        # Generate planet parameters
        self.generate_planet_parameters()
        
    def generate_planet_parameters(self):
        """Generate realistic planet parameters"""
        if self.planet_type == PlanetType.TERRESTRIAL:
            self.mass = random.uniform(0.1, 2.0)
            self.radius = random.uniform(0.3, 1.5)
            self.atmosphere_thickness = random.uniform(0, 2)
            self.surface_temperature = random.uniform(150, 400)
            self.color = (100, 150, 200) if self.surface_temperature < 300 else (200, 100, 50)
        elif self.planet_type == PlanetType.GAS_GIANT:
            self.mass = random.uniform(10, 300)
            self.radius = random.uniform(3, 11)
            self.atmosphere_thickness = self.radius
            self.surface_temperature = random.uniform(50, 200)
            self.color = (200, 150, 100)
        elif self.planet_type == PlanetType.ICE_GIANT:
            self.mass = random.uniform(5, 20)
            self.radius = random.uniform(2, 5)
            self.atmosphere_thickness = self.radius * 0.8
            self.surface_temperature = random.uniform(30, 80)
            self.color = (100, 200, 255)
        
        # Check for habitability
        if (200 < self.surface_temperature < 350 and 
            self.atmosphere_thickness > 0.5 and 
            self.planet_type == PlanetType.TERRESTRIAL):
            self.has_life = random.random() < 0.3
            if self.has_life:
                self.color = (50, 255, 50)

class GravitationalWave:
    """Gravitational wave propagation"""
    def __init__(self, source_x: float, source_y: float, strength: float):
        self.source_x = source_x
        self.source_y = source_y
        self.strength = strength
        self.radius = 0.0
        self.frequency = 100.0  # Hz
        self.amplitude = strength
        
    def propagate(self, dt: float):
        """Propagate gravitational wave"""
        # Speed of light (scaled for simulation)
        c = 100.0
        self.radius += c * dt
        
        # Amplitude decreases with distance
        self.amplitude = self.strength / (1 + self.radius * 0.01)
        
    def get_strain_at_point(self, x: float, y: float) -> float:
        """Calculate strain at given point"""
        distance = math.sqrt((x - self.source_x)**2 + (y - self.source_y)**2)
        if distance <= self.radius and distance > 0:
            phase = 2 * math.pi * self.frequency * (distance / 100.0)
            return self.amplitude * math.sin(phase) / distance
        return 0.0

class AstrophysicsSimulator:
    """Main astrophysics simulation engine"""
    def __init__(self):
        self.simulation_mode = SimulationMode.SOLAR_SYSTEM
        self.stars = []
        self.planets = []
        self.gravitational_waves = []
        
        # Simulation parameters
        self.time_scale = 1.0
        self.show_orbits = True
        self.show_gravitational_waves = True
        self.show_stellar_evolution = True
        self.show_magnetic_fields = False
        self.show_dark_matter = False
        
        # Physics constants (scaled for simulation)
        self.G = 100.0  # Gravitational constant
        self.c = 100.0  # Speed of light
        
        # UI state
        self.show_hud = True
        self.show_parameters = True
        self.selected_object = None
        self.paused = False
        
        # Initialize simulation based on mode
        self.initialize_simulation()
        
        # Mode names
        self.mode_names = {
            SimulationMode.SOLAR_SYSTEM: "Solar System",
            SimulationMode.STELLAR_EVOLUTION: "Stellar Evolution",
            SimulationMode.GALAXY_FORMATION: "Galaxy Formation",
            SimulationMode.COSMIC_PHENOMENA: "Cosmic Phenomena",
            SimulationMode.GRAVITATIONAL_WAVES: "Gravitational Waves",
            SimulationMode.DARK_MATTER: "Dark Matter",
            SimulationMode.EXOPLANET_HUNT: "Exoplanet Hunt",
            SimulationMode.SUPERNOVA_SIMULATION: "Supernova Simulation"
        }
        
    def initialize_simulation(self):
        """Initialize simulation based on current mode"""
        self.stars.clear()
        self.planets.clear()
        self.gravitational_waves.clear()
        
        if self.simulation_mode == SimulationMode.SOLAR_SYSTEM:
            self.create_solar_system()
        elif self.simulation_mode == SimulationMode.STELLAR_EVOLUTION:
            self.create_stellar_evolution_demo()
        elif self.simulation_mode == SimulationMode.GALAXY_FORMATION:
            self.create_galaxy_formation()
        elif self.simulation_mode == SimulationMode.GRAVITATIONAL_WAVES:
            self.create_gravitational_wave_demo()
        elif self.simulation_mode == SimulationMode.SUPERNOVA_SIMULATION:
            self.create_supernova_demo()
        else:
            self.create_generic_system()
    
    def create_solar_system(self):
        """Create a solar system simulation"""
        # Central star
        star = Star(WIDTH // 2, HEIGHT // 2, StellarType.MAIN_SEQUENCE)
        star.stellar_params.mass = 1.0
        star.mass = 1.0
        star.radius = 10
        self.stars.append(star)
        
        # Planets
        planet_distances = [30, 50, 80, 120, 160, 200]
        planet_types = [PlanetType.TERRESTRIAL, PlanetType.TERRESTRIAL, 
                       PlanetType.TERRESTRIAL, PlanetType.GAS_GIANT,
                       PlanetType.GAS_GIANT, PlanetType.ICE_GIANT]
        
        for i, (distance, ptype) in enumerate(zip(planet_distances, planet_types)):
            angle = random.uniform(0, 2 * math.pi)
            x = WIDTH // 2 + distance * math.cos(angle)
            y = HEIGHT // 2 + distance * math.sin(angle)
            
            planet = Planet(x, y, ptype)
            planet.orbital_radius = distance
            planet.orbital_angle = angle
            planet.orbital_velocity = math.sqrt(self.G * star.mass / distance)
            self.planets.append(planet)
    
    def create_stellar_evolution_demo(self):
        """Create stellar evolution demonstration"""
        # Stars at different evolutionary stages
        stellar_types = [StellarType.MAIN_SEQUENCE, StellarType.RED_GIANT,
                        StellarType.WHITE_DWARF, StellarType.NEUTRON_STAR,
                        StellarType.BLACK_HOLE]
        
        for i, stype in enumerate(stellar_types):
            x = 60 + i * 80
            y = HEIGHT // 2
            star = Star(x, y, stype)
            self.stars.append(star)
    
    def create_galaxy_formation(self):
        """Create galaxy formation simulation"""
        # Central supermassive black hole
        central_bh = Star(WIDTH // 2, HEIGHT // 2, StellarType.BLACK_HOLE)
        central_bh.stellar_params.mass = 1000.0
        central_bh.mass = 1000.0
        central_bh.radius = 5
        self.stars.append(central_bh)
        
        # Spiral arms with stars
        for arm in range(3):
            for i in range(20):
                angle = arm * 2 * math.pi / 3 + i * 0.3
                distance = 30 + i * 8
                x = WIDTH // 2 + distance * math.cos(angle)
                y = HEIGHT // 2 + distance * math.sin(angle)
                
                star = Star(x, y, StellarType.MAIN_SEQUENCE)
                star.stellar_params.mass = random.uniform(0.1, 10.0)
                star.mass = star.stellar_params.mass
                star.radius = max(1, star.stellar_params.mass * 2)
                
                # Orbital motion around galactic center
                orbital_velocity = math.sqrt(self.G * central_bh.mass / distance)
                star.velocity_x = -orbital_velocity * math.sin(angle)
                star.velocity_y = orbital_velocity * math.cos(angle)
                
                self.stars.append(star)
    
    def create_gravitational_wave_demo(self):
        """Create gravitational wave demonstration"""
        # Binary black hole system
        bh1 = Star(WIDTH // 2 - 30, HEIGHT // 2, StellarType.BLACK_HOLE)
        bh1.stellar_params.mass = 10.0
        bh1.mass = 10.0
        bh1.velocity_y = 20.0
        
        bh2 = Star(WIDTH // 2 + 30, HEIGHT // 2, StellarType.BLACK_HOLE)
        bh2.stellar_params.mass = 10.0
        bh2.mass = 10.0
        bh2.velocity_y = -20.0
        
        self.stars.extend([bh1, bh2])
    
    def create_supernova_demo(self):
        """Create supernova demonstration"""
        # Massive star about to explode
        star = Star(WIDTH // 2, HEIGHT // 2, StellarType.MAIN_SEQUENCE)
        star.stellar_params.mass = 25.0
        star.mass = 25.0
        star.radius = 15
        star.stellar_params.age = 9900  # Near end of life
        self.stars.append(star)
        
        # Surrounding stars to show shockwave effects
        for i in range(8):
            angle = i * math.pi / 4
            distance = 80
            x = WIDTH // 2 + distance * math.cos(angle)
            y = HEIGHT // 2 + distance * math.sin(angle)
            
            nearby_star = Star(x, y, StellarType.MAIN_SEQUENCE)
            nearby_star.stellar_params.mass = random.uniform(0.5, 2.0)
            nearby_star.mass = nearby_star.stellar_params.mass
            self.stars.append(nearby_star)
    
    def create_generic_system(self):
        """Create a generic multi-star system"""
        for i in range(5):
            x = random.uniform(50, WIDTH - 50)
            y = random.uniform(50, HEIGHT - 50)
            stype = random.choice(list(StellarType))
            star = Star(x, y, stype)
            self.stars.append(star)
    
    def update_simulation(self, dt: float):
        """Update the astrophysics simulation"""
        if self.paused:
            return
        
        scaled_dt = dt * self.time_scale
        
        # Update stellar evolution
        if self.show_stellar_evolution:
            for star in self.stars:
                star.evolve(scaled_dt)
        
        # Update gravitational interactions
        for i, star1 in enumerate(self.stars):
            for j, star2 in enumerate(self.stars):
                if i != j:
                    star1.apply_gravity(star2, scaled_dt)
        
        # Update positions
        for star in self.stars:
            star.update_position(scaled_dt)
            
            # Keep within bounds
            star.x = max(star.radius, min(WIDTH - star.radius, star.x))
            star.y = max(star.radius, min(HEIGHT - star.radius, star.y))
        
        # Update planetary orbits
        for planet in self.planets:
            if self.stars:
                central_star = self.stars[0]  # Assume first star is central
                
                # Calculate orbital motion
                dx = central_star.x - planet.x
                dy = central_star.y - planet.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 0:
                    # Orbital velocity
                    orbital_speed = math.sqrt(self.G * central_star.mass / distance)
                    
                    # Perpendicular velocity vector
                    planet.velocity_x = -orbital_speed * dy / distance
                    planet.velocity_y = orbital_speed * dx / distance
                    
                    planet.update_position(scaled_dt)
        
        # Update gravitational waves
        for wave in self.gravitational_waves[:]:
            wave.propagate(scaled_dt)
            
            # Remove old waves
            if wave.radius > WIDTH * 2:
                self.gravitational_waves.remove(wave)
        
        # Detect mergers and create gravitational waves
        if self.show_gravitational_waves:
            for i, star1 in enumerate(self.stars):
                for j, star2 in enumerate(self.stars[i+1:], i+1):
                    distance = math.sqrt((star1.x - star2.x)**2 + (star1.y - star2.y)**2)
                    
                    if distance < (star1.radius + star2.radius) * 0.5:
                        # Create gravitational wave
                        wave_strength = star1.mass * star2.mass / 100
                        wave = GravitationalWave(star1.x, star1.y, wave_strength)
                        self.gravitational_waves.append(wave)
                        
                        # Merge stars (simplified)
                        if len(self.stars) > 1:
                            merged_mass = star1.mass + star2.mass
                            star1.mass = merged_mass
                            star1.stellar_params.mass = merged_mass
                            star1.radius = max(star1.radius, star2.radius) * 1.2
                            self.stars.remove(star2)
                            break
    
    def draw_star(self, surface, star: Star):
        """Draw a star with appropriate visual effects"""
        x, y = int(star.x), int(star.y)
        
        # Draw star core
        pygame.draw.circle(surface, star.color, (x, y), int(star.radius))
        
        # Draw glow effect
        glow_radius = int(star.radius * 1.5)
        glow_color = tuple(int(c * 0.3) for c in star.color)
        pygame.draw.circle(surface, glow_color, (x, y), glow_radius, 2)
        
        # Draw stellar wind for massive stars
        if star.stellar_params.mass > 5.0:
            for i in range(8):
                angle = i * math.pi / 4
                wind_x = x + math.cos(angle) * glow_radius * 1.5
                wind_y = y + math.sin(angle) * glow_radius * 1.5
                pygame.draw.line(surface, glow_color, (x, y), (wind_x, wind_y), 1)
        
        # Special effects for different stellar types
        if star.stellar_type == StellarType.BLACK_HOLE:
            # Draw accretion disk
            for ring in range(3):
                ring_radius = int(star.radius * (2 + ring))
                pygame.draw.circle(surface, (100, 50, 200), (x, y), ring_radius, 1)
        
        elif star.stellar_type == StellarType.SUPERNOVA:
            # Draw explosion
            explosion_radius = int(star.radius * 3)
            explosion_color = (255, 200, 100)
            pygame.draw.circle(surface, explosion_color, (x, y), explosion_radius, 3)
            
            # Draw shockwave
            shockwave_radius = int(star.radius * 5)
            pygame.draw.circle(surface, (255, 100, 100), (x, y), shockwave_radius, 1)
        
        elif star.stellar_type == StellarType.NEUTRON_STAR:
            # Draw magnetic field lines
            for i in range(4):
                angle = i * math.pi / 2
                field_x = x + math.cos(angle) * star.radius * 3
                field_y = y + math.sin(angle) * star.radius * 3
                pygame.draw.line(surface, NEON_BLUE, (x, y), (field_x, field_y), 1)
    
    def draw_planet(self, surface, planet: Planet):
        """Draw a planet"""
        x, y = int(planet.x), int(planet.y)
        
        # Draw planet
        pygame.draw.circle(surface, planet.color, (x, y), int(planet.radius * 2))
        
        # Draw atmosphere
        if planet.atmosphere_thickness > 0:
            atm_radius = int(planet.radius * 2 + planet.atmosphere_thickness)
            atm_color = tuple(int(c * 0.3) for c in planet.color)
            pygame.draw.circle(surface, atm_color, (x, y), atm_radius, 1)
        
        # Draw life indicator
        if planet.has_life:
            life_color = NEON_GREEN
            pygame.draw.circle(surface, life_color, (x, y), int(planet.radius * 2), 1)
    
    def draw_gravitational_waves(self, surface):
        """Draw gravitational wave visualization"""
        for wave in self.gravitational_waves:
            if wave.amplitude > 0.1:
                x, y = int(wave.source_x), int(wave.source_y)
                
                # Draw wave fronts
                for i in range(3):
                    radius = int(wave.radius - i * 20)
                    if radius > 0:
                        alpha = int(wave.amplitude * 100)
                        color = (100, 100, 255, alpha)
                        pygame.draw.circle(surface, color[:3], (x, y), radius, 2)
    
    def draw_orbits(self, surface):
        """Draw orbital paths"""
        if not self.show_orbits or not self.stars:
            return
        
        central_star = self.stars[0]
        
        for planet in self.planets:
            distance = math.sqrt((planet.x - central_star.x)**2 + (planet.y - central_star.y)**2)
            orbit_color = (50, 50, 100)
            pygame.draw.circle(surface, orbit_color, 
                             (int(central_star.x), int(central_star.y)), 
                             int(distance), 1)
    
    def draw_hud(self, surface):
        """Draw heads-up display"""
        if not self.show_hud:
            return
        
        # Mode and status
        font = pygame.font.Font(None, 16)
        mode_text = f"Mode: {self.mode_names[self.simulation_mode]}"
        text = font.render(mode_text, True, NEON_CYAN)
        surface.blit(text, (10, 10))
        
        status_text = f"Objects: {len(self.stars)} stars, {len(self.planets)} planets"
        text = font.render(status_text, True, NEON_GREEN)
        surface.blit(text, (10, 30))
        
        time_text = f"Time Scale: {self.time_scale:.1f}x"
        text = font.render(time_text, True, NEON_YELLOW)
        surface.blit(text, (10, 50))
        
        # Gravitational waves
        if self.gravitational_waves:
            wave_text = f"Gravitational Waves: {len(self.gravitational_waves)}"
            text = font.render(wave_text, True, NEON_PURPLE)
            surface.blit(text, (10, 70))
    
    def draw_parameters(self, surface):
        """Draw physics parameters panel"""
        if not self.show_parameters:
            return
        
        panel_rect = pygame.Rect(WIDTH - 200, 10, 190, 200)
        pygame.draw.rect(surface, (0, 0, 0, 180), panel_rect)
        pygame.draw.rect(surface, NEON_CYAN, panel_rect, 2)
        
        font = pygame.font.Font(None, 12)
        
        # Selected object info
        if self.selected_object:
            if isinstance(self.selected_object, Star):
                star = self.selected_object
                lines = [
                    f"STAR ANALYSIS",
                    f"Type: {star.stellar_type.name}",
                    f"Mass: {star.stellar_params.mass:.1f} M☉",
                    f"Radius: {star.stellar_params.radius:.1f} R☉",
                    f"Temp: {star.stellar_params.temperature:.0f} K",
                    f"Age: {star.stellar_params.age:.0f} Myr",
                    f"Luminosity: {star.stellar_params.luminosity:.2f} L☉"
                ]
            elif isinstance(self.selected_object, Planet):
                planet = self.selected_object
                lines = [
                    f"PLANET ANALYSIS",
                    f"Type: {planet.planet_type.name}",
                    f"Mass: {planet.mass:.1f} M⊕",
                    f"Radius: {planet.radius:.1f} R⊕",
                    f"Temp: {planet.surface_temperature:.0f} K",
                    f"Atmosphere: {planet.atmosphere_thickness:.1f}",
                    f"Life: {'Yes' if planet.has_life else 'No'}"
                ]
            else:
                lines = ["No object selected"]
        else:
            lines = ["Click to select object"]
        
        y_offset = 20
        for line in lines:
            color = NEON_YELLOW if line.endswith("ANALYSIS") else NEON_CYAN
            text = font.render(line, True, color)
            surface.blit(text, (WIDTH - 195, y_offset))
            y_offset += 15
    
    def draw_controls(self, surface):
        """Draw control instructions"""
        controls_rect = pygame.Rect(10, HEIGHT - 100, 460, 90)
        pygame.draw.rect(surface, (0, 0, 0, 180), controls_rect)
        
        font = pygame.font.Font(None, 12)
        controls = [
            "TAB - Switch Modes  |  SPACE - Pause/Resume  |  +/- - Time Scale",
            "1-8 - Select Mode  |  O - Toggle Orbits  |  G - Toggle Grav Waves",
            "S - Stellar Evolution  |  P - Parameters  |  R - Reset Simulation",
            "Click - Select Object  |  F8 - Fullscreen  |  ESC - Launcher"
        ]
        
        for i, control in enumerate(controls):
            text = font.render(control, True, NEON_YELLOW)
            surface.blit(text, (15, HEIGHT - 95 + i * 15))
    
    def handle_input(self, keys, events):
        """Handle user input"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    # Cycle through modes
                    modes = list(SimulationMode)
                    current_index = modes.index(self.simulation_mode)
                    self.simulation_mode = modes[(current_index + 1) % len(modes)]
                    self.initialize_simulation()
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.time_scale = min(10.0, self.time_scale * 1.5)
                elif event.key == pygame.K_MINUS:
                    self.time_scale = max(0.1, self.time_scale / 1.5)
                elif event.key == pygame.K_o:
                    self.show_orbits = not self.show_orbits
                elif event.key == pygame.K_g:
                    self.show_gravitational_waves = not self.show_gravitational_waves
                elif event.key == pygame.K_s:
                    self.show_stellar_evolution = not self.show_stellar_evolution
                elif event.key == pygame.K_p:
                    self.show_parameters = not self.show_parameters
                elif event.key == pygame.K_h:
                    self.show_hud = not self.show_hud
                elif event.key == pygame.K_r:
                    self.initialize_simulation()
                
                # Mode selection
                elif event.key == pygame.K_1:
                    self.simulation_mode = SimulationMode.SOLAR_SYSTEM
                    self.initialize_simulation()
                elif event.key == pygame.K_2:
                    self.simulation_mode = SimulationMode.STELLAR_EVOLUTION
                    self.initialize_simulation()
                elif event.key == pygame.K_3:
                    self.simulation_mode = SimulationMode.GALAXY_FORMATION
                    self.initialize_simulation()
                elif event.key == pygame.K_4:
                    self.simulation_mode = SimulationMode.COSMIC_PHENOMENA
                    self.initialize_simulation()
                elif event.key == pygame.K_5:
                    self.simulation_mode = SimulationMode.GRAVITATIONAL_WAVES
                    self.initialize_simulation()
                elif event.key == pygame.K_6:
                    self.simulation_mode = SimulationMode.DARK_MATTER
                    self.initialize_simulation()
                elif event.key == pygame.K_7:
                    self.simulation_mode = SimulationMode.EXOPLANET_HUNT
                    self.initialize_simulation()
                elif event.key == pygame.K_8:
                    self.simulation_mode = SimulationMode.SUPERNOVA_SIMULATION
                    self.initialize_simulation()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Object selection
                mouse_x, mouse_y = event.pos
                self.selected_object = None
                
                # Check stars
                for star in self.stars:
                    distance = math.sqrt((star.x - mouse_x)**2 + (star.y - mouse_y)**2)
                    if distance < star.radius * 2:
                        self.selected_object = star
                        break
                
                # Check planets
                for planet in self.planets:
                    distance = math.sqrt((planet.x - mouse_x)**2 + (planet.y - mouse_y)**2)
                    if distance < planet.radius * 3:
                        self.selected_object = planet
                        break
    
    def draw(self, surface):
        """Draw the complete astrophysics simulation"""
        # Clear screen with space background
        surface.fill(CYBER_BLACK)
        
        # Draw background stars
        for i in range(100):
            x = (i * 47) % WIDTH
            y = (i * 73) % HEIGHT
            brightness = 0.3 + 0.4 * math.sin(time.time() * 0.5 + i * 0.1)
            color = (int(100 * brightness), int(100 * brightness), int(150 * brightness))
            pygame.draw.circle(surface, color, (x, y), 1)
        
        # Draw orbital paths
        self.draw_orbits(surface)
        
        # Draw gravitational waves
        if self.show_gravitational_waves:
            self.draw_gravitational_waves(surface)
        
        # Draw celestial bodies
        for star in self.stars:
            self.draw_star(surface, star)
        
        for planet in self.planets:
            self.draw_planet(surface, planet)
        
        # Draw UI elements
        self.draw_hud(surface)
        self.draw_parameters(surface)
        self.draw_controls(surface)

def toggle_fullscreen():
    """Toggle fullscreen mode using F8"""
    global screen, fullscreen
    
    if fullscreen:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        fullscreen = False
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        fullscreen = True

def return_to_launcher():
    """Return to the main launcher"""
    try:
        subprocess.run([sys.executable, "run_art.py"], check=True)
    except subprocess.CalledProcessError:
        print("Could not launch main menu")
    pygame.quit()
    sys.exit()

def main():
    """Main astrophysics simulation loop"""
    global screen
    
    # Initialize astrophysics simulator
    simulator = AstrophysicsSimulator()
    
    # Main loop
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds
        
        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F8:
                    toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    return_to_launcher()
        
        # Handle input
        keys = pygame.key.get_pressed()
        simulator.handle_input(keys, events)
        
        # Update simulation
        simulator.update_simulation(dt)
        
        # Draw everything
        simulator.draw(screen)
        
        # Update display
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 