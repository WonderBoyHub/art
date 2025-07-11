#!/usr/bin/env python3
"""
Advanced Fire & Combustion Simulator - Realistic fire physics simulation
Perfect for Raspberry Pi 5 with 3.5" display (480x320)
COMPLETE FIRE PHYSICS WITH FUEL MANAGEMENT AND SPREAD MECHANICS
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
pygame.display.set_caption("Advanced Fire & Combustion Simulator")

# Fullscreen support
fullscreen = False
clock = pygame.time.Clock()
start_time = time.time()

# Enhanced fire color palette
CYBER_BLACK = (10, 10, 15)
NEON_BLUE = (50, 150, 255)
NEON_GREEN = (50, 255, 150)
NEON_CYAN = (50, 255, 255)
NEON_YELLOW = (255, 255, 50)
NEON_RED = (255, 50, 50)
NEON_ORANGE = (255, 150, 50)
FIRE_COLORS = {
    'blue_flame': (100, 150, 255),
    'white_hot': (255, 255, 255),
    'yellow_flame': (255, 255, 100),
    'orange_flame': (255, 150, 50),
    'red_flame': (255, 50, 50),
    'ember': (255, 100, 0),
    'smoke': (100, 100, 100),
    'ash': (80, 80, 80),
    'fuel': (139, 69, 19),
    'oxygen': (200, 220, 255),
    'water': (100, 150, 255)
}

class FuelType(Enum):
    WOOD = 0
    PAPER = 1
    GASOLINE = 2
    PROPANE = 3
    ALCOHOL = 4
    COAL = 5
    OIL = 6

class FireState(Enum):
    COLD = 0
    HEATING = 1
    IGNITION = 2
    BURNING = 3
    EXTINGUISHING = 4
    EXTINGUISHED = 5

class SimulationMode(Enum):
    SANDBOX = 0
    FIREFIGHTING = 1
    FOREST_FIRE = 2
    CHEMISTRY_LAB = 3
    INDUSTRIAL = 4

@dataclass
class FuelProperties:
    """Properties of different fuel types"""
    ignition_temp: float
    burn_rate: float
    heat_output: float
    oxygen_consumption: float
    smoke_production: float
    color: Tuple[int, int, int]
    volatility: float
    
    @staticmethod
    def get_properties(fuel_type: FuelType) -> 'FuelProperties':
        properties = {
            FuelType.WOOD: FuelProperties(300, 0.3, 18.0, 0.2, 0.4, (139, 69, 19), 0.1),
            FuelType.PAPER: FuelProperties(230, 0.8, 16.0, 0.3, 0.3, (255, 248, 220), 0.4),
            FuelType.GASOLINE: FuelProperties(280, 1.5, 44.0, 0.5, 0.6, (255, 182, 193), 0.9),
            FuelType.PROPANE: FuelProperties(470, 2.0, 50.0, 0.6, 0.1, (200, 200, 255), 0.8),
            FuelType.ALCOHOL: FuelProperties(365, 1.2, 30.0, 0.4, 0.2, (240, 248, 255), 0.6),
            FuelType.COAL: FuelProperties(400, 0.2, 25.0, 0.3, 0.8, (64, 64, 64), 0.05),
            FuelType.OIL: FuelProperties(250, 0.7, 42.0, 0.4, 0.9, (139, 90, 43), 0.3)
        }
        return properties[fuel_type]

class FireCell:
    """Individual cell in the fire simulation grid"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.temperature = 20.0  # Celsius
        self.fuel_amount = 0.0
        self.fuel_type = FuelType.WOOD
        self.oxygen_level = 21.0  # Percentage
        self.humidity = 50.0  # Percentage
        self.state = FireState.COLD
        self.heat_energy = 0.0
        self.burn_time = 0.0
        self.smoke_density = 0.0
        self.wind_velocity_x = 0.0
        self.wind_velocity_y = 0.0
        self.pressure = 1013.25  # mbar
        self.contains_water = False
        self.water_amount = 0.0
        
    def can_ignite(self) -> bool:
        """Check if cell can ignite"""
        fuel_props = FuelProperties.get_properties(self.fuel_type)
        return (self.fuel_amount > 0 and 
                self.temperature >= fuel_props.ignition_temp and
                self.oxygen_level > 10.0 and
                not self.contains_water)
    
    def get_burn_rate(self) -> float:
        """Calculate burn rate based on conditions"""
        if self.state != FireState.BURNING:
            return 0.0
        
        fuel_props = FuelProperties.get_properties(self.fuel_type)
        
        # Base burn rate
        rate = fuel_props.burn_rate
        
        # Oxygen effect
        oxygen_factor = min(1.0, self.oxygen_level / 21.0)
        rate *= oxygen_factor
        
        # Temperature effect
        temp_factor = min(2.0, self.temperature / fuel_props.ignition_temp)
        rate *= temp_factor
        
        # Humidity effect
        humidity_factor = max(0.1, 1.0 - self.humidity / 200.0)
        rate *= humidity_factor
        
        # Wind effect (increases burn rate)
        wind_speed = math.sqrt(self.wind_velocity_x**2 + self.wind_velocity_y**2)
        wind_factor = 1.0 + wind_speed * 0.1
        rate *= wind_factor
        
        # Water suppression
        if self.contains_water:
            rate *= max(0.0, 1.0 - self.water_amount)
        
        return rate
    
    def update_combustion(self, dt: float):
        """Update combustion physics"""
        if self.state == FireState.BURNING:
            burn_rate = self.get_burn_rate()
            fuel_props = FuelProperties.get_properties(self.fuel_type)
            
            # Consume fuel
            fuel_consumed = burn_rate * dt
            self.fuel_amount = max(0, self.fuel_amount - fuel_consumed)
            
            # Generate heat
            heat_generated = fuel_consumed * fuel_props.heat_output
            self.heat_energy += heat_generated
            self.temperature += heat_generated * 0.1
            
            # Consume oxygen
            oxygen_consumed = fuel_consumed * fuel_props.oxygen_consumption
            self.oxygen_level = max(0, self.oxygen_level - oxygen_consumed)
            
            # Produce smoke
            smoke_produced = fuel_consumed * fuel_props.smoke_production
            self.smoke_density = min(100, self.smoke_density + smoke_produced)
            
            # Increase burn time
            self.burn_time += dt
            
            # Check for extinguishment
            if self.fuel_amount <= 0 or self.oxygen_level <= 5.0:
                self.state = FireState.EXTINGUISHED
                self.temperature = max(20, self.temperature - 50)
        
        # Heat dissipation
        if self.temperature > 20:
            cooling_rate = (self.temperature - 20) * 0.02 * dt
            self.temperature -= cooling_rate
            self.heat_energy *= 0.99
        
        # Smoke dissipation
        if self.smoke_density > 0:
            dissipation = self.smoke_density * 0.01 * dt
            self.smoke_density = max(0, self.smoke_density - dissipation)
        
        # Water evaporation
        if self.contains_water and self.temperature > 100:
            evaporation = min(self.water_amount, 0.1 * dt)
            self.water_amount -= evaporation
            self.temperature -= evaporation * 10  # Cooling effect
            if self.water_amount <= 0:
                self.contains_water = False
    
    def get_display_color(self) -> Tuple[int, int, int]:
        """Get color for display based on state"""
        if self.state == FireState.BURNING:
            # Temperature-based fire colors
            if self.temperature > 1200:
                return FIRE_COLORS['white_hot']
            elif self.temperature > 1000:
                return FIRE_COLORS['blue_flame']
            elif self.temperature > 800:
                return FIRE_COLORS['yellow_flame']
            elif self.temperature > 600:
                return FIRE_COLORS['orange_flame']
            else:
                return FIRE_COLORS['red_flame']
        elif self.fuel_amount > 0:
            fuel_props = FuelProperties.get_properties(self.fuel_type)
            return fuel_props.color
        elif self.smoke_density > 10:
            intensity = min(255, int(self.smoke_density * 2.55))
            return (intensity, intensity, intensity)
        elif self.contains_water:
            return FIRE_COLORS['water']
        else:
            # Temperature visualization for cold areas
            temp_intensity = min(255, max(0, int((self.temperature - 20) * 5)))
            return (temp_intensity, 0, 0)

