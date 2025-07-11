#!/usr/bin/env python3
"""
Advanced Ecosystem Life Simulator - Multi-species cellular life simulation
Perfect for Raspberry Pi 5 with 3.5" display
ADVANCED LIFE SIMULATION VERSION
"""

import pygame
import numpy as np
import random
import time
import math
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Ecosystem Simulator")

# Fullscreen support
fullscreen = False

clock = pygame.time.Clock()
start_time = time.time()

# Grid settings
CELL_SIZE = 3
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Enhanced colors
CYBER_BLACK = (10, 10, 15)
NEON_BLUE = (50, 150, 255)
NEON_GREEN = (50, 255, 150)
NEON_CYAN = (50, 255, 255)
NEON_YELLOW = (255, 255, 50)
NEON_RED = (255, 50, 50)
NEON_PURPLE = (150, 50, 255)
NEON_ORANGE = (255, 150, 50)
LIFE_GREEN = (100, 255, 100)
PREDATOR_RED = (255, 100, 100)
PLANT_GREEN = (50, 200, 50)
WATER_BLUE = (100, 150, 255)

# Species types
EMPTY = 0
PLANT = 1
HERBIVORE = 2
CARNIVORE = 3
OMNIVORE = 4
DECOMPOSER = 5
WATER = 6
NUTRIENT = 7

class Species:
    def __init__(self, species_type, x, y):
        self.type = species_type
        self.x = x
        self.y = y
        self.age = 0
        self.energy = 100
        self.health = 100
        self.reproductive_energy = 0
        self.mutation_rate = 0.01
        
        # Genetic traits (0.0 to 1.0)
        self.speed = random.uniform(0.3, 1.0)
        self.efficiency = random.uniform(0.3, 1.0)
        self.resilience = random.uniform(0.3, 1.0)
        self.fertility = random.uniform(0.3, 1.0)
        self.aggression = random.uniform(0.0, 1.0)
        self.intelligence = random.uniform(0.0, 1.0)
        
        # Species-specific initialization
        self.initialize_species_traits()
    
    def initialize_species_traits(self):
        """Initialize species-specific traits"""
        if self.type == PLANT:
            self.energy = 50
            self.max_energy = 150
            self.reproduction_threshold = 80
            self.lifespan = 200
        elif self.type == HERBIVORE:
            self.energy = 80
            self.max_energy = 120
            self.reproduction_threshold = 100
            self.lifespan = 150
        elif self.type == CARNIVORE:
            self.energy = 100
            self.max_energy = 200
            self.reproduction_threshold = 150
            self.lifespan = 120
        elif self.type == OMNIVORE:
            self.energy = 90
            self.max_energy = 180
            self.reproduction_threshold = 130
            self.lifespan = 140
        elif self.type == DECOMPOSER:
            self.energy = 60
            self.max_energy = 100
            self.reproduction_threshold = 70
            self.lifespan = 100
    
    def mutate(self):
        """Apply genetic mutations"""
        if random.random() < self.mutation_rate:
            trait = random.choice(['speed', 'efficiency', 'resilience', 'fertility', 'aggression', 'intelligence'])
            change = random.uniform(-0.1, 0.1)
            current_value = getattr(self, trait)
            new_value = max(0.0, min(1.0, current_value + change))
            setattr(self, trait, new_value)
    
    def age_one_turn(self):
        """Age the organism and apply aging effects"""
        self.age += 1
        
        # Energy decay based on age and species
        decay_rate = 1 + (self.age / self.lifespan) * 2
        self.energy -= decay_rate
        
        # Health degradation
        if self.age > self.lifespan * 0.8:
            self.health -= random.uniform(0.5, 2.0)
        
        return self.energy > 0 and self.health > 0
    
    def can_reproduce(self):
        """Check if organism can reproduce"""
        return (self.energy > self.reproduction_threshold and 
                self.age > 10 and 
                self.reproductive_energy > 50)
    
    def reproduce(self, partner=None):
        """Create offspring with genetic inheritance"""
        if not self.can_reproduce():
            return None
        
        # Energy cost for reproduction
        self.energy -= 30
        self.reproductive_energy = 0
        
        child = Species(self.type, self.x, self.y)
        
        # Genetic inheritance
        if partner:
            # Sexual reproduction - blend traits
            child.speed = (self.speed + partner.speed) / 2
            child.efficiency = (self.efficiency + partner.efficiency) / 2
            child.resilience = (self.resilience + partner.resilience) / 2
            child.fertility = (self.fertility + partner.fertility) / 2
            child.aggression = (self.aggression + partner.aggression) / 2
            child.intelligence = (self.intelligence + partner.intelligence) / 2
        else:
            # Asexual reproduction - copy traits
            child.speed = self.speed
            child.efficiency = self.efficiency
            child.resilience = self.resilience
            child.fertility = self.fertility
            child.aggression = self.aggression
            child.intelligence = self.intelligence
        
        # Apply mutations
        child.mutate()
        
        return child

