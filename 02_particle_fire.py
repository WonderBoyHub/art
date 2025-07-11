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

class WeatherSystem:
    """Manages environmental conditions"""
    def __init__(self):
        self.wind_speed = 0.0
        self.wind_direction = 0.0
        self.humidity = 50.0
        self.temperature = 20.0
        self.pressure = 1013.25
        self.precipitation = 0.0
        
    def update(self, dt: float):
        """Update weather conditions"""
        # Random weather changes
        if random.random() < 0.01:
            self.wind_speed += random.uniform(-0.5, 0.5)
            self.wind_speed = max(0, min(10, self.wind_speed))
            
            self.wind_direction += random.uniform(-0.2, 0.2)
            self.wind_direction = self.wind_direction % (2 * math.pi)
            
            self.humidity += random.uniform(-2, 2)
            self.humidity = max(0, min(100, self.humidity))
            
            self.temperature += random.uniform(-1, 1)
            self.temperature = max(-20, min(50, self.temperature))
    
    def apply_to_grid(self, grid: List[List[FireCell]]):
        """Apply weather effects to grid"""
        wind_x = self.wind_speed * math.cos(self.wind_direction)
        wind_y = self.wind_speed * math.sin(self.wind_direction)
        
        for row in grid:
            for cell in row:
                cell.wind_velocity_x = wind_x
                cell.wind_velocity_y = wind_y
                cell.humidity = self.humidity
                
                # Temperature effect
                if cell.state == FireState.COLD:
                    cell.temperature = self.temperature
                
                # Precipitation effect
                if self.precipitation > 0:
                    cell.water_amount += self.precipitation * 0.1
                    cell.contains_water = True

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