class FireSpreadManager:
    """Manages fire spread between cells"""
    def __init__(self, grid_width: int, grid_height: int):
        self.grid_width = grid_width
        self.grid_height = grid_height
    
    def spread_fire(self, grid: List[List[FireCell]], dt: float):
        """Spread fire to adjacent cells"""
        spread_events = []
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell = grid[y][x]
                
                if cell.state == FireState.BURNING:
                    # Check all 8 neighbors
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            if dx == 0 and dy == 0:
                                continue
                            
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                                neighbor = grid[ny][nx]
                                
                                if neighbor.can_ignite():
                                    # Calculate spread probability
                                    distance = math.sqrt(dx*dx + dy*dy)
                                    heat_transfer = cell.heat_energy / (distance * 100)
                                    
                                    # Wind effect on spread
                                    wind_effect = 1.0
                                    if cell.wind_velocity_x != 0 or cell.wind_velocity_y != 0:
                                        wind_direction = math.atan2(cell.wind_velocity_y, cell.wind_velocity_x)
                                        spread_direction = math.atan2(dy, dx)
                                        angle_diff = abs(wind_direction - spread_direction)
                                        wind_effect = 1.0 + math.cos(angle_diff) * 0.5
                                    
                                    spread_probability = heat_transfer * wind_effect * dt * 0.1
                                    
                                    if random.random() < spread_probability:
                                        spread_events.append((nx, ny))
        
        # Apply spread events
        for x, y in spread_events:
            grid[y][x].state = FireState.IGNITION
            grid[y][x].temperature += 100

class WeatherType(Enum):
    CLEAR = 0
    RAIN = 1
    SNOW = 2
    STORM = 3
    DROUGHT = 4
    HEATWAVE = 5

class FireScenario(Enum):
    WILDFIRE = 0
    HOUSE_FIRE = 1
    INDUSTRIAL = 2
    VEHICLE_FIRE = 3
    ELECTRICAL = 4
    CHEMICAL = 5

class HeatTransferMode(Enum):
    CONDUCTION = 0
    CONVECTION = 1
    RADIATION = 2

@dataclass
class WeatherConditions:
    """Advanced weather conditions"""
    weather_type: WeatherType
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: float
    precipitation: float
    visibility: float
    uv_index: float
    
    def get_fire_risk(self) -> float:
        """Calculate fire risk based on weather conditions"""
        risk = 0.0
        
        # Temperature effect
        if self.temperature > 30:
            risk += (self.temperature - 30) * 0.02
        
        # Humidity effect (lower humidity = higher risk)
        risk += (100 - self.humidity) * 0.01
        
        # Wind effect
        risk += self.wind_speed * 0.1
        
        # Precipitation reduces risk
        risk -= self.precipitation * 0.5
        
        # Weather type modifiers
        if self.weather_type == WeatherType.DROUGHT:
            risk *= 2.0
        elif self.weather_type == WeatherType.HEATWAVE:
            risk *= 1.5
        elif self.weather_type == WeatherType.RAIN:
            risk *= 0.3
        elif self.weather_type == WeatherType.STORM:
            risk *= 0.1
        
        return max(0.0, min(1.0, risk))

class SmokeParticle:
    """Individual smoke particle for realistic smoke simulation"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.velocity_x = random.uniform(-0.5, 0.5)
        self.velocity_y = random.uniform(-2.0, -0.5)
        self.life = 1.0
        self.size = random.uniform(1.0, 3.0)
        self.density = random.uniform(0.5, 1.0)
        self.temperature = random.uniform(100, 300)
    
    def update(self, dt: float, wind_x: float, wind_y: float):
        """Update smoke particle"""
        # Apply wind
        self.velocity_x += wind_x * 0.1
        self.velocity_y += wind_y * 0.1
        
        # Apply buoyancy (hot air rises)
        buoyancy = (self.temperature - 20) * 0.001
        self.velocity_y -= buoyancy
        
        # Update position
        self.x += self.velocity_x * dt * 60
        self.y += self.velocity_y * dt * 60
        
        # Age particle
        self.life -= dt * 0.5
        
        # Cool down
        self.temperature = max(20, self.temperature - dt * 50)
        
        # Expand as it cools
        self.size += dt * 0.5
        
        # Fade as it ages
        self.density *= 0.995
    
    def is_alive(self) -> bool:
        return self.life > 0 and self.density > 0.1

class FlameParticle:
    """Individual flame particle for realistic fire visualization"""
    def __init__(self, x: float, y: float, intensity: float):
        self.x = x
        self.y = y
        self.velocity_x = random.uniform(-0.2, 0.2)
        self.velocity_y = random.uniform(-1.0, -0.2)
        self.life = 1.0
        self.size = random.uniform(0.5, 2.0)
        self.intensity = intensity
        self.temperature = random.uniform(600, 1200)
    
    def update(self, dt: float, wind_x: float, wind_y: float):
        """Update flame particle"""
        # Apply wind
        self.velocity_x += wind_x * 0.05
        self.velocity_y += wind_y * 0.05
        
        # Natural flame motion (upward)
        self.velocity_y -= 0.5 * dt
        
        # Random flickering
        self.velocity_x += random.uniform(-0.1, 0.1)
        self.velocity_y += random.uniform(-0.1, 0.1)
        
        # Update position
        self.x += self.velocity_x * dt * 60
        self.y += self.velocity_y * dt * 60
        
        # Age particle
        self.life -= dt * 2.0
        
        # Cool down
        self.temperature = max(300, self.temperature - dt * 200)
        
        # Shrink as it ages
        self.size *= 0.99
    
    def is_alive(self) -> bool:
        return self.life > 0 and self.size > 0.1
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get color based on temperature"""
        if self.temperature > 1000:
            return (255, 255, 255)  # White hot
        elif self.temperature > 800:
            return (255, 255, 100)  # Yellow
        elif self.temperature > 600:
            return (255, 150, 50)   # Orange
        else:
            return (255, 50, 50)    # Red

