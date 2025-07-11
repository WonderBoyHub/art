#!/usr/bin/env python3
"""
Advanced Civilization Simulator - WorldBox-style civilization game
Perfect for Raspberry Pi 5 with 3.5" display (480x320)
COMPLETE CIVILIZATION SIMULATOR WITH DNA GENETICS AND CHARACTER CREATION
"""

import pygame
import numpy as np
import random
import time
import math
import sys
import subprocess
import json
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

# Initialize Pygame
pygame.init()

# Screen dimensions optimized for Pi 5
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Civilization Simulator")

# Fullscreen support
fullscreen = False
clock = pygame.time.Clock()
start_time = time.time()

# Grid settings for pixel art style
TILE_SIZE = 4
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

# Enhanced cyberpunk color palette
CYBER_BLACK = (10, 10, 15)
NEON_BLUE = (50, 150, 255)
NEON_GREEN = (50, 255, 150)
NEON_CYAN = (50, 255, 255)
NEON_YELLOW = (255, 255, 50)
NEON_RED = (255, 50, 50)
NEON_PURPLE = (150, 50, 255)
NEON_ORANGE = (255, 150, 50)
TERRAIN_COLORS = {
    'water': (50, 100, 200),
    'grass': (50, 150, 50),
    'forest': (30, 100, 30),
    'mountain': (100, 80, 60),
    'desert': (200, 180, 100),
    'snow': (240, 240, 255),
    'swamp': (80, 100, 60),
    'volcanic': (150, 50, 50)
}

# Civilization colors
CIVILIZATION_COLORS = [
    (255, 100, 100),  # Red tribe
    (100, 255, 100),  # Green tribe
    (100, 100, 255),  # Blue tribe
    (255, 255, 100),  # Yellow tribe
    (255, 100, 255),  # Magenta tribe
    (100, 255, 255),  # Cyan tribe
    (255, 150, 100),  # Orange tribe
    (150, 100, 255),  # Purple tribe
]

class TerrainType(Enum):
    WATER = 0
    GRASS = 1
    FOREST = 2
    MOUNTAIN = 3
    DESERT = 4
    SNOW = 5
    SWAMP = 6
    VOLCANIC = 7

class ResourceType(Enum):
    FOOD = 0
    WOOD = 1
    STONE = 2
    METAL = 3
    KNOWLEDGE = 4
    ENERGY = 5

class TechType(Enum):
    AGRICULTURE = 0
    TOOLS = 1
    WEAPONS = 2
    CONSTRUCTION = 3
    MEDICINE = 4
    MAGIC = 5
    WARFARE = 6
    TRADE = 7

@dataclass
class DNAGene:
    """Individual DNA gene with specific traits"""
    strength: float  # Physical power (0.0-1.0)
    intelligence: float  # Learning ability
    charisma: float  # Social influence
    agility: float  # Speed and dexterity
    endurance: float  # Health and longevity
    creativity: float  # Innovation and art
    aggression: float  # Combat tendency
    cooperation: float  # Team work ability
    fertility: float  # Reproduction rate
    adaptability: float  # Environmental adaptation
    
    def __init__(self):
        """Initialize random DNA"""
        self.strength = random.uniform(0.1, 1.0)
        self.intelligence = random.uniform(0.1, 1.0)
        self.charisma = random.uniform(0.1, 1.0)
        self.agility = random.uniform(0.1, 1.0)
        self.endurance = random.uniform(0.1, 1.0)
        self.creativity = random.uniform(0.1, 1.0)
        self.aggression = random.uniform(0.0, 1.0)
        self.cooperation = random.uniform(0.0, 1.0)
        self.fertility = random.uniform(0.1, 1.0)
        self.adaptability = random.uniform(0.1, 1.0)
    
    def mate_with(self, other_dna: 'DNAGene') -> 'DNAGene':
        """Create offspring DNA by combining two parents"""
        child = DNAGene()
        
        # Blend traits from both parents
        child.strength = (self.strength + other_dna.strength) / 2
        child.intelligence = (self.intelligence + other_dna.intelligence) / 2
        child.charisma = (self.charisma + other_dna.charisma) / 2
        child.agility = (self.agility + other_dna.agility) / 2
        child.endurance = (self.endurance + other_dna.endurance) / 2
        child.creativity = (self.creativity + other_dna.creativity) / 2
        child.aggression = (self.aggression + other_dna.aggression) / 2
        child.cooperation = (self.cooperation + other_dna.cooperation) / 2
        child.fertility = (self.fertility + other_dna.fertility) / 2
        child.adaptability = (self.adaptability + other_dna.adaptability) / 2
        
        # Apply mutations
        child.mutate()
        return child
    
    def mutate(self, mutation_rate: float = 0.05):
        """Apply random mutations to DNA"""
        traits = ['strength', 'intelligence', 'charisma', 'agility', 'endurance', 
                 'creativity', 'aggression', 'cooperation', 'fertility', 'adaptability']
        
        for trait in traits:
            if random.random() < mutation_rate:
                current_value = getattr(self, trait)
                change = random.uniform(-0.1, 0.1)
                new_value = max(0.0, min(1.0, current_value + change))
                setattr(self, trait, new_value)
    
    def get_overall_fitness(self) -> float:
        """Calculate overall fitness score"""
        return (self.strength + self.intelligence + self.charisma + 
                self.agility + self.endurance + self.creativity + 
                self.cooperation + self.adaptability) / 8

