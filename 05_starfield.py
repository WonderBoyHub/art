#!/usr/bin/env python3
"""
Advanced Space Exploration Simulator - No Man's Sky/Star Citizen style game
Perfect for Raspberry Pi 5 with 3.5" display (480x320)
COMPLETE SPACE EXPLORATION WITH PLANETS, TRADING, ALIENS, AND SHIP UPGRADES
"""

import pygame
import random
import math
import time
import sys
import subprocess
import json
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Any

# Initialize Pygame
pygame.init()

# Screen dimensions optimized for Pi 5
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Space Exploration Simulator")

# Fullscreen support
fullscreen = False
clock = pygame.time.Clock()
start_time = time.time()

# Enhanced cyberpunk color palette
CYBER_BLACK = (10, 10, 15)
NEON_BLUE = (50, 150, 255)
NEON_GREEN = (50, 255, 150)
NEON_CYAN = (50, 255, 255)
NEON_YELLOW = (255, 255, 50)
NEON_RED = (255, 50, 50)
NEON_PURPLE = (150, 50, 255)
NEON_ORANGE = (255, 150, 50)
SPACE_COLORS = {
    'deep_space': (5, 5, 20),
    'nebula': (100, 50, 200),
    'star_yellow': (255, 255, 150),
    'star_blue': (150, 200, 255),
    'star_red': (255, 150, 150),
    'planet_earth': (100, 150, 255),
    'planet_desert': (200, 150, 100),
    'planet_ice': (200, 230, 255),
    'planet_lava': (255, 100, 50),
    'planet_forest': (100, 200, 100),
    'planet_toxic': (150, 255, 50),
    'asteroid': (150, 120, 100),
    'ship_hull': (120, 120, 150),
    'alien_green': (100, 255, 100),
    'alien_purple': (200, 100, 255),
    'alien_orange': (255, 150, 50)
}

class GameState(Enum):
    SPACE_FLIGHT = 0
    PLANET_SURFACE = 1
    STATION_DOCKED = 2
    TRADING = 3
    SHIP_UPGRADE = 4
    ALIEN_ENCOUNTER = 5
    GALAXY_MAP = 6

class PlanetType(Enum):
    EARTH_LIKE = 0
    DESERT = 1
    ICE = 2
    LAVA = 3
    FOREST = 4
    TOXIC = 5
    OCEAN = 6
    BARREN = 7

class ResourceType(Enum):
    CARBON = 0
    IRON = 1
    PLATINUM = 2
    QUANTUM_CRYSTAL = 3
    EXOTIC_MATTER = 4
    FUEL = 5
    CREDITS = 6

class AlienRace(Enum):
    HUMANOID = 0
    INSECTOID = 1
    CRYSTALLINE = 2
    ENERGY_BEING = 3
    MECHANICAL = 4

@dataclass
class Ship:
    """Player's spaceship with upgrades and customization"""
    name: str
    ship_class: str  # Fighter, Explorer, Trader, Freighter
    hull_integrity: float
    max_hull: float
    shields: float
    max_shields: float
    fuel: float
    max_fuel: float
    cargo_capacity: int
    cargo: Dict[ResourceType, int]
    
    # Ship systems
    engine_power: float
    weapon_power: float
    scanner_range: float
    hyperdrive_class: int
    life_support: float
    
    # Upgrades
    upgrades: Dict[str, int]
    
    def __init__(self, name: str = "Explorer"):
        self.name = name
        self.ship_class = "Explorer"
        self.hull_integrity = 100.0
        self.max_hull = 100.0
        self.shields = 100.0
        self.max_shields = 100.0
        self.fuel = 100.0
        self.max_fuel = 100.0
        self.cargo_capacity = 50
        self.cargo = {resource: 0 for resource in ResourceType}
        
        # Basic systems
        self.engine_power = 1.0
        self.weapon_power = 1.0
        self.scanner_range = 100.0
        self.hyperdrive_class = 1
        self.life_support = 100.0
        
        # No upgrades initially
        self.upgrades = {
            'engine': 0,
            'weapons': 0,
            'shields': 0,
            'hyperdrive': 0,
            'scanner': 0,
            'cargo': 0
        }
    
    def get_cargo_used(self) -> int:
        """Get total cargo space used"""
        return sum(self.cargo.values())
    
    def can_add_cargo(self, resource: ResourceType, amount: int) -> bool:
        """Check if cargo can be added"""
        return self.get_cargo_used() + amount <= self.cargo_capacity
    
    def add_cargo(self, resource: ResourceType, amount: int) -> bool:
        """Add cargo if space available"""
        if self.can_add_cargo(resource, amount):
            self.cargo[resource] += amount
            return True
        return False
    
    def remove_cargo(self, resource: ResourceType, amount: int) -> bool:
        """Remove cargo if available"""
        if self.cargo[resource] >= amount:
            self.cargo[resource] -= amount
            return True
        return False
    
    def apply_upgrade(self, upgrade_type: str):
        """Apply ship upgrade"""
        if upgrade_type in self.upgrades:
            self.upgrades[upgrade_type] += 1
            
            # Apply upgrade effects
            if upgrade_type == 'engine':
                self.engine_power += 0.2
            elif upgrade_type == 'weapons':
                self.weapon_power += 0.3
            elif upgrade_type == 'shields':
                self.max_shields += 20
                self.shields = self.max_shields
            elif upgrade_type == 'hyperdrive':
                self.hyperdrive_class += 1
            elif upgrade_type == 'scanner':
                self.scanner_range += 50
            elif upgrade_type == 'cargo':
                self.cargo_capacity += 10
    
    def repair_hull(self, amount: float):
        """Repair hull damage"""
        self.hull_integrity = min(self.max_hull, self.hull_integrity + amount)
    
    def recharge_shields(self, amount: float):
        """Recharge shields"""
        self.shields = min(self.max_shields, self.shields + amount)
    
    def refuel(self, amount: float):
        """Refuel ship"""
        self.fuel = min(self.max_fuel, self.fuel + amount)

