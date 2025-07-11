#!/usr/bin/env python3
"""
Interactive Art Program Launcher for Raspberry Pi 5
RETRO CYBERPUNK PIXEL ART LAUNCHER
Cross-platform compatible (Pi 5 + Mac)
"""

import os
import sys
import subprocess
import pygame
import time
import math
import random

# Initialize Pygame for the launcher
pygame.init()

# Screen dimensions (optimized for 3.5" Pi display)
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("◉ CYBER.ART.TERMINAL ◉ Retro Computing Mode")

# Cyberpunk color palette
NEON_CYAN = (0, 255, 255)
NEON_PINK = (255, 20, 147)
NEON_GREEN = (57, 255, 20)
NEON_PURPLE = (191, 64, 191)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 165, 0)
NEON_BLUE = (100, 150, 255)
CYBER_BLACK = (10, 10, 25)
CYBER_DARK = (25, 25, 50)
CYBER_GRAY = (60, 60, 80)
TERMINAL_GREEN = (0, 200, 0)

# Load or create pixel font
def create_pixel_font(size):
    """Create or load pixel-style font for cross-platform compatibility"""
    try:
        # Try to load a pixel font if available
        font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'pixel.ttf')
        if os.path.exists(font_path):
            return pygame.font.Font(font_path, size)
    except:
        pass
    
    # Fallback to system font with pixel-like appearance
    return pygame.font.Font(None, size)

# Enhanced Art programs list with cyberpunk descriptions
ART_PROGRAMS = [
    ("01_dark_ages_rpg.py", "DARK.AGES.RPG", "Medieval fantasy RPG ◇ Economy & Politics"),
    ("02_particle_fire.py", "PYRO.SIM", "Thermal dynamics engine ◇ Wind control"),
    ("03_matrix_rain.py", "MATRIX.TERM", "Data stream visualizer ◇ 6 encodings"),
    ("05_starfield.py", "WARP.DRIVE", "Hyperspace navigator ◇ 4 warp modes"),
    ("06_game_of_life.py", "LIFE.SIM", "Cellular automaton lab ◇ 4 rule sets"),
    ("09_spiral_galaxy.py", "COSMOS.SIM", "Stellar formation model ◇ Gravity"),
    ("10_lightning_effect.py", "TESLA.LAB", "Electrical discharge sim ◇ 6 colors"),
    ("11_water_ripples.py", "FLUID.DYN", "Wave interference engine ◇ Physics"),
]

# Control information for cyberpunk interface
CONTROL_INFO = {
    "01_dark_ages_rpg.py": [
        "▶ ARROW.KEYS NAVIGATE ◇ ENTER CONFIRM",
        "▶ [I] INVENTORY ◇ [C] CHARACTER.SHEET",
        "▶ [Q] QUEST.LOG ◇ [S] SAVE.GAME",
        "▶ [ESC] RETURN.LAUNCHER ◇ [F8] FULLSCREEN"
    ],
    "02_particle_fire.py": [
        "▶ ↑↓ THERMAL.INTENSITY ◇ ←→ WIND.FORCE",
        "▶ [F] FIRE.TYPE ◇ [C] COLOR.MODE",
        "▶ [S] SPARK.TOGGLE ◇ [ESC] EXIT.SYS"
    ],
    "03_matrix_rain.py": [
        "▶ ↑↓ DATA.SPEED ◇ ←→ STREAM.DENSITY",
        "▶ [S] CHAR.SET ◇ [C] COLOR.MODE",
        "▶ [M] RAIN.PATTERN ◇ [ESC] EXIT.SYS"
    ],
    "05_starfield.py": [
        "▶ ↑↓ WARP.SPEED ◇ WASD NAV.CONTROL",
        "▶ [C] STAR.COLOR ◇ [M] WARP.MODE",
        "▶ [T] TWINKLE.FX ◇ [ESC] EXIT.SYS"
    ],
    "06_game_of_life.py": [
        "▶ [SPACE] PLAY/PAUSE ◇ MOUSE DRAW.CELLS",
        "▶ [L] RULE.SET ◇ [V] COLOR.MODE",
        "▶ [P] PATTERN.GEN ◇ [ESC] EXIT.SYS"
    ],
    "09_spiral_galaxy.py": [
        "▶ ↑↓ ROTATION.SPEED ◇ ←→ GRAVITY.FORCE",
        "▶ [C] COLOR.MODE ◇ [G] GALAXY.TYPE",
        "▶ [S] STELLAR.FORMATION ◇ [ESC] EXIT.SYS"
    ],
    "10_lightning_effect.py": [
        "▶ ↑↓ STRIKE.FREQ ◇ ←→ BOLT.POWER",
        "▶ [C] ENERGY.COLOR ◇ [B] BOLT.TYPE",
        "▶ [S] STORM.MODE ◇ [ESC] EXIT.SYS"
    ],
    "11_water_ripples.py": [
        "▶ CLICK CREATE.RIPPLES ◇ ↑↓ WAVE.SPEED",
        "▶ [C] COLOR.MODE ◇ [W] WAVE.TYPE",
        "▶ [P] PHYSICS.MODE ◇ [ESC] EXIT.SYS"
    ]
}