class FireCombustionSimulator:
    """Main fire simulation class"""
    def __init__(self):
        self.grid_size = 4
        self.grid_width = WIDTH // self.grid_size
        self.grid_height = HEIGHT // self.grid_size
        
        # Initialize grid
        self.grid = [[FireCell(x, y) for x in range(self.grid_width)] 
                     for y in range(self.grid_height)]
        
        # Systems
        self.fire_spread = FireSpreadManager(self.grid_width, self.grid_height)
        self.weather = WeatherSystem()
        self.firefighting = FirefightingTools()
        
        # Simulation state
        self.simulation_mode = SimulationMode.SANDBOX
        self.paused = False
        self.time_step = 0.016  # 60 FPS
        self.simulation_speed = 1.0
        
        # UI state
        self.show_hud = True
        self.show_temperature = False
        self.show_oxygen = False
        self.show_smoke = False
        self.selected_fuel = FuelType.WOOD
        self.brush_size = 1
        
        # Mouse interaction
        self.mouse_mode = 'fuel'  # 'fuel', 'ignite', 'water', 'wind'
        self.mouse_pressed = False
        
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
        
        self.initialize_scenario()
    
    def initialize_scenario(self):
        """Initialize scenario based on simulation mode"""
        # Clear grid
        for row in self.grid:
            for cell in row:
                cell.fuel_amount = 0.0
                cell.state = FireState.COLD
                cell.temperature = 20.0
                cell.contains_water = False
        
        if self.simulation_mode == SimulationMode.SANDBOX:
            # Start with some wood
            for x in range(self.grid_width // 4, 3 * self.grid_width // 4):
                for y in range(3 * self.grid_height // 4, self.grid_height):
                    self.grid[y][x].fuel_amount = 50.0
                    self.grid[y][x].fuel_type = FuelType.WOOD
        
        elif self.simulation_mode == SimulationMode.FOREST_FIRE:
            # Create forest layout
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    if random.random() < 0.7:  # 70% forest coverage
                        self.grid[y][x].fuel_amount = random.uniform(30, 80)
                        self.grid[y][x].fuel_type = FuelType.WOOD
        
        elif self.simulation_mode == SimulationMode.CHEMISTRY_LAB:
            # Different fuel types arranged
            fuel_types = list(FuelType)
            for i, fuel in enumerate(fuel_types):
                x = (i % 4) * (self.grid_width // 4) + self.grid_width // 8
                y = (i // 4) * (self.grid_height // 2) + self.grid_height // 4
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        if 0 <= x + dx < self.grid_width and 0 <= y + dy < self.grid_height:
                            self.grid[y + dy][x + dx].fuel_amount = 40.0
                            self.grid[y + dy][x + dx].fuel_type = fuel
        
        elif self.simulation_mode == SimulationMode.INDUSTRIAL:
            # Industrial facility with various fuel types
            # Oil tanks
            for x in range(10, 20):
                for y in range(10, 20):
                    if x < self.grid_width and y < self.grid_height:
                        self.grid[y][x].fuel_amount = 100.0
                        self.grid[y][x].fuel_type = FuelType.OIL
            
            # Propane storage
            for x in range(30, 40):
                for y in range(10, 20):
                    if x < self.grid_width and y < self.grid_height:
                        self.grid[y][x].fuel_amount = 80.0
                        self.grid[y][x].fuel_type = FuelType.PROPANE
    
    def update_simulation(self):
        """Update the fire simulation"""
        if self.paused:
            return
        
        dt = self.time_step * self.simulation_speed
        
        # Update weather
        self.weather.update(dt)
        self.weather.apply_to_grid(self.grid)
        
        # Update combustion in each cell
        for row in self.grid:
            for cell in row:
                cell.update_combustion(dt)
        
        # Handle fire spread
        self.fire_spread.spread_fire(self.grid, dt)
        
        # Heat transfer between adjacent cells
        self.transfer_heat(dt)
    
    def transfer_heat(self, dt: float):
        """Transfer heat between adjacent cells"""
        heat_transfer_rate = 0.1 * dt
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell = self.grid[y][x]
                
                # Check all 4 neighbors
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                        neighbor = self.grid[ny][nx]
                        
                        # Heat flows from hot to cold
                        temp_diff = cell.temperature - neighbor.temperature
                        if abs(temp_diff) > 1:
                            heat_flow = temp_diff * heat_transfer_rate
                            cell.temperature -= heat_flow / 2
                            neighbor.temperature += heat_flow / 2
    
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
    
    def draw_grid(self, surface):
        """Draw the simulation grid"""
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell = self.grid[y][x]
                
                # Get display color based on view mode
                if self.show_temperature:
                    # Temperature visualization
                    temp_norm = min(1.0, max(0.0, (cell.temperature - 20) / 1000))
                    color = (int(255 * temp_norm), 0, int(255 * (1 - temp_norm)))
                elif self.show_oxygen:
                    # Oxygen visualization
                    oxygen_norm = cell.oxygen_level / 21.0
                    color = (0, 0, int(255 * oxygen_norm))
                elif self.show_smoke:
                    # Smoke visualization
                    smoke_norm = min(1.0, cell.smoke_density / 100.0)
                    intensity = int(100 * smoke_norm)
                    color = (intensity, intensity, intensity)
                else:
                    # Normal fire/fuel visualization
                    color = cell.get_display_color()
                
                # Draw cell
                rect = pygame.Rect(x * self.grid_size, y * self.grid_size, 
                                 self.grid_size, self.grid_size)
                pygame.draw.rect(surface, color, rect)
                
                # Draw wind arrows if significant
                if (cell.wind_velocity_x**2 + cell.wind_velocity_y**2) > 1:
                    wind_magnitude = math.sqrt(cell.wind_velocity_x**2 + cell.wind_velocity_y**2)
                    if wind_magnitude > 0.5:
                        arrow_length = min(self.grid_size, wind_magnitude * 2)
                        center_x = x * self.grid_size + self.grid_size // 2
                        center_y = y * self.grid_size + self.grid_size // 2
                        end_x = center_x + cell.wind_velocity_x * arrow_length / wind_magnitude
                        end_y = center_y + cell.wind_velocity_y * arrow_length / wind_magnitude
                        pygame.draw.line(surface, NEON_CYAN, 
                                       (center_x, center_y), (int(end_x), int(end_y)), 1)
    
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
    """Main simulation loop"""
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
        
        # Draw simulation
        simulator.draw_grid(screen)
        
        # Draw UI
        simulator.draw_hud(screen)
        simulator.draw_controls(screen)
        simulator.draw_legend(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS for smooth fire simulation
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 