@dataclass
class Planet:
    """Planet with resources and surface exploration"""
    name: str
    planet_type: PlanetType
    size: float
    temperature: float
    atmosphere: str
    gravity: float
    resources: Dict[ResourceType, int]
    hazards: List[str]
    life_forms: List[str]
    points_of_interest: List[Dict[str, Any]]
    
    def __init__(self, name: str = "Unknown"):
        self.name = name
        self.planet_type = random.choice(list(PlanetType))
        self.size = random.uniform(0.5, 2.0)
        self.temperature = random.uniform(-100, 500)
        self.atmosphere = random.choice(['None', 'Thin', 'Dense', 'Toxic', 'Corrosive'])
        self.gravity = random.uniform(0.1, 3.0)
        self.resources = {}
        self.hazards = []
        self.life_forms = []
        self.points_of_interest = []
        
        self.generate_planet_data()
    
    def generate_planet_data(self):
        """Generate planet-specific data"""
        # Resource distribution based on planet type
        if self.planet_type == PlanetType.EARTH_LIKE:
            self.resources = {
                ResourceType.CARBON: random.randint(50, 200),
                ResourceType.IRON: random.randint(30, 150),
                ResourceType.FUEL: random.randint(20, 100)
            }
            self.life_forms = ['Flora', 'Fauna', 'Microbes']
            self.hazards = ['Storms', 'Predators'] if random.random() < 0.3 else []
        elif self.planet_type == PlanetType.DESERT:
            self.resources = {
                ResourceType.IRON: random.randint(100, 300),
                ResourceType.PLATINUM: random.randint(10, 50)
            }
            self.hazards = ['Heat', 'Sandstorms']
        elif self.planet_type == PlanetType.ICE:
            self.resources = {
                ResourceType.FUEL: random.randint(50, 200),
                ResourceType.QUANTUM_CRYSTAL: random.randint(5, 30)
            }
            self.hazards = ['Extreme Cold', 'Ice Storms']
        elif self.planet_type == PlanetType.LAVA:
            self.resources = {
                ResourceType.IRON: random.randint(200, 500),
                ResourceType.EXOTIC_MATTER: random.randint(10, 40)
            }
            self.hazards = ['Lava', 'Extreme Heat', 'Volcanic Activity']
        elif self.planet_type == PlanetType.FOREST:
            self.resources = {
                ResourceType.CARBON: random.randint(100, 400),
                ResourceType.FUEL: random.randint(30, 150)
            }
            self.life_forms = ['Dense Flora', 'Complex Fauna']
            self.hazards = ['Hostile Wildlife'] if random.random() < 0.4 else []
        elif self.planet_type == PlanetType.TOXIC:
            self.resources = {
                ResourceType.EXOTIC_MATTER: random.randint(20, 100),
                ResourceType.QUANTUM_CRYSTAL: random.randint(15, 60)
            }
            self.hazards = ['Toxic Atmosphere', 'Acid Rain', 'Toxic Life Forms']
        
        # Generate points of interest
        for _ in range(random.randint(1, 5)):
            poi = {
                'type': random.choice(['Ruins', 'Cave System', 'Resource Deposit', 'Alien Structure', 'Crash Site']),
                'x': random.randint(0, 400),
                'y': random.randint(0, 300),
                'resources': random.randint(10, 100),
                'danger_level': random.randint(1, 5)
            }
            self.points_of_interest.append(poi)
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get planet color based on type"""
        color_map = {
            PlanetType.EARTH_LIKE: SPACE_COLORS['planet_earth'],
            PlanetType.DESERT: SPACE_COLORS['planet_desert'],
            PlanetType.ICE: SPACE_COLORS['planet_ice'],
            PlanetType.LAVA: SPACE_COLORS['planet_lava'],
            PlanetType.FOREST: SPACE_COLORS['planet_forest'],
            PlanetType.TOXIC: SPACE_COLORS['planet_toxic'],
            PlanetType.OCEAN: SPACE_COLORS['planet_earth'],
            PlanetType.BARREN: (100, 100, 100)
        }
        return color_map.get(self.planet_type, (150, 150, 150))
    
    def is_habitable(self) -> bool:
        """Check if planet is habitable"""
        return (self.planet_type in [PlanetType.EARTH_LIKE, PlanetType.FOREST] and
                -20 <= self.temperature <= 50 and
                self.atmosphere in ['Thin', 'Dense'] and
                0.5 <= self.gravity <= 2.0)

@dataclass
class AlienSpecies:
    """Alien species with unique characteristics"""
    name: str
    race: AlienRace
    disposition: str  # Friendly, Neutral, Hostile, Mysterious
    technology_level: int
    trade_goods: List[ResourceType]
    preferred_resources: List[ResourceType]
    territory: List[str]  # System names they control
    
    def __init__(self, name: str):
        self.name = name
        self.race = random.choice(list(AlienRace))
        self.disposition = random.choice(['Friendly', 'Neutral', 'Hostile', 'Mysterious'])
        self.technology_level = random.randint(1, 10)
        self.trade_goods = random.sample(list(ResourceType), random.randint(2, 4))
        self.preferred_resources = random.sample(list(ResourceType), random.randint(1, 3))
        self.territory = []
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get alien species color"""
        if self.race == AlienRace.HUMANOID:
            return SPACE_COLORS['alien_green']
        elif self.race == AlienRace.INSECTOID:
            return SPACE_COLORS['alien_orange']
        elif self.race == AlienRace.CRYSTALLINE:
            return SPACE_COLORS['alien_purple']
        elif self.race == AlienRace.ENERGY_BEING:
            return NEON_CYAN
        else:  # MECHANICAL
            return (150, 150, 150)
    
    def get_trade_modifier(self) -> float:
        """Get trade price modifier"""
        if self.disposition == 'Friendly':
            return 0.8  # 20% discount
        elif self.disposition == 'Hostile':
            return 1.5  # 50% markup
        elif self.disposition == 'Mysterious':
            return random.uniform(0.5, 2.0)  # Random pricing
        else:  # Neutral
            return 1.0