class CyberpunkLauncherUI:
    """Advanced retro-cyberpunk UI system"""
    
    def __init__(self):
        self.font_title = create_pixel_font(28)
        self.font_large = create_pixel_font(20)
        self.font_medium = create_pixel_font(16)
        self.font_small = create_pixel_font(14)
        self.font_tiny = create_pixel_font(12)
        
        # Animation variables
        self.glow_phase = 0
        self.scanline_offset = 0
        self.terminal_cursor = 0
        self.matrix_drops = []
        self.boot_sequence = []
        
        # Initialize matrix rain background
        for x in range(0, WIDTH, 20):
            self.matrix_drops.append({
                'x': x,
                'y': random.randint(-HEIGHT, 0),
                'speed': random.uniform(1, 4),
                'char': random.choice('010110100101')
            })
    
    def draw_matrix_background(self, surface):
        """Draw animated matrix code background"""
        # Update matrix drops
        for drop in self.matrix_drops:
            drop['y'] += drop['speed']
            if drop['y'] > HEIGHT:
                drop['y'] = -20
                drop['char'] = random.choice('010110100101')
            
            # Draw fading trail
            for i in range(5):
                alpha = max(0, 100 - i * 20)
                color = (0, alpha, 0)
                char_y = drop['y'] - i * 15
                if char_y > 0:
                    char_text = self.font_tiny.render(drop['char'], True, color)
                    surface.blit(char_text, (drop['x'], char_y))
    
    def draw_scanlines(self, surface):
        """Draw enhanced CRT-style scanlines"""
        self.scanline_offset = (self.scanline_offset + 1) % 6
        
        # Primary scanlines
        for y in range(self.scanline_offset, HEIGHT, 6):
            alpha = 40 + 20 * math.sin(time.time() * 3 + y * 0.1)
            pygame.draw.line(surface, (0, 0, 0, int(alpha)), (0, y), (WIDTH, y))
        
        # Secondary interference lines
        for y in range(0, HEIGHT, 3):
            if random.random() < 0.05:
                alpha = random.randint(20, 60)
                pygame.draw.line(surface, (alpha, alpha, alpha), (0, y), (WIDTH, y))
    
    def draw_glowing_border(self, surface, rect, color, thickness=2):
        """Enhanced glowing neon border"""
        self.glow_phase += 0.08
        
        # Multiple glow layers
        for i in range(thickness * 2, 0, -1):
            alpha = int(80 + 40 * math.sin(self.glow_phase) * (thickness * 2 - i + 1) / (thickness * 2))
            glow_color = tuple(max(0, min(255, c + alpha//3)) for c in color)
            
            border_rect = pygame.Rect(rect.x - i, rect.y - i, 
                                    rect.width + 2*i, rect.height + 2*i)
            pygame.draw.rect(surface, glow_color, border_rect, 1)
    
    def draw_cyber_panel(self, surface, rect, title="", corners=True):
        """Enhanced cyberpunk panel with animations"""
        # Main panel with transparency
        panel_surface = pygame.Surface((rect.width, rect.height))
        panel_surface.set_alpha(220)
        panel_surface.fill(CYBER_BLACK)
        surface.blit(panel_surface, rect)
        
        # Animated border
        border_colors = [NEON_CYAN, NEON_PINK, NEON_GREEN, NEON_PURPLE]
        color_index = int(time.time() * 2) % len(border_colors)
        self.draw_glowing_border(surface, rect, border_colors[color_index], 3)
        
        # Corner circuit decorations
        if corners:
            corner_size = 12
            corners_pos = [
                (rect.x, rect.y),
                (rect.x + rect.width - corner_size, rect.y),
                (rect.x, rect.y + rect.height - corner_size),
                (rect.x + rect.width - corner_size, rect.y + rect.height - corner_size)
            ]
            
            for i, (corner_x, corner_y) in enumerate(corners_pos):
                corner_color = border_colors[(i + int(time.time())) % len(border_colors)]
                
                # Draw circuit pattern
                pygame.draw.rect(surface, corner_color, 
                               (corner_x + 2, corner_y + 2, corner_size - 4, corner_size - 4))
                pygame.draw.rect(surface, CYBER_BLACK, 
                               (corner_x + 4, corner_y + 4, corner_size - 8, corner_size - 8))
                
                # Circuit lines
                pygame.draw.line(surface, corner_color,
                               (corner_x + 6, corner_y + 2),
                               (corner_x + 6, corner_y + corner_size - 2))
                pygame.draw.line(surface, corner_color,
                               (corner_x + 2, corner_y + 6),
                               (corner_x + corner_size - 2, corner_y + 6))
        
        # Title bar with animation
        if title:
            title_rect = pygame.Rect(rect.x + 20, rect.y - 18, rect.width - 40, 22)
            title_surface = pygame.Surface((title_rect.width, title_rect.height))
            title_surface.fill(CYBER_BLACK)
            title_surface.set_alpha(240)
            surface.blit(title_surface, title_rect)
            
            # Animated title text with proper color clamping
            pulse = 1.0 + 0.2 * math.sin(time.time() * 4)
            title_color = tuple(max(0, min(255, int(c * pulse))) for c in NEON_GREEN)
            title_text = self.font_small.render(f"▶ {title} ◀", True, title_color)
            title_pos = (title_rect.x + 8, title_rect.y + 3)
            surface.blit(title_text, title_pos)
    
    def draw_cyber_text(self, surface, text, pos, color=NEON_CYAN, font=None, glow=True, flicker=False):
        """Enhanced cyberpunk text with effects"""
        if font is None:
            font = self.font_small
        
        # Text flicker effect
        if flicker and random.random() < 0.05:
            return
        
        # Glow effect
        if glow:
            glow_offsets = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            for offset in glow_offsets:
                glow_pos = (pos[0] + offset[0], pos[1] + offset[1])
                glow_color = tuple(max(0, min(255, c//5)) for c in color)
                glow_text = font.render(text, True, glow_color)
                surface.blit(glow_text, glow_pos)
        
        # Main text with potential color shift
        main_color = color
        if random.random() < 0.02:  # Rare color glitch
            main_color = random.choice([NEON_PINK, NEON_YELLOW, NEON_PURPLE])
        
        main_text = font.render(text, True, main_color)
        surface.blit(main_text, pos)
    
    def draw_terminal_cursor(self, surface, pos):
        """Draw blinking terminal cursor"""
        self.terminal_cursor = (self.terminal_cursor + 1) % 60
        if self.terminal_cursor < 30:
            cursor_rect = pygame.Rect(pos[0], pos[1], 2, 16)
            pygame.draw.rect(surface, NEON_GREEN, cursor_rect)
    
    def draw_progress_bar(self, surface, rect, value, max_value, color=NEON_GREEN):
        """Enhanced cyberpunk progress bar with animations"""
        # Background
        pygame.draw.rect(surface, CYBER_DARK, rect)
        self.draw_glowing_border(surface, rect, color, 1)
        
        if max_value > 0:
            fill_width = int((value / max_value) * (rect.width - 4))
            fill_rect = pygame.Rect(rect.x + 2, rect.y + 2, fill_width, rect.height - 4)
            
            # Animated fill with segments
            segment_width = 8
            for i in range(0, fill_width, segment_width):
                segment_rect = pygame.Rect(rect.x + 2 + i, rect.y + 2, 
                                         min(segment_width - 1, fill_width - i), rect.height - 4)
                
                # Segment color with animation and proper color clamping
                pulse = 0.8 + 0.2 * math.sin(time.time() * 8 + i * 0.3)
                segment_color = tuple(max(0, min(255, int(c * pulse))) for c in color)
                pygame.draw.rect(surface, segment_color, segment_rect)
    
    def draw_holographic_lines(self, surface):
        """Draw holographic scanning lines effect"""
        scan_y = int((time.time() * 50) % HEIGHT)
        
        # Main scan line
        for thickness in range(5, 0, -1):
            alpha = 100 - thickness * 15
            scan_color = (*NEON_CYAN, alpha)
            pygame.draw.line(surface, scan_color[:3], 
                           (0, scan_y + thickness), (WIDTH, scan_y + thickness))
        
        # Secondary random glitch lines
        if random.random() < 0.1:
            glitch_y = random.randint(0, HEIGHT)
            glitch_color = random.choice([NEON_PINK, NEON_YELLOW, NEON_PURPLE])
            pygame.draw.line(surface, glitch_color, (0, glitch_y), (WIDTH, glitch_y))

class InteractiveArtLauncher:
    def __init__(self):
        self.ui = CyberpunkLauncherUI()
        self.selected_index = 0
        self.scroll_offset = 0
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.show_controls = False
        self.boot_complete = False
        self.boot_timer = 0
        
        # Boot sequence messages
        self.boot_messages = [
            "INITIALIZING NEURAL INTERFACE...",
            "LOADING PIXEL ART MATRIX...",
            "CONNECTING TO CYBER NETWORK...",
            "ESTABLISHING RETRO PROTOCOLS...",
            "ACTIVATING VISUAL SYNTHESIZERS...",
            "SYSTEM READY - WELCOME TO THE GRID"
        ]
        self.current_boot_msg = 0
    
    def draw_boot_sequence(self, surface):
        """Draw cyberpunk boot sequence"""
        surface.fill(CYBER_BLACK)
        
        # Boot progress
        self.boot_timer += 1
        
        if self.boot_timer < 180:  # 3 seconds at 60fps
            # Boot messages
            y_pos = HEIGHT // 2 - 60
            
            for i in range(min(self.current_boot_msg + 1, len(self.boot_messages))):
                if i == self.current_boot_msg:
                    # Current message with typing effect
                    msg = self.boot_messages[i]
                    char_count = min(len(msg), (self.boot_timer - i * 30) // 2)
                    displayed_msg = msg[:char_count]
                    
                    if char_count < len(msg):
                        displayed_msg += "_"  # Cursor
                else:
                    displayed_msg = self.boot_messages[i]
                
                color = NEON_GREEN if i == self.current_boot_msg else CYBER_GRAY
                self.ui.draw_cyber_text(surface, displayed_msg, (50, y_pos), color, 
                                       self.ui.font_small, False)
                y_pos += 25
            
            # Progress bar
            progress = self.boot_timer / 180
            bar_rect = pygame.Rect(50, HEIGHT - 80, WIDTH - 100, 20)
            self.ui.draw_progress_bar(surface, bar_rect, progress, 1.0, NEON_CYAN)
            
            # Update current message
            if self.boot_timer > (self.current_boot_msg + 1) * 30:
                self.current_boot_msg = min(self.current_boot_msg + 1, len(self.boot_messages) - 1)
            
            # Scanlines during boot
            self.ui.draw_scanlines(surface)
            
            return False
        else:
            self.boot_complete = True
            return True
    
    def draw_animated_background(self):
        """Draw enhanced animated background"""
        # Matrix rain background
        self.ui.draw_matrix_background(screen)
        
        # Circuit board pattern
        for x in range(0, WIDTH, 40):
            for y in range(0, HEIGHT, 40):
                current_time = time.time() - self.start_time
                phase = current_time + x * 0.01 + y * 0.01
                
                if math.sin(phase) > 0.8:
                    circuit_color = (*CYBER_DARK, 100)
                    pygame.draw.rect(screen, circuit_color[:3], (x, y, 2, 2))
        
        # Holographic scanning effect
        self.ui.draw_holographic_lines(screen)
    
    def draw_title(self):
        """Draw enhanced cyberpunk title"""
        current_time = time.time() - self.start_time
        
        # Main title with rainbow cycling
        title_colors = [NEON_CYAN, NEON_PINK, NEON_GREEN, NEON_PURPLE, NEON_YELLOW, NEON_ORANGE]
        color_index = int(current_time * 3) % len(title_colors)
        title_color = title_colors[color_index]
        
        # Glitch effect occasionally
        if random.random() < 0.02:
            title_color = random.choice(title_colors)
        
        # Main title with enhanced styling
        title = self.ui.font_title.render("◉ CYBER.ART.TERMINAL ◉", True, title_color)
        title_rect = title.get_rect(center=(WIDTH // 2, 25))
        
        # Draw title with glow
        for offset in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
            glow_pos = (title_rect.x + offset[0], title_rect.y + offset[1])
            glow_color = tuple(max(0, min(255, c//4)) for c in title_color)
            glow_title = self.ui.font_title.render("◉ CYBER.ART.TERMINAL ◉", True, glow_color)
            screen.blit(glow_title, glow_pos)
        
        screen.blit(title, title_rect)
        
        # Animated subtitle
        bounce_offset = int(2 * math.sin(current_time * 6))
        subtitle = self.ui.font_medium.render("RETRO.COMPUTING.MODE", True, TERMINAL_GREEN)
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 50 + bounce_offset))
        screen.blit(subtitle, subtitle_rect)
        
        # System info
        sys_info = self.ui.font_tiny.render("Raspberry Pi 5 ◇ 3.5\" Display ◇ Cross-Platform", True, CYBER_GRAY)
        sys_rect = sys_info.get_rect(center=(WIDTH // 2, 70))
        screen.blit(sys_info, sys_rect)
    
    def draw_menu(self):
        """Draw enhanced cyberpunk menu"""
        start_y = 95
        item_height = 35
        visible_items = 5
        
        # Calculate scroll
        if self.selected_index >= self.scroll_offset + visible_items:
            self.scroll_offset = self.selected_index - visible_items + 1
        elif self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        
        # Menu panel background
        menu_rect = pygame.Rect(5, start_y - 10, WIDTH - 10, visible_items * item_height + 15)
        self.ui.draw_cyber_panel(screen, menu_rect, "PROGRAM.SELECTION.MATRIX", False)
        
        # Draw menu items
        for i in range(visible_items):
            item_index = i + self.scroll_offset
            if item_index >= len(ART_PROGRAMS):
                break
            
            filename, title, description = ART_PROGRAMS[item_index]
            y_pos = start_y + i * item_height
            
            # Selection highlighting with animation
            if item_index == self.selected_index:
                # Animated selection background with proper color clamping
                pulse = 0.3 + 0.2 * math.sin(time.time() * 8)
                bg_color = tuple(max(0, min(255, int(c * pulse))) for c in NEON_CYAN)
                select_rect = pygame.Rect(15, y_pos - 2, WIDTH - 30, item_height - 8)
                
                # Draw selection with glow
                pygame.draw.rect(screen, bg_color, select_rect)
                self.ui.draw_glowing_border(screen, select_rect, NEON_CYAN, 2)
                
                title_color = CYBER_BLACK
                desc_color = CYBER_BLACK
                num_color = CYBER_BLACK
            else:
                title_color = TERMINAL_GREEN
                desc_color = CYBER_GRAY
                num_color = NEON_YELLOW
            
            # Enhanced program number with hex styling
            num_text = self.ui.font_medium.render(f"0x{item_index:02X}", True, num_color)
            screen.blit(num_text, (20, y_pos + 2))
            
            # Program title with enhancement indicators
            enhanced = "★" if filename in CONTROL_INFO else "○"
            title_full = f"{enhanced} {title}"
            title_text = self.ui.font_medium.render(title_full, True, title_color)
            screen.blit(title_text, (70, y_pos + 2))
            
            # Description with cyberpunk styling
            desc_text = self.ui.font_tiny.render(description, True, desc_color)
            screen.blit(desc_text, (70, y_pos + 18))
    
    def draw_controls_panel(self):
        """Draw enhanced controls panel"""
        if not self.show_controls:
            return
        
        filename, title, description = ART_PROGRAMS[self.selected_index]
        
        # Controls panel
        panel_rect = pygame.Rect(WIDTH - 230, 95, 225, 200)
        self.ui.draw_cyber_panel(screen, panel_rect, "CONTROL.INTERFACE")
        
        y_offset = 120
        if filename in CONTROL_INFO:
            for control in CONTROL_INFO[filename]:
                color = random.choice([NEON_GREEN, NEON_CYAN, NEON_YELLOW])
                self.ui.draw_cyber_text(screen, control, (WIDTH - 220, y_offset), 
                                       color, self.ui.font_tiny, False, True)
                y_offset += 18
        else:
            default_controls = [
                "▶ BASIC.PROGRAM.MODE",
                "▶ [ESC] EXIT.TO.LAUNCHER", 
                "▶ LIMITED.INTERACTIVITY",
                "▶ UPGRADE.RECOMMENDED"
            ]
            for control in default_controls:
                self.ui.draw_cyber_text(screen, control, (WIDTH - 220, y_offset), 
                                       CYBER_GRAY, self.ui.font_tiny, False)
                y_offset += 18
    
    def draw_instructions(self):
        """Draw enhanced instruction panel"""
        instructions_rect = pygame.Rect(10, HEIGHT - 80, WIDTH - 20, 70)
        self.ui.draw_cyber_panel(screen, instructions_rect, "NEURAL.COMMANDS")
        
        instructions = [
            "↑↓ NAVIGATE.MATRIX ◇ [ENTER] EXECUTE.PROGRAM ◇ [ESC] SHUTDOWN.SYS",
            "[R] RANDOM.SELECT ◇ [TAB] SHOW.CONTROLS ◇ [0-9] DIRECT.ACCESS"
        ]
        
        y_start = HEIGHT - 65
        for i, instruction in enumerate(instructions):
            colors = [NEON_CYAN, NEON_GREEN]
            self.ui.draw_cyber_text(screen, instruction, (20, y_start + i * 18), 
                                   colors[i], self.ui.font_tiny, False)
    
    def draw_system_monitor(self):
        """Draw system monitoring panel"""
        monitor_rect = pygame.Rect(WIDTH - 150, 10, 140, 80)
        self.ui.draw_cyber_panel(screen, monitor_rect, "SYS.MONITOR", False)
        
        # System stats
        current_time = time.time() - self.start_time
        cpu_usage = 50 + 30 * math.sin(current_time * 2)
        memory_usage = 60 + 20 * math.sin(current_time * 1.5)
        
        y_pos = 30
        
        # CPU usage
        cpu_rect = pygame.Rect(WIDTH - 140, y_pos, 80, 8)
        self.ui.draw_progress_bar(screen, cpu_rect, cpu_usage, 100, NEON_GREEN)
        self.ui.draw_cyber_text(screen, f"CPU:{cpu_usage:.0f}%", (WIDTH - 140, y_pos + 12), 
                               NEON_GREEN, self.ui.font_tiny, False)
        
        # Memory usage
        y_pos += 25
        mem_rect = pygame.Rect(WIDTH - 140, y_pos, 80, 8)
        self.ui.draw_progress_bar(screen, mem_rect, memory_usage, 100, NEON_CYAN)
        self.ui.draw_cyber_text(screen, f"MEM:{memory_usage:.0f}%", (WIDTH - 140, y_pos + 12), 
                               NEON_CYAN, self.ui.font_tiny, False)
        
        # Terminal cursor
        self.ui.draw_terminal_cursor(screen, (WIDTH - 50, y_pos + 12))
    
    def run_program(self, filename):
        """Execute selected program with enhanced feedback"""
        global screen
        try:
            # Show execution feedback
            exec_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 20, 200, 40)
            self.ui.draw_cyber_panel(screen, exec_rect, "EXECUTING")
            self.ui.draw_cyber_text(screen, f"LOADING {filename}...", 
                                   (WIDTH//2 - 80, HEIGHT//2 - 5), NEON_YELLOW)
            pygame.display.flip()
            time.sleep(0.5)
            
            pygame.quit()
            result = subprocess.run([sys.executable, filename], capture_output=False, text=True)
            
            # Restart launcher
            pygame.init()
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("◉ CYBER.ART.TERMINAL ◉ Retro Computing Mode")
            
        except Exception as e:
            print(f"ERROR: {filename}: {e}")
            try:
                pygame.init()
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("◉ CYBER.ART.TERMINAL ◉ Retro Computing Mode")
            except:
                pass
    
    def run_random_program(self):
        """Execute random program with dramatic effect"""
        filename, _, _ = random.choice(ART_PROGRAMS)
        self.run_program(filename)
    
    def run(self):
        """Main cyberpunk launcher loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if not self.boot_complete:
                        continue
                        
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(ART_PROGRAMS)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(ART_PROGRAMS)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        filename, _, _ = ART_PROGRAMS[self.selected_index]
                        self.run_program(filename)
                    elif event.key == pygame.K_r:
                        self.run_random_program()
                    elif event.key == pygame.K_TAB:
                        self.show_controls = not self.show_controls
                    elif event.key >= pygame.K_0 and event.key <= pygame.K_9:
                        num = event.key - pygame.K_0
                        if num == 0:
                            num = 10
                        num -= 1
                        if 0 <= num < len(ART_PROGRAMS):
                            filename, _, _ = ART_PROGRAMS[num]
                            self.run_program(filename)
            
            # Screen rendering
            screen.fill(CYBER_BLACK)
            
            if not self.boot_complete:
                if self.draw_boot_sequence(screen):
                    self.boot_complete = True
            else:
                self.draw_animated_background()
                self.draw_title()
                self.draw_menu()
                self.draw_controls_panel()
                self.draw_instructions()
                self.draw_system_monitor()
                
                # Global scanlines and effects
                self.ui.draw_scanlines(screen)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    launcher = InteractiveArtLauncher()
    launcher.run() 