class Character:
    """Individual character with genetics, skills, and personality"""
    def __init__(self, x: int, y: int, civilization_id: int = 0):
        self.x = x
        self.y = y
        self.civilization_id = civilization_id
        self.dna = DNAGene()
        
        # Character identity
        self.name = self.generate_name()
        self.age = random.randint(18, 30)
        self.gender = random.choice(['M', 'F'])
        self.profession = random.choice(['Farmer', 'Hunter', 'Crafter', 'Warrior', 'Shaman', 'Builder'])
        
        # Stats derived from DNA
        self.health = int(self.dna.endurance * 100)
        self.max_health = self.health
        self.energy = int(self.dna.endurance * 100)
        self.max_energy = self.energy
        self.experience = 0
        self.level = 1
        
        # Skills (0-100)
        self.skills = {
            'combat': int(self.dna.strength * 50 + self.dna.agility * 30),
            'crafting': int(self.dna.creativity * 50 + self.dna.intelligence * 30),
            'farming': int(self.dna.endurance * 40 + self.dna.intelligence * 20),
            'hunting': int(self.dna.agility * 40 + self.dna.strength * 30),
            'social': int(self.dna.charisma * 60 + self.dna.cooperation * 20),
            'magic': int(self.dna.intelligence * 40 + self.dna.creativity * 40),
            'building': int(self.dna.strength * 30 + self.dna.intelligence * 40),
            'leadership': int(self.dna.charisma * 50 + self.dna.intelligence * 30)
        }
        
        # Inventory and equipment
        self.inventory = {}
        self.equipment = {'weapon': None, 'armor': None, 'tool': None}
        
        # Relationships
        self.relationships = {}  # character_id -> relationship_value (-100 to 100)
        self.family = {'spouse': None, 'children': [], 'parents': []}
        
        # Goals and personality
        self.goals = []
        self.personality_traits = self.generate_personality()
        
        # Visual customization
        self.appearance = self.generate_appearance()
        
        # Life state
        self.alive = True
        self.task = None
        self.location_history = [(x, y)]
        
    def generate_name(self) -> str:
        """Generate procedural name based on DNA traits"""
        consonants = "bcdfghjklmnpqrstvwxyz"
        vowels = "aeiou"
        
        # Name length influenced by charisma
        name_length = 3 + int(self.dna.charisma * 4)
        name = ""
        
        for i in range(name_length):
            if i % 2 == 0:
                name += random.choice(consonants)
            else:
                name += random.choice(vowels)
        
        return name.capitalize()
    
    def generate_personality(self) -> Dict[str, float]:
        """Generate personality traits from DNA"""
        return {
            'brave': self.dna.strength * 0.7 + self.dna.endurance * 0.3,
            'kind': self.dna.cooperation * 0.8 + self.dna.charisma * 0.2,
            'curious': self.dna.intelligence * 0.6 + self.dna.creativity * 0.4,
            'social': self.dna.charisma * 0.8 + self.dna.cooperation * 0.2,
            'aggressive': self.dna.aggression,
            'creative': self.dna.creativity * 0.9 + self.dna.intelligence * 0.1,
            'adaptable': self.dna.adaptability
        }
    
    def generate_appearance(self) -> Dict[str, any]:
        """Generate visual appearance based on DNA"""
        return {
            'hair_color': random.choice(['black', 'brown', 'blonde', 'red', 'white']),
            'eye_color': random.choice(['brown', 'blue', 'green', 'hazel', 'gray']),
            'skin_tone': random.choice(['light', 'medium', 'dark']),
            'height': 0.8 + self.dna.strength * 0.4,  # Relative height
            'build': 'strong' if self.dna.strength > 0.7 else 'average' if self.dna.strength > 0.3 else 'slender'
        }
    
    def age_one_year(self):
        """Age the character one year"""
        self.age += 1
        
        # Skill development based on profession and DNA
        if self.profession == 'Farmer':
            self.skills['farming'] = min(100, self.skills['farming'] + random.randint(1, 3))
        elif self.profession == 'Hunter':
            self.skills['hunting'] = min(100, self.skills['hunting'] + random.randint(1, 3))
        elif self.profession == 'Warrior':
            self.skills['combat'] = min(100, self.skills['combat'] + random.randint(1, 3))
        elif self.profession == 'Crafter':
            self.skills['crafting'] = min(100, self.skills['crafting'] + random.randint(1, 3))
        elif self.profession == 'Shaman':
            self.skills['magic'] = min(100, self.skills['magic'] + random.randint(1, 3))
        elif self.profession == 'Builder':
            self.skills['building'] = min(100, self.skills['building'] + random.randint(1, 3))
        
        # Health effects of aging
        if self.age > 50:
            health_loss = int((self.age - 50) * 0.5)
            self.max_health = max(20, self.max_health - health_loss)
            self.health = min(self.health, self.max_health)
        
        # Death from old age
        if self.age > 80:
            death_chance = (self.age - 80) * 0.02
            if random.random() < death_chance:
                self.alive = False
    
    def can_reproduce(self) -> bool:
        """Check if character can have children"""
        return (self.alive and 18 <= self.age <= 45 and 
                self.health > 50 and self.energy > 30)
    
    def reproduce_with(self, partner: 'Character') -> Optional['Character']:
        """Have a child with another character"""
        if not (self.can_reproduce() and partner.can_reproduce()):
            return None
        
        # Energy cost for reproduction
        self.energy -= 20
        partner.energy -= 20
        
        # Create child
        child_x = self.x + random.randint(-2, 2)
        child_y = self.y + random.randint(-2, 2)
        child = Character(child_x, child_y, self.civilization_id)
        
        # Inherit DNA from both parents
        child.dna = self.dna.mate_with(partner.dna)
        
        # Update family relationships
        child.family['parents'] = [self, partner]
        self.family['children'].append(child)
        partner.family['children'].append(child)
        
        return child
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get character's display color"""
        if self.civilization_id < len(CIVILIZATION_COLORS):
            base_color = CIVILIZATION_COLORS[self.civilization_id]
        else:
            base_color = (255, 255, 255)
        
        # Modify color based on profession
        if self.profession == 'Warrior':
            return tuple(min(255, c + 20) for c in base_color)
        elif self.profession == 'Shaman':
            return tuple(max(0, c - 30) for c in base_color)
        else:
            return base_color

