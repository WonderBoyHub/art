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

class AISecurityType(Enum):
    BASIC_ICE = 0
    ADAPTIVE_ICE = 1
    NEURAL_FIREWALL = 2
    QUANTUM_GUARDIAN = 3
    HIVE_MIND = 4
    SENTIENT_WATCHDOG = 5

class EncryptionType(Enum):
    BASIC = 0
    AES = 1
    RSA = 2
    QUANTUM = 3
    NEURAL = 4
    BLOCKCHAIN = 5

class SecurityProtocol(Enum):
    NONE = 0
    BASIC_AUTH = 1
    TWO_FACTOR = 2
    BIOMETRIC = 3
    QUANTUM_KEY = 4
    NEURAL_PATTERN = 5
    SOCIAL_PROOF = 6

class AttackVector(Enum):
    DIRECT_HACK = 0
    SOCIAL_ENGINEERING = 1
    PHYSICAL_ACCESS = 2
    INSIDER_THREAT = 3
    SUPPLY_CHAIN = 4
    ZERO_DAY = 5

class NetworkArchitecture(Enum):
    HIERARCHICAL = 0
    MESH = 1
    STAR = 2
    RING = 3
    FLAT = 4

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
    is_honeypot: bool = False # Added honeypot attribute
    
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
        self.is_honeypot = False
        
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

@dataclass
class AISecurityAgent:
    """AI-powered security agent that adapts to threats"""
    agent_type: AISecurityType
    learning_rate: float
    adaptation_level: int
    threat_patterns: List[str]
    response_protocols: List[str]
    memory_bank: Dict[str, float]
    active: bool
    
    def __init__(self, agent_type: AISecurityType):
        self.agent_type = agent_type
        self.learning_rate = random.uniform(0.1, 0.5)
        self.adaptation_level = random.randint(1, 5)
        self.threat_patterns = []
        self.response_protocols = []
        self.memory_bank = {}
        self.active = True
        
        # Initialize based on agent type
        if agent_type == AISecurityType.ADAPTIVE_ICE:
            self.learning_rate *= 1.5
            self.response_protocols = ['counterhack', 'trace', 'isolate']
        elif agent_type == AISecurityType.NEURAL_FIREWALL:
            self.response_protocols = ['pattern_match', 'behavior_analysis', 'anomaly_detect']
        elif agent_type == AISecurityType.QUANTUM_GUARDIAN:
            self.adaptation_level += 2
            self.response_protocols = ['quantum_entangle', 'probability_shift', 'observer_effect']
        elif agent_type == AISecurityType.HIVE_MIND:
            self.response_protocols = ['collective_response', 'distributed_analysis', 'swarm_attack']
        elif agent_type == AISecurityType.SENTIENT_WATCHDOG:
            self.learning_rate *= 2
            self.response_protocols = ['predictive_analysis', 'preemptive_strike', 'adaptive_shield']
    
    def learn_from_attack(self, attack_pattern: str, success: bool):
        """Learn from observed attack patterns"""
        if attack_pattern not in self.memory_bank:
            self.memory_bank[attack_pattern] = 0.0
        
        # Update memory based on attack success
        if success:
            self.memory_bank[attack_pattern] += self.learning_rate
        else:
            self.memory_bank[attack_pattern] -= self.learning_rate * 0.5
        
        # Adaptation
        if attack_pattern not in self.threat_patterns:
            self.threat_patterns.append(attack_pattern)
    
    def calculate_threat_level(self, attack_pattern: str) -> float:
        """Calculate threat level for given attack pattern"""
        base_threat = 0.5
        
        # Check memory bank
        if attack_pattern in self.memory_bank:
            memory_modifier = self.memory_bank[attack_pattern] * 0.1
            base_threat += memory_modifier
        
        # Adaptation level modifier
        adaptation_modifier = self.adaptation_level * 0.05
        base_threat += adaptation_modifier
        
        return max(0.0, min(1.0, base_threat))
    
    def generate_countermeasure(self, attack_pattern: str) -> str:
        """Generate appropriate countermeasure"""
        threat_level = self.calculate_threat_level(attack_pattern)
        
        if threat_level > 0.8:
            return random.choice(['lockdown', 'counterhack', 'trace_origin'])
        elif threat_level > 0.6:
            return random.choice(['increase_encryption', 'pattern_scramble', 'decoy_deploy'])
        elif threat_level > 0.4:
            return random.choice(['alert_admin', 'log_activity', 'minor_countermeasure'])
        else:
            return 'monitor'

