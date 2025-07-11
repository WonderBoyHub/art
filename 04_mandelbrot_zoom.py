#!/usr/bin/env python3
"""
Advanced Mathematical Explorer - Interactive fractal and equation visualization
Perfect for Raspberry Pi 5 with 3.5" display (480x320)
COMPLETE MATHEMATICAL VISUALIZATION WITH FRACTALS AND EQUATION MANIPULATION
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
from typing import List, Dict, Optional, Tuple, Callable

# Initialize Pygame
pygame.init()

# Screen dimensions optimized for Pi 5
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Mathematical Explorer")

# Fullscreen support
fullscreen = False
clock = pygame.time.Clock()
start_time = time.time()

# Enhanced mathematical color palette
CYBER_BLACK = (10, 10, 15)
NEON_BLUE = (50, 150, 255)
NEON_GREEN = (50, 255, 150)
NEON_CYAN = (50, 255, 255)
NEON_YELLOW = (255, 255, 50)
NEON_RED = (255, 50, 50)
NEON_PURPLE = (150, 50, 255)
NEON_ORANGE = (255, 150, 50)
MATH_COLORS = {
    'mandelbrot': (100, 150, 255),
    'julia': (255, 100, 255),
    'newton': (100, 255, 100),
    'burning_ship': (255, 150, 100),
    'function': (255, 255, 100),
    'parametric': (150, 255, 255),
    'polar': (255, 200, 150),
    'complex': (200, 100, 255),
    'iteration': (150, 150, 255),
    'convergence': (100, 255, 200)
}

class FractalType(Enum):
    MANDELBROT = 0
    JULIA = 1
    NEWTON = 2
    BURNING_SHIP = 3
    TRICORN = 4
    MULTIBROT = 5
    PHOENIX = 6
    SIERPINSKI = 7

class VisualizationMode(Enum):
    FRACTAL = 0
    FUNCTION_PLOT = 1
    PARAMETRIC = 2
    POLAR = 3
    COMPLEX_PLANE = 4
    ITERATION_MAP = 5

class ColorScheme(Enum):
    CLASSIC = 0
    RAINBOW = 1
    FIRE = 2
    ICE = 3
    ELECTRIC = 4
    SPECTRUM = 5

@dataclass
class MathFunction:
    """Mathematical function with parameters"""
    name: str
    expression: str
    func: Callable
    parameters: Dict[str, float]
    domain: Tuple[float, float]
    range_bounds: Tuple[float, float]
    
    def evaluate(self, x: float, **kwargs) -> float:
        """Evaluate function at point x"""
        params = {**self.parameters, **kwargs}
        try:
            return self.func(x, **params)
        except:
            return 0.0

class FractalCalculator:
    """High-performance fractal calculations"""
    
    @staticmethod
    def mandelbrot(c: complex, max_iter: int = 100) -> int:
        """Calculate Mandelbrot set iterations"""
        z = 0
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return max_iter
    
    @staticmethod
    def julia(z: complex, c: complex, max_iter: int = 100) -> int:
        """Calculate Julia set iterations"""
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return max_iter
    
    @staticmethod
    def newton(z: complex, max_iter: int = 100) -> int:
        """Newton fractal for z^3 - 1 = 0"""
        for n in range(max_iter):
            if abs(z) < 1e-6:
                return n
            try:
                z = z - (z**3 - 1) / (3 * z**2)
            except:
                return n
            if abs(z) > 10:
                return n
        return max_iter
    
    @staticmethod
    def burning_ship(c: complex, max_iter: int = 100) -> int:
        """Burning Ship fractal"""
        z = 0
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = complex(abs(z.real), abs(z.imag))**2 + c
        return max_iter
    
    @staticmethod
    def tricorn(c: complex, max_iter: int = 100) -> int:
        """Tricorn fractal"""
        z = 0
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z.conjugate()**2 + c
        return max_iter
    
    @staticmethod
    def multibrot(c: complex, power: float = 3.0, max_iter: int = 100) -> int:
        """Multibrot fractal with variable power"""
        z = 0
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z**power + c
        return max_iter

class ParameterController:
    """Interactive parameter control system"""
    def __init__(self):
        self.parameters = {
            'julia_real': -0.7269,
            'julia_imag': 0.1889,
            'multibrot_power': 3.0,
            'newton_root': 1.0,
            'color_offset': 0.0,
            'zoom': 1.0,
            'center_x': 0.0,
            'center_y': 0.0,
            'iterations': 100,
            'escape_radius': 2.0,
            'color_density': 1.0,
            'animation_speed': 1.0
        }
        
        self.parameter_ranges = {
            'julia_real': (-2.0, 2.0),
            'julia_imag': (-2.0, 2.0),
            'multibrot_power': (2.0, 6.0),
            'newton_root': (0.5, 3.0),
            'color_offset': (0.0, 1.0),
            'zoom': (0.1, 1000.0),
            'center_x': (-2.0, 2.0),
            'center_y': (-2.0, 2.0),
            'iterations': (10, 500),
            'escape_radius': (1.5, 10.0),
            'color_density': (0.1, 5.0),
            'animation_speed': (0.1, 5.0)
        }
        
        self.selected_parameter = 'julia_real'
    
    def get_value(self, param: str) -> float:
        """Get parameter value"""
        return self.parameters.get(param, 0.0)
    
    def set_value(self, param: str, value: float):
        """Set parameter value with bounds checking"""
        if param in self.parameter_ranges:
            min_val, max_val = self.parameter_ranges[param]
            self.parameters[param] = max(min_val, min(max_val, value))
    
    def adjust_selected(self, delta: float):
        """Adjust currently selected parameter"""
        current = self.get_value(self.selected_parameter)
        self.set_value(self.selected_parameter, current + delta)
    
    def cycle_parameter(self):
        """Cycle to next parameter"""
        params = list(self.parameters.keys())
        current_index = params.index(self.selected_parameter)
        self.selected_parameter = params[(current_index + 1) % len(params)]

class ColorMapper:
    """Advanced color mapping for mathematical visualization"""
    def __init__(self):
        self.scheme = ColorScheme.CLASSIC
        self.brightness = 1.0
        self.contrast = 1.0
        self.saturation = 1.0
        
    def map_iterations(self, iterations: int, max_iter: int, time_offset: float = 0) -> Tuple[int, int, int]:
        """Map iteration count to color"""
        if iterations >= max_iter:
            return (0, 0, 0)  # Black for points in set
        
        ratio = iterations / max_iter
        
        if self.scheme == ColorScheme.CLASSIC:
            return self._classic_scheme(ratio, time_offset)
        elif self.scheme == ColorScheme.RAINBOW:
            return self._rainbow_scheme(ratio, time_offset)
        elif self.scheme == ColorScheme.FIRE:
            return self._fire_scheme(ratio, time_offset)
        elif self.scheme == ColorScheme.ICE:
            return self._ice_scheme(ratio, time_offset)
        elif self.scheme == ColorScheme.ELECTRIC:
            return self._electric_scheme(ratio, time_offset)
        else:  # SPECTRUM
            return self._spectrum_scheme(ratio, time_offset)
    
    def _classic_scheme(self, ratio: float, time_offset: float) -> Tuple[int, int, int]:
        """Classic mathematical visualization colors"""
        r = int(255 * min(1.0, ratio * 2))
        g = int(255 * min(1.0, (ratio - 0.3) * 2))
        b = int(255 * min(1.0, (ratio - 0.6) * 2))
        return self._apply_adjustments(r, g, b)
    
    def _rainbow_scheme(self, ratio: float, time_offset: float) -> Tuple[int, int, int]:
        """Rainbow spectrum colors"""
        hue = (ratio + time_offset) % 1.0
        return self._hsv_to_rgb(hue, 1.0, 1.0)
    
    def _fire_scheme(self, ratio: float, time_offset: float) -> Tuple[int, int, int]:
        """Fire-like colors"""
        r = int(255 * min(1.0, ratio * 1.5))
        g = int(255 * min(1.0, (ratio - 0.2) * 2))
        b = int(100 * max(0, ratio - 0.8))
        return self._apply_adjustments(r, g, b)
    
    def _ice_scheme(self, ratio: float, time_offset: float) -> Tuple[int, int, int]:
        """Ice-like colors"""
        r = int(100 * max(0, ratio - 0.8))
        g = int(255 * min(1.0, (ratio - 0.2) * 2))
        b = int(255 * min(1.0, ratio * 1.5))
        return self._apply_adjustments(r, g, b)
    
    def _electric_scheme(self, ratio: float, time_offset: float) -> Tuple[int, int, int]:
        """Electric/neon colors"""
        phase = ratio * math.pi * 2 + time_offset
        r = int(128 + 127 * math.sin(phase))
        g = int(128 + 127 * math.sin(phase + 2.1))
        b = int(128 + 127 * math.sin(phase + 4.2))
        return self._apply_adjustments(r, g, b)
    
    def _spectrum_scheme(self, ratio: float, time_offset: float) -> Tuple[int, int, int]:
        """Scientific spectrum colors"""
        wavelength = 380 + ratio * 400  # Visible spectrum
        return self._wavelength_to_rgb(wavelength)
    
    def _hsv_to_rgb(self, h: float, s: float, v: float) -> Tuple[int, int, int]:
        """Convert HSV to RGB"""
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
        
        return self._apply_adjustments(int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))
    
    def _wavelength_to_rgb(self, wavelength: float) -> Tuple[int, int, int]:
        """Convert wavelength to RGB color"""
        if wavelength < 380 or wavelength > 780:
            return (0, 0, 0)
        
        if 380 <= wavelength <= 440:
            r = -(wavelength - 440) / (440 - 380)
            g = 0
            b = 1
        elif 440 <= wavelength <= 490:
            r = 0
            g = (wavelength - 440) / (490 - 440)
            b = 1
        elif 490 <= wavelength <= 510:
            r = 0
            g = 1
            b = -(wavelength - 510) / (510 - 490)
        elif 510 <= wavelength <= 580:
            r = (wavelength - 510) / (580 - 510)
            g = 1
            b = 0
        elif 580 <= wavelength <= 645:
            r = 1
            g = -(wavelength - 645) / (645 - 580)
            b = 0
        elif 645 <= wavelength <= 780:
            r = 1
            g = 0
            b = 0
        
        return self._apply_adjustments(int(r * 255), int(g * 255), int(b * 255))
    
    def _apply_adjustments(self, r: int, g: int, b: int) -> Tuple[int, int, int]:
        """Apply brightness, contrast, and saturation adjustments"""
        # Apply brightness
        r = min(255, int(r * self.brightness))
        g = min(255, int(g * self.brightness))
        b = min(255, int(b * self.brightness))
        
        # Apply contrast
        r = min(255, max(0, int((r - 128) * self.contrast + 128)))
        g = min(255, max(0, int((g - 128) * self.contrast + 128)))
        b = min(255, max(0, int((b - 128) * self.contrast + 128)))
        
        return (r, g, b)

class FunctionPlotter:
    """Function plotting and visualization"""
    def __init__(self):
        self.functions = {
            'sine': MathFunction('sin(x)', 'sin(x)', lambda x, **k: math.sin(x), {}, (-math.pi*2, math.pi*2), (-1, 1)),
            'cosine': MathFunction('cos(x)', 'cos(x)', lambda x, **k: math.cos(x), {}, (-math.pi*2, math.pi*2), (-1, 1)),
            'exponential': MathFunction('exp(x)', 'e^x', lambda x, **k: math.exp(min(x, 10)), {}, (-3, 3), (0, 20)),
            'logarithm': MathFunction('log(x)', 'ln(x)', lambda x, **k: math.log(max(x, 0.001)), {}, (0.1, 10), (-3, 3)),
            'polynomial': MathFunction('x^n', 'x^n', lambda x, n=2, **k: x**n, {'n': 2}, (-3, 3), (-10, 10)),
            'tangent': MathFunction('tan(x)', 'tan(x)', lambda x, **k: math.tan(x), {}, (-math.pi/2*0.9, math.pi/2*0.9), (-10, 10)),
            'hyperbolic': MathFunction('sinh(x)', 'sinh(x)', lambda x, **k: math.sinh(min(x, 10)), {}, (-3, 3), (-10, 10))
        }
        
        self.current_function = 'sine'
        self.parametric_t = 0.0
    
    def plot_function(self, surface, func_name: str, width: int, height: int, **params):
        """Plot function on surface"""
        if func_name not in self.functions:
            return
        
        func = self.functions[func_name]
        domain_start, domain_end = func.domain
        
        points = []
        for x_pixel in range(width):
            # Map pixel to domain
            x = domain_start + (x_pixel / width) * (domain_end - domain_start)
            
            try:
                y = func.evaluate(x, **params)
                
                # Map y to pixel coordinates
                y_range = func.range_bounds[1] - func.range_bounds[0]
                y_pixel = height - int((y - func.range_bounds[0]) / y_range * height)
                
                if 0 <= y_pixel < height:
                    points.append((x_pixel, y_pixel))
            except:
                continue
        
        # Draw function
        if len(points) > 1:
            pygame.draw.lines(surface, MATH_COLORS['function'], False, points, 2)

class MathematicalExplorer:
    """Main mathematical exploration class"""
    def __init__(self):
        self.fractal_type = FractalType.MANDELBROT
        self.visualization_mode = VisualizationMode.FRACTAL
        self.parameter_controller = ParameterController()
        self.color_mapper = ColorMapper()
        self.function_plotter = FunctionPlotter()
        self.fractal_calculator = FractalCalculator()
        
        # View settings
        self.view_center = complex(0, 0)
        self.view_zoom = 1.0
        self.pixel_size = 2
        self.max_iterations = 100
        
        # Animation
        self.animate = False
        self.animation_time = 0.0
        
        # UI state
        self.show_hud = True
        self.show_parameters = True
        self.show_equations = False
        self.paused = False
        
        # Educational content
        self.show_info = False
        self.current_explanation = ""
        
        # Performance optimization
        self.grid_cache = {}
        self.last_calculation_time = 0
        
        self.fractal_names = {
            FractalType.MANDELBROT: "Mandelbrot Set",
            FractalType.JULIA: "Julia Set",
            FractalType.NEWTON: "Newton Fractal",
            FractalType.BURNING_SHIP: "Burning Ship",
            FractalType.TRICORN: "Tricorn",
            FractalType.MULTIBROT: "Multibrot",
            FractalType.PHOENIX: "Phoenix",
            FractalType.SIERPINSKI: "Sierpinski"
        }
        
        self.mode_names = {
            VisualizationMode.FRACTAL: "Fractal Explorer",
            VisualizationMode.FUNCTION_PLOT: "Function Plotter",
            VisualizationMode.PARAMETRIC: "Parametric Curves",
            VisualizationMode.POLAR: "Polar Coordinates",
            VisualizationMode.COMPLEX_PLANE: "Complex Plane",
            VisualizationMode.ITERATION_MAP: "Iteration Mapping"
        }
    
    def calculate_fractal_point(self, x: int, y: int) -> int:
        """Calculate fractal value for screen coordinates"""
        # Map screen to complex plane
        real = self.view_center.real + (x - WIDTH/2) / (WIDTH/2) / self.view_zoom
        imag = self.view_center.imag + (y - HEIGHT/2) / (HEIGHT/2) / self.view_zoom
        
        if self.fractal_type == FractalType.MANDELBROT:
            return self.fractal_calculator.mandelbrot(complex(real, imag), self.max_iterations)
        elif self.fractal_type == FractalType.JULIA:
            c = complex(
                self.parameter_controller.get_value('julia_real'),
                self.parameter_controller.get_value('julia_imag')
            )
            return self.fractal_calculator.julia(complex(real, imag), c, self.max_iterations)
        elif self.fractal_type == FractalType.NEWTON:
            return self.fractal_calculator.newton(complex(real, imag), self.max_iterations)
        elif self.fractal_type == FractalType.BURNING_SHIP:
            return self.fractal_calculator.burning_ship(complex(real, imag), self.max_iterations)
        elif self.fractal_type == FractalType.TRICORN:
            return self.fractal_calculator.tricorn(complex(real, imag), self.max_iterations)
        elif self.fractal_type == FractalType.MULTIBROT:
            power = self.parameter_controller.get_value('multibrot_power')
            return self.fractal_calculator.multibrot(complex(real, imag), power, self.max_iterations)
        else:
            return 0
    
    def render_fractal(self, surface):
        """Render fractal to surface"""
        pixel_array = pygame.surfarray.array3d(surface)
        
        for x in range(0, WIDTH, self.pixel_size):
            for y in range(0, HEIGHT, self.pixel_size):
                iterations = self.calculate_fractal_point(x, y)
                color = self.color_mapper.map_iterations(
                    iterations, 
                    self.max_iterations, 
                    self.animation_time * self.parameter_controller.get_value('animation_speed')
                )
                
                # Fill pixel block
                for px in range(x, min(x + self.pixel_size, WIDTH)):
                    for py in range(y, min(y + self.pixel_size, HEIGHT)):
                        if px < WIDTH and py < HEIGHT:
                            pixel_array[px][py] = color
        
        pygame.surfarray.blit_array(surface, pixel_array)
    
    def render_function_plot(self, surface):
        """Render function plot"""
        surface.fill(CYBER_BLACK)
        
        # Draw grid
        self.draw_grid(surface)
        
        # Plot current function
        params = {
            'n': self.parameter_controller.get_value('multibrot_power'),
            'a': self.parameter_controller.get_value('julia_real'),
            'b': self.parameter_controller.get_value('julia_imag')
        }
        
        self.function_plotter.plot_function(
            surface, 
            self.function_plotter.current_function, 
            WIDTH, 
            HEIGHT, 
            **params
        )
    
    def draw_grid(self, surface):
        """Draw coordinate grid"""
        grid_color = (50, 50, 50)
        
        # Vertical lines
        for x in range(0, WIDTH, 40):
            pygame.draw.line(surface, grid_color, (x, 0), (x, HEIGHT))
        
        # Horizontal lines
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(surface, grid_color, (0, y), (WIDTH, y))
        
        # Axes
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        pygame.draw.line(surface, NEON_GREEN, (center_x, 0), (center_x, HEIGHT), 2)
        pygame.draw.line(surface, NEON_GREEN, (0, center_y), (WIDTH, center_y), 2)
    
    def update_animation(self, dt: float):
        """Update animation"""
        if self.animate and not self.paused:
            self.animation_time += dt
            
            # Animate parameters
            if self.fractal_type == FractalType.JULIA:
                # Animate Julia constant
                julia_real = math.sin(self.animation_time * 0.5) * 0.7
                julia_imag = math.cos(self.animation_time * 0.3) * 0.7
                self.parameter_controller.set_value('julia_real', julia_real)
                self.parameter_controller.set_value('julia_imag', julia_imag)
    
    def draw_hud(self, surface):
        """Draw heads-up display"""
        if not self.show_hud:
            return
        
        # HUD background
        hud_rect = pygame.Rect(0, 0, WIDTH, 80)
        pygame.draw.rect(surface, (0, 0, 0, 180), hud_rect)
        
        # Current mode and fractal
        font = pygame.font.Font(None, 20)
        mode_text = f"Mode: {self.mode_names[self.visualization_mode]}"
        text = font.render(mode_text, True, NEON_CYAN)
        surface.blit(text, (10, 10))
        
        if self.visualization_mode == VisualizationMode.FRACTAL:
            fractal_text = f"Fractal: {self.fractal_names[self.fractal_type]}"
            text = font.render(fractal_text, True, NEON_GREEN)
            surface.blit(text, (10, 30))
        
        # View parameters
        zoom_text = f"Zoom: {self.view_zoom:.2e}"
        text = font.render(zoom_text, True, NEON_YELLOW)
        surface.blit(text, (250, 10))
        
        iter_text = f"Iterations: {self.max_iterations}"
        text = font.render(iter_text, True, NEON_ORANGE)
        surface.blit(text, (250, 30))
        
        # Performance info
        fps = clock.get_fps()
        perf_text = f"FPS: {fps:.1f}"
        text = font.render(perf_text, True, NEON_RED if fps < 30 else NEON_GREEN)
        surface.blit(text, (250, 50))
        
        # Animation status
        if self.animate:
            anim_text = "ANIMATING"
            text = font.render(anim_text, True, NEON_PURPLE)
            surface.blit(text, (10, 50))
    
    def draw_parameter_panel(self, surface):
        """Draw parameter control panel"""
        if not self.show_parameters:
            return
        
        panel_rect = pygame.Rect(WIDTH - 180, 90, 170, 200)
        pygame.draw.rect(surface, (0, 0, 0, 200), panel_rect)
        pygame.draw.rect(surface, NEON_CYAN, panel_rect, 2)
        
        font = pygame.font.Font(None, 16)
        title_text = font.render("PARAMETERS", True, NEON_CYAN)
        surface.blit(title_text, (WIDTH - 175, 95))
        
        y_offset = 115
        for i, (param, value) in enumerate(self.parameter_controller.parameters.items()):
            if i >= 8:  # Limit display
                break
            
            color = NEON_YELLOW if param == self.parameter_controller.selected_parameter else NEON_GREEN
            param_text = f"{param}: {value:.3f}"
            text = font.render(param_text, True, color)
            surface.blit(text, (WIDTH - 175, y_offset))
            y_offset += 18
    
    def draw_controls(self, surface):
        """Draw control instructions"""
        controls_rect = pygame.Rect(10, HEIGHT - 100, 460, 90)
        pygame.draw.rect(surface, (0, 0, 0, 180), controls_rect)
        
        font = pygame.font.Font(None, 14)
        controls = [
            "WASD - Navigate  |  Mouse Wheel - Zoom  |  M - Mode  |  F - Fractal",
            "TAB - Parameter  |  +/- - Adjust  |  A - Animate  |  C - Color",
            "P - Parameters  |  I - Info  |  H - HUD  |  R - Reset",
            "F8 - Fullscreen  |  ESC - Return to Launcher"
        ]
        
        for i, control in enumerate(controls):
            text = font.render(control, True, NEON_YELLOW)
            surface.blit(text, (15, HEIGHT - 95 + i * 18))
    
    def draw_info_panel(self, surface):
        """Draw educational information panel"""
        if not self.show_info:
            return
        
        info_rect = pygame.Rect(50, 50, WIDTH - 100, HEIGHT - 100)
        pygame.draw.rect(surface, (0, 0, 0, 220), info_rect)
        pygame.draw.rect(surface, NEON_PURPLE, info_rect, 3)
        
        font = pygame.font.Font(None, 18)
        title_text = font.render("MATHEMATICAL INFO", True, NEON_PURPLE)
        surface.blit(title_text, (60, 60))
        
        # Get current explanation
        info_text = self.get_current_explanation()
        lines = info_text.split('\n')
        
        y_offset = 85
        for line in lines[:8]:  # Limit lines
            if line.strip():
                text = font.render(line, True, NEON_GREEN)
                surface.blit(text, (60, y_offset))
            y_offset += 20
    
    def get_current_explanation(self) -> str:
        """Get explanation for current visualization"""
        if self.visualization_mode == VisualizationMode.FRACTAL:
            if self.fractal_type == FractalType.MANDELBROT:
                return """The Mandelbrot Set:
z[n+1] = z[n]^2 + c
Where c is the position in complex plane.
Points that don't escape to infinity
are in the set (shown in black).
Color shows escape time."""
            elif self.fractal_type == FractalType.JULIA:
                return """Julia Sets:
z[n+1] = z[n]^2 + c
Where c is a constant and z starts
at each point in the complex plane.
Different c values create different
Julia sets. Related to Mandelbrot."""
            elif self.fractal_type == FractalType.NEWTON:
                return """Newton Fractal:
Uses Newton's method to find roots
of z^3 - 1 = 0. Different colors
show which root each point converges
to. Shows basins of attraction."""
        
        return "Mathematical visualization\nExplore equations and their\ngraphical representations."
    
    def handle_input(self, keys, events):
        """Handle user input"""
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.cycle_visualization_mode()
                elif event.key == pygame.K_f:
                    self.cycle_fractal_type()
                elif event.key == pygame.K_c:
                    self.cycle_color_scheme()
                elif event.key == pygame.K_TAB:
                    self.parameter_controller.cycle_parameter()
                elif event.key == pygame.K_a:
                    self.animate = not self.animate
                elif event.key == pygame.K_p:
                    self.show_parameters = not self.show_parameters
                elif event.key == pygame.K_i:
                    self.show_info = not self.show_info
                elif event.key == pygame.K_h:
                    self.show_hud = not self.show_hud
                elif event.key == pygame.K_r:
                    self.reset_view()
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.parameter_controller.adjust_selected(0.1)
                elif event.key == pygame.K_MINUS:
                    self.parameter_controller.adjust_selected(-0.1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Mouse wheel up
                    self.view_zoom *= 1.2
                elif event.button == 5:  # Mouse wheel down
                    self.view_zoom /= 1.2
        
        # Continuous input
        move_speed = 0.1 / self.view_zoom
        if keys[pygame.K_w]:
            self.view_center = complex(self.view_center.real, self.view_center.imag - move_speed)
        if keys[pygame.K_s]:
            self.view_center = complex(self.view_center.real, self.view_center.imag + move_speed)
        if keys[pygame.K_a]:
            self.view_center = complex(self.view_center.real - move_speed, self.view_center.imag)
        if keys[pygame.K_d]:
            self.view_center = complex(self.view_center.real + move_speed, self.view_center.imag)
        
        if keys[pygame.K_UP]:
            self.max_iterations = min(500, self.max_iterations + 5)
        if keys[pygame.K_DOWN]:
            self.max_iterations = max(10, self.max_iterations - 5)
    
    def cycle_visualization_mode(self):
        """Cycle to next visualization mode"""
        modes = list(VisualizationMode)
        current_index = modes.index(self.visualization_mode)
        self.visualization_mode = modes[(current_index + 1) % len(modes)]
    
    def cycle_fractal_type(self):
        """Cycle to next fractal type"""
        fractals = list(FractalType)
        current_index = fractals.index(self.fractal_type)
        self.fractal_type = fractals[(current_index + 1) % len(fractals)]
    
    def cycle_color_scheme(self):
        """Cycle to next color scheme"""
        schemes = list(ColorScheme)
        current_index = schemes.index(self.color_mapper.scheme)
        self.color_mapper.scheme = schemes[(current_index + 1) % len(schemes)]
    
    def reset_view(self):
        """Reset view to default"""
        self.view_center = complex(0, 0)
        self.view_zoom = 1.0
        self.max_iterations = 100
        self.animation_time = 0.0

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
    
    # Initialize explorer
    explorer = MathematicalExplorer()
    
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
        explorer.handle_input(keys, events)
        
        # Update animation
        explorer.update_animation(dt)
        
        # Clear screen
        screen.fill(CYBER_BLACK)
        
        # Render based on mode
        if explorer.visualization_mode == VisualizationMode.FRACTAL:
            explorer.render_fractal(screen)
        elif explorer.visualization_mode == VisualizationMode.FUNCTION_PLOT:
            explorer.render_function_plot(screen)
        else:
            # Other visualization modes
            explorer.render_function_plot(screen)
        
        # Draw UI
        explorer.draw_hud(screen)
        explorer.draw_parameter_panel(screen)
        explorer.draw_controls(screen)
        explorer.draw_info_panel(screen)
        
        # Update display
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 