@dataclass
class StarSystem:
    """Star system with planets and stations"""
    name: str
    star_type: str
    star_color: Tuple[int, int, int]
    x: float
    y: float
    planets: List[Planet]
    space_stations: List[Dict[str, Any]]
    alien_presence: Optional[AlienSpecies]
    asteroid_fields: List[Dict[str, Any]]
    
    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.star_type = random.choice(['G-class', 'K-class', 'M-class', 'F-class', 'A-class'])
        self.x = x
        self.y = y
        self.planets = []
        self.space_stations = []
        self.alien_presence = None
        self.asteroid_fields = []
        
        # Star color based on type
        star_colors = {
            'G-class': SPACE_COLORS['star_yellow'],
            'K-class': SPACE_COLORS['star_red'],
            'M-class': (255, 100, 100),
            'F-class': (255, 255, 200),
            'A-class': SPACE_COLORS['star_blue']
        }
        self.star_color = star_colors.get(self.star_type, SPACE_COLORS['star_yellow'])
        
        self.generate_system()
    
    def generate_system(self):
        """Generate system contents"""
        # Generate planets
        num_planets = random.randint(1, 8)
        for i in range(num_planets):
            planet_name = f"{self.name} {chr(ord('A') + i)}"
            planet = Planet(planet_name)
            self.planets.append(planet)
        
        # Generate space stations
        if random.random() < 0.3:  # 30% chance of space station
            station = {
                'name': f"{self.name} Station",
                'type': random.choice(['Trading Post', 'Research Station', 'Military Base', 'Refinery']),
                'services': random.sample(['Fuel', 'Repairs', 'Trading', 'Upgrades'], random.randint(2, 4)),
                'x': random.randint(100, 380),
                'y': random.randint(100, 220)
            }
            self.space_stations.append(station)
        
        # Generate asteroid fields
        if random.random() < 0.4:  # 40% chance of asteroid field
            field = {
                'name': f"{self.name} Asteroid Field",
                'x': random.randint(50, 430),
                'y': random.randint(50, 270),
                'size': random.randint(20, 80),
                'resources': {
                    ResourceType.IRON: random.randint(50, 200),
                    ResourceType.PLATINUM: random.randint(10, 50)
                },
                'danger_level': random.randint(1, 5)
            }
            self.asteroid_fields.append(field)
        
        # Alien presence
        if random.random() < 0.2:  # 20% chance of alien presence
            alien_names = ['Zorblaxians', 'Crystallites', 'Voidwalkers', 'Technomancers', 'Starhunters']
            alien_name = random.choice(alien_names)
            self.alien_presence = AlienSpecies(alien_name)
            self.alien_presence.territory.append(self.name)