class Environment:
    def __init__(self):
        self.temperature = 20.0  # Celsius
        self.humidity = 0.5
        self.oxygen_level = 1.0
        self.co2_level = 0.04
        self.toxicity = 0.0
        self.radiation = 0.0
        
        # Climate events
        self.drought = False
        self.flood = False
        self.ice_age = False
        self.volcanic_activity = False
        
        # Seasonal cycle
        self.season = 0  # 0: Spring, 1: Summer, 2: Autumn, 3: Winter
        self.day_cycle = 0.0  # 0.0 to 1.0
        
    def update(self, time_val):
        """Update environmental conditions"""
        # Seasonal changes
        season_progress = (time_val * 0.1) % 4
        self.season = int(season_progress)
        
        # Temperature variation
        base_temp = 20 + math.sin(season_progress * math.pi / 2) * 15
        daily_variation = math.sin(self.day_cycle * 2 * math.pi) * 5
        self.temperature = base_temp + daily_variation
        
        # Day/night cycle
        self.day_cycle = (time_val * 0.5) % 1.0
        
        # Random climate events
        if random.random() < 0.001:  # 0.1% chance per update
            self.trigger_climate_event()
        
        # Clear events randomly
        if random.random() < 0.01:
            self.clear_climate_events()
        
        # Environmental effects on atmosphere
        if self.drought:
            self.humidity = max(0.1, self.humidity - 0.01)
        elif self.flood:
            self.humidity = min(1.0, self.humidity + 0.01)
        
        if self.volcanic_activity:
            self.toxicity = min(1.0, self.toxicity + 0.005)
            self.co2_level = min(0.1, self.co2_level + 0.001)
        else:
            self.toxicity = max(0.0, self.toxicity - 0.002)
            self.co2_level = max(0.03, self.co2_level - 0.0001)
    
    def trigger_climate_event(self):
        """Trigger a random climate event"""
        event = random.choice(['drought', 'flood', 'ice_age', 'volcanic'])
        if event == 'drought':
            self.drought = True
        elif event == 'flood':
            self.flood = True
        elif event == 'ice_age':
            self.ice_age = True
        elif event == 'volcanic':
            self.volcanic_activity = True
    
    def clear_climate_events(self):
        """Clear all climate events"""
        self.drought = False
        self.flood = False
        self.ice_age = False
        self.volcanic_activity = False
    
    def get_survival_modifier(self, species_type):
        """Get survival modifier based on environmental conditions"""
        modifier = 1.0
        
        # Temperature effects
        if species_type == PLANT:
            if 15 <= self.temperature <= 30:
                modifier *= 1.2
            elif self.temperature < 5 or self.temperature > 40:
                modifier *= 0.5
        elif species_type in [HERBIVORE, OMNIVORE]:
            if 10 <= self.temperature <= 35:
                modifier *= 1.1
            elif self.temperature < 0 or self.temperature > 45:
                modifier *= 0.6
        elif species_type == CARNIVORE:
            if 0 <= self.temperature <= 40:
                modifier *= 1.0
            else:
                modifier *= 0.7
        
        # Climate event effects
        if self.drought and species_type == PLANT:
            modifier *= 0.3
        if self.flood and species_type in [HERBIVORE, CARNIVORE]:
            modifier *= 0.7
        if self.ice_age:
            modifier *= 0.8
        if self.volcanic_activity:
            modifier *= (1.0 - self.toxicity)
        
        return modifier