class HackingEngine:
    """Enhanced hacking mechanics with AI countermeasures"""
    def __init__(self):
        self.stealth_level = 100.0
        self.detection_risk = 0.0
        self.available_tools = [HackingTool.SCANNER]
        self.skill_levels = {tool: 1 for tool in HackingTool}
        self.credits = 100
        self.reputation = 0
        self.heat_level = 0.0
        
        # Advanced hacking capabilities
        self.ai_assistant_active = False
        self.quantum_tools_unlocked = False
        self.social_engineering_profile = {}
        self.zero_day_exploits = 1
        self.neural_patterns_analyzed = set()
        self.forensic_cleaning_available = True
        self.botnet_size = 0
        
        # Countermeasures tracking
        self.active_countermeasures = []
        self.traced_connections = []
        self.honeypot_detected = []
        
    def enhance_ai_capabilities(self):
        """Unlock AI-enhanced hacking capabilities"""
        self.ai_assistant_active = True
        self.skill_levels[HackingTool.SCANNER] += 2
        self.skill_levels[HackingTool.STEALTH] += 2
        
    def unlock_quantum_tools(self):
        """Unlock quantum hacking tools"""
        self.quantum_tools_unlocked = True
        if HackingTool.DECRYPTOR not in self.available_tools:
            self.available_tools.append(HackingTool.DECRYPTOR)
    
    def develop_social_profile(self, target_info: Dict[str, Any]):
        """Develop social engineering profile"""
        self.social_engineering_profile.update(target_info)
        
    def attempt_advanced_breach(self, node: NetworkNode, tool: HackingTool, ai_agent: Optional[AISecurityAgent] = None) -> Dict[str, Any]:
        """Attempt advanced breach with AI countermeasures"""
        attack_pattern = f"{tool.name.lower()}_attack"
        
        # Check if AI agent is present and active
        if ai_agent and ai_agent.active:
            threat_level = ai_agent.calculate_threat_level(attack_pattern)
            countermeasure = ai_agent.generate_countermeasure(attack_pattern)
            
            # Apply countermeasure
            if countermeasure == 'lockdown':
                return {'success': False, 'message': 'System locked down by AI security'}
            elif countermeasure == 'counterhack':
                self.heat_level += 25
                return {'success': False, 'message': 'Counterhack detected! Heat level increased'}
            elif countermeasure == 'trace_origin':
                self.traced_connections.append(node)
                self.detection_risk += 30
                return {'success': False, 'message': 'Connection traced! High detection risk'}
            elif countermeasure == 'pattern_scramble':
                # Make future attacks harder
                self.skill_levels[tool] = max(1, self.skill_levels[tool] - 1)
                return {'success': False, 'message': 'Security patterns scrambled'}
        
        # Standard breach attempt
        success = self.attempt_breach(node, tool)
        
        # AI learning from attack
        if ai_agent:
            ai_agent.learn_from_attack(attack_pattern, success)
        
        if success:
            return {'success': True, 'message': 'Breach successful'}
        else:
            return {'success': False, 'message': 'Breach failed'}
    
    def deploy_advanced_stealth(self):
        """Deploy advanced stealth with AI assistance"""
        base_stealth = 20
        
        if self.ai_assistant_active:
            base_stealth += 15
        
        if self.quantum_tools_unlocked:
            base_stealth += 10
        
        self.stealth_level = min(100, self.stealth_level + base_stealth)
        self.detection_risk = max(0, self.detection_risk - base_stealth)
        
        if self.forensic_cleaning_available:
            self.clean_forensic_traces()
    
    def clean_forensic_traces(self):
        """Clean forensic evidence"""
        if self.forensic_cleaning_available:
            self.traced_connections.clear()
            self.heat_level = max(0, self.heat_level - 15)
            self.forensic_cleaning_available = False  # Limited use
    
    def analyze_neural_patterns(self, node: NetworkNode) -> Dict[str, Any]:
        """Analyze neural patterns in security systems"""
        node_id = id(node)
        
        if node_id in self.neural_patterns_analyzed:
            return {'success': True, 'message': 'Neural patterns already analyzed'}
        
        # Analyze neural patterns
        analysis_success = random.random() < (self.skill_levels[HackingTool.SCANNER] * 0.15)
        
        if analysis_success:
            self.neural_patterns_analyzed.add(node_id)
            # Increase effectiveness against neural security
            if hasattr(node, 'ai_agent') and node.ai_agent:
                node.ai_agent.adaptation_level = max(1, node.ai_agent.adaptation_level - 1)
            return {'success': True, 'message': 'Neural patterns analyzed and weakened'}
        else:
            return {'success': False, 'message': 'Neural pattern analysis failed'}
    
    def social_engineering_attack(self, target_info: Dict[str, Any]) -> Dict[str, Any]:
        """Perform social engineering attack"""
        if not self.social_engineering_profile:
            return {'success': False, 'message': 'No social engineering profile available'}
        
        # Calculate success based on profile completeness
        profile_completeness = len(self.social_engineering_profile) / 10.0
        social_skill = self.skill_levels.get(HackingTool.KEYLOGGER, 1)  # Using keylogger as social skill
        
        success_rate = min(0.8, profile_completeness * social_skill * 0.2)
        
        if random.random() < success_rate:
            return {'success': True, 'message': 'Social engineering successful', 'access_level': 'partial'}
        else:
            return {'success': False, 'message': 'Social engineering failed'}
    
    def deploy_zero_day_exploit(self, node: NetworkNode) -> Dict[str, Any]:
        """Deploy zero-day exploit"""
        if self.zero_day_exploits <= 0:
            return {'success': False, 'message': 'No zero-day exploits available'}
        
        self.zero_day_exploits -= 1
        
        # Zero-day has very high success rate
        if random.random() < 0.9:
            node.is_breached = True
            node.access_level = 10
            return {'success': True, 'message': 'Zero-day exploit successful - full access gained'}
        else:
            return {'success': False, 'message': 'Zero-day exploit failed'}
    
    def expand_botnet(self, compromised_node: NetworkNode):
        """Add compromised node to botnet"""
        if compromised_node.is_breached:
            self.botnet_size += 1
            # Botnet provides distributed computing power
            self.skill_levels[HackingTool.VIRUS] += 1
            
    def coordinate_distributed_attack(self, target_nodes: List[NetworkNode]) -> Dict[str, Any]:
        """Coordinate distributed attack using botnet"""
        if self.botnet_size < 3:
            return {'success': False, 'message': 'Insufficient botnet size for distributed attack'}
        
        success_count = 0
        
        for node in target_nodes:
            # Distributed attack has higher success rate
            enhanced_success_rate = min(0.7, self.botnet_size * 0.1)
            
            if random.random() < enhanced_success_rate:
                node.is_breached = True
                success_count += 1
        
        if success_count > 0:
            return {'success': True, 'message': f'Distributed attack breached {success_count} nodes'}
        else:
            return {'success': False, 'message': 'Distributed attack failed'}
    
    def quantum_entanglement_hack(self, node: NetworkNode) -> Dict[str, Any]:
        """Perform quantum entanglement hack"""
        if not self.quantum_tools_unlocked:
            return {'success': False, 'message': 'Quantum tools not available'}
        
        # Quantum hack bypasses traditional security
        quantum_success = random.random() < 0.6
        
        if quantum_success:
            node.is_breached = True
            # Quantum hack is stealthy
            self.detection_risk = max(0, self.detection_risk - 10)
            return {'success': True, 'message': 'Quantum entanglement hack successful'}
        else:
            return {'success': False, 'message': 'Quantum entanglement failed'}
    
    def attempt_breach(self, node: NetworkNode, tool: HackingTool) -> bool:
        """Original breach method for compatibility"""
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
    
    def get_hacking_report(self) -> Dict[str, Any]:
        """Get comprehensive hacking report"""
        return {
            'stealth_level': self.stealth_level,
            'detection_risk': self.detection_risk,
            'heat_level': self.heat_level,
            'botnet_size': self.botnet_size,
            'neural_patterns_analyzed': len(self.neural_patterns_analyzed),
            'zero_day_exploits': self.zero_day_exploits,
            'ai_assistant': self.ai_assistant_active,
            'quantum_tools': self.quantum_tools_unlocked,
            'traced_connections': len(self.traced_connections),
            'active_countermeasures': len(self.active_countermeasures)
        }