class Settlement:
    """Civilization settlement with buildings and population"""
    def __init__(self, x: int, y: int, civilization_id: int, name: str = ""):
        self.x = x
        self.y = y
        self.civilization_id = civilization_id
        self.name = name if name else self.generate_name()
        self.population = []
        self.buildings = {}
        self.resources = {resource: 0 for resource in ResourceType}
        self.technologies = {tech: 0 for tech in TechType}
        self.defense = 10
        self.happiness = 50
        self.growth_rate = 1.0
        self.trade_routes = []
        self.culture_points = 0
        self.established_year = 0
        
    def generate_name(self) -> str:
        """Generate settlement name"""
        prefixes = ["New", "Old", "Great", "Little", "Upper", "Lower", "North", "South", "East", "West"]
        suffixes = ["ville", "town", "burg", "haven", "ford", "wood", "hill", "dale", "field", "port"]
        
        if random.random() < 0.3:
            return random.choice(prefixes) + " " + random.choice(suffixes)
        else:
            return random.choice(suffixes).capitalize()
    
    def add_population(self, character: Character):
        """Add character to settlement"""
        self.population.append(character)
        character.x = self.x + random.randint(-5, 5)
        character.y = self.y + random.randint(-5, 5)
    
    def get_total_population(self) -> int:
        """Get total living population"""
        return len([c for c in self.population if c.alive])
    
    def get_resource_production(self) -> Dict[ResourceType, int]:
        """Calculate resource production per turn"""
        production = {resource: 0 for resource in ResourceType}
        
        for character in self.population:
            if not character.alive:
                continue
                
            # Production based on profession and skills
            if character.profession == 'Farmer':
                production[ResourceType.FOOD] += character.skills['farming'] // 10
            elif character.profession == 'Hunter':
                production[ResourceType.FOOD] += character.skills['hunting'] // 15
            elif character.profession == 'Crafter':
                production[ResourceType.WOOD] += character.skills['crafting'] // 20
                production[ResourceType.STONE] += character.skills['crafting'] // 25
            elif character.profession == 'Builder':
                production[ResourceType.STONE] += character.skills['building'] // 15
            elif character.profession == 'Shaman':
                production[ResourceType.KNOWLEDGE] += character.skills['magic'] // 10
        
        return production
    
    def update_settlement(self):
        """Update settlement each turn"""
        # Population growth/decline
        living_pop = self.get_total_population()
        
        # Resource consumption
        food_needed = living_pop * 2
        food_available = self.resources[ResourceType.FOOD]
        
        if food_available < food_needed:
            # Starvation effects
            self.happiness -= 10
            starvation_deaths = min(living_pop // 4, (food_needed - food_available) // 2)
            for _ in range(starvation_deaths):
                if self.population:
                    victim = random.choice([c for c in self.population if c.alive])
                    victim.alive = False
        
        # Resource production
        production = self.get_resource_production()
        for resource, amount in production.items():
            self.resources[resource] += amount
        
        # Resource consumption
        self.resources[ResourceType.FOOD] = max(0, self.resources[ResourceType.FOOD] - food_needed)
        
        # Technology advancement
        knowledge_for_tech = self.resources[ResourceType.KNOWLEDGE] // 100
        if knowledge_for_tech > 0:
            available_techs = [tech for tech in TechType if self.technologies[tech] < 5]
            if available_techs:
                tech_to_advance = random.choice(available_techs)
                self.technologies[tech_to_advance] += 1
                self.resources[ResourceType.KNOWLEDGE] -= 100
        
        # Culture development
        self.culture_points += living_pop // 10
        
        # Happiness effects
        if self.happiness > 70:
            self.growth_rate = 1.2
        elif self.happiness < 30:
            self.growth_rate = 0.8
        else:
            self.growth_rate = 1.0

class Civilization:
    """Complete civilization with settlements, technology, and culture"""
    def __init__(self, civ_id: int, name: str = ""):
        self.id = civ_id
        self.name = name if name else self.generate_name()
        self.color = CIVILIZATION_COLORS[civ_id % len(CIVILIZATION_COLORS)]
        self.settlements = []
        self.characters = []
        self.technologies = {tech: 0 for tech in TechType}
        self.culture = {
            'art_style': random.choice(['Geometric', 'Organic', 'Abstract', 'Realistic']),
            'values': random.choice(['Peaceful', 'Aggressive', 'Scholarly', 'Mercantile']),
            'religion': random.choice(['Ancestor Worship', 'Nature Spirits', 'Sky Gods', 'Earth Mother']),
            'government': random.choice(['Tribal', 'Monarchy', 'Council', 'Democracy'])
        }
        self.diplomacy = {}  # other_civ_id -> relationship (-100 to 100)
        self.wars = []
        self.trade_agreements = []
        self.total_population = 0
        
    def generate_name(self) -> str:
        """Generate civilization name"""
        prefixes = ["The", "Great", "Ancient", "Noble", "Proud", "Wise", "Strong", "Free"]
        roots = ["Axel", "Borin", "Celt", "Drak", "Elf", "Goth", "Hun", "Kelt", "Nord", "Orc", "Pict", "Sax", "Tyr", "Van"]
        suffixes = ["ans", "ians", "ites", "ese", "ish", "ic", "ar", "er", "en", "on"]
        
        if random.random() < 0.4:
            return random.choice(prefixes) + " " + random.choice(roots) + random.choice(suffixes)
        else:
            return random.choice(roots) + random.choice(suffixes)
    
    def add_settlement(self, settlement: Settlement):
        """Add settlement to civilization"""
        self.settlements.append(settlement)
        settlement.civilization_id = self.id
    
    def get_total_population(self) -> int:
        """Get total population across all settlements"""
        return sum(settlement.get_total_population() for settlement in self.settlements)
    
    def get_total_resources(self) -> Dict[ResourceType, int]:
        """Get total resources across all settlements"""
        total = {resource: 0 for resource in ResourceType}
        for settlement in self.settlements:
            for resource, amount in settlement.resources.items():
                total[resource] += amount
        return total
    
    def update_civilization(self):
        """Update entire civilization"""
        # Update all settlements
        for settlement in self.settlements:
            settlement.update_settlement()
        
        # Update total population
        self.total_population = self.get_total_population()
        
        # Technology sharing between settlements
        for tech in TechType:
            max_tech_level = max(s.technologies[tech] for s in self.settlements)
            for settlement in self.settlements:
                if settlement.technologies[tech] < max_tech_level:
                    # Slow tech spread
                    if random.random() < 0.1:
                        settlement.technologies[tech] += 1
        
        # Diplomacy updates
        for other_civ_id in self.diplomacy:
            # Gradual relationship decay toward neutral
            current_rel = self.diplomacy[other_civ_id]
            if current_rel > 0:
                self.diplomacy[other_civ_id] = max(0, current_rel - 1)
            elif current_rel < 0:
                self.diplomacy[other_civ_id] = min(0, current_rel + 1)

class WorldMap:
    """Game world with terrain, resources, and biomes"""
    def __init__(self):
        self.terrain = np.full((GRID_HEIGHT, GRID_WIDTH), TerrainType.GRASS, dtype=object)
        self.resources = np.zeros((GRID_HEIGHT, GRID_WIDTH, len(ResourceType)), dtype=int)
        self.biomes = np.full((GRID_HEIGHT, GRID_WIDTH), 'temperate', dtype=object)
        self.elevation = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=float)
        self.temperature = np.full((GRID_HEIGHT, GRID_WIDTH), 20.0, dtype=float)
        self.rainfall = np.full((GRID_HEIGHT, GRID_WIDTH), 0.5, dtype=float)
        
        self.generate_world()
    
    def generate_world(self):
        """Generate the world terrain and resources"""
        # Generate elevation using simple noise
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                # Simple pseudo-noise for elevation
                noise = (math.sin(x * 0.1) + math.sin(y * 0.1) + 
                        math.sin(x * 0.05) + math.sin(y * 0.05)) / 4
                self.elevation[y][x] = max(0, min(1, 0.5 + noise * 0.3))
        
        # Generate temperature based on latitude
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                # Temperature decreases toward poles and with elevation
                latitude_factor = 1.0 - abs(y - GRID_HEIGHT/2) / (GRID_HEIGHT/2)
                elevation_factor = 1.0 - self.elevation[y][x] * 0.5
                self.temperature[y][x] = 30 * latitude_factor * elevation_factor
        
        # Generate rainfall using simple patterns
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                # More rain in middle latitudes and near water
                self.rainfall[y][x] = random.uniform(0.2, 0.8)
        
        # Generate terrain based on elevation, temperature, and rainfall
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                elevation = self.elevation[y][x]
                temp = self.temperature[y][x]
                rain = self.rainfall[y][x]
                
                if elevation < 0.2:
                    self.terrain[y][x] = TerrainType.WATER
                elif elevation > 0.8:
                    if temp < 5:
                        self.terrain[y][x] = TerrainType.SNOW
                    else:
                        self.terrain[y][x] = TerrainType.MOUNTAIN
                elif rain < 0.3:
                    self.terrain[y][x] = TerrainType.DESERT
                elif rain > 0.7:
                    if temp > 25:
                        self.terrain[y][x] = TerrainType.SWAMP
                    else:
                        self.terrain[y][x] = TerrainType.FOREST
                else:
                    self.terrain[y][x] = TerrainType.GRASS
                
                # Volcanic terrain (rare)
                if random.random() < 0.01:
                    self.terrain[y][x] = TerrainType.VOLCANIC
        
        # Place resources based on terrain
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                terrain = self.terrain[y][x]
                
                if terrain == TerrainType.FOREST:
                    self.resources[y][x][ResourceType.WOOD.value] = random.randint(50, 200)
                elif terrain == TerrainType.MOUNTAIN:
                    self.resources[y][x][ResourceType.STONE.value] = random.randint(100, 300)
                    self.resources[y][x][ResourceType.METAL.value] = random.randint(20, 100)
                elif terrain == TerrainType.GRASS:
                    self.resources[y][x][ResourceType.FOOD.value] = random.randint(30, 150)
                elif terrain == TerrainType.WATER:
                    self.resources[y][x][ResourceType.FOOD.value] = random.randint(20, 100)
                elif terrain == TerrainType.VOLCANIC:
                    self.resources[y][x][ResourceType.ENERGY.value] = random.randint(100, 500)
    
    def get_terrain_color(self, terrain_type: TerrainType) -> Tuple[int, int, int]:
        """Get color for terrain type"""
        terrain_map = {
            TerrainType.WATER: TERRAIN_COLORS['water'],
            TerrainType.GRASS: TERRAIN_COLORS['grass'],
            TerrainType.FOREST: TERRAIN_COLORS['forest'],
            TerrainType.MOUNTAIN: TERRAIN_COLORS['mountain'],
            TerrainType.DESERT: TERRAIN_COLORS['desert'],
            TerrainType.SNOW: TERRAIN_COLORS['snow'],
            TerrainType.SWAMP: TERRAIN_COLORS['swamp'],
            TerrainType.VOLCANIC: TERRAIN_COLORS['volcanic']
        }
        return terrain_map.get(terrain_type, (100, 100, 100))