class AdvancedEcosystemSimulator:
    def __init__(self):
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=object)
        self.resource_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=float)
        self.water_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=float)
        
        self.running = False
        self.speed = 5  # Updates per second
        self.last_update = time.time()
        self.generation = 0
        self.total_time = 0.0
        
        # Environment
        self.environment = Environment()
        
        # Population statistics
        self.population_stats = {
            PLANT: 0,
            HERBIVORE: 0,
            CARNIVORE: 0,
            OMNIVORE: 0,
            DECOMPOSER: 0
        }
        
        # Visual settings
        self.view_mode = 0  # 0: Species, 1: Energy, 2: Age, 3: Resources, 4: Environment
        self.show_grid = False
        self.show_stats = True
        self.pixel_size = CELL_SIZE
        
        # Ecosystem settings
        self.carrying_capacity = 1000
        self.mutation_rate = 0.01
        self.reproduction_rate = 0.1
        self.predation_rate = 0.05
        
        # Advanced features
        self.genetic_diversity = True
        self.evolution_tracking = True
        self.climate_effects = True
        
        self.view_modes = {
            0: "SPECIES.VIEW",
            1: "ENERGY.LEVELS",
            2: "AGE.DISTRIBUTION",
            3: "RESOURCE.MAP",
            4: "ENVIRONMENT.DATA"
        }
        
        self.initialize_ecosystem()
    
    def initialize_ecosystem(self):
        """Initialize the ecosystem with balanced populations"""
        self.clear_ecosystem()
        
        # Add water sources
        for _ in range(15):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                        self.water_grid[ny][nx] = 1.0
        
        # Add initial plant population
        for _ in range(200):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if self.grid[y][x] is None:
                self.grid[y][x] = Species(PLANT, x, y)
                self.resource_grid[y][x] = 0.5
        
        # Add herbivores
        for _ in range(50):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if self.grid[y][x] is None:
                self.grid[y][x] = Species(HERBIVORE, x, y)
        
        # Add carnivores
        for _ in range(20):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if self.grid[y][x] is None:
                self.grid[y][x] = Species(CARNIVORE, x, y)
        
        # Add omnivores
        for _ in range(30):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if self.grid[y][x] is None:
                self.grid[y][x] = Species(OMNIVORE, x, y)
        
        # Add decomposers
        for _ in range(40):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if self.grid[y][x] is None:
                self.grid[y][x] = Species(DECOMPOSER, x, y)
        
        self.generation = 0
        self.update_population_stats()
    
    def clear_ecosystem(self):
        """Clear the entire ecosystem"""
        self.grid.fill(None)
        self.resource_grid.fill(0.0)
        self.water_grid.fill(0.0)
        self.generation = 0
        self.population_stats = {k: 0 for k in self.population_stats}
    
    def update_population_stats(self):
        """Update population statistics"""
        self.population_stats = {k: 0 for k in self.population_stats}
        
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                organism = self.grid[y][x]
                if organism is not None:
                    self.population_stats[organism.type] += 1
    
    def get_neighbors(self, x, y, radius=1):
        """Get neighboring organisms within radius"""
        neighbors = []
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                    if self.grid[ny][nx] is not None:
                        neighbors.append(self.grid[ny][nx])
        return neighbors
    
    def find_empty_nearby(self, x, y, radius=2):
        """Find empty spaces nearby"""
        empty_spots = []
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                    if self.grid[ny][nx] is None:
                        empty_spots.append((nx, ny))
        return empty_spots
    
    def process_organism(self, organism, x, y):
        """Process a single organism's behavior"""
        if organism is None:
            return
        
        # Age the organism
        if not organism.age_one_turn():
            self.grid[y][x] = None
            if organism.type != PLANT:
                # Add nutrients from decomposition
                self.resource_grid[y][x] = min(1.0, self.resource_grid[y][x] + 0.3)
            return
        
        # Apply environmental effects
        survival_modifier = self.environment.get_survival_modifier(organism.type)
        organism.energy *= survival_modifier
        
        # Species-specific behavior
        if organism.type == PLANT:
            self.process_plant(organism, x, y)
        elif organism.type == HERBIVORE:
            self.process_herbivore(organism, x, y)
        elif organism.type == CARNIVORE:
            self.process_carnivore(organism, x, y)
        elif organism.type == OMNIVORE:
            self.process_omnivore(organism, x, y)
        elif organism.type == DECOMPOSER:
            self.process_decomposer(organism, x, y)
        
        # Reproduction
        if organism.can_reproduce():
            self.attempt_reproduction(organism, x, y)
    
    def process_plant(self, plant, x, y):
        """Process plant behavior"""
        # Photosynthesis (more effective during day)
        light_efficiency = 0.5 + 0.5 * max(0, math.sin(self.environment.day_cycle * 2 * math.pi))
        co2_bonus = min(2.0, self.environment.co2_level * 20)
        water_access = self.water_grid[y][x]
        
        photosynthesis_rate = 2 * plant.efficiency * light_efficiency * co2_bonus * (0.5 + 0.5 * water_access)
        plant.energy += photosynthesis_rate
        
        # Absorb nutrients
        if self.resource_grid[y][x] > 0:
            absorbed = min(self.resource_grid[y][x], 5 * plant.efficiency)
            plant.energy += absorbed
            self.resource_grid[y][x] -= absorbed
        
        # Cap energy
        plant.energy = min(plant.energy, plant.max_energy)
        
        # Build reproductive energy
        if plant.energy > plant.reproduction_threshold * 0.8:
            plant.reproductive_energy += 2
    
    def process_herbivore(self, herbivore, x, y):
        """Process herbivore behavior"""
        # Look for plants to eat
        neighbors = self.get_neighbors(x, y)
        plants = [n for n in neighbors if n.type == PLANT]
        
        if plants and herbivore.energy < herbivore.max_energy * 0.8:
            target = random.choice(plants)
            # Energy transfer (with efficiency loss)
            energy_gained = min(target.energy * 0.6 * herbivore.efficiency, 20)
            herbivore.energy += energy_gained
            target.energy -= energy_gained / 0.6
        
        # Movement (costs energy)
        if random.random() < herbivore.speed:
            empty_spots = self.find_empty_nearby(x, y)
            if empty_spots:
                new_x, new_y = random.choice(empty_spots)
                self.grid[y][x] = None
                self.grid[new_y][new_x] = herbivore
                herbivore.x, herbivore.y = new_x, new_y
                herbivore.energy -= 1
        
        # Build reproductive energy
        if herbivore.energy > herbivore.reproduction_threshold * 0.7:
            herbivore.reproductive_energy += 1
    
    def process_carnivore(self, carnivore, x, y):
        """Process carnivore behavior"""
        # Hunt prey
        neighbors = self.get_neighbors(x, y, 2)  # Larger hunting radius
        prey = [n for n in neighbors if n.type in [HERBIVORE, OMNIVORE]]
        
        if prey and carnivore.energy < carnivore.max_energy * 0.9:
            # Hunting success based on aggression and speed
            hunt_success = carnivore.aggression * carnivore.speed * 0.5
            if random.random() < hunt_success:
                target = random.choice(prey)
                # Energy transfer
                energy_gained = min(target.energy * 0.8 * carnivore.efficiency, 30)
                carnivore.energy += energy_gained
                # Kill prey
                for py in range(GRID_HEIGHT):
                    for px in range(GRID_WIDTH):
                        if self.grid[py][px] is target:
                            self.grid[py][px] = None
                            self.resource_grid[py][px] += 0.2
                            break
        
        # Movement (carnivores are more active)
        if random.random() < carnivore.speed * 1.2:
            empty_spots = self.find_empty_nearby(x, y, 2)
            if empty_spots:
                new_x, new_y = random.choice(empty_spots)
                self.grid[y][x] = None
                self.grid[new_y][new_x] = carnivore
                carnivore.x, carnivore.y = new_x, new_y
                carnivore.energy -= 2
        
        # Build reproductive energy
        if carnivore.energy > carnivore.reproduction_threshold * 0.8:
            carnivore.reproductive_energy += 1
    
    def process_omnivore(self, omnivore, x, y):
        """Process omnivore behavior"""
        neighbors = self.get_neighbors(x, y)
        
        # Flexible diet
        plants = [n for n in neighbors if n.type == PLANT]
        prey = [n for n in neighbors if n.type == HERBIVORE and n.energy < omnivore.energy]
        
        if omnivore.energy < omnivore.max_energy * 0.8:
            if plants and (not prey or random.random() < 0.7):
                # Eat plants
                target = random.choice(plants)
                energy_gained = min(target.energy * 0.5 * omnivore.efficiency, 15)
                omnivore.energy += energy_gained
                target.energy -= energy_gained / 0.5
            elif prey:
                # Hunt small prey
                hunt_success = omnivore.aggression * 0.3
                if random.random() < hunt_success:
                    target = random.choice(prey)
                    energy_gained = min(target.energy * 0.7 * omnivore.efficiency, 25)
                    omnivore.energy += energy_gained
                    for py in range(GRID_HEIGHT):
                        for px in range(GRID_WIDTH):
                            if self.grid[py][px] is target:
                                self.grid[py][px] = None
                                self.resource_grid[py][px] += 0.15
                                break
        
        # Moderate movement
        if random.random() < omnivore.speed * 0.8:
            empty_spots = self.find_empty_nearby(x, y)
            if empty_spots:
                new_x, new_y = random.choice(empty_spots)
                self.grid[y][x] = None
                self.grid[new_y][new_x] = omnivore
                omnivore.x, omnivore.y = new_x, new_y
                omnivore.energy -= 1.5
        
        # Build reproductive energy
        if omnivore.energy > omnivore.reproduction_threshold * 0.75:
            omnivore.reproductive_energy += 1
    
    def process_decomposer(self, decomposer, x, y):
        """Process decomposer behavior"""
        # Consume organic matter
        if self.resource_grid[y][x] > 0:
            consumed = min(self.resource_grid[y][x], 10 * decomposer.efficiency)
            decomposer.energy += consumed * 2
            self.resource_grid[y][x] -= consumed
        
        # Convert waste to nutrients
        neighbors = self.get_neighbors(x, y)
        for neighbor in neighbors:
            if neighbor.energy < neighbor.max_energy * 0.3:  # Sick/dying organisms
                decomposer.energy += 1
                self.resource_grid[y][x] += 0.1
        
        # Limited movement
        if random.random() < decomposer.speed * 0.3:
            empty_spots = self.find_empty_nearby(x, y, 1)
            if empty_spots:
                new_x, new_y = random.choice(empty_spots)
                self.grid[y][x] = None
                self.grid[new_y][new_x] = decomposer
                decomposer.x, decomposer.y = new_x, new_y
                decomposer.energy -= 0.5
        
        # Build reproductive energy
        if decomposer.energy > decomposer.reproduction_threshold * 0.6:
            decomposer.reproductive_energy += 1
    
    def attempt_reproduction(self, organism, x, y):
        """Attempt reproduction for an organism"""
        empty_spots = self.find_empty_nearby(x, y)
        if not empty_spots:
            return
        
        # Check for partners (for sexual reproduction)
        neighbors = self.get_neighbors(x, y)
        partners = [n for n in neighbors if n.type == organism.type and n.can_reproduce()]
        
        partner = random.choice(partners) if partners else None
        child = organism.reproduce(partner)
        
        if child:
            child_x, child_y = random.choice(empty_spots)
            child.x, child.y = child_x, child_y
            self.grid[child_y][child_x] = child
    
    def update_generation(self):
        """Update the ecosystem simulation"""
        if not self.running:
            return
        
        current_time = time.time()
        if current_time - self.last_update < 1.0 / self.speed:
            return
        
        self.last_update = current_time
        self.total_time += 1.0 / self.speed
        
        # Update environment
        self.environment.update(self.total_time)
        
        # Create a list of all organisms to process
        organisms_to_process = []
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] is not None:
                    organisms_to_process.append((self.grid[y][x], x, y))
        
        # Shuffle to avoid processing bias
        random.shuffle(organisms_to_process)
        
        # Process each organism
        for organism, x, y in organisms_to_process:
            if self.grid[y][x] is organism:  # Organism might have moved or died
                self.process_organism(organism, x, y)
        
        # Environmental resource regeneration
        self.regenerate_resources()
        
        self.generation += 1
        self.update_population_stats()
    
    def regenerate_resources(self):
        """Regenerate environmental resources"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                # Slow resource regeneration near water
                if self.water_grid[y][x] > 0:
                    self.resource_grid[y][x] = min(1.0, self.resource_grid[y][x] + 0.01)
                
                # Seasonal effects
                if self.environment.season == 0:  # Spring - resource boost
                    self.resource_grid[y][x] = min(1.0, self.resource_grid[y][x] + 0.005)
                elif self.environment.season == 2:  # Autumn - resource decay
                    self.resource_grid[y][x] = max(0.0, self.resource_grid[y][x] - 0.002)
    
    def get_cell_color(self, x, y):
        """Get color based on view mode and cell content"""
        organism = self.grid[y][x]
        
        if self.view_mode == 0:  # Species view
            if organism is None:
                # Show water and resources
                if self.water_grid[y][x] > 0:
                    intensity = int(100 + self.water_grid[y][x] * 100)
                    return (0, 0, intensity)
                elif self.resource_grid[y][x] > 0:
                    intensity = int(50 + self.resource_grid[y][x] * 100)
                    return (intensity, intensity//2, 0)
                else:
                    return CYBER_BLACK
            
            # Species colors with health/energy modulation
            base_colors = {
                PLANT: PLANT_GREEN,
                HERBIVORE: NEON_YELLOW,
                CARNIVORE: PREDATOR_RED,
                OMNIVORE: NEON_PURPLE,
                DECOMPOSER: NEON_ORANGE
            }
            
            if organism.type in base_colors:
                base_color = base_colors[organism.type]
                health_factor = organism.health / 100
                energy_factor = organism.energy / organism.max_energy
                vitality = (health_factor + energy_factor) / 2
                
                return tuple(max(10, min(255, int(c * vitality))) for c in base_color)
        
        elif self.view_mode == 1:  # Energy view
            if organism is None:
                return CYBER_BLACK
            energy_ratio = organism.energy / organism.max_energy
            intensity = int(255 * energy_ratio)
            return (intensity, intensity, 0)
        
        elif self.view_mode == 2:  # Age view
            if organism is None:
                return CYBER_BLACK
            age_ratio = min(1.0, organism.age / organism.lifespan)
            return (int(255 * age_ratio), 0, int(255 * (1 - age_ratio)))
        
        elif self.view_mode == 3:  # Resource view
            resource_intensity = int(255 * min(1.0, self.resource_grid[y][x]))
            water_intensity = int(255 * min(1.0, self.water_grid[y][x]))
            return (resource_intensity, water_intensity, 50)
        
        elif self.view_mode == 4:  # Environment view
            temp_normalized = (self.environment.temperature + 20) / 60  # -20 to 40 range
            humidity_color = int(255 * self.environment.humidity)
            temp_color = int(255 * temp_normalized)
            return (temp_color, humidity_color, 100)
        
        return CYBER_BLACK
    
    def draw_grid(self, surface):
        """Draw the ecosystem grid"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = self.get_cell_color(x, y)
                rect = pygame.Rect(x * self.pixel_size, y * self.pixel_size, 
                                 self.pixel_size, self.pixel_size)
                pygame.draw.rect(surface, color, rect)
        
        # Draw grid lines
        if self.show_grid:
            grid_color = (30, 30, 30)
            for x in range(0, WIDTH, self.pixel_size):
                pygame.draw.line(surface, grid_color, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, self.pixel_size):
                pygame.draw.line(surface, grid_color, (0, y), (WIDTH, y))
    
    def draw_environmental_effects(self, surface):
        """Draw environmental effect overlays"""
        # Climate event indicators
        if self.environment.drought:
            # Yellow overlay
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(30)
            overlay.fill(NEON_YELLOW)
            surface.blit(overlay, (0, 0))
        
        if self.environment.flood:
            # Blue overlay
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(40)
            overlay.fill(WATER_BLUE)
            surface.blit(overlay, (0, 0))
        
        if self.environment.ice_age:
            # Cyan overlay
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(35)
            overlay.fill(NEON_CYAN)
            surface.blit(overlay, (0, 0))
        
        if self.environment.volcanic_activity:
            # Red overlay
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(25)
            overlay.fill(NEON_RED)
            surface.blit(overlay, (0, 0))
    
    def draw_statistics(self, surface):
        """Draw detailed ecosystem statistics"""
        font = pygame.font.Font(None, 16)
        small_font = pygame.font.Font(None, 14)
        y_offset = 5
        
        # Generation and time
        gen_text = font.render(f"GEN: {self.generation}", True, NEON_GREEN)
        surface.blit(gen_text, (5, y_offset))
        
        time_text = small_font.render(f"TIME: {self.total_time:.1f}s", True, NEON_CYAN)
        surface.blit(time_text, (80, y_offset + 2))
        y_offset += 20
        
        # Population counts
        total_pop = sum(self.population_stats.values())
        pop_text = font.render(f"TOTAL POP: {total_pop}", True, NEON_YELLOW)
        surface.blit(pop_text, (5, y_offset))
        y_offset += 18
        
        species_names = {
            PLANT: "PLANTS",
            HERBIVORE: "HERB",
            CARNIVORE: "CARN", 
            OMNIVORE: "OMNI",
            DECOMPOSER: "DECOMP"
        }
        
        colors = {
            PLANT: PLANT_GREEN,
            HERBIVORE: NEON_YELLOW,
            CARNIVORE: PREDATOR_RED,
            OMNIVORE: NEON_PURPLE,
            DECOMPOSER: NEON_ORANGE
        }
        
        for species_type, count in self.population_stats.items():
            if species_type in species_names:
                text = small_font.render(f"{species_names[species_type]}: {count}", 
                                       True, colors[species_type])
                surface.blit(text, (5, y_offset))
                y_offset += 14
        
        # Environmental status
        y_offset += 5
        env_text = font.render("ENVIRONMENT:", True, NEON_CYAN)
        surface.blit(env_text, (5, y_offset))
        y_offset += 16
        
        temp_text = small_font.render(f"TEMP: {self.environment.temperature:.1f}°C", 
                                    True, NEON_BLUE)
        surface.blit(temp_text, (5, y_offset))
        y_offset += 14
        
        season_names = ["SPRING", "SUMMER", "AUTUMN", "WINTER"]
        season_text = small_font.render(f"SEASON: {season_names[self.environment.season]}", 
                                      True, NEON_GREEN)
        surface.blit(season_text, (5, y_offset))
        y_offset += 14
        
        # Climate warnings
        if self.environment.drought:
            drought_text = small_font.render("⚠ DROUGHT", True, NEON_YELLOW)
            surface.blit(drought_text, (5, y_offset))
            y_offset += 14
        
        if self.environment.flood:
            flood_text = small_font.render("⚠ FLOOD", True, WATER_BLUE)
            surface.blit(flood_text, (5, y_offset))
            y_offset += 14
        
        if self.environment.ice_age:
            ice_text = small_font.render("⚠ ICE AGE", True, NEON_CYAN)
            surface.blit(ice_text, (5, y_offset))
            y_offset += 14
        
        if self.environment.volcanic_activity:
            volcano_text = small_font.render("⚠ VOLCANIC", True, NEON_RED)
            surface.blit(volcano_text, (5, y_offset))
    
    def draw_controls(self, surface):
        """Draw control instructions"""
        font = pygame.font.Font(None, 12)
        controls = [
            "ECOSYSTEM CONTROLS:",
            "SPACE: Play/Pause", "S: Step", "R: Reset", "C: Clear",
            "↑↓: Speed", "V: View Mode", "G: Grid", "I: Initialize",
            "",
            "ENVIRONMENT:",
            "D: Drought", "F: Flood", "T: Ice Age", "Y: Volcanic",
            "",
            "SPECIAL:",
            "F11: Fullscreen", "ESC: Return to Launcher"
        ]
        
        y_start = HEIGHT - 180
        for i, control in enumerate(controls):
            color = NEON_GREEN if control.endswith(":") else NEON_CYAN
            if control.startswith("⚠"):
                color = NEON_RED
            
            text = font.render(control, True, color)
            surface.blit(text, (5, y_start + i * 11))
    
    def handle_mouse_input(self, mouse_pos, mouse_pressed):
        """Handle mouse input for ecosystem manipulation"""
        if mouse_pressed[0]:  # Left click - add organisms
            mouse_x, mouse_y = mouse_pos
            grid_x = mouse_x // self.pixel_size
            grid_y = mouse_y // self.pixel_size
            
            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                if self.grid[grid_y][grid_x] is None:
                    # Cycle through species types
                    species_type = random.choice([PLANT, HERBIVORE, CARNIVORE, OMNIVORE, DECOMPOSER])
                    self.grid[grid_y][grid_x] = Species(species_type, grid_x, grid_y)
        
        elif mouse_pressed[2]:  # Right click - remove organisms
            mouse_x, mouse_y = mouse_pos
            grid_x = mouse_x // self.pixel_size
            grid_y = mouse_y // self.pixel_size
            
            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                self.grid[grid_y][grid_x] = None
    
    def cycle_view_mode(self):
        """Cycle view mode"""
        self.view_mode = (self.view_mode + 1) % len(self.view_modes)
    
    def toggle_running(self):
        """Toggle simulation"""
        self.running = not self.running
    
    def step_once(self):
        """Step simulation once"""
        old_running = self.running
        self.running = True
        self.last_update = 0
        self.update_generation()
        self.running = old_running

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
    ecosystem = AdvancedEcosystemSimulator()
    running = True
    show_stats = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return_to_launcher()
                elif event.key == pygame.K_F11:
                    toggle_fullscreen()
                elif event.key == pygame.K_SPACE:
                    ecosystem.toggle_running()
                elif event.key == pygame.K_s:
                    ecosystem.step_once()
                elif event.key == pygame.K_r:
                    ecosystem.initialize_ecosystem()
                elif event.key == pygame.K_c:
                    ecosystem.clear_ecosystem()
                elif event.key == pygame.K_v:
                    ecosystem.cycle_view_mode()
                elif event.key == pygame.K_g:
                    ecosystem.show_grid = not ecosystem.show_grid
                elif event.key == pygame.K_i:
                    ecosystem.initialize_ecosystem()
                elif event.key == pygame.K_d:
                    ecosystem.environment.drought = not ecosystem.environment.drought
                elif event.key == pygame.K_f:
                    ecosystem.environment.flood = not ecosystem.environment.flood
                elif event.key == pygame.K_t:
                    ecosystem.environment.ice_age = not ecosystem.environment.ice_age
                elif event.key == pygame.K_y:
                    ecosystem.environment.volcanic_activity = not ecosystem.environment.volcanic_activity
                elif event.key == pygame.K_h:
                    show_stats = not show_stats
                elif event.key == pygame.K_UP:
                    ecosystem.speed = min(ecosystem.speed + 1, 30)
                elif event.key == pygame.K_DOWN:
                    ecosystem.speed = max(ecosystem.speed - 1, 1)
        
        # Handle mouse input
        ecosystem.handle_mouse_input(mouse_pos, mouse_pressed)
        
        # Update ecosystem
        ecosystem.update_generation()
        
        # Draw everything
        screen.fill(CYBER_BLACK)
        
        # Draw ecosystem
        ecosystem.draw_grid(screen)
        
        # Draw environmental effects
        ecosystem.draw_environmental_effects(screen)
        
        # Draw statistics if enabled
        if show_stats:
            # Semi-transparent background
            stats_surface = pygame.Surface((200, 300))
            stats_surface.set_alpha(220)
            stats_surface.fill(CYBER_BLACK)
            screen.blit(stats_surface, (0, 0))
            
            ecosystem.draw_statistics(screen)
            ecosystem.draw_controls(screen)
        
        # Draw status
        status_font = pygame.font.Font(None, 20)
        status_text = f"{'RUNNING' if ecosystem.running else 'PAUSED'} | {ecosystem.view_modes[ecosystem.view_mode]} | SPEED: {ecosystem.speed}"
        status_color = LIFE_GREEN if ecosystem.running else NEON_YELLOW
        text_surface = status_font.render(status_text, True, status_color)
        screen.blit(text_surface, (WIDTH - 350, HEIGHT - 25))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main() 