#!/usr/bin/env python3
"""
Advanced Cyberpunk Hacking Simulator - Interactive network infiltration
Perfect for Raspberry Pi 5 with 3.5" display (480x320)
COMPLETE HACKING SIMULATION WITH NETWORK INFILTRATION AND DATA MINING
"""

import pygame
import random
import math
import time
import sys
import subprocess
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Any

# Initialize Pygame
pygame.init()

# Screen dimensions optimized for Pi 5
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Cyberpunk Hacking Simulator")

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
HACK_COLORS = {
    'terminal': (50, 255, 150),
    'data_stream': (100, 200, 255),
    'firewall': (255, 100, 100),
    'ice': (200, 100, 255),
    'secure_node': (255, 255, 100),
    'breached': (100, 255, 100),
    'detected': (255, 50, 50),
    'stealth': (100, 100, 255),
    'exploit': (255, 150, 50),
    'payload': (255, 255, 255)
}

class NodeType(Enum):
    TERMINAL = 0
    DATABASE = 1
    FIREWALL = 2
    ICE = 3
    DATASTORE = 4
    ROUTER = 5
    SERVER = 6
    MAINFRAME = 7

class SecurityLevel(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    MILITARY = 3
    QUANTUM = 4

class HackingTool(Enum):
    SCANNER = 0
    EXPLOIT = 1
    STEALTH = 2
    DECRYPTOR = 3
    VIRUS = 4
    BACKDOOR = 5
    KEYLOGGER = 6
    DATA_MINER = 7

class GameMode(Enum):
    TUTORIAL = 0
    INFILTRATION = 1
    DATA_HEIST = 2
    CORPORATE_WAR = 3
    CYBER_DETECTIVE = 4

@dataclass
class NetworkNode:
    """Individual network node with security and data"""
    x: int
    y: int
    node_type: NodeType
    security_level: SecurityLevel
    is_breached: bool
    is_detected: bool
    data_value: int
    connections: List['NetworkNode']
    firewall_strength: float
    ice_strength: float
    encryption_level: int
    access_level: int
    contains_data: bool
    
    def __init__(self, x: int, y: int, node_type: NodeType):
        self.x = x
        self.y = y
        self.node_type = node_type
        self.security_level = random.choice(list(SecurityLevel))
        self.is_breached = False
        self.is_detected = False
        self.data_value = random.randint(10, 1000)
        self.connections = []
        self.firewall_strength = random.uniform(20, 100)
        self.ice_strength = random.uniform(10, 80)
        self.encryption_level = random.randint(1, 10)
        self.access_level = 0
        self.contains_data = random.random() < 0.6
        
        # Adjust properties based on node type
        if node_type == NodeType.FIREWALL:
            self.firewall_strength *= 2
        elif node_type == NodeType.ICE:
            self.ice_strength *= 2
        elif node_type == NodeType.MAINFRAME:
            self.data_value *= 5
            self.encryption_level += 5
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get node color based on state and type"""
        if self.is_detected:
            return HACK_COLORS['detected']
        elif self.is_breached:
            return HACK_COLORS['breached']
        elif self.node_type == NodeType.FIREWALL:
            return HACK_COLORS['firewall']
        elif self.node_type == NodeType.ICE:
            return HACK_COLORS['ice']
        elif self.node_type == NodeType.MAINFRAME:
            return HACK_COLORS['secure_node']
        elif self.node_type == NodeType.DATABASE:
            return NEON_PURPLE
        elif self.node_type == NodeType.DATASTORE:
            return NEON_YELLOW
        else:
            return HACK_COLORS['terminal']
    
    def get_size(self) -> int:
        """Get node size based on importance"""
        size_map = {
            NodeType.TERMINAL: 3,
            NodeType.DATABASE: 5,
            NodeType.FIREWALL: 4,
            NodeType.ICE: 4,
            NodeType.DATASTORE: 6,
            NodeType.ROUTER: 3,
            NodeType.SERVER: 5,
            NodeType.MAINFRAME: 8
        }
        return size_map.get(self.node_type, 3)

@dataclass
class DataPacket:
    """Data packet flowing through network"""
    x: float
    y: float
    target_x: float
    target_y: float
    packet_type: str
    value: int
    intercepted: bool
    encrypted: bool
    
    def __init__(self, start_x: float, start_y: float, end_x: float, end_y: float):
        self.x = start_x
        self.y = start_y
        self.target_x = end_x
        self.target_y = end_y
        self.packet_type = random.choice(['data', 'credit', 'intel', 'code'])
        self.value = random.randint(1, 100)
        self.intercepted = False
        self.encrypted = random.random() < 0.7
    
    def update(self, speed: float = 2.0):
        """Move packet toward target"""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > speed:
            self.x += (dx / distance) * speed
            self.y += (dy / distance) * speed
        else:
            self.x = self.target_x
            self.y = self.target_y
    
    def is_at_target(self) -> bool:
        """Check if packet reached target"""
        return abs(self.x - self.target_x) < 2 and abs(self.y - self.target_y) < 2

class HackingEngine:
    """Core hacking mechanics"""
    def __init__(self):
        self.stealth_level = 100.0
        self.detection_risk = 0.0
        self.available_tools = [HackingTool.SCANNER]
        self.skill_levels = {tool: 1 for tool in HackingTool}
        self.credits = 100
        self.reputation = 0
        self.heat_level = 0.0
        
    def attempt_breach(self, node: NetworkNode, tool: HackingTool) -> bool:
        """Attempt to breach a node"""
        # Calculate success probability
        tool_skill = self.skill_levels[tool]
        base_chance = 0.3
        
        # Tool effectiveness
        if tool == HackingTool.EXPLOIT and node.node_type != NodeType.FIREWALL:
            base_chance += 0.3
        elif tool == HackingTool.SCANNER:
            base_chance += 0.2
        elif tool == HackingTool.VIRUS and node.node_type in [NodeType.SERVER, NodeType.DATABASE]:
            base_chance += 0.4
        
        # Skill modifier
        skill_modifier = tool_skill * 0.1
        
        # Security modifier
        security_modifier = -node.security_level.value * 0.15
        
        # Stealth modifier
        stealth_modifier = (self.stealth_level / 100.0) * 0.2
        
        success_chance = base_chance + skill_modifier + security_modifier + stealth_modifier
        success_chance = max(0.05, min(0.95, success_chance))
        
        # Increase detection risk
        self.detection_risk += (1.0 - self.stealth_level / 100.0) * 10
        
        # Attempt breach
        if random.random() < success_chance:
            node.is_breached = True
            node.access_level = tool_skill
            self.skill_levels[tool] = min(10, self.skill_levels[tool] + 1)
            return True
        else:
            # Failed attempt increases detection risk
            self.detection_risk += 15
            if self.detection_risk > 50:
                node.is_detected = True
                self.heat_level += 10
            return False
    
    def extract_data(self, node: NetworkNode) -> int:
        """Extract data from breached node"""
        if not node.is_breached or not node.contains_data:
            return 0
        
        # Decryption skill affects extraction efficiency
        decryption_skill = self.skill_levels[HackingTool.DECRYPTOR]
        extraction_rate = min(1.0, decryption_skill / node.encryption_level)
        
        extracted = int(node.data_value * extraction_rate)
        node.data_value -= extracted
        
        if node.data_value <= 0:
            node.contains_data = False
        
        self.credits += extracted
        return extracted
    
    def deploy_stealth(self):
        """Deploy stealth countermeasures"""
        if HackingTool.STEALTH in self.available_tools:
            stealth_skill = self.skill_levels[HackingTool.STEALTH]
            self.stealth_level = min(100, self.stealth_level + stealth_skill * 10)
            self.detection_risk = max(0, self.detection_risk - stealth_skill * 5)
    
    def install_backdoor(self, node: NetworkNode) -> bool:
        """Install backdoor for persistent access"""
        if not node.is_breached or HackingTool.BACKDOOR not in self.available_tools:
            return False
        
        backdoor_skill = self.skill_levels[HackingTool.BACKDOOR]
        success_chance = backdoor_skill * 0.1
        
        if random.random() < success_chance:
            node.access_level = 10  # Permanent access
            return True
        return False

class NetworkTopology:
    """Manages network structure and connections"""
    def __init__(self, node_count: int = 20):
        self.nodes = []
        self.data_packets = []
        self.generate_network(node_count)
        
    def generate_network(self, node_count: int):
        """Generate network topology"""
        self.nodes.clear()
        
        # Create nodes
        for _ in range(node_count):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            node_type = random.choice(list(NodeType))
            node = NetworkNode(x, y, node_type)
            self.nodes.append(node)
        
        # Create connections
        for node in self.nodes:
            # Connect to nearby nodes
            nearby_nodes = [n for n in self.nodes if n != node and 
                          math.sqrt((n.x - node.x)**2 + (n.y - node.y)**2) < 80]
            
            # Random connections
            connection_count = random.randint(1, min(4, len(nearby_nodes)))
            connections = random.sample(nearby_nodes, connection_count)
            node.connections.extend(connections)
        
        # Ensure all nodes are connected
        self.ensure_connectivity()
    
    def ensure_connectivity(self):
        """Ensure all nodes are reachable"""
        if not self.nodes:
            return
        
        visited = set()
        to_visit = [self.nodes[0]]
        
        while to_visit:
            node = to_visit.pop()
            if node in visited:
                continue
            visited.add(node)
            to_visit.extend(node.connections)
        
        # Connect isolated nodes
        for node in self.nodes:
            if node not in visited:
                closest = min(visited, key=lambda n: math.sqrt((n.x - node.x)**2 + (n.y - node.y)**2))
                node.connections.append(closest)
                closest.connections.append(node)
                visited.add(node)
    
    def spawn_data_packet(self):
        """Spawn random data packet"""
        if len(self.nodes) < 2:
            return
        
        start_node = random.choice(self.nodes)
        end_node = random.choice([n for n in self.nodes if n != start_node])
        
        packet = DataPacket(start_node.x, start_node.y, end_node.x, end_node.y)
        self.data_packets.append(packet)
    
    def update_data_flow(self):
        """Update data packet movement"""
        for packet in self.data_packets[:]:
            packet.update()
            if packet.is_at_target():
                self.data_packets.remove(packet)
        
        # Spawn new packets occasionally
        if random.random() < 0.1:
            self.spawn_data_packet()
    
    def draw_network(self, surface):
        """Draw network visualization"""
        # Draw connections
        for node in self.nodes:
            for connected in node.connections:
                pygame.draw.line(surface, HACK_COLORS['data_stream'], 
                               (node.x, node.y), (connected.x, connected.y), 1)
        
        # Draw data packets
        for packet in self.data_packets:
            color = HACK_COLORS['payload'] if packet.encrypted else NEON_GREEN
            pygame.draw.circle(surface, color, (int(packet.x), int(packet.y)), 2)
        
        # Draw nodes
        for node in self.nodes:
            color = node.get_color()
            size = node.get_size()
            
            # Draw node
            pygame.draw.circle(surface, color, (node.x, node.y), size)
            
            # Draw node type indicator
            if node.node_type == NodeType.FIREWALL:
                pygame.draw.rect(surface, color, (node.x - 3, node.y - 3, 6, 6), 2)
            elif node.node_type == NodeType.ICE:
                pygame.draw.polygon(surface, color, 
                                  [(node.x, node.y - 5), (node.x - 4, node.y + 3), (node.x + 4, node.y + 3)])

class CyberpunkTerminal:
    """Simulated terminal interface"""
    def __init__(self):
        self.command_history = []
        self.current_command = ""
        self.output_buffer = []
        self.cursor_blink = 0
        self.font = pygame.font.Font(None, 16)
        
        # Available commands
        self.commands = {
            'scan': self.cmd_scan,
            'hack': self.cmd_hack,
            'extract': self.cmd_extract,
            'stealth': self.cmd_stealth,
            'status': self.cmd_status,
            'tools': self.cmd_tools,
            'help': self.cmd_help,
            'clear': self.cmd_clear
        }
        
        self.add_output(">>> NEUROMANCER TERMINAL V2.1 <<<")
        self.add_output("Type 'help' for available commands")
    
    def add_output(self, text: str):
        """Add text to output buffer"""
        self.output_buffer.append(text)
        if len(self.output_buffer) > 15:  # Keep only recent output
            self.output_buffer.pop(0)
    
    def execute_command(self, command: str, hacking_engine: HackingEngine, 
                       network: NetworkTopology, selected_node: Optional[NetworkNode]):
        """Execute terminal command"""
        self.command_history.append(command)
        self.add_output(f"> {command}")
        
        parts = command.split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd in self.commands:
            self.commands[cmd](args, hacking_engine, network, selected_node)
        else:
            self.add_output(f"Unknown command: {cmd}")
    
    def cmd_scan(self, args, hacking_engine, network, selected_node):
        """Scan network or node"""
        if selected_node:
            self.add_output(f"Scanning node at ({selected_node.x}, {selected_node.y})")
            self.add_output(f"Type: {selected_node.node_type.name}")
            self.add_output(f"Security: {selected_node.security_level.name}")
            self.add_output(f"Firewall: {selected_node.firewall_strength:.1f}")
            if selected_node.contains_data:
                self.add_output(f"Data value: {selected_node.data_value}")
        else:
            self.add_output(f"Network scan: {len(network.nodes)} nodes detected")
            breached = sum(1 for n in network.nodes if n.is_breached)
            self.add_output(f"Breached nodes: {breached}")
    
    def cmd_hack(self, args, hacking_engine, network, selected_node):
        """Hack selected node"""
        if not selected_node:
            self.add_output("No node selected")
            return
        
        tool = HackingTool.EXPLOIT
        if args:
            try:
                tool_name = args[0].upper()
                tool = HackingTool[tool_name]
            except KeyError:
                self.add_output(f"Unknown tool: {args[0]}")
                return
        
        if tool not in hacking_engine.available_tools:
            self.add_output(f"Tool {tool.name} not available")
            return
        
        success = hacking_engine.attempt_breach(selected_node, tool)
        if success:
            self.add_output(f"Successfully breached node!")
            self.add_output(f"Access level: {selected_node.access_level}")
        else:
            self.add_output("Breach attempt failed")
            self.add_output(f"Detection risk: {hacking_engine.detection_risk:.1f}%")
    
    def cmd_extract(self, args, hacking_engine, network, selected_node):
        """Extract data from node"""
        if not selected_node:
            self.add_output("No node selected")
            return
        
        if not selected_node.is_breached:
            self.add_output("Node not breached")
            return
        
        extracted = hacking_engine.extract_data(selected_node)
        if extracted > 0:
            self.add_output(f"Extracted {extracted} credits worth of data")
        else:
            self.add_output("No data to extract")
    
    def cmd_stealth(self, args, hacking_engine, network, selected_node):
        """Activate stealth mode"""
        hacking_engine.deploy_stealth()
        self.add_output(f"Stealth activated. Level: {hacking_engine.stealth_level:.1f}")
    
    def cmd_status(self, args, hacking_engine, network, selected_node):
        """Show status"""
        self.add_output("=== STATUS ===")
        self.add_output(f"Credits: {hacking_engine.credits}")
        self.add_output(f"Stealth: {hacking_engine.stealth_level:.1f}%")
        self.add_output(f"Detection: {hacking_engine.detection_risk:.1f}%")
        self.add_output(f"Heat Level: {hacking_engine.heat_level:.1f}")
    
    def cmd_tools(self, args, hacking_engine, network, selected_node):
        """List available tools"""
        self.add_output("=== TOOLS ===")
        for tool in hacking_engine.available_tools:
            skill = hacking_engine.skill_levels[tool]
            self.add_output(f"{tool.name}: Level {skill}")
    
    def cmd_help(self, args, hacking_engine, network, selected_node):
        """Show help"""
        self.add_output("=== COMMANDS ===")
        self.add_output("scan - Scan network/node")
        self.add_output("hack [tool] - Breach node")
        self.add_output("extract - Extract data")
        self.add_output("stealth - Activate stealth")
        self.add_output("status - Show status")
        self.add_output("tools - List tools")
    
    def cmd_clear(self, args, hacking_engine, network, selected_node):
        """Clear terminal"""
        self.output_buffer.clear()
    
    def draw(self, surface, x: int, y: int, width: int, height: int):
        """Draw terminal interface"""
        # Terminal background
        terminal_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, (0, 0, 0, 200), terminal_rect)
        pygame.draw.rect(surface, HACK_COLORS['terminal'], terminal_rect, 2)
        
        # Output text
        y_offset = y + 5
        for line in self.output_buffer:
            if y_offset < y + height - 20:
                text = self.font.render(line, True, HACK_COLORS['terminal'])
                surface.blit(text, (x + 5, y_offset))
                y_offset += 12
        
        # Command prompt
        prompt = f"> {self.current_command}"
        if int(time.time() * 2) % 2:  # Blinking cursor
            prompt += "_"
        
        prompt_text = self.font.render(prompt, True, NEON_GREEN)
        surface.blit(prompt_text, (x + 5, y + height - 15))

class CyberpunkHackingSimulator:
    """Main hacking simulation class"""
    def __init__(self):
        self.network = NetworkTopology()
        self.hacking_engine = HackingEngine()
        self.terminal = CyberpunkTerminal()
        self.game_mode = GameMode.TUTORIAL
        self.selected_node = None
        self.view_mode = 'network'  # 'network', 'terminal', 'split'
        self.paused = False
        
        # UI state
        self.show_hud = True
        self.show_connections = True
        self.show_data_flow = True
        self.zoom = 1.0
        self.camera_x = 0
        self.camera_y = 0
        
        # Mission system
        self.current_mission = None
        self.mission_objective = ""
        self.mission_progress = 0
        
        self.mode_names = {
            GameMode.TUTORIAL: "Tutorial Mode",
            GameMode.INFILTRATION: "Network Infiltration",
            GameMode.DATA_HEIST: "Data Heist",
            GameMode.CORPORATE_WAR: "Corporate Warfare",
            GameMode.CYBER_DETECTIVE: "Cyber Detective"
        }
        
        self.initialize_mission()
    
    def initialize_mission(self):
        """Initialize mission based on game mode"""
        if self.game_mode == GameMode.TUTORIAL:
            self.mission_objective = "Breach any node and extract data"
            self.hacking_engine.available_tools = [HackingTool.SCANNER, HackingTool.EXPLOIT]
        elif self.game_mode == GameMode.INFILTRATION:
            self.mission_objective = "Infiltrate mainframe without detection"
            self.hacking_engine.available_tools = list(HackingTool)[:4]
        elif self.game_mode == GameMode.DATA_HEIST:
            self.mission_objective = "Extract 1000 credits worth of data"
            self.hacking_engine.available_tools = list(HackingTool)
        elif self.game_mode == GameMode.CORPORATE_WAR:
            self.mission_objective = "Plant virus in all competitor systems"
            self.hacking_engine.available_tools = list(HackingTool)
        elif self.game_mode == GameMode.CYBER_DETECTIVE:
            self.mission_objective = "Trace data packets to find criminal network"
            self.hacking_engine.available_tools = [HackingTool.SCANNER, HackingTool.DATA_MINER]
    
    def update_simulation(self):
        """Update hacking simulation"""
        if self.paused:
            return
        
        # Update network data flow
        self.network.update_data_flow()
        
        # Decrease stealth over time
        self.hacking_engine.stealth_level = max(0, self.hacking_engine.stealth_level - 0.1)
        
        # Decrease detection risk over time
        self.hacking_engine.detection_risk = max(0, self.hacking_engine.detection_risk - 0.2)
        
        # Check mission progress
        self.check_mission_progress()
    
    def check_mission_progress(self):
        """Check mission completion"""
        if self.game_mode == GameMode.TUTORIAL:
            breached_with_data = any(n.is_breached and not n.contains_data for n in self.network.nodes)
            if breached_with_data:
                self.mission_progress = 100
        elif self.game_mode == GameMode.DATA_HEIST:
            if self.hacking_engine.credits >= 1000:
                self.mission_progress = 100
        # Add more mission checks as needed
    
    def handle_mouse_click(self, pos: Tuple[int, int]):
        """Handle mouse click for node selection"""
        mouse_x, mouse_y = pos
        
        # Find closest node to click
        closest_node = None
        min_distance = float('inf')
        
        for node in self.network.nodes:
            distance = math.sqrt((node.x - mouse_x)**2 + (node.y - mouse_y)**2)
            if distance < min_distance and distance < 20:
                min_distance = distance
                closest_node = node
        
        self.selected_node = closest_node
        if closest_node:
            self.terminal.add_output(f"Selected {closest_node.node_type.name} node")
    
    def draw_network_view(self, surface):
        """Draw network visualization"""
        # Draw network
        self.network.draw_network(surface)
        
        # Highlight selected node
        if self.selected_node:
            pygame.draw.circle(surface, NEON_YELLOW, 
                             (self.selected_node.x, self.selected_node.y), 
                             self.selected_node.get_size() + 3, 2)
        
        # Draw scanning effect
        if self.hacking_engine.detection_risk > 50:
            # Draw detection waves
            wave_radius = int(time.time() * 50) % 100
            for node in self.network.nodes:
                if node.is_detected:
                    pygame.draw.circle(surface, HACK_COLORS['detected'], 
                                     (node.x, node.y), wave_radius, 1)
    
    def draw_hud(self, surface):
        """Draw heads-up display"""
        if not self.show_hud:
            return
        
        # HUD background
        hud_rect = pygame.Rect(0, 0, WIDTH, 60)
        pygame.draw.rect(surface, (0, 0, 0, 180), hud_rect)
        
        # Game mode and mission
        font = pygame.font.Font(None, 18)
        mode_text = f"Mode: {self.mode_names[self.game_mode]}"
        text = font.render(mode_text, True, NEON_CYAN)
        surface.blit(text, (10, 10))
        
        # Mission objective
        mission_text = f"Objective: {self.mission_objective}"
        text = font.render(mission_text, True, NEON_GREEN)
        surface.blit(text, (10, 30))
        
        # Status indicators
        credits_text = f"Credits: {self.hacking_engine.credits}"
        text = font.render(credits_text, True, NEON_YELLOW)
        surface.blit(text, (300, 10))
        
        stealth_text = f"Stealth: {self.hacking_engine.stealth_level:.0f}%"
        color = NEON_GREEN if self.hacking_engine.stealth_level > 50 else NEON_RED
        text = font.render(stealth_text, True, color)
        surface.blit(text, (300, 30))
        
        # Detection warning
        if self.hacking_engine.detection_risk > 70:
            warning_text = "! DETECTION IMMINENT !"
            text = font.render(warning_text, True, NEON_RED)
            surface.blit(text, (WIDTH // 2 - 80, 45))
    
    def draw_controls(self, surface):
        """Draw control instructions"""
        if self.view_mode == 'terminal':
            return
        
        controls_rect = pygame.Rect(10, HEIGHT - 80, 460, 70)
        pygame.draw.rect(surface, (0, 0, 0, 180), controls_rect)
        
        font = pygame.font.Font(None, 14)
        controls = [
            "Click - Select Node  |  TAB - Toggle Terminal  |  M - Change Mode",
            "SPACE - Pause  |  H - Toggle HUD  |  V - Change View",
            "F8 - Fullscreen  |  ESC - Return to Launcher"
        ]
        
        for i, control in enumerate(controls):
            text = font.render(control, True, NEON_YELLOW)
            surface.blit(text, (15, HEIGHT - 75 + i * 15))
    
    def handle_input(self, keys, events):
        """Handle user input"""
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_TAB:
                    if self.view_mode == 'network':
                        self.view_mode = 'terminal'
                    elif self.view_mode == 'terminal':
                        self.view_mode = 'split'
                    else:
                        self.view_mode = 'network'
                elif event.key == pygame.K_m:
                    self.cycle_game_mode()
                elif event.key == pygame.K_v:
                    self.show_connections = not self.show_connections
                elif event.key == pygame.K_h:
                    self.show_hud = not self.show_hud
                elif event.key == pygame.K_r:
                    self.network.generate_network(20)
                    self.initialize_mission()
                elif self.view_mode in ['terminal', 'split']:
                    # Handle terminal input
                    if event.key == pygame.K_RETURN:
                        if self.terminal.current_command:
                            self.terminal.execute_command(
                                self.terminal.current_command,
                                self.hacking_engine,
                                self.network,
                                self.selected_node
                            )
                            self.terminal.current_command = ""
                    elif event.key == pygame.K_BACKSPACE:
                        if self.terminal.current_command:
                            self.terminal.current_command = self.terminal.current_command[:-1]
                    else:
                        # Add character to command
                        if event.unicode.isprintable():
                            self.terminal.current_command += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_mouse_click(event.pos)
    
    def cycle_game_mode(self):
        """Cycle to next game mode"""
        modes = list(GameMode)
        current_index = modes.index(self.game_mode)
        self.game_mode = modes[(current_index + 1) % len(modes)]
        self.initialize_mission()
        self.network.generate_network(20)

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
    simulator = CyberpunkHackingSimulator()
    
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
        
        # Draw based on view mode
        if simulator.view_mode == 'network':
            simulator.draw_network_view(screen)
        elif simulator.view_mode == 'terminal':
            simulator.terminal.draw(screen, 10, 70, WIDTH - 20, HEIGHT - 90)
        else:  # split view
            # Network view on left
            network_surface = pygame.Surface((WIDTH // 2, HEIGHT))
            network_surface.fill(CYBER_BLACK)
            simulator.draw_network_view(network_surface)
            screen.blit(network_surface, (0, 0))
            
            # Terminal on right
            simulator.terminal.draw(screen, WIDTH // 2 + 5, 70, WIDTH // 2 - 10, HEIGHT - 90)
        
        # Draw UI
        simulator.draw_hud(screen)
        simulator.draw_controls(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS for smooth hacking experience
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 