#!/usr/bin/env python3
"""
Advanced Quantum Physics Simulator - Interactive quantum mechanics visualization
Perfect for Raspberry Pi 5 with 3.5" display (480x320)
COMPLETE QUANTUM PHYSICS SIMULATION WITH WAVE-PARTICLE DUALITY
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
from typing import List, Dict, Optional, Tuple, Complex

# Initialize Pygame
pygame.init()

# Screen dimensions optimized for Pi 5
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Quantum Physics Simulator")

# Fullscreen support
fullscreen = False
clock = pygame.time.Clock()
start_time = time.time()

# Enhanced quantum color palette
CYBER_BLACK = (10, 10, 15)
NEON_BLUE = (50, 150, 255)
NEON_GREEN = (50, 255, 150)
NEON_CYAN = (50, 255, 255)
NEON_YELLOW = (255, 255, 50)
NEON_RED = (255, 50, 50)
NEON_PURPLE = (150, 50, 255)
NEON_ORANGE = (255, 150, 50)
QUANTUM_COLORS = {
    'probability': (100, 200, 255),
    'wave': (255, 100, 255),
    'particle': (255, 255, 100),
    'entangled': (255, 100, 100),
    'tunnel': (100, 255, 100),
    'interference': (200, 100, 255),
    'field': (100, 255, 255),
    'uncertainty': (255, 150, 150),
    'superposition': (150, 255, 150),
    'collapse': (255, 255, 255)
}

class QuantumState(Enum):
    WAVE = 0
    PARTICLE = 1
    SUPERPOSITION = 2
    ENTANGLED = 3

class ExperimentType(Enum):
    DOUBLE_SLIT = 0
    QUANTUM_TUNNELING = 1
    INTERFERENCE = 2
    ENTANGLEMENT = 3
    UNCERTAINTY = 4
    FIELD_INTERACTION = 5

@dataclass
class QuantumParticle:
    """Individual quantum particle with wave-particle properties"""
    x: float
    y: float
    velocity_x: float
    velocity_y: float
    wave_function: complex
    probability_amplitude: float
    spin: float
    entangled_with: Optional['QuantumParticle']
    state: QuantumState
    phase: float
    energy: float
    mass: float
    charge: float
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.velocity_x = random.uniform(-2, 2)
        self.velocity_y = random.uniform(-2, 2)
        self.wave_function = complex(random.uniform(0, 1), random.uniform(0, 1))
        self.probability_amplitude = abs(self.wave_function)**2
        self.spin = random.choice([0.5, -0.5])
        self.entangled_with = None
        self.state = QuantumState.SUPERPOSITION
        self.phase = random.uniform(0, 2 * math.pi)
        self.energy = random.uniform(1, 5)
        self.mass = 1.0
        self.charge = random.choice([-1, 0, 1])
    
    def update_wave_function(self, dt: float, potential: float = 0):
        """Update quantum wave function using Schrödinger equation"""
        # Simplified time evolution of wave function
        kinetic_energy = (self.velocity_x**2 + self.velocity_y**2) * self.mass / 2
        total_energy = kinetic_energy + potential
        
        # Phase evolution
        self.phase += total_energy * dt * 6.626e-34 / 1.055e-34  # ħ factor simplified
        
        # Update wave function
        amplitude = abs(self.wave_function)
        self.wave_function = amplitude * complex(math.cos(self.phase), math.sin(self.phase))
        
        # Update probability amplitude
        self.probability_amplitude = abs(self.wave_function)**2
    
    def apply_uncertainty_principle(self):
        """Apply Heisenberg uncertainty principle"""
        # More precise position means less precise momentum
        position_uncertainty = 0.5
        momentum_uncertainty = 1.0 / position_uncertainty
        
        # Add quantum noise
        self.x += random.gauss(0, position_uncertainty)
        self.y += random.gauss(0, position_uncertainty)
        self.velocity_x += random.gauss(0, momentum_uncertainty * 0.1)
        self.velocity_y += random.gauss(0, momentum_uncertainty * 0.1)
    
    def collapse_wave_function(self):
        """Collapse wave function upon measurement"""
        if self.state == QuantumState.SUPERPOSITION:
            # Random collapse to particle or wave state
            if random.random() < self.probability_amplitude:
                self.state = QuantumState.PARTICLE
            else:
                self.state = QuantumState.WAVE
        
        # Entangled particles collapse together
        if self.entangled_with and self.entangled_with.state == QuantumState.SUPERPOSITION:
            if self.spin > 0:
                self.entangled_with.spin = -0.5
            else:
                self.entangled_with.spin = 0.5
            self.entangled_with.state = self.state
    
    def quantum_tunnel(self, barrier_height: float, barrier_width: float) -> bool:
        """Calculate probability of quantum tunneling"""
        if self.energy < barrier_height:
            # Tunneling probability (simplified)
            transmission_coeff = math.exp(-2 * math.sqrt(2 * self.mass * (barrier_height - self.energy)) * barrier_width)
            return random.random() < transmission_coeff
        return True
    
    def interfere_with(self, other: 'QuantumParticle') -> float:
        """Calculate quantum interference between particles"""
        phase_difference = abs(self.phase - other.phase)
        # Constructive interference at phase difference 0, 2π, 4π...
        # Destructive interference at phase difference π, 3π, 5π...
        interference = math.cos(phase_difference)
        return interference
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get particle color based on quantum state"""
        if self.state == QuantumState.WAVE:
            base_color = QUANTUM_COLORS['wave']
        elif self.state == QuantumState.PARTICLE:
            base_color = QUANTUM_COLORS['particle']
        elif self.state == QuantumState.SUPERPOSITION:
            base_color = QUANTUM_COLORS['superposition']
        else:  # ENTANGLED
            base_color = QUANTUM_COLORS['entangled']
        
        # Modulate by probability amplitude
        intensity = min(1.0, self.probability_amplitude * 2)
        return tuple(int(c * intensity) for c in base_color)