class NetworkTopology:
    """Enhanced network structure with AI security agents"""
    def __init__(self, node_count: int = 20):
        self.nodes = []
        self.data_packets = []
        self.ai_security_agents = []
        self.honeypots = []
        self.network_architecture = random.choice(list(NetworkArchitecture))
        self.security_level = random.choice(list(SecurityLevel))
        self.generate_advanced_network(node_count)
        
    def generate_advanced_network(self, node_count: int):
        """Generate advanced network topology with AI security"""
        self.nodes.clear()
        self.ai_security_agents.clear()
        self.honeypots.clear()
        
        # Create nodes based on network architecture
        if self.network_architecture == NetworkArchitecture.HIERARCHICAL:
            self.generate_hierarchical_network(node_count)
        elif self.network_architecture == NetworkArchitecture.MESH:
            self.generate_mesh_network(node_count)
        elif self.network_architecture == NetworkArchitecture.STAR:
            self.generate_star_network(node_count)
        elif self.network_architecture == NetworkArchitecture.RING:
            self.generate_ring_network(node_count)
        else:
            self.generate_flat_network(node_count)
        
        # Add AI security agents to critical nodes
        self.deploy_ai_security()
        
        # Add honeypots
        self.deploy_honeypots()
        
        # Ensure connectivity
        self.ensure_connectivity()
        
    def generate_hierarchical_network(self, node_count: int):
        """Generate hierarchical network structure"""
        # Core layer (1-2 mainframes)
        core_nodes = min(2, node_count // 10)
        for i in range(core_nodes):
            x = WIDTH // 2 + random.randint(-50, 50)
            y = HEIGHT // 4 + random.randint(-30, 30)
            node = NetworkNode(x, y, NodeType.MAINFRAME)
            node.security_level = SecurityLevel.MILITARY
            self.nodes.append(node)
        
        # Distribution layer (firewalls and servers)
        dist_nodes = min(6, node_count // 4)
        for i in range(dist_nodes):
            x = random.randint(100, WIDTH - 100)
            y = HEIGHT // 2 + random.randint(-50, 50)
            node_type = NodeType.FIREWALL if i % 2 == 0 else NodeType.SERVER
            node = NetworkNode(x, y, node_type)
            node.security_level = SecurityLevel.HIGH
            self.nodes.append(node)
        
        # Access layer (terminals and databases)
        remaining_nodes = node_count - len(self.nodes)
        for i in range(remaining_nodes):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(3 * HEIGHT // 4, HEIGHT - 50)
            node_type = random.choice([NodeType.TERMINAL, NodeType.DATABASE, NodeType.DATASTORE])
            node = NetworkNode(x, y, node_type)
            self.nodes.append(node)
    
    def generate_mesh_network(self, node_count: int):
        """Generate mesh network structure"""
        for i in range(node_count):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            node_type = random.choice(list(NodeType))
            node = NetworkNode(x, y, node_type)
            self.nodes.append(node)
    
    def generate_star_network(self, node_count: int):
        """Generate star network structure"""
        # Central hub
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        hub = NetworkNode(center_x, center_y, NodeType.MAINFRAME)
        hub.security_level = SecurityLevel.MILITARY
        self.nodes.append(hub)
        
        # Spoke nodes
        for i in range(node_count - 1):
            angle = (2 * math.pi * i) / (node_count - 1)
            radius = random.randint(80, 120)
            x = center_x + int(radius * math.cos(angle))
            y = center_y + int(radius * math.sin(angle))
            node_type = random.choice(list(NodeType))
            node = NetworkNode(x, y, node_type)
            self.nodes.append(node)
    
    def generate_ring_network(self, node_count: int):
        """Generate ring network structure"""
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        radius = 100
        
        for i in range(node_count):
            angle = (2 * math.pi * i) / node_count
            x = center_x + int(radius * math.cos(angle))
            y = center_y + int(radius * math.sin(angle))
            node_type = random.choice(list(NodeType))
            node = NetworkNode(x, y, node_type)
            self.nodes.append(node)
    
    def generate_flat_network(self, node_count: int):
        """Generate flat network structure (original)"""
        for _ in range(node_count):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            node_type = random.choice(list(NodeType))
            node = NetworkNode(x, y, node_type)
            self.nodes.append(node)
    
    def deploy_ai_security(self):
        """Deploy AI security agents to critical nodes"""
        critical_nodes = [n for n in self.nodes if n.node_type in [NodeType.MAINFRAME, NodeType.FIREWALL, NodeType.ICE]]
        
        for node in critical_nodes:
            if random.random() < 0.7:  # 70% chance for critical nodes
                agent_type = random.choice(list(AISecurityType))
                
                # Adjust agent type based on node type
                if node.node_type == NodeType.MAINFRAME:
                    agent_type = random.choice([AISecurityType.QUANTUM_GUARDIAN, AISecurityType.SENTIENT_WATCHDOG])
                elif node.node_type == NodeType.FIREWALL:
                    agent_type = AISecurityType.NEURAL_FIREWALL
                elif node.node_type == NodeType.ICE:
                    agent_type = AISecurityType.ADAPTIVE_ICE
                
                ai_agent = AISecurityAgent(agent_type)
                node.ai_agent = ai_agent
                self.ai_security_agents.append(ai_agent)
        
        # Some regular nodes might also have basic AI
        regular_nodes = [n for n in self.nodes if not hasattr(n, 'ai_agent')]
        for node in random.sample(regular_nodes, min(3, len(regular_nodes))):
            if random.random() < 0.2:  # 20% chance for regular nodes
                ai_agent = AISecurityAgent(AISecurityType.BASIC_ICE)
                node.ai_agent = ai_agent
                self.ai_security_agents.append(ai_agent)
    
    def deploy_honeypots(self):
        """Deploy honeypot nodes to detect attacks"""
        honeypot_count = max(1, len(self.nodes) // 10)  # 10% of nodes are honeypots
        
        for _ in range(honeypot_count):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            # Honeypots look like valuable targets
            node_type = random.choice([NodeType.DATABASE, NodeType.SERVER])
            honeypot = NetworkNode(x, y, node_type)
            honeypot.is_honeypot = True
            honeypot.data_value *= 2  # Make it look more valuable
            honeypot.security_level = SecurityLevel.LOW  # Make it look easier
            self.nodes.append(honeypot)
            self.honeypots.append(honeypot)
    
    def create_smart_connections(self):
        """Create intelligent connections based on network architecture"""
        if self.network_architecture == NetworkArchitecture.HIERARCHICAL:
            self.create_hierarchical_connections()
        elif self.network_architecture == NetworkArchitecture.STAR:
            self.create_star_connections()
        elif self.network_architecture == NetworkArchitecture.RING:
            self.create_ring_connections()
        elif self.network_architecture == NetworkArchitecture.MESH:
            self.create_mesh_connections()
        else:
            self.create_random_connections()
    
    def create_hierarchical_connections(self):
        """Create connections for hierarchical network"""
        core_nodes = [n for n in self.nodes if n.node_type == NodeType.MAINFRAME]
        dist_nodes = [n for n in self.nodes if n.node_type in [NodeType.FIREWALL, NodeType.SERVER]]
        access_nodes = [n for n in self.nodes if n not in core_nodes and n not in dist_nodes]
        
        # Connect core nodes to each other
        for i, node1 in enumerate(core_nodes):
            for node2 in core_nodes[i+1:]:
                node1.connections.append(node2)
                node2.connections.append(node1)
        
        # Connect core to distribution
        for core_node in core_nodes:
            for dist_node in dist_nodes:
                if random.random() < 0.8:
                    core_node.connections.append(dist_node)
                    dist_node.connections.append(core_node)
        
        # Connect distribution to access
        for dist_node in dist_nodes:
            nearby_access = [n for n in access_nodes if 
                           math.sqrt((n.x - dist_node.x)**2 + (n.y - dist_node.y)**2) < 150]
            for access_node in nearby_access:
                if random.random() < 0.6:
                    dist_node.connections.append(access_node)
                    access_node.connections.append(dist_node)
    
    def create_star_connections(self):
        """Create connections for star network"""
        if self.nodes:
            hub = self.nodes[0]  # First node is the hub
            for node in self.nodes[1:]:
                hub.connections.append(node)
                node.connections.append(hub)
    
    def create_ring_connections(self):
        """Create connections for ring network"""
        for i, node in enumerate(self.nodes):
            next_node = self.nodes[(i + 1) % len(self.nodes)]
            node.connections.append(next_node)
            next_node.connections.append(node)
    
    def create_mesh_connections(self):
        """Create connections for mesh network"""
        for node in self.nodes:
            # Connect to nearby nodes
            nearby_nodes = [n for n in self.nodes if n != node and 
                          math.sqrt((n.x - node.x)**2 + (n.y - node.y)**2) < 100]
            
            # Random connections
            connection_count = random.randint(2, min(5, len(nearby_nodes)))
            connections = random.sample(nearby_nodes, connection_count)
            node.connections.extend(connections)
    
    def create_random_connections(self):
        """Create random connections (original method)"""
        for node in self.nodes:
            # Connect to nearby nodes
            nearby_nodes = [n for n in self.nodes if n != node and 
                          math.sqrt((n.x - node.x)**2 + (n.y - node.y)**2) < 80]
            
            # Random connections
            connection_count = random.randint(1, min(4, len(nearby_nodes)))
            connections = random.sample(nearby_nodes, connection_count)
            node.connections.extend(connections)
    
    def detect_intrusion(self, attacking_node: NetworkNode) -> List[AISecurityAgent]:
        """Detect intrusion and activate AI responses"""
        activated_agents = []
        
        for agent in self.ai_security_agents:
            if agent.active:
                # AI agents can detect attacks on connected nodes
                connected_nodes = [n for n in self.nodes if hasattr(n, 'ai_agent') and n.ai_agent == agent]
                
                for node in connected_nodes:
                    if any(conn == attacking_node for conn in node.connections):
                        # Activate agent response
                        activated_agents.append(agent)
                        break
        
        return activated_agents
    
    def update_ai_learning(self, attack_patterns: List[str]):
        """Update AI learning based on observed attack patterns"""
        for agent in self.ai_security_agents:
            for pattern in attack_patterns:
                # Random success/failure for learning
                success = random.random() < 0.5
                agent.learn_from_attack(pattern, success)
    
    def ensure_connectivity(self):
        """Ensure all nodes are reachable"""
        if not self.nodes:
            return
        
        # First create connections based on architecture
        self.create_smart_connections()
        
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
        """Enhanced HUD with AI security information"""
        if not self.show_hud:
            return
        
        # Background panel
        hud_panel = pygame.Rect(10, 10, 460, 60)
        pygame.draw.rect(surface, (10, 10, 20), hud_panel)
        pygame.draw.rect(surface, NEON_CYAN, hud_panel, 2)
        
        font = pygame.font.Font(None, 16)
        
        # Game mode and mission
        mode_text = f"Mode: {self.mode_names[self.game_mode]}"
        text = font.render(mode_text, True, NEON_YELLOW)
        surface.blit(text, (15, 15))
        
        mission_text = f"Mission: {self.mission_objective}"
        text = font.render(mission_text, True, NEON_GREEN)
        surface.blit(text, (15, 30))
        
        # Hacking engine stats
        engine_stats = self.hacking_engine.get_hacking_report()
        
        stats_text = [
            f"Stealth: {engine_stats['stealth_level']:.1f}%",
            f"Detection: {engine_stats['detection_risk']:.1f}%",
            f"Heat: {engine_stats['heat_level']:.1f}",
            f"Botnet: {engine_stats['botnet_size']} nodes"
        ]
        
        for i, stat in enumerate(stats_text):
            color = NEON_RED if "Detection" in stat and engine_stats['detection_risk'] > 50 else NEON_GREEN
            text = font.render(stat, True, color)
            surface.blit(text, (200 + (i % 2) * 100, 15 + (i // 2) * 15))
        
        # AI capabilities
        ai_text = []
        if engine_stats['ai_assistant']:
            ai_text.append("AI: ACTIVE")
        if engine_stats['quantum_tools']:
            ai_text.append("QUANTUM: READY")
        if engine_stats['zero_day_exploits'] > 0:
            ai_text.append(f"0-DAY: {engine_stats['zero_day_exploits']}")
        
        for i, text_str in enumerate(ai_text):
            text = font.render(text_str, True, NEON_PURPLE)
            surface.blit(text, (400, 15 + i * 15))
        
        # Network information
        network_info = f"Network: {self.network.network_architecture.name} | Security: {self.network.security_level.name}"
        text = font.render(network_info, True, NEON_CYAN)
        surface.blit(text, (15, 45))
        
        # AI agents status
        ai_count = len([a for a in self.network.ai_security_agents if a.active])
        total_agents = len(self.network.ai_security_agents)
        breached_nodes = len([n for n in self.network.nodes if n.is_breached])
        honeypots_triggered = len([h for h in self.network.honeypots if h.is_breached])
        
        security_text = f"AI Agents: {ai_count}/{total_agents} active | {breached_nodes} nodes breached | {honeypots_triggered} honeypots triggered"
        text = font.render(security_text, True, NEON_RED)
        surface.blit(text, (250, 45))
    
    def draw_enhanced_controls(self, surface):
        """Draw enhanced control instructions"""
        controls_panel = pygame.Rect(10, HEIGHT - 100, 460, 90)
        pygame.draw.rect(surface, (5, 5, 15), controls_panel)
        pygame.draw.rect(surface, NEON_BLUE, controls_panel, 2)
        
        font = pygame.font.Font(None, 14)
        
        # Enhanced controls
        controls = [
            "MOUSE: Select nodes | SPACE: Pause | ESC: Exit",
            "1-8: Hacking tools | A: AI assistant | Q: Quantum tools",
            "S: Social engineering | Z: Zero-day | B: Botnet attack",
            "N: Neural analysis | F: Forensic clean | R: Reset network",
            "T: Terminal mode | H: Toggle HUD | M: Change mode"
        ]
        
        title = pygame.font.Font(None, 16).render("ENHANCED CYBERPUNK CONTROLS", True, NEON_CYAN)
        surface.blit(title, (15, HEIGHT - 95))
        
        for i, control in enumerate(controls):
            text = font.render(control, True, NEON_GREEN)
            surface.blit(text, (15, HEIGHT - 75 + i * 12))
    
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
    
    def handle_advanced_input(self, keys, events):
        """Handle enhanced input for AI features"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                # AI and quantum tools
                if event.key == pygame.K_a:
                    self.hacking_engine.enhance_ai_capabilities()
                elif event.key == pygame.K_q:
                    self.hacking_engine.unlock_quantum_tools()
                elif event.key == pygame.K_z and self.selected_node:
                    # Zero-day exploit
                    result = self.hacking_engine.deploy_zero_day_exploit(self.selected_node)
                    print(result['message'])
                elif event.key == pygame.K_n and self.selected_node:
                    # Neural analysis
                    result = self.hacking_engine.analyze_neural_patterns(self.selected_node)
                    print(result['message'])
                elif event.key == pygame.K_f:
                    # Forensic cleaning
                    self.hacking_engine.clean_forensic_traces()
                elif event.key == pygame.K_b:
                    # Botnet attack
                    target_nodes = [n for n in self.network.nodes if not n.is_breached][:3]
                    if target_nodes:
                        result = self.hacking_engine.coordinate_distributed_attack(target_nodes)
                        print(result['message'])
                elif event.key == pygame.K_s and self.selected_node:
                    # Social engineering
                    target_info = {'node_type': self.selected_node.node_type.name}
                    self.hacking_engine.develop_social_profile(target_info)
                    result = self.hacking_engine.social_engineering_attack(target_info)
                    print(result['message'])
                elif event.key == pygame.K_r:
                    # Reset network
                    self.network = NetworkTopology()
                    self.selected_node = None
                
                # Enhanced hacking attempts
                if self.selected_node and event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    tools = [HackingTool.SCANNER, HackingTool.EXPLOIT, HackingTool.STEALTH, HackingTool.DECRYPTOR]
                    tool_index = event.key - pygame.K_1
                    
                    if tool_index < len(tools):
                        tool = tools[tool_index]
                        ai_agent = getattr(self.selected_node, 'ai_agent', None)
                        result = self.hacking_engine.attempt_advanced_breach(self.selected_node, tool, ai_agent)
                        
                        # Add to botnet if successful
                        if result['success'] and self.selected_node.is_breached:
                            self.hacking_engine.expand_botnet(self.selected_node)
                        
                        print(result['message'])
    
    def update_ai_simulation(self):
        """Update AI security simulation"""
        if self.paused:
            return
        
        # Update AI learning based on recent attacks
        attack_patterns = []
        for node in self.network.nodes:
            if node.is_detected:
                attack_patterns.append(f"detected_attack_{node.node_type.name}")
            if node.is_breached:
                attack_patterns.append(f"successful_breach_{node.node_type.name}")
        
        if attack_patterns:
            self.network.update_ai_learning(attack_patterns)
        
        # AI agents adapt over time
        for agent in self.network.ai_security_agents:
            if agent.active and random.random() < 0.01:  # 1% chance per frame
                # AI improves its defenses
                agent.adaptation_level = min(10, agent.adaptation_level + 1)
        
        # Honeypot detection
        for honeypot in self.network.honeypots:
            if honeypot.is_breached and not honeypot.is_detected:
                # Honeypot was accessed - increase detection for all nodes
                for node in self.network.nodes:
                    if hasattr(node, 'ai_agent') and node.ai_agent:
                        node.ai_agent.adaptation_level += 1
                honeypot.is_detected = True
                self.hacking_engine.heat_level += 20
                print("Honeypot accessed! AI security enhanced!")
    
    def get_ai_security_report(self) -> str:
        """Get AI security status report"""
        active_agents = len([a for a in self.network.ai_security_agents if a.active])
        total_agents = len(self.network.ai_security_agents)
        breached_nodes = len([n for n in self.network.nodes if n.is_breached])
        honeypots_triggered = len([h for h in self.network.honeypots if h.is_breached])
        
        return f"AI Security Status: {active_agents}/{total_agents} agents active | {breached_nodes} nodes breached | {honeypots_triggered} honeypots triggered"

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
        simulator.handle_advanced_input(keys, events)
        
        # Update simulation
        simulator.update_simulation()
        simulator.update_ai_simulation()
        
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
        simulator.draw_enhanced_controls(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS for smooth hacking experience
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 