class CivilizationSimulator:
    """Main civilization simulation game"""
    def __init__(self):
        self.world = WorldMap()
        self.civilizations = []
        self.all_characters = []
        self.settlements = []
        self.running = False
        self.paused = False
        self.speed = 1
        self.year = 0
        self.day = 0
        self.selected_character = None
        self.selected_settlement = None
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1.0
        
        # UI state
        self.view_mode = 0  # 0: Overview, 1: Terrain, 2: Resources, 3: Demographics, 4: Diplomacy
        self.show_hud = True
        self.show_names = True
        self.show_stats = True
        self.character_creation_mode = False
        self.current_civilization = 0
        
        # Performance optimization
        self.last_update = time.time()
        self.update_interval = 0.1  # Update every 0.1 seconds
        
        self.view_mode_names = [
            "OVERVIEW",
            "TERRAIN",
            "RESOURCES",
            "DEMOGRAPHICS",
            "DIPLOMACY"
        ]
        
        self.initialize_world()
    
    def initialize_world(self):
        """Initialize the world with starting civilizations"""
        # Create initial civilizations
        for i in range(4):  # Start with 4 civilizations
            civ = Civilization(i)
            self.civilizations.append(civ)
            
            # Create starting settlement
            attempts = 0
            while attempts < 100:  # Avoid infinite loop
                x = random.randint(10, GRID_WIDTH - 10)
                y = random.randint(10, GRID_HEIGHT - 10)
                
                # Check if location is suitable (not water, not too close to others)
                if self.world.terrain[y][x] != TerrainType.WATER:
                    suitable = True
                    for settlement in self.settlements:
                        if abs(settlement.x - x) < 15 or abs(settlement.y - y) < 15:
                            suitable = False
                            break
                    
                    if suitable:
                        settlement = Settlement(x, y, i)
                        settlement.established_year = self.year
                        civ.add_settlement(settlement)
                        self.settlements.append(settlement)
                        
                        # Add starting population
                        for _ in range(random.randint(8, 15)):
                            character = Character(x, y, i)
                            settlement.add_population(character)
                            self.all_characters.append(character)
                        
                        break
                
                attempts += 1
        
        # Initialize diplomacy
        for i, civ1 in enumerate(self.civilizations):
            for j, civ2 in enumerate(self.civilizations):
                if i != j:
                    # Start with neutral to slightly negative relations
                    civ1.diplomacy[j] = random.randint(-20, 20)
    
    def update_simulation(self):
        """Update the entire simulation"""
        current_time = time.time()
        if current_time - self.last_update < self.update_interval:
            return
        
        self.last_update = current_time
        
        if self.paused:
            return
        
        # Update day/year
        self.day += 1
        if self.day >= 365:
            self.day = 0
            self.year += 1
            
            # Annual updates
            for character in self.all_characters:
                if character.alive:
                    character.age_one_year()
            
            # Settlement and civilization updates
            for settlement in self.settlements:
                settlement.update_settlement()
            
            for civ in self.civilizations:
                civ.update_civilization()
        
        # Character behavior and reproduction
        if self.day % 30 == 0:  # Monthly updates
            self.update_character_behavior()
            self.handle_reproduction()
            self.handle_migration()
    
    def update_character_behavior(self):
        """Update character behavior, relationships, and actions"""
        for character in self.all_characters:
            if not character.alive:
                continue
            
            # Random movement
            if random.random() < 0.3:
                dx = random.randint(-2, 2)
                dy = random.randint(-2, 2)
                new_x = max(0, min(GRID_WIDTH - 1, character.x + dx))
                new_y = max(0, min(GRID_HEIGHT - 1, character.y + dy))
                character.x = new_x
                character.y = new_y
            
            # Skill development
            if random.random() < 0.1:
                skill = random.choice(list(character.skills.keys()))
                character.skills[skill] = min(100, character.skills[skill] + 1)
            
            # Relationship building
            nearby_characters = self.get_nearby_characters(character, 5)
            for other in nearby_characters:
                if other.civilization_id == character.civilization_id:
                    # Same civilization - build friendship
                    if other.name not in character.relationships:
                        character.relationships[other.name] = 0
                    
                    compatibility = abs(character.personality_traits['social'] - other.personality_traits['social'])
                    if compatibility < 0.3:
                        character.relationships[other.name] = min(100, character.relationships[other.name] + 1)
                else:
                    # Different civilization - depends on diplomacy
                    civ_relation = self.civilizations[character.civilization_id].diplomacy.get(other.civilization_id, 0)
                    if civ_relation > 0:
                        if other.name not in character.relationships:
                            character.relationships[other.name] = 0
                        character.relationships[other.name] = min(50, character.relationships[other.name] + 1)
    
    def handle_reproduction(self):
        """Handle character reproduction"""
        for character in self.all_characters:
            if not character.alive or not character.can_reproduce():
                continue
            
            if character.family['spouse'] is None:
                # Look for potential spouse
                potential_partners = [
                    c for c in self.all_characters 
                    if (c.alive and c.can_reproduce() and 
                        c.civilization_id == character.civilization_id and
                        c.gender != character.gender and
                        c.family['spouse'] is None and
                        abs(c.x - character.x) < 10 and
                        abs(c.y - character.y) < 10)
                ]
                
                if potential_partners and random.random() < 0.1:
                    partner = random.choice(potential_partners)
                    character.family['spouse'] = partner
                    partner.family['spouse'] = character
            
            # Have children
            if (character.family['spouse'] is not None and 
                character.family['spouse'].alive and 
                len(character.family['children']) < 5 and
                random.random() < 0.05):
                
                child = character.reproduce_with(character.family['spouse'])
                if child:
                    self.all_characters.append(child)
                    
                    # Add to appropriate settlement
                    nearest_settlement = self.find_nearest_settlement(child.x, child.y, child.civilization_id)
                    if nearest_settlement:
                        nearest_settlement.add_population(child)
    
    def handle_migration(self):
        """Handle character migration between settlements"""
        for character in self.all_characters:
            if not character.alive:
                continue
            
            # Small chance of migration
            if random.random() < 0.01:
                # Find settlements in same civilization
                same_civ_settlements = [s for s in self.settlements if s.civilization_id == character.civilization_id]
                if len(same_civ_settlements) > 1:
                    new_settlement = random.choice(same_civ_settlements)
                    character.x = new_settlement.x + random.randint(-5, 5)
                    character.y = new_settlement.y + random.randint(-5, 5)
    
    def get_nearby_characters(self, character: Character, radius: int) -> List[Character]:
        """Get characters within radius of given character"""
        nearby = []
        for other in self.all_characters:
            if other != character and other.alive:
                distance = math.sqrt((other.x - character.x)**2 + (other.y - character.y)**2)
                if distance <= radius:
                    nearby.append(other)
        return nearby
    
    def find_nearest_settlement(self, x: int, y: int, civ_id: int) -> Optional[Settlement]:
        """Find nearest settlement for given civilization"""
        nearest = None
        min_distance = float('inf')
        
        for settlement in self.settlements:
            if settlement.civilization_id == civ_id:
                distance = math.sqrt((settlement.x - x)**2 + (settlement.y - y)**2)
                if distance < min_distance:
                    min_distance = distance
                    nearest = settlement
        
        return nearest
    
    def handle_mouse_click(self, mouse_pos: Tuple[int, int]):
        """Handle mouse click for character/settlement selection"""
        world_x = (mouse_pos[0] - self.camera_x) // TILE_SIZE
        world_y = (mouse_pos[1] - self.camera_y) // TILE_SIZE
        
        # Check for character selection
        for character in self.all_characters:
            if character.alive and abs(character.x - world_x) <= 1 and abs(character.y - world_y) <= 1:
                self.selected_character = character
                self.selected_settlement = None
                return
        
        # Check for settlement selection
        for settlement in self.settlements:
            if abs(settlement.x - world_x) <= 3 and abs(settlement.y - world_y) <= 3:
                self.selected_settlement = settlement
                self.selected_character = None
                return
        
        # Clear selection
        self.selected_character = None
        self.selected_settlement = None
    
    def enter_character_creation_mode(self):
        """Enter character creation mode"""
        self.character_creation_mode = True
        self.paused = True
    
    def create_custom_character(self, x: int, y: int, customization: Dict):
        """Create a custom character with player customization"""
        character = Character(x, y, self.current_civilization)
        
        # Apply customizations
        if 'name' in customization:
            character.name = customization['name']
        if 'profession' in customization:
            character.profession = customization['profession']
        if 'appearance' in customization:
            character.appearance.update(customization['appearance'])
        
        # Custom DNA modifications
        if 'dna_mods' in customization:
            for trait, value in customization['dna_mods'].items():
                if hasattr(character.dna, trait):
                    setattr(character.dna, trait, max(0.0, min(1.0, value)))
        
        # Recalculate stats based on modified DNA
        character.health = int(character.dna.endurance * 100)
        character.max_health = character.health
        character.energy = int(character.dna.endurance * 100)
        character.max_energy = character.energy
        
        # Recalculate skills
        character.skills = {
            'combat': int(character.dna.strength * 50 + character.dna.agility * 30),
            'crafting': int(character.dna.creativity * 50 + character.dna.intelligence * 30),
            'farming': int(character.dna.endurance * 40 + character.dna.intelligence * 20),
            'hunting': int(character.dna.agility * 40 + character.dna.strength * 30),
            'social': int(character.dna.charisma * 60 + character.dna.cooperation * 20),
            'magic': int(character.dna.intelligence * 40 + character.dna.creativity * 40),
            'building': int(character.dna.strength * 30 + character.dna.intelligence * 40),
            'leadership': int(character.dna.charisma * 50 + character.dna.intelligence * 30)
        }
        
        self.all_characters.append(character)
        
        # Add to appropriate settlement
        nearest_settlement = self.find_nearest_settlement(x, y, self.current_civilization)
        if nearest_settlement:
            nearest_settlement.add_population(character)
        
        self.character_creation_mode = False
        self.paused = False
        return character
    
    def draw_world(self, surface):
        """Draw the world terrain and entities"""
        # Draw terrain
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                screen_x = x * TILE_SIZE + self.camera_x
                screen_y = y * TILE_SIZE + self.camera_y
                
                if -TILE_SIZE <= screen_x < WIDTH and -TILE_SIZE <= screen_y < HEIGHT:
                    if self.view_mode == 1:  # Terrain view
                        color = self.world.get_terrain_color(self.world.terrain[y][x])
                    elif self.view_mode == 2:  # Resources view
                        # Show dominant resource
                        max_resource = 0
                        resource_color = (50, 50, 50)
                        for i, resource in enumerate(ResourceType):
                            if self.world.resources[y][x][i] > max_resource:
                                max_resource = self.world.resources[y][x][i]
                                if resource == ResourceType.FOOD:
                                    resource_color = (100, 255, 100)
                                elif resource == ResourceType.WOOD:
                                    resource_color = (150, 100, 50)
                                elif resource == ResourceType.STONE:
                                    resource_color = (150, 150, 150)
                                elif resource == ResourceType.METAL:
                                    resource_color = (255, 200, 100)
                                elif resource == ResourceType.ENERGY:
                                    resource_color = (255, 100, 255)
                        color = resource_color
                    else:  # Overview
                        color = self.world.get_terrain_color(self.world.terrain[y][x])
                    
                    pygame.draw.rect(surface, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
        
        # Draw settlements
        for settlement in self.settlements:
            screen_x = settlement.x * TILE_SIZE + self.camera_x
            screen_y = settlement.y * TILE_SIZE + self.camera_y
            
            if -TILE_SIZE <= screen_x < WIDTH and -TILE_SIZE <= screen_y < HEIGHT:
                # Settlement color based on civilization
                color = CIVILIZATION_COLORS[settlement.civilization_id % len(CIVILIZATION_COLORS)]
                
                # Settlement size based on population
                size = min(TILE_SIZE * 3, TILE_SIZE + settlement.get_total_population() // 5)
                
                pygame.draw.rect(surface, color, (screen_x, screen_y, size, size))
                
                # Selection highlight
                if settlement == self.selected_settlement:
                    pygame.draw.rect(surface, NEON_YELLOW, (screen_x-2, screen_y-2, size+4, size+4), 2)
                
                # Draw settlement name
                if self.show_names:
                    font = pygame.font.Font(None, 16)
                    text = font.render(settlement.name, True, NEON_CYAN)
                    surface.blit(text, (screen_x, screen_y - 15))
        
        # Draw characters
        for character in self.all_characters:
            if not character.alive:
                continue
            
            screen_x = character.x * TILE_SIZE + self.camera_x
            screen_y = character.y * TILE_SIZE + self.camera_y
            
            if -TILE_SIZE <= screen_x < WIDTH and -TILE_SIZE <= screen_y < HEIGHT:
                color = character.get_color()
                
                # Character size based on profession
                size = TILE_SIZE - 1
                if character.profession == 'Warrior':
                    size = TILE_SIZE
                
                pygame.draw.rect(surface, color, (screen_x, screen_y, size, size))
                
                # Selection highlight
                if character == self.selected_character:
                    pygame.draw.rect(surface, NEON_YELLOW, (screen_x-1, screen_y-1, size+2, size+2), 2)
                
                # Draw character name
                if self.show_names and character == self.selected_character:
                    font = pygame.font.Font(None, 14)
                    text = font.render(character.name, True, NEON_GREEN)
                    surface.blit(text, (screen_x, screen_y - 12))
    
    def draw_hud(self, surface):
        """Draw the heads-up display"""
        if not self.show_hud:
            return
        
        # Background panel
        hud_rect = pygame.Rect(0, 0, WIDTH, 60)
        pygame.draw.rect(surface, (0, 0, 0, 180), hud_rect)
        
        # Time display
        font = pygame.font.Font(None, 24)
        time_text = f"Year {self.year}, Day {self.day}"
        text = font.render(time_text, True, NEON_CYAN)
        surface.blit(text, (10, 10))
        
        # View mode
        mode_text = f"View: {self.view_mode_names[self.view_mode]}"
        text = font.render(mode_text, True, NEON_GREEN)
        surface.blit(text, (10, 30))
        
        # Speed indicator
        speed_text = f"Speed: {self.speed}x"
        text = font.render(speed_text, True, NEON_YELLOW)
        surface.blit(text, (200, 10))
        
        # Population count
        total_pop = sum(len([c for c in self.all_characters if c.alive and c.civilization_id == civ.id]) 
                       for civ in self.civilizations)
        pop_text = f"Population: {total_pop}"
        text = font.render(pop_text, True, NEON_ORANGE)
        surface.blit(text, (200, 30))
        
        # Civilization count
        civ_text = f"Civilizations: {len(self.civilizations)}"
        text = font.render(civ_text, True, NEON_PURPLE)
        surface.blit(text, (350, 10))
        
        # Pause indicator
        if self.paused:
            pause_text = "PAUSED"
            text = font.render(pause_text, True, NEON_RED)
            surface.blit(text, (350, 30))
    
    def draw_character_info(self, surface):
        """Draw selected character information"""
        if not self.selected_character:
            return
        
        char = self.selected_character
        
        # Info panel
        panel_rect = pygame.Rect(WIDTH - 200, 70, 190, 200)
        pygame.draw.rect(surface, (0, 0, 0, 200), panel_rect)
        pygame.draw.rect(surface, NEON_CYAN, panel_rect, 2)
        
        y_offset = 80
        font = pygame.font.Font(None, 16)
        
        # Character name and basic info
        info_lines = [
            f"Name: {char.name}",
            f"Age: {char.age}",
            f"Profession: {char.profession}",
            f"Health: {char.health}/{char.max_health}",
            f"Energy: {char.energy}/{char.max_energy}",
            "",
            "DNA Traits:",
            f"Strength: {char.dna.strength:.2f}",
            f"Intelligence: {char.dna.intelligence:.2f}",
            f"Charisma: {char.dna.charisma:.2f}",
            f"Agility: {char.dna.agility:.2f}",
            f"Endurance: {char.dna.endurance:.2f}",
            f"Creativity: {char.dna.creativity:.2f}"
        ]
        
        for line in info_lines:
            if line:
                text = font.render(line, True, NEON_GREEN)
                surface.blit(text, (WIDTH - 195, y_offset))
            y_offset += 12
    
    def draw_settlement_info(self, surface):
        """Draw selected settlement information"""
        if not self.selected_settlement:
            return
        
        settlement = self.selected_settlement
        
        # Info panel
        panel_rect = pygame.Rect(WIDTH - 200, 70, 190, 200)
        pygame.draw.rect(surface, (0, 0, 0, 200), panel_rect)
        pygame.draw.rect(surface, NEON_CYAN, panel_rect, 2)
        
        y_offset = 80
        font = pygame.font.Font(None, 16)
        
        # Settlement info
        info_lines = [
            f"Name: {settlement.name}",
            f"Population: {settlement.get_total_population()}",
            f"Civilization: {self.civilizations[settlement.civilization_id].name}",
            f"Happiness: {settlement.happiness}",
            f"Defense: {settlement.defense}",
            "",
            "Resources:",
            f"Food: {settlement.resources[ResourceType.FOOD]}",
            f"Wood: {settlement.resources[ResourceType.WOOD]}",
            f"Stone: {settlement.resources[ResourceType.STONE]}",
            f"Metal: {settlement.resources[ResourceType.METAL]}",
            f"Knowledge: {settlement.resources[ResourceType.KNOWLEDGE]}",
            f"Energy: {settlement.resources[ResourceType.ENERGY]}"
        ]
        
        for line in info_lines:
            if line:
                text = font.render(line, True, NEON_GREEN)
                surface.blit(text, (WIDTH - 195, y_offset))
            y_offset += 12
    
    def draw_controls(self, surface):
        """Draw control instructions"""
        controls_rect = pygame.Rect(10, HEIGHT - 100, 300, 90)
        pygame.draw.rect(surface, (0, 0, 0, 180), controls_rect)
        
        font = pygame.font.Font(None, 16)
        controls = [
            "SPACE - Pause/Resume",
            "V - Change View Mode",
            "F8 - Fullscreen",
            "ESC - Return to Launcher",
            "C - Create Character",
            "Click - Select Character/Settlement"
        ]
        
        for i, control in enumerate(controls):
            text = font.render(control, True, NEON_YELLOW)
            surface.blit(text, (15, HEIGHT - 95 + i * 12))
    
    def handle_input(self, keys, events):
        """Handle keyboard and mouse input"""
        # Camera movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.camera_x += 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.camera_x -= 5
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.camera_y += 5
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.camera_y -= 5
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_v:
                    self.view_mode = (self.view_mode + 1) % len(self.view_mode_names)
                elif event.key == pygame.K_h:
                    self.show_hud = not self.show_hud
                elif event.key == pygame.K_n:
                    self.show_names = not self.show_names
                elif event.key == pygame.K_c:
                    self.enter_character_creation_mode()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.speed = min(10, self.speed + 1)
                elif event.key == pygame.K_MINUS:
                    self.speed = max(1, self.speed - 1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_mouse_click(event.pos)

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
    """Main game loop"""
    global screen
    
    # Initialize game
    game = CivilizationSimulator()
    
    # Main game loop
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
        game.handle_input(keys, events)
        
        # Update simulation
        game.update_simulation()
        
        # Clear screen
        screen.fill(CYBER_BLACK)
        
        # Draw everything
        game.draw_world(screen)
        game.draw_hud(screen)
        game.draw_character_info(screen)
        game.draw_settlement_info(screen)
        game.draw_controls(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS for smooth experience
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 