class EmberParticle:
    """Flying ember particles that can spread fire"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.velocity_x = random.uniform(-2.0, 2.0)
        self.velocity_y = random.uniform(-3.0, -1.0)
        self.life = random.uniform(5.0, 15.0)
        self.size = random.uniform(0.5, 2.0)
        self.temperature = random.uniform(500, 800)
        self.ignition_potential = 0.3
    
    def update(self, dt: float, wind_x: float, wind_y: float):
        """Update ember particle"""
        # Apply wind (embers are strongly affected by wind)
        self.velocity_x += wind_x * 0.2
        self.velocity_y += wind_y * 0.2
        
        # Gravity
        self.velocity_y += 0.5 * dt
        
        # Update position
        self.x += self.velocity_x * dt * 60
        self.y += self.velocity_y * dt * 60
        
        # Age particle
        self.life -= dt
        
        # Cool down
        self.temperature = max(100, self.temperature - dt * 50)
        
        # Reduce ignition potential as it cools
        self.ignition_potential = max(0, self.ignition_potential - dt * 0.05)
    
    def is_alive(self) -> bool:
        return self.life > 0 and self.temperature > 200
    
    def can_ignite(self) -> bool:
        return self.ignition_potential > 0.1 and self.temperature > 400

class AdvancedPhysicsEngine:
    """Advanced physics for heat transfer and fluid dynamics"""
    def __init__(self, grid_width: int, grid_height: int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.convection_strength = 0.1
        self.radiation_constant = 5.67e-8  # Stefan-Boltzmann constant (simplified)
        
    def calculate_heat_transfer(self, grid: List[List[FireCell]], dt: float):
        """Calculate heat transfer through conduction, convection, and radiation"""
        # Create temporary arrays for heat transfer
        new_temperatures = [[cell.temperature for cell in row] for row in grid]
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell = grid[y][x]
                
                # Conduction - heat transfer to adjacent cells
                conduction_heat = 0.0
                neighbors = 0
                
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue
                        
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                            neighbor = grid[ny][nx]
                            temp_diff = neighbor.temperature - cell.temperature
                            conduction_heat += temp_diff * 0.01
                            neighbors += 1
                
                if neighbors > 0:
                    conduction_heat /= neighbors
                
                # Convection - hot air rises
                convection_heat = 0.0
                if cell.temperature > 100:  # Hot enough for convection
                    # Heat rises to cell above
                    if y > 0:
                        above_cell = grid[y-1][x]
                        if above_cell.temperature < cell.temperature:
                            convection_heat = -(cell.temperature - above_cell.temperature) * self.convection_strength
                    
                    # Cool air sinks to cell below
                    if y < self.grid_height - 1:
                        below_cell = grid[y+1][x]
                        if below_cell.temperature > cell.temperature:
                            convection_heat += (below_cell.temperature - cell.temperature) * self.convection_strength * 0.5
                
                # Radiation - heat loss to environment
                radiation_heat = 0.0
                if cell.temperature > 20:
                    # Simplified radiation cooling
                    radiation_heat = -(cell.temperature - 20) * 0.001
                
                # Apply heat transfer
                total_heat_change = (conduction_heat + convection_heat + radiation_heat) * dt
                new_temperatures[y][x] = max(20, cell.temperature + total_heat_change)
        
        # Apply new temperatures
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                grid[y][x].temperature = new_temperatures[y][x]

class FireDamageCalculator:
    """Calculate fire damage to structures and environment"""
    def __init__(self):
        self.damage_threshold = 300  # Temperature at which damage begins
        self.total_damage = 0.0
        self.structure_health = {}
        
    def calculate_damage(self, grid: List[List[FireCell]], dt: float):
        """Calculate damage from fire"""
        damage_this_frame = 0.0
        
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                cell = grid[y][x]
                
                if cell.temperature > self.damage_threshold:
                    # Calculate damage based on temperature and time
                    damage_rate = (cell.temperature - self.damage_threshold) * 0.01
                    damage = damage_rate * dt
                    damage_this_frame += damage
                    
                    # Track structure damage
                    pos_key = f"{x},{y}"
                    if pos_key not in self.structure_health:
                        self.structure_health[pos_key] = 100.0
                    
                    self.structure_health[pos_key] = max(0, self.structure_health[pos_key] - damage)
        
        self.total_damage += damage_this_frame
        return damage_this_frame
    
    def get_damage_report(self) -> Dict[str, float]:
        """Get comprehensive damage report"""
        destroyed_structures = sum(1 for health in self.structure_health.values() if health <= 0)
        damaged_structures = sum(1 for health in self.structure_health.values() if 0 < health < 100)
        
        return {
            'total_damage': self.total_damage,
            'destroyed_structures': destroyed_structures,
            'damaged_structures': damaged_structures,
            'economic_loss': self.total_damage * 1000  # Simplified economic calculation
        }

class FireScenarioManager:
    """Manages different fire scenarios"""
    def __init__(self):
        self.current_scenario = FireScenario.WILDFIRE
        self.scenario_time = 0.0
        self.objectives = []
        self.completed_objectives = []
        
    def setup_scenario(self, scenario: FireScenario, grid: List[List[FireCell]]):
        """Setup a specific fire scenario"""
        self.current_scenario = scenario
        self.scenario_time = 0.0
        self.objectives = []
        self.completed_objectives = []
        
        # Clear grid
        for row in grid:
            for cell in row:
                cell.fuel_amount = 0.0
                cell.state = FireState.COLD
                cell.temperature = 20.0
                cell.contains_water = False
        
        if scenario == FireScenario.WILDFIRE:
            self.setup_wildfire_scenario(grid)
        elif scenario == FireScenario.HOUSE_FIRE:
            self.setup_house_fire_scenario(grid)
        elif scenario == FireScenario.INDUSTRIAL:
            self.setup_industrial_scenario(grid)
        elif scenario == FireScenario.VEHICLE_FIRE:
            self.setup_vehicle_fire_scenario(grid)
        elif scenario == FireScenario.ELECTRICAL:
            self.setup_electrical_scenario(grid)
        elif scenario == FireScenario.CHEMICAL:
            self.setup_chemical_scenario(grid)
    
    def setup_wildfire_scenario(self, grid: List[List[FireCell]]):
        """Setup wildfire scenario"""
        # Create forest with varying fuel loads
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if random.random() < 0.8:  # 80% forest coverage
                    grid[y][x].fuel_amount = random.uniform(20, 100)
                    grid[y][x].fuel_type = FuelType.WOOD
                    grid[y][x].humidity = random.uniform(30, 70)
        
        # Create fire breaks (roads, rivers)
        for x in range(len(grid[0])):
            if len(grid) > 20:  # Create horizontal firebreak
                grid[len(grid)//2][x].fuel_amount = 0
                grid[len(grid)//2][x].contains_water = True
        
        # Start fire in one corner
        grid[0][0].state = FireState.BURNING
        grid[0][0].temperature = 800
        
        self.objectives = [
            "Contain the fire within 500 units",
            "Protect the firebreak",
            "Minimize burned area",
            "Prevent fire from reaching the bottom edge"
        ]
    
    def setup_house_fire_scenario(self, grid: List[List[FireCell]]):
        """Setup house fire scenario"""
        # Create house structure
        house_x, house_y = len(grid[0])//2, len(grid)//2
        
        # Walls and rooms
        for x in range(house_x - 10, house_x + 10):
            for y in range(house_y - 8, house_y + 8):
                if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
                    grid[y][x].fuel_amount = 60.0
                    grid[y][x].fuel_type = FuelType.WOOD
        
        # Kitchen (higher fuel load)
        for x in range(house_x - 5, house_x):
            for y in range(house_y - 4, house_y):
                if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
                    grid[y][x].fuel_amount = 80.0
                    grid[y][x].fuel_type = FuelType.OIL
        
        # Start fire in kitchen
        grid[house_y - 2][house_x - 2].state = FireState.BURNING
        grid[house_y - 2][house_x - 2].temperature = 600
        
        self.objectives = [
            "Contain fire to kitchen",
            "Protect escape routes",
            "Minimize smoke damage",
            "Extinguish fire in under 10 minutes"
        ]
    
    def setup_industrial_scenario(self, grid: List[List[FireCell]]):
        """Setup industrial fire scenario"""
        # Chemical storage area
        for x in range(10, 30):
            for y in range(10, 30):
                if x < len(grid[0]) and y < len(grid):
                    grid[y][x].fuel_amount = 100.0
                    grid[y][x].fuel_type = random.choice([FuelType.OIL, FuelType.GASOLINE, FuelType.ALCOHOL])
        
        # Start fire
        grid[15][15].state = FireState.BURNING
        grid[15][15].temperature = 800
        
        self.objectives = [
            "Prevent chemical explosion",
            "Contain hazardous material spread",
            "Minimize environmental damage",
            "Evacuate danger zone"
        ]
    
    def setup_vehicle_fire_scenario(self, grid: List[List[FireCell]]):
        """Setup vehicle fire scenario"""
        # Vehicle fuel
        for x in range(len(grid[0])//2 - 3, len(grid[0])//2 + 3):
            for y in range(len(grid)//2 - 2, len(grid)//2 + 2):
                if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
                    grid[y][x].fuel_amount = 80.0
                    grid[y][x].fuel_type = FuelType.GASOLINE
        
        # Start fire
        grid[len(grid)//2][len(grid[0])//2].state = FireState.BURNING
        grid[len(grid)//2][len(grid[0])//2].temperature = 700
        
        self.objectives = [
            "Extinguish fire quickly",
            "Prevent fuel tank explosion",
            "Protect nearby vehicles",
            "Clear evacuation routes"
        ]
    
    def setup_electrical_scenario(self, grid: List[List[FireCell]]):
        """Setup electrical fire scenario"""
        # Electrical components
        for x in range(len(grid[0])//2 - 5, len(grid[0])//2 + 5):
            for y in range(len(grid)//2 - 5, len(grid)//2 + 5):
                if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
                    grid[y][x].fuel_amount = 40.0
                    grid[y][x].fuel_type = FuelType.PAPER  # Insulation
        
        # Start electrical fire
        grid[len(grid)//2][len(grid[0])//2].state = FireState.BURNING
        grid[len(grid)//2][len(grid[0])//2].temperature = 500
        
        self.objectives = [
            "Cut power supply",
            "Use appropriate extinguishing agent",
            "Prevent electrical shock",
            "Contain fire to electrical room"
        ]
    
    def setup_chemical_scenario(self, grid: List[List[FireCell]]):
        """Setup chemical fire scenario"""
        # Different chemicals
        chemicals = [FuelType.ALCOHOL, FuelType.OIL, FuelType.GASOLINE]
        
        for i, chemical in enumerate(chemicals):
            x_start = i * (len(grid[0]) // 3)
            for x in range(x_start, x_start + len(grid[0]) // 3):
                for y in range(len(grid)//2 - 5, len(grid)//2 + 5):
                    if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
                        grid[y][x].fuel_amount = 70.0
                        grid[y][x].fuel_type = chemical
        
        # Start fire in middle
        grid[len(grid)//2][len(grid[0])//2].state = FireState.BURNING
        grid[len(grid)//2][len(grid[0])//2].temperature = 600
        
        self.objectives = [
            "Identify chemical types",
            "Use appropriate suppression method",
            "Prevent chemical mixing",
            "Minimize toxic smoke"
        ]
    
    def update_scenario(self, dt: float):
        """Update scenario progress"""
        self.scenario_time += dt
        
        # Check objective completion
        # This would be implemented based on specific conditions
        
    def get_scenario_status(self) -> Dict[str, any]:
        """Get current scenario status"""
        return {
            'scenario': self.current_scenario.name,
            'time': self.scenario_time,
            'objectives': self.objectives,
            'completed': self.completed_objectives,
            'progress': len(self.completed_objectives) / len(self.objectives) if self.objectives else 0
        }

class FirefightingTools:
    """Tools for fighting fires"""
    def __init__(self):
        self.water_capacity = 100.0
        self.water_remaining = 100.0
        self.foam_capacity = 50.0
        self.foam_remaining = 50.0
        self.fire_retardant = 30.0
        
    def use_water(self, amount: float) -> float:
        """Use water and return amount actually used"""
        used = min(amount, self.water_remaining)
        self.water_remaining -= used
        return used
    
    def use_foam(self, amount: float) -> float:
        """Use foam and return amount actually used"""
        used = min(amount, self.foam_remaining)
        self.foam_remaining -= used
        return used
    
    def use_retardant(self, amount: float) -> float:
        """Use fire retardant and return amount actually used"""
        used = min(amount, self.fire_retardant)
        self.fire_retardant -= used
        return used
    
    def refill(self):
        """Refill all firefighting materials"""
        self.water_remaining = self.water_capacity
        self.foam_remaining = self.foam_capacity
        self.fire_retardant = 30.0

class WeatherSystem:
    """Advanced weather management system"""
    def __init__(self):
        self.conditions = WeatherConditions(
            weather_type=WeatherType.CLEAR,
            temperature=20.0,
            humidity=50.0,
            wind_speed=2.0,
            wind_direction=0.0,
            precipitation=0.0,
            visibility=10.0,
            uv_index=5.0
        )
        self.time_of_day = 0.5  # 0.0 = midnight, 0.5 = noon
        self.season = "Summer"
        
    def update(self, dt: float):
        """Update weather conditions"""
        # Time progression
        self.time_of_day += dt * 0.001  # Accelerated time
        if self.time_of_day >= 1.0:
            self.time_of_day = 0.0
            self.advance_day()
        
        # Random weather changes
        if random.random() < 0.005:  # 0.5% chance per frame
            self.change_weather()
        
        # Gradual parameter changes
        self.conditions.wind_speed += random.uniform(-0.1, 0.1)
        self.conditions.wind_speed = max(0, min(15, self.conditions.wind_speed))
        
        self.conditions.wind_direction += random.uniform(-0.05, 0.05)
        self.conditions.wind_direction = self.conditions.wind_direction % (2 * math.pi)
        
        # Temperature varies with time of day
        base_temp = 20.0
        temp_variation = 10.0 * math.sin(self.time_of_day * 2 * math.pi)
        self.conditions.temperature = base_temp + temp_variation
        
        # Humidity varies with precipitation
        if self.conditions.precipitation > 0:
            self.conditions.humidity = min(100, self.conditions.humidity + 2)
        else:
            self.conditions.humidity += random.uniform(-1, 1)
            self.conditions.humidity = max(10, min(90, self.conditions.humidity))
    
    def advance_day(self):
        """Advance to next day"""
        # Seasonal changes could be implemented here
        pass
    
    def change_weather(self):
        """Change weather type"""
        current_type = self.conditions.weather_type
        
        # Weather transition probabilities
        if current_type == WeatherType.CLEAR:
            new_type = random.choice([WeatherType.RAIN, WeatherType.STORM, WeatherType.DROUGHT])
        elif current_type == WeatherType.RAIN:
            new_type = random.choice([WeatherType.CLEAR, WeatherType.STORM, WeatherType.SNOW])
        elif current_type == WeatherType.STORM:
            new_type = random.choice([WeatherType.RAIN, WeatherType.CLEAR])
        elif current_type == WeatherType.SNOW:
            new_type = random.choice([WeatherType.CLEAR, WeatherType.STORM])
        elif current_type == WeatherType.DROUGHT:
            new_type = random.choice([WeatherType.CLEAR, WeatherType.HEATWAVE])
        else:  # HEATWAVE
            new_type = random.choice([WeatherType.CLEAR, WeatherType.DROUGHT])
        
        self.conditions.weather_type = new_type
        
        # Adjust parameters based on weather type
        if new_type == WeatherType.RAIN:
            self.conditions.precipitation = random.uniform(2, 8)
            self.conditions.visibility = random.uniform(3, 7)
        elif new_type == WeatherType.STORM:
            self.conditions.precipitation = random.uniform(5, 15)
            self.conditions.wind_speed = random.uniform(8, 15)
            self.conditions.visibility = random.uniform(1, 4)
        elif new_type == WeatherType.SNOW:
            self.conditions.precipitation = random.uniform(1, 5)
            self.conditions.temperature = random.uniform(-10, 5)
            self.conditions.visibility = random.uniform(2, 6)
        elif new_type == WeatherType.DROUGHT:
            self.conditions.precipitation = 0
            self.conditions.humidity = random.uniform(10, 30)
            self.conditions.temperature += random.uniform(5, 15)
        elif new_type == WeatherType.HEATWAVE:
            self.conditions.precipitation = 0
            self.conditions.humidity = random.uniform(20, 40)
            self.conditions.temperature = random.uniform(35, 45)
        else:  # CLEAR
            self.conditions.precipitation = 0
            self.conditions.visibility = 10.0
    
    def apply_to_grid(self, grid: List[List[FireCell]]):
        """Apply weather effects to grid"""
        wind_x = self.conditions.wind_speed * math.cos(self.conditions.wind_direction)
        wind_y = self.conditions.wind_speed * math.sin(self.conditions.wind_direction)
        
        for row in grid:
            for cell in row:
                cell.wind_velocity_x = wind_x
                cell.wind_velocity_y = wind_y
                cell.humidity = self.conditions.humidity
                
                # Temperature effect
                if cell.state == FireState.COLD:
                    cell.temperature = self.conditions.temperature
                
                # Precipitation effect
                if self.conditions.precipitation > 0:
                    cell.water_amount += self.conditions.precipitation * 0.02
                    cell.contains_water = True
                    
                    # Snow provides additional cooling
                    if self.conditions.weather_type == WeatherType.SNOW:
                        cell.temperature -= 5
    
    def get_fire_danger_rating(self) -> str:
        """Get fire danger rating"""
        risk = self.conditions.get_fire_risk()
        
        if risk < 0.2:
            return "LOW"
        elif risk < 0.4:
            return "MODERATE"
        elif risk < 0.6:
            return "HIGH"
        elif risk < 0.8:
            return "VERY HIGH"
        else:
            return "EXTREME"

class FireCombustionSimulator:
    """Main fire simulation class with advanced physics and scenarios"""
    def __init__(self):
        self.grid_size = 4
        self.grid_width = WIDTH // self.grid_size
        self.grid_height = HEIGHT // self.grid_size
        
        # Initialize grid
        self.grid = [[FireCell(x, y) for x in range(self.grid_width)] 
                     for y in range(self.grid_height)]
        
        # Advanced systems
        self.fire_spread = FireSpreadManager(self.grid_width, self.grid_height)
        self.weather = WeatherSystem()
        self.firefighting = FirefightingTools()
        self.physics_engine = AdvancedPhysicsEngine(self.grid_width, self.grid_height)
        self.damage_calculator = FireDamageCalculator()
        self.scenario_manager = FireScenarioManager()
        
        # Particle systems
        self.smoke_particles = []
        self.flame_particles = []
        self.ember_particles = []
        self.max_particles = 500  # Performance limit
        
        # Simulation state
        self.simulation_mode = SimulationMode.SANDBOX
        self.paused = False
        self.time_step = 0.016  # 60 FPS
        self.simulation_speed = 1.0
        self.total_simulation_time = 0.0
        
        # UI state
        self.show_hud = True
        self.show_temperature = False
        self.show_oxygen = False
        self.show_smoke = False
        self.show_particles = True
        self.show_damage = False
        self.show_objectives = True
        self.selected_fuel = FuelType.WOOD
        self.brush_size = 1
        
        # Mouse interaction
        self.mouse_mode = 'fuel'  # 'fuel', 'ignite', 'water', 'wind', 'extinguish'
        self.mouse_pressed = False
        
        # Performance monitoring
        self.performance_stats = {
            'fps': 60,
            'particle_count': 0,
            'active_fires': 0,
            'total_damage': 0.0
        }
        
        self.mode_names = {
            SimulationMode.SANDBOX: "Sandbox Mode",
            SimulationMode.FIREFIGHTING: "Firefighting Training",
            SimulationMode.FOREST_FIRE: "Forest Fire Simulation",
            SimulationMode.CHEMISTRY_LAB: "Chemistry Lab",
            SimulationMode.INDUSTRIAL: "Industrial Safety"
        }
        
        self.fuel_names = {
            FuelType.WOOD: "Wood",
            FuelType.PAPER: "Paper",
            FuelType.GASOLINE: "Gasoline",
            FuelType.PROPANE: "Propane",
            FuelType.ALCOHOL: "Alcohol",
            FuelType.COAL: "Coal",
            FuelType.OIL: "Oil"
        }
        
        self.scenario_names = {
            FireScenario.WILDFIRE: "Wildfire",
            FireScenario.HOUSE_FIRE: "House Fire",
            FireScenario.INDUSTRIAL: "Industrial Fire",
            FireScenario.VEHICLE_FIRE: "Vehicle Fire",
            FireScenario.ELECTRICAL: "Electrical Fire",
            FireScenario.CHEMICAL: "Chemical Fire"
        }
        
        self.initialize_scenario()
    
    def initialize_scenario(self):
        """Initialize scenario based on simulation mode"""
        if self.simulation_mode == SimulationMode.SANDBOX:
            self.setup_sandbox_mode()
        elif self.simulation_mode == SimulationMode.FIREFIGHTING:
            self.scenario_manager.setup_scenario(FireScenario.HOUSE_FIRE, self.grid)
        elif self.simulation_mode == SimulationMode.FOREST_FIRE:
            self.scenario_manager.setup_scenario(FireScenario.WILDFIRE, self.grid)
        elif self.simulation_mode == SimulationMode.CHEMISTRY_LAB:
            self.scenario_manager.setup_scenario(FireScenario.CHEMICAL, self.grid)
        elif self.simulation_mode == SimulationMode.INDUSTRIAL:
            self.scenario_manager.setup_scenario(FireScenario.INDUSTRIAL, self.grid)
        
        # Reset particles and damage
        self.smoke_particles.clear()
        self.flame_particles.clear()
        self.ember_particles.clear()
        self.damage_calculator = FireDamageCalculator()
        self.total_simulation_time = 0.0
    
    def setup_sandbox_mode(self):
        """Setup sandbox mode with basic fuel layout"""
        # Clear grid
        for row in self.grid:
            for cell in row:
                cell.fuel_amount = 0.0
                cell.state = FireState.COLD
                cell.temperature = 20.0
                cell.contains_water = False
        
        # Add some initial fuel
        center_x, center_y = self.grid_width // 2, self.grid_height // 2
        for x in range(center_x - 5, center_x + 5):
            for y in range(center_y - 5, center_y + 5):
                if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
                    self.grid[y][x].fuel_amount = 50.0
                    self.grid[y][x].fuel_type = FuelType.WOOD
    
    def update_simulation(self):
        """Update the advanced fire simulation"""
        if self.paused:
            return
        
        dt = self.time_step * self.simulation_speed
        self.total_simulation_time += dt
        
        # Update weather
        self.weather.update(dt)
        self.weather.apply_to_grid(self.grid)
        
        # Update combustion in each cell
        active_fires = 0
        for row in self.grid:
            for cell in row:
                cell.update_combustion(dt)
                if cell.state == FireState.BURNING:
                    active_fires += 1
                    
                    # Generate particles
                    if self.show_particles and len(self.smoke_particles) < self.max_particles:
                        # Generate smoke
                        if random.random() < 0.3:
                            smoke_x = cell.x * self.grid_size + random.uniform(-2, 2)
                            smoke_y = cell.y * self.grid_size + random.uniform(-2, 2)
                            self.smoke_particles.append(SmokeParticle(smoke_x, smoke_y))
                        
                        # Generate flames
                        if random.random() < 0.5:
                            flame_x = cell.x * self.grid_size + random.uniform(-1, 1)
                            flame_y = cell.y * self.grid_size + random.uniform(-1, 1)
                            intensity = min(1.0, cell.temperature / 800.0)
                            self.flame_particles.append(FlameParticle(flame_x, flame_y, intensity))
                        
                        # Generate embers (less frequently)
                        if random.random() < 0.1 and self.weather.conditions.wind_speed > 3:
                            ember_x = cell.x * self.grid_size + random.uniform(-1, 1)
                            ember_y = cell.y * self.grid_size + random.uniform(-1, 1)
                            self.ember_particles.append(EmberParticle(ember_x, ember_y))
        
        # Update particles
        wind_x = self.weather.conditions.wind_speed * math.cos(self.weather.conditions.wind_direction)
        wind_y = self.weather.conditions.wind_speed * math.sin(self.weather.conditions.wind_direction)
        
        # Update smoke particles
        self.smoke_particles = [p for p in self.smoke_particles if p.is_alive()]
        for particle in self.smoke_particles:
            particle.update(dt, wind_x, wind_y)
        
        # Update flame particles
        self.flame_particles = [p for p in self.flame_particles if p.is_alive()]
        for particle in self.flame_particles:
            particle.update(dt, wind_x, wind_y)
        
        # Update ember particles and check for new ignitions
        self.ember_particles = [p for p in self.ember_particles if p.is_alive()]
        for particle in self.ember_particles:
            particle.update(dt, wind_x, wind_y)
            
            # Check if ember can ignite a new cell
            if particle.can_ignite():
                grid_x = int(particle.x // self.grid_size)
                grid_y = int(particle.y // self.grid_size)
                
                if (0 <= grid_x < self.grid_width and 
                    0 <= grid_y < self.grid_height and 
                    self.grid[grid_y][grid_x].can_ignite()):
                    self.grid[grid_y][grid_x].state = FireState.BURNING
                    self.grid[grid_y][grid_x].temperature = 400
                    particle.ignition_potential = 0  # Ember used up
        
        # Advanced physics
        self.physics_engine.calculate_heat_transfer(self.grid, dt)
        
        # Handle fire spread
        self.fire_spread.spread_fire(self.grid, dt)
        
        # Calculate damage
        damage_this_frame = self.damage_calculator.calculate_damage(self.grid, dt)
        
        # Update scenario
        self.scenario_manager.update_scenario(dt)
        
        # Update performance stats
        self.performance_stats['particle_count'] = (len(self.smoke_particles) + 
                                                   len(self.flame_particles) + 
                                                   len(self.ember_particles))
        self.performance_stats['active_fires'] = active_fires
        self.performance_stats['total_damage'] = self.damage_calculator.total_damage
    
    def cycle_scenario(self):
        """Cycle through different fire scenarios"""
        scenarios = list(FireScenario)
        current_index = scenarios.index(self.scenario_manager.current_scenario)
        new_scenario = scenarios[(current_index + 1) % len(scenarios)]
        self.scenario_manager.setup_scenario(new_scenario, self.grid)
        
        # Reset particles and damage
        self.smoke_particles.clear()
        self.flame_particles.clear()
        self.ember_particles.clear()
        self.damage_calculator = FireDamageCalculator()
        self.total_simulation_time = 0.0
    
    def toggle_weather(self):
        """Manually trigger weather change"""
        self.weather.change_weather()
    
    def reset_simulation(self):
        """Reset the simulation"""
        self.initialize_scenario()
        self.total_simulation_time = 0.0
    
    def handle_mouse_interaction(self, mouse_pos: Tuple[int, int], mouse_pressed: bool):
        """Handle mouse interaction with the grid"""
        grid_x = mouse_pos[0] // self.grid_size
        grid_y = mouse_pos[1] // self.grid_size
        
        if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
            if mouse_pressed:
                # Apply brush in area around click
                for dy in range(-self.brush_size, self.brush_size + 1):
                    for dx in range(-self.brush_size, self.brush_size + 1):
                        nx, ny = grid_x + dx, grid_y + dy
                        if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                            cell = self.grid[ny][nx]
                            
                            if self.mouse_mode == 'fuel':
                                cell.fuel_amount = min(100, cell.fuel_amount + 10)
                                cell.fuel_type = self.selected_fuel
                            elif self.mouse_mode == 'ignite':
                                if cell.fuel_amount > 0:
                                    cell.state = FireState.IGNITION
                                    cell.temperature = 800
                            elif self.mouse_mode == 'water':
                                water_used = self.firefighting.use_water(5.0)
                                cell.water_amount += water_used
                                cell.contains_water = True
                                if cell.state == FireState.BURNING:
                                    cell.temperature -= water_used * 10
                            elif self.mouse_mode == 'wind':
                                # Set wind direction from center to click
                                center_x = self.grid_width // 2
                                center_y = self.grid_height // 2
                                wind_dx = nx - center_x
                                wind_dy = ny - center_y
                                magnitude = math.sqrt(wind_dx**2 + wind_dy**2)
                                if magnitude > 0:
                                    self.weather.wind_direction = math.atan2(wind_dy, wind_dx)
                                    self.weather.wind_speed = min(10, magnitude * 0.5)
            elif self.mouse_mode == 'extinguish':
                if cell.state == FireState.BURNING:
                    cell.state = FireState.EXTINGUISHING
                    cell.temperature = 800 # Start extinguishing
                    cell.burn_time = 0 # Reset burn time for extinguishing
                    cell.fuel_amount = 0 # Ensure no fuel left
                    cell.oxygen_level = 21.0 # Restore oxygen
                    cell.smoke_density = 0.0
                    cell.heat_energy = 0.0
                    cell.temperature = 20.0 # Final temperature after extinguishing
                    cell.contains_water = False
                    cell.water_amount = 0.0
                    cell.humidity = 50.0 # Restore humidity
                    cell.wind_velocity_x = 0.0
                    cell.wind_velocity_y = 0.0
                    cell.pressure = 1013.25
                    cell.state = FireState.EXTINGUISHED
    
    def draw_grid(self, surface):
        """Draw the fire simulation grid with particles"""
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell = self.grid[y][x]
                
                # Get display color based on current view mode
                if self.show_temperature:
                    # Temperature visualization
                    temp_intensity = min(255, max(0, int((cell.temperature - 20) * 2)))
                    color = (temp_intensity, 0, 255 - temp_intensity)
                elif self.show_oxygen:
                    # Oxygen visualization
                    oxygen_intensity = int((cell.oxygen_level / 21.0) * 255)
                    color = (255 - oxygen_intensity, 255 - oxygen_intensity, 255)
                elif self.show_smoke:
                    # Smoke visualization
                    smoke_intensity = min(255, int(cell.smoke_density * 2.55))
                    color = (smoke_intensity, smoke_intensity, smoke_intensity)
                elif self.show_damage:
                    # Damage visualization
                    pos_key = f"{x},{y}"
                    if pos_key in self.damage_calculator.structure_health:
                        health = self.damage_calculator.structure_health[pos_key]
                        damage_intensity = int((100 - health) * 2.55)
                        color = (damage_intensity, 255 - damage_intensity, 0)
                    else:
                        color = (0, 255, 0)  # No damage
                else:
                    # Normal fire visualization
                    color = cell.get_display_color()
                
                # Draw cell
                rect = pygame.Rect(x * self.grid_size, y * self.grid_size, 
                                 self.grid_size, self.grid_size)
                pygame.draw.rect(surface, color, rect)
                
                # Add fire glow effect for burning cells
                if cell.state == FireState.BURNING and not self.show_temperature:
                    glow_color = (255, 255, 0, 128)  # Yellow glow
                    glow_rect = pygame.Rect(x * self.grid_size - 1, y * self.grid_size - 1,
                                          self.grid_size + 2, self.grid_size + 2)
                    pygame.draw.rect(surface, glow_color[:3], glow_rect, 1)
        
        # Draw particles
        if self.show_particles:
            # Draw smoke particles
            for particle in self.smoke_particles:
                if 0 <= particle.x < WIDTH and 0 <= particle.y < HEIGHT:
                    alpha = int(particle.density * 255)
                    smoke_color = (100, 100, 100, alpha)
                    size = int(particle.size)
                    pygame.draw.circle(surface, smoke_color[:3], 
                                     (int(particle.x), int(particle.y)), size)
            
            # Draw flame particles
            for particle in self.flame_particles:
                if 0 <= particle.x < WIDTH and 0 <= particle.y < HEIGHT:
                    color = particle.get_color()
                    size = int(particle.size)
                    pygame.draw.circle(surface, color, 
                                     (int(particle.x), int(particle.y)), size)
            
            # Draw ember particles
            for particle in self.ember_particles:
                if 0 <= particle.x < WIDTH and 0 <= particle.y < HEIGHT:
                    color = (255, 100, 0) if particle.can_ignite() else (100, 50, 0)
                    size = int(particle.size)
                    pygame.draw.circle(surface, color, 
                                     (int(particle.x), int(particle.y)), size)
    
    def draw_hud(self, surface):
        """Draw heads-up display"""
        if not self.show_hud:
            return
        
        # HUD background
        hud_rect = pygame.Rect(0, 0, WIDTH, 70)
        pygame.draw.rect(surface, (0, 0, 0, 180), hud_rect)
        
        # Current mode and fuel
        font = pygame.font.Font(None, 18)
        mode_text = f"Mode: {self.mode_names[self.simulation_mode]}"
        text = font.render(mode_text, True, NEON_CYAN)
        surface.blit(text, (10, 10))
        
        fuel_text = f"Fuel: {self.fuel_names[self.selected_fuel]}"
        text = font.render(fuel_text, True, NEON_GREEN)
        surface.blit(text, (10, 30))
        
        mouse_text = f"Tool: {self.mouse_mode.title()}"
        text = font.render(mouse_text, True, NEON_YELLOW)
        surface.blit(text, (10, 50))
        
        # Weather conditions
        weather_text = f"Wind: {self.weather.wind_speed:.1f} m/s  Humidity: {self.weather.humidity:.0f}%"
        text = font.render(weather_text, True, NEON_ORANGE)
        surface.blit(text, (200, 10))
        
        temp_text = f"Ambient: {self.weather.temperature:.1f}°C"
        text = font.render(temp_text, True, NEON_ORANGE)
        surface.blit(text, (200, 30))
        
        # Firefighting resources
        if self.simulation_mode == SimulationMode.FIREFIGHTING:
            water_text = f"Water: {self.firefighting.water_remaining:.0f}/{self.firefighting.water_capacity:.0f}"
            text = font.render(water_text, True, NEON_BLUE)
            surface.blit(text, (200, 50))
            
            foam_text = f"Foam: {self.firefighting.foam_remaining:.0f}/{self.firefighting.foam_capacity:.0f}"
            text = font.render(foam_text, True, NEON_GREEN)
            surface.blit(text, (350, 50))
    
    def draw_controls(self, surface):
        """Draw control instructions"""
        controls_rect = pygame.Rect(10, HEIGHT - 120, 460, 110)
        pygame.draw.rect(surface, (0, 0, 0, 180), controls_rect)
        
        font = pygame.font.Font(None, 14)
        controls = [
            "SPACE - Pause/Resume  |  M - Change Mode  |  F - Change Fuel",
            "1-4 - Mouse Tools: 1=Fuel 2=Ignite 3=Water 4=Wind",
            "T/O/S - Toggle Temperature/Oxygen/Smoke View",
            "+/- - Brush Size  |  R - Reset Scenario  |  Weather: W=Wind H=Humidity",
            "Mouse - Click/Drag to interact  |  F8 - Fullscreen  |  ESC - Launcher"
        ]
        
        for i, control in enumerate(controls):
            text = font.render(control, True, NEON_YELLOW)
            surface.blit(text, (15, HEIGHT - 115 + i * 18))
    
    def draw_legend(self, surface):
        """Draw color legend"""
        legend_rect = pygame.Rect(WIDTH - 150, 80, 140, 180)
        pygame.draw.rect(surface, (0, 0, 0, 200), legend_rect)
        pygame.draw.rect(surface, NEON_CYAN, legend_rect, 2)
        
        font = pygame.font.Font(None, 16)
        title_text = font.render("LEGEND", True, NEON_CYAN)
        surface.blit(title_text, (WIDTH - 140, 90))
        
        legend_items = [
            ("White Hot", FIRE_COLORS['white_hot']),
            ("Blue Flame", FIRE_COLORS['blue_flame']),
            ("Yellow Flame", FIRE_COLORS['yellow_flame']),
            ("Orange Flame", FIRE_COLORS['orange_flame']),
            ("Red Flame", FIRE_COLORS['red_flame']),
            ("Wood Fuel", FIRE_COLORS['fuel']),
            ("Smoke", FIRE_COLORS['smoke']),
            ("Water", FIRE_COLORS['water'])
        ]
        
        y_offset = 110
        for name, color in legend_items:
            # Color square
            pygame.draw.rect(surface, color, (WIDTH - 140, y_offset, 12, 12))
            # Label
            text = font.render(name, True, NEON_GREEN)
            surface.blit(text, (WIDTH - 125, y_offset))
            y_offset += 18
    
    def handle_input(self, keys, events):
        """Handle user input"""
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_m:
                    self.cycle_simulation_mode()
                elif event.key == pygame.K_f:
                    self.cycle_fuel_type()
                elif event.key == pygame.K_1:
                    self.mouse_mode = 'fuel'
                elif event.key == pygame.K_2:
                    self.mouse_mode = 'ignite'
                elif event.key == pygame.K_3:
                    self.mouse_mode = 'water'
                elif event.key == pygame.K_4:
                    self.mouse_mode = 'wind'
                elif event.key == pygame.K_t:
                    self.show_temperature = not self.show_temperature
                    self.show_oxygen = False
                    self.show_smoke = False
                elif event.key == pygame.K_o:
                    self.show_oxygen = not self.show_oxygen
                    self.show_temperature = False
                    self.show_smoke = False
                elif event.key == pygame.K_s:
                    self.show_smoke = not self.show_smoke
                    self.show_temperature = False
                    self.show_oxygen = False
                elif event.key == pygame.K_r:
                    self.initialize_scenario()
                elif event.key == pygame.K_h:
                    self.show_hud = not self.show_hud
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.brush_size = min(3, self.brush_size + 1)
                elif event.key == pygame.K_MINUS:
                    self.brush_size = max(1, self.brush_size - 1)
                elif event.key == pygame.K_w:
                    self.weather.wind_speed = min(10, self.weather.wind_speed + 1)
                elif event.key == pygame.K_q:
                    self.weather.wind_speed = max(0, self.weather.wind_speed - 1)
                elif event.key == pygame.K_e:
                    self.weather.humidity = min(100, self.weather.humidity + 5)
                elif event.key == pygame.K_d:
                    self.weather.humidity = max(0, self.weather.humidity - 5)
                elif event.key == pygame.K_p: # Toggle particles
                    self.show_particles = not self.show_particles
                    self.show_temperature = False
                    self.show_oxygen = False
                    self.show_smoke = False
                elif event.key == pygame.K_d: # Toggle damage
                    self.show_damage = not self.show_damage
                    self.show_temperature = False
                    self.show_oxygen = False
                    self.show_smoke = False
                elif event.key == pygame.K_o: # Toggle objectives
                    self.show_objectives = not self.show_objectives
                    self.show_temperature = False
                    self.show_oxygen = False
                    self.show_smoke = False
                elif event.key == pygame.K_c: # Cycle scenarios
                    self.cycle_scenario()
                elif event.key == pygame.K_w: # Toggle weather
                    self.toggle_weather()
                elif event.key == pygame.K_r: # Reset simulation
                    self.reset_simulation()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_pressed = True
                    self.handle_mouse_interaction(event.pos, True)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_pressed = False
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_pressed:
                    self.handle_mouse_interaction(event.pos, True)
    
    def cycle_simulation_mode(self):
        """Cycle to next simulation mode"""
        modes = list(SimulationMode)
        current_index = modes.index(self.simulation_mode)
        self.simulation_mode = modes[(current_index + 1) % len(modes)]
        self.initialize_scenario()
    
    def cycle_fuel_type(self):
        """Cycle to next fuel type"""
        fuels = list(FuelType)
        current_index = fuels.index(self.selected_fuel)
        self.selected_fuel = fuels[(current_index + 1) % len(fuels)]

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
    """Main simulation loop with enhanced features"""
    global screen
    
    # Initialize simulator
    simulator = FireCombustionSimulator()
    
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
        
        # Draw everything
        simulator.draw_grid(screen)
        simulator.draw_advanced_hud(screen)
        simulator.draw_damage_report(screen)
        simulator.draw_enhanced_controls(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS for smooth fire simulation
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 