class SpaceExplorationGame:
    """Main game class managing all systems"""
    def __init__(self):
        self.game_state = GameState.SPACE_FLIGHT
        self.player_ship = Ship("Nomad")
        self.current_system = None
        self.current_planet = None
        self.galaxy_map = {}
        self.alien_species = {}
        self.discovered_systems = set()
        self.visited_planets = set()
        
        # Player stats
        self.player_credits = 1000
        self.player_reputation = {}  # alien_species -> reputation
        self.exploration_rank = 'Rookie'
        self.combat_rank = 'Harmless'
        self.trade_rank = 'Peddler'
        
        # Camera and view
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1.0
        self.selected_object = None
        
        # UI state
        self.show_hud = True
        self.show_scanner = True
        self.show_system_info = True
        self.scanner_range = 200
        
        # Game time
        self.game_time = 0
        self.day_cycle = 0.0
        
        # Performance settings
        self.star_density = 100
        self.update_frequency = 60
        
        # Initialize galaxy
        self.initialize_galaxy()
        
        # Set starting system
        self.current_system = list(self.galaxy_map.values())[0]
        self.player_ship.cargo[ResourceType.CREDITS] = 1000
    
    def initialize_galaxy(self):
        """Initialize the galaxy with star systems"""
        # Create a small galaxy for Pi 5 performance
        system_names = [
            'Alpha Centauri', 'Proxima', 'Barnard', 'Wolf 359', 'Lalande',
            'Sirius', 'Vega', 'Arcturus', 'Capella', 'Rigel',
            'Betelgeuse', 'Aldebaran', 'Antares', 'Spica', 'Pollux',
            'Fomalhaut', 'Deneb', 'Regulus', 'Adhara', 'Castor'
        ]
        
        for i, name in enumerate(system_names):
            # Arrange systems in a rough grid
            x = (i % 5) * 200 + random.randint(-50, 50)
            y = (i // 5) * 150 + random.randint(-30, 30)
            
            system = StarSystem(name, x, y)
            self.galaxy_map[name] = system
        
        # Create alien species
        alien_names = ['Zorblaxians', 'Crystallites', 'Voidwalkers', 'Technomancers', 'Starhunters']
        for name in alien_names:
            alien = AlienSpecies(name)
            self.alien_species[name] = alien
            
            # Assign territory
            available_systems = [s for s in self.galaxy_map.values() if s.alien_presence is None]
            if available_systems:
                territory_size = random.randint(1, 3)
                for _ in range(territory_size):
                    if available_systems:
                        system = random.choice(available_systems)
                        system.alien_presence = alien
                        alien.territory.append(system.name)
                        available_systems.remove(system)
    
    def update_game(self):
        """Update game state"""
        self.game_time += 1
        self.day_cycle = (self.game_time * 0.01) % 1.0
        
        # Update ship systems
        self.update_ship_systems()
        
        # Update current system
        if self.current_system:
            self.update_system_dynamics()
        
        # Update alien relationships
        self.update_alien_relations()
    
    def update_ship_systems(self):
        """Update ship systems and consumption"""
        # Fuel consumption
        if self.game_state == GameState.SPACE_FLIGHT:
            self.player_ship.fuel -= 0.01
        
        # Shield regeneration
        if self.player_ship.shields < self.player_ship.max_shields:
            self.player_ship.shields += 0.1
            self.player_ship.shields = min(self.player_ship.shields, self.player_ship.max_shields)
        
        # Life support
        if self.player_ship.life_support < 100:
            self.player_ship.life_support += 0.05
            self.player_ship.life_support = min(self.player_ship.life_support, 100)
        
        # Emergency situations
        if self.player_ship.fuel <= 0:
            self.handle_emergency('fuel_depleted')
        if self.player_ship.hull_integrity <= 0:
            self.handle_emergency('hull_breach')
    
    def update_system_dynamics(self):
        """Update dynamic elements in current system"""
        # Update planetary conditions
        for planet in self.current_system.planets:
            # Seasonal changes, weather, etc.
            pass
        
        # Update alien patrols
        if self.current_system.alien_presence:
            # Alien ship movements, etc.
            pass
    
    def update_alien_relations(self):
        """Update relationships with alien species"""
        for alien_name, alien in self.alien_species.items():
            if alien_name in self.player_reputation:
                # Reputation decay over time
                if self.player_reputation[alien_name] > 0:
                    self.player_reputation[alien_name] -= 0.001
                elif self.player_reputation[alien_name] < 0:
                    self.player_reputation[alien_name] += 0.001
            else:
                self.player_reputation[alien_name] = 0
    
    def handle_emergency(self, emergency_type: str):
        """Handle emergency situations"""
        if emergency_type == 'fuel_depleted':
            # Emergency fuel rationing
            self.player_ship.fuel = 1
        elif emergency_type == 'hull_breach':
            # Emergency repairs
            self.player_ship.hull_integrity = 1
            self.player_ship.life_support -= 20
    
    def land_on_planet(self, planet: Planet):
        """Land on a planet"""
        if self.player_ship.fuel >= 5:  # Landing requires fuel
            self.game_state = GameState.PLANET_SURFACE
            self.current_planet = planet
            self.player_ship.fuel -= 5
            self.visited_planets.add(planet.name)
            return True
        return False
    
    def take_off_from_planet(self):
        """Take off from planet"""
        if self.player_ship.fuel >= 10:  # Takeoff requires more fuel
            self.game_state = GameState.SPACE_FLIGHT
            self.current_planet = None
            self.player_ship.fuel -= 10
            return True
        return False
    
    def dock_at_station(self, station: Dict[str, Any]):
        """Dock at a space station"""
        self.game_state = GameState.STATION_DOCKED
        self.selected_object = station
        return True
    
    def undock_from_station(self):
        """Undock from station"""
        self.game_state = GameState.SPACE_FLIGHT
        self.selected_object = None
        return True
    
    def hyperjump_to_system(self, system_name: str):
        """Jump to another star system"""
        if system_name in self.galaxy_map:
            target_system = self.galaxy_map[system_name]
            distance = math.sqrt((target_system.x - self.current_system.x)**2 + 
                               (target_system.y - self.current_system.y)**2)
            
            fuel_cost = distance * 0.1 * (1.0 / self.player_ship.hyperdrive_class)
            
            if self.player_ship.fuel >= fuel_cost:
                self.current_system = target_system
                self.player_ship.fuel -= fuel_cost
                self.discovered_systems.add(system_name)
                return True
        return False
    
    def mine_resources(self, location: Dict[str, Any]):
        """Mine resources from asteroids or planets"""
        if 'resources' in location:
            mined = {}
            for resource, amount in location['resources'].items():
                if amount > 0:
                    mine_amount = min(amount, random.randint(1, 10))
                    if self.player_ship.can_add_cargo(resource, mine_amount):
                        self.player_ship.add_cargo(resource, mine_amount)
                        location['resources'][resource] -= mine_amount
                        mined[resource] = mine_amount
            return mined
        return {}
    
    def trade_with_alien(self, alien: AlienSpecies, offer: Dict[ResourceType, int], 
                        request: Dict[ResourceType, int]) -> bool:
        """Trade resources with alien species"""
        # Check if player has offered resources
        for resource, amount in offer.items():
            if self.player_ship.cargo[resource] < amount:
                return False
        
        # Check if alien wants the offered resources
        wants_trade = any(resource in alien.preferred_resources for resource in offer.keys())
        
        if wants_trade:
            # Remove offered resources from player
            for resource, amount in offer.items():
                self.player_ship.remove_cargo(resource, amount)
            
            # Add requested resources to player
            for resource, amount in request.items():
                self.player_ship.add_cargo(resource, amount)
            
            # Improve reputation
            self.player_reputation[alien.name] += 5
            return True
        
        return False
    
    def start_alien_encounter(self, alien: AlienSpecies):
        """Start an encounter with aliens"""
        self.game_state = GameState.ALIEN_ENCOUNTER
        self.selected_object = alien
    
    def end_alien_encounter(self):
        """End alien encounter"""
        self.game_state = GameState.SPACE_FLIGHT
        self.selected_object = None
    
    def upgrade_ship(self, upgrade_type: str, cost: int):
        """Upgrade ship systems"""
        if self.player_ship.cargo[ResourceType.CREDITS] >= cost:
            self.player_ship.remove_cargo(ResourceType.CREDITS, cost)
            self.player_ship.apply_upgrade(upgrade_type)
            return True
        return False
    
    def draw_space_view(self, surface):
        """Draw the space flight view"""
        # Background
        surface.fill(SPACE_COLORS['deep_space'])
        
        # Draw stars
        for i in range(self.star_density):
            x = (i * 37) % WIDTH
            y = (i * 73) % HEIGHT
            brightness = (i * 17) % 255
            color = (brightness, brightness, brightness)
            pygame.draw.circle(surface, color, (x, y), 1)
        
        # Draw current system star
        if self.current_system:
            star_x = WIDTH // 2
            star_y = HEIGHT // 2
            star_size = 8
            pygame.draw.circle(surface, self.current_system.star_color, (star_x, star_y), star_size)
            
            # Draw system name
            font = pygame.font.Font(None, 24)
            text = font.render(self.current_system.name, True, NEON_CYAN)
            surface.blit(text, (star_x - text.get_width()//2, star_y - 40))
        
        # Draw planets
        if self.current_system:
            for i, planet in enumerate(self.current_system.planets):
                angle = (self.game_time * 0.01 + i * 0.5) % (2 * math.pi)
                orbit_radius = 50 + i * 25
                planet_x = WIDTH // 2 + math.cos(angle) * orbit_radius
                planet_y = HEIGHT // 2 + math.sin(angle) * orbit_radius
                
                planet_size = int(planet.size * 3)
                pygame.draw.circle(surface, planet.get_color(), (int(planet_x), int(planet_y)), planet_size)
                
                # Planet name
                if self.show_system_info:
                    font = pygame.font.Font(None, 16)
                    text = font.render(planet.name, True, NEON_GREEN)
                    surface.blit(text, (int(planet_x) - text.get_width()//2, int(planet_y) + planet_size + 5))
        
        # Draw space stations
        if self.current_system:
            for station in self.current_system.space_stations:
                station_x = station['x']
                station_y = station['y']
                pygame.draw.rect(surface, SPACE_COLORS['ship_hull'], (station_x, station_y, 12, 8))
                
                # Station name
                if self.show_system_info:
                    font = pygame.font.Font(None, 14)
                    text = font.render(station['name'], True, NEON_YELLOW)
                    surface.blit(text, (station_x, station_y - 15))
        
        # Draw asteroid fields
        if self.current_system:
            for field in self.current_system.asteroid_fields:
                field_x = field['x']
                field_y = field['y']
                field_size = field['size']
                
                # Draw multiple asteroids
                for i in range(field_size // 10):
                    ast_x = field_x + random.randint(-field_size//2, field_size//2)
                    ast_y = field_y + random.randint(-field_size//2, field_size//2)
                    pygame.draw.circle(surface, SPACE_COLORS['asteroid'], (ast_x, ast_y), 2)
        
        # Draw player ship
        ship_x = WIDTH // 2
        ship_y = HEIGHT // 2 + 100
        pygame.draw.polygon(surface, SPACE_COLORS['ship_hull'], 
                          [(ship_x, ship_y-5), (ship_x-8, ship_y+5), (ship_x+8, ship_y+5)])
        
        # Ship trail
        for i in range(5):
            trail_x = ship_x + random.randint(-2, 2)
            trail_y = ship_y + 8 + i * 2
            trail_alpha = 255 - i * 50
            pygame.draw.circle(surface, (100, 150, 255), (trail_x, trail_y), 1)
    
    def draw_planet_surface(self, surface):
        """Draw planet surface exploration view"""
        if not self.current_planet:
            return
        
        # Background based on planet type
        bg_color = self.current_planet.get_color()
        surface.fill(bg_color)
        
        # Draw terrain features
        for i in range(50):
            x = (i * 47) % WIDTH
            y = (i * 83) % HEIGHT
            feature_color = tuple(max(0, min(255, c + random.randint(-30, 30))) for c in bg_color)
            pygame.draw.circle(surface, feature_color, (x, y), random.randint(2, 8))
        
        # Draw points of interest
        for poi in self.current_planet.points_of_interest:
            poi_x = poi['x']
            poi_y = poi['y']
            
            # Different symbols for different POI types
            if poi['type'] == 'Ruins':
                pygame.draw.rect(surface, NEON_PURPLE, (poi_x, poi_y, 8, 8))
            elif poi['type'] == 'Resource Deposit':
                pygame.draw.circle(surface, NEON_YELLOW, (poi_x, poi_y), 6)
            elif poi['type'] == 'Alien Structure':
                pygame.draw.polygon(surface, NEON_RED, 
                                  [(poi_x, poi_y-6), (poi_x-6, poi_y+6), (poi_x+6, poi_y+6)])
            else:
                pygame.draw.circle(surface, NEON_GREEN, (poi_x, poi_y), 4)
        
        # Draw player character
        player_x = WIDTH // 2
        player_y = HEIGHT // 2
        pygame.draw.circle(surface, NEON_CYAN, (player_x, player_y), 5)
        
        # Draw life support indicator
        life_support_bar = pygame.Rect(10, HEIGHT - 30, 100, 10)
        pygame.draw.rect(surface, NEON_RED, life_support_bar)
        life_support_fill = pygame.Rect(10, HEIGHT - 30, int(self.player_ship.life_support), 10)
        pygame.draw.rect(surface, NEON_GREEN, life_support_fill)
        
        # Planet info
        font = pygame.font.Font(None, 24)
        planet_name = font.render(self.current_planet.name, True, NEON_CYAN)
        surface.blit(planet_name, (10, 10))
        
        font = pygame.font.Font(None, 16)
        planet_type = font.render(f"Type: {self.current_planet.planet_type.name}", True, NEON_GREEN)
        surface.blit(planet_type, (10, 35))
        
        temp_text = font.render(f"Temperature: {self.current_planet.temperature:.1f}°C", True, NEON_YELLOW)
        surface.blit(temp_text, (10, 55))
    
    def draw_hud(self, surface):
        """Draw heads-up display"""
        if not self.show_hud:
            return
        
        # HUD background
        hud_rect = pygame.Rect(0, 0, WIDTH, 50)
        pygame.draw.rect(surface, (0, 0, 0, 180), hud_rect)
        
        # Ship status
        font = pygame.font.Font(None, 16)
        
        # Hull integrity
        hull_text = f"Hull: {self.player_ship.hull_integrity:.0f}/{self.player_ship.max_hull:.0f}"
        text = font.render(hull_text, True, NEON_GREEN if self.player_ship.hull_integrity > 50 else NEON_RED)
        surface.blit(text, (10, 10))
        
        # Shields
        shield_text = f"Shields: {self.player_ship.shields:.0f}/{self.player_ship.max_shields:.0f}"
        text = font.render(shield_text, True, NEON_BLUE)
        surface.blit(text, (10, 25))
        
        # Fuel
        fuel_text = f"Fuel: {self.player_ship.fuel:.0f}/{self.player_ship.max_fuel:.0f}"
        text = font.render(fuel_text, True, NEON_YELLOW if self.player_ship.fuel > 25 else NEON_RED)
        surface.blit(text, (150, 10))
        
        # Credits
        credits_text = f"Credits: {self.player_ship.cargo[ResourceType.CREDITS]}"
        text = font.render(credits_text, True, NEON_GREEN)
        surface.blit(text, (150, 25))
        
        # Cargo
        cargo_used = self.player_ship.get_cargo_used()
        cargo_text = f"Cargo: {cargo_used}/{self.player_ship.cargo_capacity}"
        text = font.render(cargo_text, True, NEON_CYAN)
        surface.blit(text, (300, 10))
        
        # Game state
        state_text = self.game_state.name.replace('_', ' ').title()
        text = font.render(state_text, True, NEON_PURPLE)
        surface.blit(text, (300, 25))
    
    def draw_scanner(self, surface):
        """Draw scanner display"""
        if not self.show_scanner:
            return
        
        # Scanner background
        scanner_rect = pygame.Rect(WIDTH - 120, 60, 110, 110)
        pygame.draw.rect(surface, (0, 0, 0, 180), scanner_rect)
        pygame.draw.rect(surface, NEON_GREEN, scanner_rect, 2)
        
        # Scanner grid
        for i in range(5):
            x = WIDTH - 120 + i * 22
            y = 60 + i * 22
            pygame.draw.line(surface, (0, 100, 0), (x, 60), (x, 170), 1)
            pygame.draw.line(surface, (0, 100, 0), (WIDTH - 120, y), (WIDTH - 10, y), 1)
        
        # Scanner center (player position)
        center_x = WIDTH - 65
        center_y = 115
        pygame.draw.circle(surface, NEON_CYAN, (center_x, center_y), 3)
        
        # Scanner objects
        if self.current_system:
            for i, planet in enumerate(self.current_system.planets):
                angle = (self.game_time * 0.01 + i * 0.5) % (2 * math.pi)
                orbit_radius = 10 + i * 8
                if orbit_radius < 50:  # Within scanner range
                    planet_x = center_x + math.cos(angle) * orbit_radius
                    planet_y = center_y + math.sin(angle) * orbit_radius
                    pygame.draw.circle(surface, planet.get_color(), (int(planet_x), int(planet_y)), 2)
    
    def draw_controls(self, surface):
        """Draw control instructions"""
        if self.game_state == GameState.SPACE_FLIGHT:
            controls = [
                "WASD - Navigate",
                "E - Land on Planet",
                "Q - Dock at Station",
                "M - Galaxy Map",
                "T - Trade Mode",
                "U - Upgrade Ship",
                "F8 - Fullscreen",
                "ESC - Return to Launcher"
            ]
        elif self.game_state == GameState.PLANET_SURFACE:
            controls = [
                "WASD - Move",
                "E - Interact/Mine",
                "R - Take Off",
                "ESC - Return to Launcher"
            ]
        else:
            controls = [
                "ESC - Return to Space",
                "Enter - Confirm",
                "Tab - Next Option"
            ]
        
        # Controls background
        controls_rect = pygame.Rect(10, HEIGHT - 120, 200, 110)
        pygame.draw.rect(surface, (0, 0, 0, 180), controls_rect)
        
        font = pygame.font.Font(None, 14)
        for i, control in enumerate(controls):
            text = font.render(control, True, NEON_YELLOW)
            surface.blit(text, (15, HEIGHT - 115 + i * 12))
    
    def handle_input(self, keys, events):
        """Handle user input"""
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.handle_interact()
                elif event.key == pygame.K_q:
                    self.handle_dock()
                elif event.key == pygame.K_r:
                    self.handle_takeoff()
                elif event.key == pygame.K_m:
                    self.toggle_galaxy_map()
                elif event.key == pygame.K_t:
                    self.enter_trading_mode()
                elif event.key == pygame.K_u:
                    self.enter_upgrade_mode()
                elif event.key == pygame.K_h:
                    self.show_hud = not self.show_hud
                elif event.key == pygame.K_n:
                    self.show_scanner = not self.show_scanner
                elif event.key == pygame.K_i:
                    self.show_system_info = not self.show_system_info
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_mouse_click(event.pos)
        
        # Continuous input
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.camera_y += 2
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.camera_y -= 2
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.camera_x += 2
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.camera_x -= 2
    
    def handle_interact(self):
        """Handle interaction based on current state"""
        if self.game_state == GameState.SPACE_FLIGHT:
            # Try to land on nearest planet
            if self.current_system and self.current_system.planets:
                nearest_planet = self.current_system.planets[0]  # Simplified
                self.land_on_planet(nearest_planet)
        elif self.game_state == GameState.PLANET_SURFACE:
            # Try to mine/interact with nearest POI
            if self.current_planet and self.current_planet.points_of_interest:
                poi = self.current_planet.points_of_interest[0]  # Simplified
                self.mine_resources(poi)
    
    def handle_dock(self):
        """Handle docking with stations"""
        if self.game_state == GameState.SPACE_FLIGHT:
            if self.current_system and self.current_system.space_stations:
                station = self.current_system.space_stations[0]  # Simplified
                self.dock_at_station(station)
        elif self.game_state == GameState.STATION_DOCKED:
            self.undock_from_station()
    
    def handle_takeoff(self):
        """Handle taking off from planet"""
        if self.game_state == GameState.PLANET_SURFACE:
            self.take_off_from_planet()
    
    def toggle_galaxy_map(self):
        """Toggle galaxy map view"""
        if self.game_state == GameState.GALAXY_MAP:
            self.game_state = GameState.SPACE_FLIGHT
        else:
            self.game_state = GameState.GALAXY_MAP
    
    def enter_trading_mode(self):
        """Enter trading mode"""
        self.game_state = GameState.TRADING
    
    def enter_upgrade_mode(self):
        """Enter ship upgrade mode"""
        self.game_state = GameState.SHIP_UPGRADE
    
    def handle_mouse_click(self, pos):
        """Handle mouse clicks for selection"""
        # Implementation depends on current state
        pass

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
    game = SpaceExplorationGame()
    
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
        
        # Update game
        game.update_game()
        
        # Clear screen
        screen.fill(CYBER_BLACK)
        
        # Draw based on game state
        if game.game_state == GameState.SPACE_FLIGHT:
            game.draw_space_view(screen)
        elif game.game_state == GameState.PLANET_SURFACE:
            game.draw_planet_surface(screen)
        elif game.game_state == GameState.GALAXY_MAP:
            # Draw galaxy map (simplified)
            game.draw_space_view(screen)
        
        # Draw UI
        game.draw_hud(screen)
        game.draw_scanner(screen)
        game.draw_controls(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS for smooth experience
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 