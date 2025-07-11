#!/usr/bin/env python3
"""
Interactive Conway's Game of Life - Enhanced cellular automaton with pixel art
Perfect for Raspberry Pi 5 with 3.5" display
PIXEL ART INTERACTIVE VERSION
"""

import pygame
import numpy as np
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Game of Life")

clock = pygame.time.Clock()

# Grid settings
CELL_SIZE = 4
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

class InteractiveGameOfLife:
    def __init__(self):
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
        self.age_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
        self.pattern_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
        
        self.running = False
        self.speed = 10  # Updates per second
        self.last_update = time.time()
        self.generation = 0
        
        # Visual settings
        self.color_mode = 0
        self.show_grid = True
        self.show_age = True
        self.show_trails = False
        self.pixel_size = CELL_SIZE
        
        # Rule settings
        self.rule_set = 0  # 0: Classic, 1: HighLife, 2: Maze, 3: Coral
        self.wrap_edges = False
        
        # Drawing settings
        self.brush_size = 1
        self.drawing_mode = 0  # 0: Toggle, 1: Draw, 2: Erase
        
        # Pattern settings
        self.pattern_mode = 0  # 0: Random, 1: Glider, 2: Oscillator, 3: Still Life
        
        self.color_modes = {
            0: "Age Colors",
            1: "Neon Green",
            2: "Fire Palette",
            3: "Ocean Blue",
            4: "Retro CRT",
            5: "Binary"
        }
        
        self.rule_sets = {
            0: "Classic (23/3)",
            1: "HighLife (23/36)",
            2: "Maze (12345/3)",
            3: "Coral (45678/3)"
        }
        
        self.patterns = {
            0: "Random Fill",
            1: "Glider Pattern",
            2: "Oscillators",
            3: "Still Lifes"
        }
        
        self.randomize_grid()
    
    def randomize_grid(self, density=0.3):
        """Initialize grid with random cells"""
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
        self.age_grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
        
        if self.pattern_mode == 0:  # Random
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if random.random() < density:
                        self.grid[y][x] = 1
                        self.age_grid[y][x] = 1
        elif self.pattern_mode == 1:  # Gliders
            self.add_gliders()
        elif self.pattern_mode == 2:  # Oscillators
            self.add_oscillators()
        else:  # Still lifes
            self.add_still_lifes()
        
        self.generation = 0
    
    def add_gliders(self):
        """Add glider patterns"""
        glider_pattern = [[0, 1, 0], [0, 0, 1], [1, 1, 1]]
        
        for _ in range(5):
            x = random.randint(0, GRID_WIDTH - 3)
            y = random.randint(0, GRID_HEIGHT - 3)
            
            for dy in range(3):
                for dx in range(3):
                    if glider_pattern[dy][dx]:
                        self.grid[y + dy][x + dx] = 1
                        self.age_grid[y + dy][x + dx] = 1
    
    def add_oscillators(self):
        """Add oscillator patterns"""
        # Blinker
        for _ in range(3):
            x = random.randint(1, GRID_WIDTH - 2)
            y = random.randint(0, GRID_HEIGHT - 1)
            for dx in range(3):
                self.grid[y][x + dx - 1] = 1
                self.age_grid[y][x + dx - 1] = 1
        
        # Toad
        for _ in range(2):
            x = random.randint(1, GRID_WIDTH - 3)
            y = random.randint(1, GRID_HEIGHT - 2)
            toad_pattern = [[0, 1, 1, 1], [1, 1, 1, 0]]
            for dy in range(2):
                for dx in range(4):
                    if toad_pattern[dy][dx]:
                        self.grid[y + dy][x + dx] = 1
                        self.age_grid[y + dy][x + dx] = 1
    
    def add_still_lifes(self):
        """Add still life patterns"""
        # Block
        for _ in range(5):
            x = random.randint(0, GRID_WIDTH - 2)
            y = random.randint(0, GRID_HEIGHT - 2)
            for dy in range(2):
                for dx in range(2):
                    self.grid[y + dy][x + dx] = 1
                    self.age_grid[y + dy][x + dx] = 1
        
        # Beehive
        for _ in range(3):
            x = random.randint(1, GRID_WIDTH - 3)
            y = random.randint(1, GRID_HEIGHT - 3)
            beehive_pattern = [[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]]
            for dy in range(3):
                for dx in range(4):
                    if beehive_pattern[dy][dx]:
                        self.grid[y + dy][x + dx] = 1
                        self.age_grid[y + dy][x + dx] = 1
    
    def count_neighbors(self, x, y):
        """Count living neighbors around a cell"""
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                nx, ny = x + dx, y + dy
                
                if self.wrap_edges:
                    nx = nx % GRID_WIDTH
                    ny = ny % GRID_HEIGHT
                    count += self.grid[ny][nx]
                else:
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                        count += self.grid[ny][nx]
        return count
    
    def apply_rules(self, neighbors, alive):
        """Apply cellular automaton rules"""
        if self.rule_set == 0:  # Classic Conway's Game of Life
            if alive:
                return neighbors in [2, 3]
            else:
                return neighbors == 3
        elif self.rule_set == 1:  # HighLife
            if alive:
                return neighbors in [2, 3]
            else:
                return neighbors in [3, 6]
        elif self.rule_set == 2:  # Maze
            if alive:
                return neighbors in [1, 2, 3, 4, 5]
            else:
                return neighbors == 3
        else:  # Coral
            if alive:
                return neighbors in [4, 5, 6, 7, 8]
            else:
                return neighbors == 3
    
    def update_generation(self):
        """Update grid according to rules"""
        if not self.running:
            return
        
        current_time = time.time()
        if current_time - self.last_update < 1.0 / self.speed:
            return
        
        self.last_update = current_time
        
        new_grid = np.zeros_like(self.grid)
        new_age_grid = np.zeros_like(self.age_grid)
        
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                neighbors = self.count_neighbors(x, y)
                alive = self.grid[y][x] == 1
                
                if self.apply_rules(neighbors, alive):
                    new_grid[y][x] = 1
                    new_age_grid[y][x] = self.age_grid[y][x] + 1 if alive else 1
        
        self.grid = new_grid
        self.age_grid = new_age_grid
        self.generation += 1
    
    def get_cell_color(self, x, y):
        """Get color based on cell state and age"""
        if self.grid[y][x] == 0:
            return (0, 0, 0)  # Dead cells are black
        
        age = self.age_grid[y][x]
        
        if self.color_mode == 0:  # Age colors
            if age == 1:
                return (255, 255, 255)  # Newborn cells are white
            elif age < 5:
                return (255, 255 - age * 40, 0)  # Young cells are yellow-orange
            elif age < 10:
                return (255 - (age - 5) * 30, 100, 0)  # Mature cells are red
            else:
                return (100, 0, 100)  # Old cells are purple
        elif self.color_mode == 1:  # Neon green
            intensity = min(255, 150 + age * 10)
            return (0, intensity, 0)
        elif self.color_mode == 2:  # Fire palette
            if age < 3:
                return (255, 255, 0)  # Yellow
            elif age < 6:
                return (255, 150, 0)  # Orange
            else:
                return (255, 0, 0)  # Red
        elif self.color_mode == 3:  # Ocean blue
            intensity = min(255, 100 + age * 15)
            return (0, intensity // 2, intensity)
        elif self.color_mode == 4:  # Retro CRT
            if age < 3:
                return (0, 255, 0)  # Green
            elif age < 6:
                return (255, 255, 0)  # Yellow
            else:
                return (255, 0, 255)  # Magenta
        else:  # Binary
            return (255, 255, 255) if age % 2 == 0 else (100, 100, 100)
    
    def draw_grid(self, surface):
        """Draw the cellular automaton grid"""
        # Draw cells
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
    
    def handle_mouse_input(self, mouse_pos, mouse_pressed):
        """Handle mouse input for drawing"""
        if mouse_pressed[0]:  # Left click
            mouse_x, mouse_y = mouse_pos
            grid_x = mouse_x // self.pixel_size
            grid_y = mouse_y // self.pixel_size
            
            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                # Apply brush
                for dy in range(-self.brush_size + 1, self.brush_size):
                    for dx in range(-self.brush_size + 1, self.brush_size):
                        nx, ny = grid_x + dx, grid_y + dy
                        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                            if self.drawing_mode == 0:  # Toggle
                                self.grid[ny][nx] = 1 - self.grid[ny][nx]
                                self.age_grid[ny][nx] = 1 if self.grid[ny][nx] else 0
                            elif self.drawing_mode == 1:  # Draw
                                self.grid[ny][nx] = 1
                                self.age_grid[ny][nx] = 1
                            else:  # Erase
                                self.grid[ny][nx] = 0
                                self.age_grid[ny][nx] = 0
    
    def cycle_color_mode(self):
        """Cycle to next color mode"""
        self.color_mode = (self.color_mode + 1) % len(self.color_modes)
    
    def cycle_rule_set(self):
        """Cycle to next rule set"""
        self.rule_set = (self.rule_set + 1) % len(self.rule_sets)
    
    def cycle_pattern_mode(self):
        """Cycle to next pattern mode"""
        self.pattern_mode = (self.pattern_mode + 1) % len(self.patterns)
    
    def toggle_running(self):
        """Toggle simulation running state"""
        self.running = not self.running
    
    def step_once(self):
        """Step simulation once"""
        old_running = self.running
        self.running = True
        self.last_update = 0  # Force update
        self.update_generation()
        self.running = old_running
    
    def draw_ui(self, surface):
        """Draw UI information"""
        font = pygame.font.Font(None, 20)
        small_font = pygame.font.Font(None, 16)
        y_offset = 10
        
        # Current settings
        gen_text = font.render(f"Generation: {self.generation}", True, (255, 255, 255))
        surface.blit(gen_text, (10, y_offset))
        y_offset += 25
        
        speed_text = font.render(f"Speed: {self.speed} FPS", True, (255, 255, 255))
        surface.blit(speed_text, (10, y_offset))
        y_offset += 25
        
        rule_text = font.render(f"Rules: {self.rule_sets[self.rule_set]}", True, (255, 255, 255))
        surface.blit(rule_text, (10, y_offset))
        y_offset += 25
        
        color_text = font.render(f"Color: {self.color_modes[self.color_mode]}", True, (255, 255, 255))
        surface.blit(color_text, (10, y_offset))
        y_offset += 25
        
        # Status
        status_text = font.render(f"Status: {'RUNNING' if self.running else 'PAUSED'}", 
                                True, (0, 255, 0) if self.running else (255, 255, 0))
        surface.blit(status_text, (10, y_offset))
        y_offset += 25
        
        # Population count
        population = np.sum(self.grid)
        pop_text = font.render(f"Population: {population}", True, (255, 255, 255))
        surface.blit(pop_text, (10, y_offset))
        
        # Controls
        controls = [
            "SPACE: Play/Pause  S: Step  R: Reset  C: Clear",
            "↑↓ Speed  L: Rules  P: Pattern  V: Color",
            "G: Grid  W: Wrap  Mouse: Draw  B: Brush++",
            "ESC: Exit"
        ]
        
        for i, control in enumerate(controls):
            control_text = small_font.render(control, True, (200, 200, 200))
            surface.blit(control_text, (10, HEIGHT - 80 + i * 16))

def main():
    game = InteractiveGameOfLife()
    running = True
    show_ui = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    game.toggle_running()
                elif event.key == pygame.K_s:
                    game.step_once()
                elif event.key == pygame.K_r:
                    game.randomize_grid()
                elif event.key == pygame.K_c:
                    game.grid.fill(0)
                    game.age_grid.fill(0)
                    game.generation = 0
                elif event.key == pygame.K_l:
                    game.cycle_rule_set()
                elif event.key == pygame.K_p:
                    game.cycle_pattern_mode()
                elif event.key == pygame.K_v:
                    game.cycle_color_mode()
                elif event.key == pygame.K_g:
                    game.show_grid = not game.show_grid
                elif event.key == pygame.K_w:
                    game.wrap_edges = not game.wrap_edges
                elif event.key == pygame.K_b:
                    game.brush_size = min(game.brush_size + 1, 5)
                elif event.key == pygame.K_h:
                    show_ui = not show_ui
                elif event.key == pygame.K_UP:
                    game.speed = min(game.speed + 1, 30)
                elif event.key == pygame.K_DOWN:
                    game.speed = max(game.speed - 1, 1)
        
        # Handle mouse input
        game.handle_mouse_input(mouse_pos, mouse_pressed)
        
        # Update game
        game.update_generation()
        
        # Draw everything
        screen.fill((0, 0, 0))
        game.draw_grid(screen)
        
        # Draw UI if enabled
        if show_ui:
            # Semi-transparent background for UI
            ui_surface = pygame.Surface((280, 180))
            ui_surface.set_alpha(180)
            ui_surface.fill((0, 0, 0))
            screen.blit(ui_surface, (5, 5))
            
            game.draw_ui(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main() 