@dataclass
class QuantumField:
    """Quantum field affecting particle behavior"""
    x: int
    y: int
    field_type: str  # 'potential', 'magnetic', 'electric'
    strength: float
    size: int
    
    def get_potential(self, px: float, py: float) -> float:
        """Get field potential at position"""
        distance = math.sqrt((px - self.x)**2 + (py - self.y)**2)
        if distance < self.size:
            if self.field_type == 'potential':
                return self.strength * (1 - distance / self.size)
            elif self.field_type == 'electric':
                return self.strength / max(1, distance)
            elif self.field_type == 'magnetic':
                return self.strength * math.sin(distance * 0.1)
        return 0
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get field visualization color"""
        if self.field_type == 'potential':
            return QUANTUM_COLORS['field']
        elif self.field_type == 'electric':
            return NEON_BLUE
        elif self.field_type == 'magnetic':
            return NEON_RED
        return NEON_GREEN

class QuantumBarrier:
    """Potential barrier for tunneling experiments"""
    def __init__(self, x: int, y: int, width: int, height: int, barrier_height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.barrier_height = barrier_height
    
    def is_inside(self, px: float, py: float) -> bool:
        """Check if particle is inside barrier"""
        return (self.x <= px <= self.x + self.width and 
                self.y <= py <= self.y + self.height)
    
    def draw(self, surface):
        """Draw barrier visualization"""
        alpha = int(100 + 50 * math.sin(time.time() * 2))
        barrier_color = (*NEON_RED, alpha)
        pygame.draw.rect(surface, barrier_color[:3], 
                        (self.x, self.y, self.width, self.height))
        
        # Draw barrier outline
        pygame.draw.rect(surface, NEON_RED, 
                        (self.x, self.y, self.width, self.height), 2)

class DoubleSlit:
    """Double-slit experiment setup"""
    def __init__(self, x: int, slit_separation: int, slit_width: int):
        self.x = x
        self.slit_separation = slit_separation
        self.slit_width = slit_width
        self.slit1_y = HEIGHT // 2 - slit_separation // 2
        self.slit2_y = HEIGHT // 2 + slit_separation // 2
        self.detection_screen = []  # Store detection events
    
    def can_pass_through(self, py: float) -> bool:
        """Check if particle can pass through slits"""
        # Check if particle is at the barrier x-position
        slit1_range = (self.slit1_y, self.slit1_y + self.slit_width)
        slit2_range = (self.slit2_y, self.slit2_y + self.slit_width)
        
        return (slit1_range[0] <= py <= slit1_range[1] or 
                slit2_range[0] <= py <= slit2_range[1])
    
    def add_detection(self, y: float):
        """Add detection event to screen"""
        self.detection_screen.append(y)
        # Keep only recent detections
        if len(self.detection_screen) > 1000:
            self.detection_screen = self.detection_screen[-1000:]
    
    def draw(self, surface):
        """Draw double-slit apparatus"""
        # Draw barrier
        pygame.draw.line(surface, NEON_CYAN, (self.x, 0), (self.x, HEIGHT), 3)
        
        # Draw slits (gaps in the barrier)
        pygame.draw.line(surface, CYBER_BLACK, 
                        (self.x, self.slit1_y), (self.x, self.slit1_y + self.slit_width), 5)
        pygame.draw.line(surface, CYBER_BLACK, 
                        (self.x, self.slit2_y), (self.x, self.slit2_y + self.slit_width), 5)
        
        # Draw detection screen
        screen_x = self.x + 100
        pygame.draw.line(surface, NEON_GREEN, (screen_x, 0), (screen_x, HEIGHT), 2)
        
        # Draw interference pattern
        if len(self.detection_screen) > 10:
            histogram = {}
            for y in self.detection_screen:
                y_bin = int(y // 5) * 5
                histogram[y_bin] = histogram.get(y_bin, 0) + 1
            
            max_count = max(histogram.values()) if histogram else 1
            for y_bin, count in histogram.items():
                intensity = count / max_count
                bar_width = int(intensity * 20)
                color = tuple(int(c * intensity) for c in QUANTUM_COLORS['interference'])
                pygame.draw.line(surface, color, 
                               (screen_x + 5, y_bin), (screen_x + 5 + bar_width, y_bin), 2)

class QuantumPhysicsSimulator:
    """Main quantum physics simulation class"""
    def __init__(self):
        self.particles = []
        self.quantum_fields = []
        self.barriers = []
        self.double_slit = None
        self.experiment_type = ExperimentType.DOUBLE_SLIT
        self.measurement_active = False
        self.show_wave_function = True
        self.show_probability = True
        self.show_fields = True
        self.show_hud = True
        self.paused = False
        
        # Simulation parameters
        self.particle_count = 50
        self.time_step = 0.016  # 60 FPS
        self.quantum_effects = True
        self.decoherence_rate = 0.01
        
        # Camera and interaction
        self.selected_particle = None
        self.mouse_field = None
        
        self.experiment_names = {
            ExperimentType.DOUBLE_SLIT: "Double-Slit Experiment",
            ExperimentType.QUANTUM_TUNNELING: "Quantum Tunneling",
            ExperimentType.INTERFERENCE: "Wave Interference",
            ExperimentType.ENTANGLEMENT: "Quantum Entanglement",
            ExperimentType.UNCERTAINTY: "Uncertainty Principle",
            ExperimentType.FIELD_INTERACTION: "Field Interactions"
        }
        
        self.initialize_experiment()
    
    def initialize_experiment(self):
        """Initialize current experiment setup"""
        self.particles.clear()
        self.quantum_fields.clear()
        self.barriers.clear()
        self.double_slit = None
        
        if self.experiment_type == ExperimentType.DOUBLE_SLIT:
            self.setup_double_slit_experiment()
        elif self.experiment_type == ExperimentType.QUANTUM_TUNNELING:
            self.setup_tunneling_experiment()
        elif self.experiment_type == ExperimentType.INTERFERENCE:
            self.setup_interference_experiment()
        elif self.experiment_type == ExperimentType.ENTANGLEMENT:
            self.setup_entanglement_experiment()
        elif self.experiment_type == ExperimentType.UNCERTAINTY:
            self.setup_uncertainty_experiment()
        elif self.experiment_type == ExperimentType.FIELD_INTERACTION:
            self.setup_field_experiment()
    
    def setup_double_slit_experiment(self):
        """Setup double-slit experiment"""
        self.double_slit = DoubleSlit(WIDTH // 3, 40, 20)
        
        # Create particle source
        for _ in range(self.particle_count):
            particle = QuantumParticle(50, HEIGHT // 2 + random.randint(-20, 20))
            particle.velocity_x = 2
            particle.velocity_y = random.uniform(-0.5, 0.5)
            self.particles.append(particle)
    
    def setup_tunneling_experiment(self):
        """Setup quantum tunneling experiment"""
        # Create potential barrier
        barrier = QuantumBarrier(WIDTH // 2 - 25, HEIGHT // 2 - 50, 50, 100, 3.0)
        self.barriers.append(barrier)
        
        # Create particles with varying energies
        for _ in range(self.particle_count):
            particle = QuantumParticle(50, HEIGHT // 2 + random.randint(-50, 50))
            particle.velocity_x = 1.5
            particle.energy = random.uniform(1, 4)  # Some below barrier height
            self.particles.append(particle)
    
    def setup_interference_experiment(self):
        """Setup wave interference experiment"""
        # Create two particle sources
        for _ in range(self.particle_count // 2):
            particle1 = QuantumParticle(50, HEIGHT // 3)
            particle1.velocity_x = 1
            particle1.velocity_y = 0.5
            particle1.state = QuantumState.WAVE
            self.particles.append(particle1)
            
            particle2 = QuantumParticle(50, 2 * HEIGHT // 3)
            particle2.velocity_x = 1
            particle2.velocity_y = -0.5
            particle2.state = QuantumState.WAVE
            self.particles.append(particle2)
    
    def setup_entanglement_experiment(self):
        """Setup quantum entanglement experiment"""
        # Create entangled particle pairs
        for _ in range(self.particle_count // 2):
            particle1 = QuantumParticle(WIDTH // 4, HEIGHT // 2 + random.randint(-30, 30))
            particle2 = QuantumParticle(3 * WIDTH // 4, HEIGHT // 2 + random.randint(-30, 30))
            
            # Entangle particles
            particle1.entangled_with = particle2
            particle2.entangled_with = particle1
            particle1.state = QuantumState.ENTANGLED
            particle2.state = QuantumState.ENTANGLED
            
            # Opposite spins
            particle1.spin = 0.5
            particle2.spin = -0.5
            
            self.particles.extend([particle1, particle2])
    
    def setup_uncertainty_experiment(self):
        """Setup uncertainty principle demonstration"""
        # Create particles with precise position but uncertain momentum
        for _ in range(self.particle_count):
            particle = QuantumParticle(WIDTH // 2, HEIGHT // 2)
            particle.velocity_x = random.gauss(0, 2)
            particle.velocity_y = random.gauss(0, 2)
            self.particles.append(particle)
    
    def setup_field_experiment(self):
        """Setup quantum field interaction experiment"""
        # Create various quantum fields
        field1 = QuantumField(WIDTH // 4, HEIGHT // 3, 'electric', 2.0, 50)
        field2 = QuantumField(3 * WIDTH // 4, 2 * HEIGHT // 3, 'magnetic', -1.5, 40)
        field3 = QuantumField(WIDTH // 2, HEIGHT // 2, 'potential', 3.0, 60)
        
        self.quantum_fields.extend([field1, field2, field3])
        
        # Create particles
        for _ in range(self.particle_count):
            particle = QuantumParticle(random.randint(50, WIDTH - 50), 
                                     random.randint(50, HEIGHT - 50))
            self.particles.append(particle)
    
    def update_simulation(self):
        """Update quantum simulation"""
        if self.paused:
            return
        
        for particle in self.particles[:]:  # Copy list to avoid modification issues
            # Update position
            particle.x += particle.velocity_x * self.time_step
            particle.y += particle.velocity_y * self.time_step
            
            # Calculate potential at particle position
            total_potential = 0
            for field in self.quantum_fields:
                total_potential += field.get_potential(particle.x, particle.y)
            
            # Update wave function
            particle.update_wave_function(self.time_step, total_potential)
            
            # Apply quantum effects
            if self.quantum_effects:
                particle.apply_uncertainty_principle()
                
                # Decoherence
                if random.random() < self.decoherence_rate:
                    particle.collapse_wave_function()
            
            # Handle experiment-specific behavior
            self.handle_experiment_physics(particle)
            
            # Remove particles that have left the screen
            if particle.x > WIDTH + 50 or particle.x < -50 or particle.y > HEIGHT + 50 or particle.y < -50:
                self.particles.remove(particle)
        
        # Add new particles periodically
        if len(self.particles) < self.particle_count and random.random() < 0.1:
            self.add_new_particle()
    
    def handle_experiment_physics(self, particle: QuantumParticle):
        """Handle experiment-specific physics"""
        if self.experiment_type == ExperimentType.DOUBLE_SLIT and self.double_slit:
            if abs(particle.x - self.double_slit.x) < 5:
                if not self.double_slit.can_pass_through(particle.y):
                    # Particle blocked by barrier
                    self.particles.remove(particle)
                else:
                    # Particle passes through, add quantum interference
                    if particle.state == QuantumState.SUPERPOSITION:
                        particle.wave_function *= complex(math.cos(particle.phase), 
                                                         math.sin(particle.phase))
            
            # Detection at screen
            elif particle.x > self.double_slit.x + 95:
                self.double_slit.add_detection(particle.y)
                self.particles.remove(particle)
        
        elif self.experiment_type == ExperimentType.QUANTUM_TUNNELING:
            for barrier in self.barriers:
                if barrier.is_inside(particle.x, particle.y):
                    if not particle.quantum_tunnel(barrier.barrier_height, barrier.width):
                        # Particle reflected
                        particle.velocity_x *= -1
                        particle.x = barrier.x - 5  # Move outside barrier
        
        elif self.experiment_type == ExperimentType.INTERFERENCE:
            # Calculate interference between nearby particles
            for other in self.particles:
                if other != particle and other.state == QuantumState.WAVE:
                    distance = math.sqrt((particle.x - other.x)**2 + (particle.y - other.y)**2)
                    if distance < 30:
                        interference = particle.interfere_with(other)
                        particle.probability_amplitude *= (1 + interference * 0.1)
        
        elif self.experiment_type == ExperimentType.ENTANGLEMENT:
            # Measurement on one particle affects entangled partner
            if self.measurement_active and particle.entangled_with:
                if random.random() < 0.01:  # Occasional measurement
                    particle.collapse_wave_function()
    
    def add_new_particle(self):
        """Add new particle based on current experiment"""
        if self.experiment_type == ExperimentType.DOUBLE_SLIT:
            particle = QuantumParticle(50, HEIGHT // 2 + random.randint(-20, 20))
            particle.velocity_x = 2
            particle.velocity_y = random.uniform(-0.5, 0.5)
        elif self.experiment_type == ExperimentType.QUANTUM_TUNNELING:
            particle = QuantumParticle(50, HEIGHT // 2 + random.randint(-50, 50))
            particle.velocity_x = 1.5
            particle.energy = random.uniform(1, 4)
        else:
            particle = QuantumParticle(50, random.randint(50, HEIGHT - 50))
        
        self.particles.append(particle)
    
    def draw_wave_function(self, surface):
        """Draw quantum wave function visualization"""
        if not self.show_wave_function:
            return
        
        # Create wave function grid
        grid_size = 8
        for x in range(0, WIDTH, grid_size):
            for y in range(0, HEIGHT, grid_size):
                total_amplitude = 0
                total_phase = 0
                
                # Sum contributions from nearby particles
                for particle in self.particles:
                    distance = math.sqrt((x - particle.x)**2 + (y - particle.y)**2)
                    if distance < 50:
                        amplitude = particle.probability_amplitude * math.exp(-distance * 0.05)
                        total_amplitude += amplitude
                        total_phase += particle.phase * amplitude
                
                if total_amplitude > 0.01:
                    # Visualize wave function
                    intensity = min(255, int(total_amplitude * 255))
                    phase_color = (
                        int(intensity * abs(math.sin(total_phase))),
                        int(intensity * abs(math.sin(total_phase + 2.1))),
                        int(intensity * abs(math.sin(total_phase + 4.2)))
                    )
                    pygame.draw.rect(surface, phase_color, (x, y, grid_size, grid_size))
    
    def draw_probability_clouds(self, surface):
        """Draw probability cloud around particles"""
        if not self.show_probability:
            return
        
        for particle in self.particles:
            if particle.state == QuantumState.SUPERPOSITION:
                # Draw probability cloud
                cloud_size = int(20 * particle.probability_amplitude)
                for i in range(cloud_size):
                    angle = random.uniform(0, 2 * math.pi)
                    radius = random.uniform(0, cloud_size)
                    cloud_x = int(particle.x + math.cos(angle) * radius)
                    cloud_y = int(particle.y + math.sin(angle) * radius)
                    
                    if 0 <= cloud_x < WIDTH and 0 <= cloud_y < HEIGHT:
                        alpha = int(100 * (1 - radius / cloud_size))
                        color = (*QUANTUM_COLORS['probability'], alpha)
                        pygame.draw.circle(surface, color[:3], (cloud_x, cloud_y), 1)
    
    def draw_particles(self, surface):
        """Draw quantum particles"""
        for particle in self.particles:
            # Particle position
            x, y = int(particle.x), int(particle.y)
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                color = particle.get_color()
                
                # Different visualization based on state
                if particle.state == QuantumState.WAVE:
                    # Draw as wave pattern
                    for i in range(-10, 11, 2):
                        wave_x = x + i
                        wave_y = y + int(5 * math.sin(particle.phase + i * 0.5))
                        if 0 <= wave_x < WIDTH and 0 <= wave_y < HEIGHT:
                            pygame.draw.circle(surface, color, (wave_x, wave_y), 2)
                elif particle.state == QuantumState.PARTICLE:
                    # Draw as solid particle
                    pygame.draw.circle(surface, color, (x, y), 4)
                elif particle.state == QuantumState.SUPERPOSITION:
                    # Draw as fuzzy probability
                    for offset in range(-3, 4):
                        alpha = 255 - abs(offset) * 50
                        fuzz_color = tuple(min(255, max(0, c)) for c in color)
                        pygame.draw.circle(surface, fuzz_color, (x + offset, y), 2)
                else:  # ENTANGLED
                    # Draw with entanglement connection
                    pygame.draw.circle(surface, color, (x, y), 5)
                    if particle.entangled_with:
                        ex, ey = int(particle.entangled_with.x), int(particle.entangled_with.y)
                        if 0 <= ex < WIDTH and 0 <= ey < HEIGHT:
                            pygame.draw.line(surface, QUANTUM_COLORS['entangled'], (x, y), (ex, ey), 1)
                
                # Draw selection indicator
                if particle == self.selected_particle:
                    pygame.draw.circle(surface, NEON_YELLOW, (x, y), 8, 2)
    
    def draw_quantum_fields(self, surface):
        """Draw quantum fields"""
        if not self.show_fields:
            return
        
        for field in self.quantum_fields:
            # Draw field influence area
            field_color = field.get_color()
            pygame.draw.circle(surface, field_color, (field.x, field.y), field.size, 2)
            
            # Draw field center
            pygame.draw.circle(surface, field_color, (field.x, field.y), 5)
            
            # Draw field lines
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                end_x = field.x + math.cos(rad) * field.size
                end_y = field.y + math.sin(rad) * field.size
                pygame.draw.line(surface, field_color, 
                               (field.x, field.y), (int(end_x), int(end_y)), 1)
    
    def draw_experiment_specific(self, surface):
        """Draw experiment-specific elements"""
        if self.experiment_type == ExperimentType.DOUBLE_SLIT and self.double_slit:
            self.double_slit.draw(surface)
        elif self.experiment_type == ExperimentType.QUANTUM_TUNNELING:
            for barrier in self.barriers:
                barrier.draw(surface)
    
    def draw_hud(self, surface):
        """Draw heads-up display"""
        if not self.show_hud:
            return
        
        # HUD background
        hud_rect = pygame.Rect(0, 0, WIDTH, 60)
        pygame.draw.rect(surface, (0, 0, 0, 180), hud_rect)
        
        # Current experiment
        font = pygame.font.Font(None, 24)
        exp_text = f"Experiment: {self.experiment_names[self.experiment_type]}"
        text = font.render(exp_text, True, NEON_CYAN)
        surface.blit(text, (10, 10))
        
        # Particle count
        font = pygame.font.Font(None, 18)
        count_text = f"Particles: {len(self.particles)}"
        text = font.render(count_text, True, NEON_GREEN)
        surface.blit(text, (10, 35))
        
        # Quantum effects status
        effects_text = f"Quantum Effects: {'ON' if self.quantum_effects else 'OFF'}"
        text = font.render(effects_text, True, NEON_YELLOW if self.quantum_effects else NEON_RED)
        surface.blit(text, (150, 35))
        
        # Measurement status
        if self.measurement_active:
            measure_text = "MEASURING - Wave Function Collapse!"
            text = font.render(measure_text, True, NEON_RED)
            surface.blit(text, (300, 35))
        
        # Selected particle info
        if self.selected_particle:
            particle = self.selected_particle
            info_rect = pygame.Rect(WIDTH - 150, 70, 140, 120)
            pygame.draw.rect(surface, (0, 0, 0, 200), info_rect)
            pygame.draw.rect(surface, NEON_CYAN, info_rect, 2)
            
            font = pygame.font.Font(None, 16)
            info_lines = [
                f"State: {particle.state.name}",
                f"Energy: {particle.energy:.2f}",
                f"Spin: {particle.spin}",
                f"Phase: {particle.phase:.2f}",
                f"Prob: {particle.probability_amplitude:.3f}",
                f"Pos: ({particle.x:.1f}, {particle.y:.1f})"
            ]
            
            for i, line in enumerate(info_lines):
                text = font.render(line, True, NEON_GREEN)
                surface.blit(text, (WIDTH - 145, 80 + i * 15))
    
    def draw_controls(self, surface):
        """Draw control instructions"""
        controls_rect = pygame.Rect(10, HEIGHT - 100, 300, 90)
        pygame.draw.rect(surface, (0, 0, 0, 180), controls_rect)
        
        font = pygame.font.Font(None, 14)
        controls = [
            "SPACE - Pause/Resume",
            "E - Change Experiment",
            "M - Toggle Measurement",
            "W/P/F - Toggle Wave/Probability/Fields",
            "Q - Toggle Quantum Effects",
            "Click - Select Particle",
            "F8 - Fullscreen",
            "ESC - Return to Launcher"
        ]
        
        for i, control in enumerate(controls):
            text = font.render(control, True, NEON_YELLOW)
            surface.blit(text, (15, HEIGHT - 95 + i * 10))
    
    def handle_input(self, keys, events):
        """Handle user input"""
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_e:
                    self.cycle_experiment()
                elif event.key == pygame.K_m:
                    self.measurement_active = not self.measurement_active
                elif event.key == pygame.K_w:
                    self.show_wave_function = not self.show_wave_function
                elif event.key == pygame.K_p:
                    self.show_probability = not self.show_probability
                elif event.key == pygame.K_f:
                    self.show_fields = not self.show_fields
                elif event.key == pygame.K_q:
                    self.quantum_effects = not self.quantum_effects
                elif event.key == pygame.K_h:
                    self.show_hud = not self.show_hud
                elif event.key == pygame.K_r:
                    self.initialize_experiment()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_mouse_click(event.pos)
    
    def cycle_experiment(self):
        """Cycle to next experiment"""
        experiments = list(ExperimentType)
        current_index = experiments.index(self.experiment_type)
        self.experiment_type = experiments[(current_index + 1) % len(experiments)]
        self.initialize_experiment()
    
    def handle_mouse_click(self, pos):
        """Handle mouse click for particle selection"""
        mouse_x, mouse_y = pos
        closest_particle = None
        min_distance = float('inf')
        
        for particle in self.particles:
            distance = math.sqrt((particle.x - mouse_x)**2 + (particle.y - mouse_y)**2)
            if distance < min_distance and distance < 20:
                min_distance = distance
                closest_particle = particle
        
        self.selected_particle = closest_particle

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
    """Main simulation loop"""
    global screen
    
    # Initialize simulator
    simulator = QuantumPhysicsSimulator()
    
    # Main loop
    running = True
    while running:
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
        simulator.update_simulation()
        
        # Clear screen
        screen.fill(CYBER_BLACK)
        
        # Draw quantum wave function
        simulator.draw_wave_function(screen)
        
        # Draw probability clouds
        simulator.draw_probability_clouds(screen)
        
        # Draw quantum fields
        simulator.draw_quantum_fields(screen)
        
        # Draw experiment-specific elements
        simulator.draw_experiment_specific(screen)
        
        # Draw particles
        simulator.draw_particles(screen)
        
        # Draw UI
        simulator.draw_hud(screen)
        simulator.draw_controls(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS for smooth quantum simulation
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 