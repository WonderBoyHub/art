#!/usr/bin/env python3
"""
Dark Ages: Kingdom of Shadows - Epic Single-Player RPG
Perfect for Raspberry Pi 5 with 3.5" display (480x320)
COMPLETE RPG WITH ECONOMY, POLITICS, RELIGIONS, COMBAT & MORE
"""

import pygame
import json
import random
import math
import time
import sys
import subprocess
import os
from enum import Enum
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any

# Initialize Pygame
pygame.init()

# Screen dimensions optimized for Pi 5
WIDTH = 480
HEIGHT = 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dark Ages: Kingdom of Shadows")

# Fullscreen support
fullscreen = False
clock = pygame.time.Clock()

# RPG Color Palette
DARK_BACKGROUND = (15, 15, 25)
UI_DARK = (25, 25, 40)
UI_MEDIUM = (40, 40, 60)
UI_LIGHT = (60, 60, 80)
TEXT_WHITE = (255, 255, 255)
TEXT_YELLOW = (255, 255, 100)
TEXT_GREEN = (100, 255, 100)
TEXT_RED = (255, 100, 100)
TEXT_BLUE = (100, 150, 255)
TEXT_PURPLE = (200, 100, 255)
GOLD_COLOR = (255, 215, 0)
HEALTH_RED = (220, 50, 50)
MANA_BLUE = (50, 100, 255)
EXP_GREEN = (100, 200, 100)

class GameState(Enum):
    MAIN_MENU = 0
    CHARACTER_CREATION = 1
    WORLD_MAP = 2
    TOWN = 3
    DUNGEON = 4
    COMBAT = 5
    INVENTORY = 6
    CHARACTER_SHEET = 7
    SHOP = 8
    TEMPLE = 9
    PALACE = 10
    QUEST_LOG = 11
    SAVE_LOAD = 12
    SKILL_TREE = 13
    CRAFTING = 14

class CharacterClass(Enum):
    WARRIOR = "Warrior"
    MAGE = "Mage"
    ROGUE = "Rogue"
    CLERIC = "Cleric"
    PALADIN = "Paladin"
    RANGER = "Ranger"

class ItemType(Enum):
    WEAPON = "Weapon"
    ARMOR = "Armor"
    SHIELD = "Shield"
    ACCESSORY = "Accessory"
    CONSUMABLE = "Consumable"
    QUEST = "Quest Item"
    MATERIAL = "Material"

class Religion(Enum):
    ORDER_OF_LIGHT = "Order of Light"
    SHADOW_CULT = "Shadow Cult"
    NATURE_SPIRITS = "Nature Spirits"
    WAR_GODS = "War Gods"
    MERCHANTS_GUILD = "Merchants Guild"

class Faction(Enum):
    ROYAL_COURT = "Royal Court"
    REBELS = "Rebels"
    MERCHANTS = "Merchants"
    SCHOLARS = "Scholars"
    THIEVES_GUILD = "Thieves Guild"
    KNIGHTS_ORDER = "Knights Order"

class SkillType(Enum):
    COMBAT = "Combat"
    MAGIC = "Magic"
    STEALTH = "Stealth"
    DIPLOMACY = "Diplomacy"
    SURVIVAL = "Survival"
    CRAFTING = "Crafting"

class WeatherType(Enum):
    CLEAR = "Clear"
    RAIN = "Rain"
    STORM = "Storm"
    SNOW = "Snow"
    FOG = "Fog"

class CombatAction(Enum):
    ATTACK = "Attack"
    DEFEND = "Defend"
    CAST_SPELL = "Cast Spell"
    USE_ITEM = "Use Item"
    FLEE = "Flee"

@dataclass
class Skill:
    name: str
    skill_type: SkillType
    level: int = 1
    experience: int = 0
    experience_needed: int = 100
    description: str = ""
    
    def gain_experience(self, amount: int):
        self.experience += amount
        while self.experience >= self.experience_needed:
            self.level_up()
    
    def level_up(self):
        self.experience -= self.experience_needed
        self.level += 1
        self.experience_needed = int(self.experience_needed * 1.3)

@dataclass
class Enemy:
    name: str
    level: int
    max_health: int
    current_health: int
    attack_power: int
    defense: int
    experience_reward: int
    gold_reward: int
    possible_drops: List[str]
    
    def __init__(self, name: str, level: int = 1):
        self.name = name
        self.level = level
        self.max_health = 30 + level * 15
        self.current_health = self.max_health
        self.attack_power = 5 + level * 3
        self.defense = 2 + level * 2
        self.experience_reward = level * 25
        self.gold_reward = level * 10 + random.randint(5, 15)
        self.possible_drops = ["health_potion", "iron_ore", "silver_nugget"]

@dataclass
class CombatState:
    player: 'Character'
    enemy: Enemy
    player_turn: bool = True
    turn_count: int = 0
    combat_log: List[str] = None
    player_action: Optional[CombatAction] = None
    player_defending: bool = False
    
    def __post_init__(self):
        if self.combat_log is None:
            self.combat_log = []

@dataclass
class WeatherSystem:
    current_weather: WeatherType = WeatherType.CLEAR
    temperature: int = 20  # Celsius
    wind_speed: int = 5    # km/h
    humidity: int = 50     # percentage
    time_of_day: float = 0.5  # 0.0 = midnight, 0.5 = noon, 1.0 = midnight
    season: str = "Spring"
    
    def update(self, dt: float):
        """Update weather and time"""
        self.time_of_day += dt * 0.001  # Accelerated time
        if self.time_of_day >= 1.0:
            self.time_of_day = 0.0
            self.advance_day()
    
    def advance_day(self):
        """Advance to next day with weather changes"""
        # Random weather changes
        if random.random() < 0.3:  # 30% chance of weather change
            self.current_weather = random.choice(list(WeatherType))
        
        # Temperature variation
        self.temperature += random.randint(-5, 5)
        self.temperature = max(-10, min(35, self.temperature))
        
        # Wind and humidity changes
        self.wind_speed = max(0, min(50, self.wind_speed + random.randint(-10, 10)))
        self.humidity = max(20, min(90, self.humidity + random.randint(-15, 15)))

@dataclass
class Character:
    name: str = "Hero"
    character_class: CharacterClass = CharacterClass.WARRIOR
    level: int = 1
    experience: int = 0
    experience_needed: int = 100
    
    # Core Stats
    strength: int = 10
    intelligence: int = 10
    dexterity: int = 10
    constitution: int = 10
    wisdom: int = 10
    charisma: int = 10
    
    # Derived Stats
    max_health: int = 100
    current_health: int = 100
    max_mana: int = 50
    current_mana: int = 50
    
    # Resources
    gold: int = 100
    
    # Progression
    skill_points: int = 0
    attribute_points: int = 0
    
    # Social Systems
    reputation: Dict[Faction, int] = None
    faith: Dict[Religion, int] = None
    
    # Skills
    skills: Dict[SkillType, Skill] = None
    
    # Equipment
    equipped_weapon: Optional[str] = None
    equipped_armor: Optional[str] = None
    equipped_shield: Optional[str] = None
    equipped_accessory: Optional[str] = None
    
    # Location
    current_location: str = "royal_city"
    x: int = 240
    y: int = 160
    
    # Status Effects
    status_effects: List[str] = None
    
    # Combat Stats
    initiative: int = 10
    critical_chance: float = 0.05
    
    def __post_init__(self):
        if self.reputation is None:
            self.reputation = {faction: 0 for faction in Faction}
        if self.faith is None:
            self.faith = {religion: 0 for religion in Religion}
        if self.skills is None:
            self.skills = {
                SkillType.COMBAT: Skill("Swordplay", SkillType.COMBAT, description="Skill with melee weapons"),
                SkillType.MAGIC: Skill("Arcane Arts", SkillType.MAGIC, description="Knowledge of magical spells"),
                SkillType.STEALTH: Skill("Stealth", SkillType.STEALTH, description="Moving unseen and unheard"),
                SkillType.DIPLOMACY: Skill("Diplomacy", SkillType.DIPLOMACY, description="Art of persuasion"),
                SkillType.SURVIVAL: Skill("Survival", SkillType.SURVIVAL, description="Living off the land"),
                SkillType.CRAFTING: Skill("Crafting", SkillType.CRAFTING, description="Creating items and tools")
            }
        if self.status_effects is None:
            self.status_effects = []
        
        self.calculate_derived_stats()
    
    def calculate_derived_stats(self):
        """Calculate health, mana, and other derived stats"""
        base_health = 50 + (self.constitution * 10) + (self.level * 20)
        base_mana = 25 + (self.intelligence * 5) + (self.level * 10)
        
        self.max_health = base_health
        self.max_mana = base_mana
        
        # Ensure current values don't exceed maximum
        self.current_health = min(self.current_health, self.max_health)
        self.current_mana = min(self.current_mana, self.max_mana)
    
    def gain_experience(self, amount: int):
        """Gain experience and handle leveling up"""
        self.experience += amount
        while self.experience >= self.experience_needed:
            self.level_up()
    
    def level_up(self):
        """Level up the character"""
        self.experience -= self.experience_needed
        self.level += 1
        self.experience_needed = int(self.experience_needed * 1.2)
        self.skill_points += 2
        self.attribute_points += 1
        
        # Restore health and mana on level up
        self.calculate_derived_stats()
        self.current_health = self.max_health
        self.current_mana = self.max_mana
    
    def modify_reputation(self, faction: Faction, amount: int):
        """Modify reputation with a faction"""
        self.reputation[faction] = max(-100, min(100, self.reputation[faction] + amount))
    
    def modify_faith(self, religion: Religion, amount: int):
        """Modify faith in a religion"""
        self.faith[religion] = max(-100, min(100, self.faith[religion] + amount))
    
    def get_attack_power(self) -> int:
        """Calculate total attack power including weapon and skills"""
        base_attack = self.strength + self.skills[SkillType.COMBAT].level * 2
        weapon_bonus = 0
        
        # Add weapon bonus if equipped
        # This would be calculated elsewhere based on equipped weapon
        
        return base_attack + weapon_bonus
    
    def get_defense_power(self) -> int:
        """Calculate total defense including armor and constitution"""
        base_defense = self.constitution // 2 + self.skills[SkillType.COMBAT].level
        armor_bonus = 0
        
        # Add armor bonus if equipped
        # This would be calculated elsewhere based on equipped armor
        
        return base_defense + armor_bonus
    
    def take_damage(self, damage: int) -> int:
        """Take damage and return actual damage dealt"""
        actual_damage = max(1, damage - self.get_defense_power() // 2)
        self.current_health = max(0, self.current_health - actual_damage)
        return actual_damage
    
    def heal(self, amount: int):
        """Heal the character"""
        self.current_health = min(self.max_health, self.current_health + amount)
    
    def is_alive(self) -> bool:
        """Check if character is alive"""
        return self.current_health > 0
    
    def gain_skill_experience(self, skill_type: SkillType, amount: int):
        """Gain experience in a specific skill"""
        if skill_type in self.skills:
            self.skills[skill_type].gain_experience(amount)

@dataclass
class Item:
    name: str
    item_type: ItemType
    value: int
    description: str
    attack_bonus: int = 0
    defense_bonus: int = 0
    stat_bonuses: Dict[str, int] = None
    consumable_effect: Optional[str] = None
    quantity: int = 1
    
    def __post_init__(self):
        if self.stat_bonuses is None:
            self.stat_bonuses = {}

@dataclass
class Quest:
    id: str
    title: str
    description: str
    objectives: List[str]
    completed_objectives: List[bool]
    reward_gold: int
    reward_experience: int
    reward_items: List[str]
    faction_rewards: Dict[Faction, int]
    completed: bool = False

@dataclass
class NPC:
    name: str
    dialogue: List[str]
    shop_items: List[str] = None
    quests: List[str] = None
    faction: Optional[Faction] = None
    religion: Optional[Religion] = None

class GameData:
    """Central repository for all game data"""
    def __init__(self):
        self.items = self.create_items()
        self.npcs = self.create_npcs()
        self.quests = self.create_quests()
        self.locations = self.create_locations()
    
    def create_items(self) -> Dict[str, Item]:
        """Create all game items"""
        return {
            # Weapons
            "iron_sword": Item("Iron Sword", ItemType.WEAPON, 50, "A sturdy iron blade", attack_bonus=10),
            "steel_sword": Item("Steel Sword", ItemType.WEAPON, 150, "A sharp steel sword", attack_bonus=20),
            "magic_staff": Item("Magic Staff", ItemType.WEAPON, 100, "A staff crackling with energy", attack_bonus=5, stat_bonuses={"intelligence": 5}),
            "silver_dagger": Item("Silver Dagger", ItemType.WEAPON, 75, "A quick silver blade", attack_bonus=8, stat_bonuses={"dexterity": 3}),
            
            # Armor
            "leather_armor": Item("Leather Armor", ItemType.ARMOR, 40, "Basic leather protection", defense_bonus=5),
            "chain_mail": Item("Chain Mail", ItemType.ARMOR, 120, "Flexible metal armor", defense_bonus=12),
            "plate_armor": Item("Plate Armor", ItemType.ARMOR, 300, "Heavy plate protection", defense_bonus=20, stat_bonuses={"constitution": 3}),
            "mage_robes": Item("Mage Robes", ItemType.ARMOR, 80, "Robes of magical power", defense_bonus=3, stat_bonuses={"intelligence": 8}),
            
            # Shields
            "wooden_shield": Item("Wooden Shield", ItemType.SHIELD, 25, "Basic wooden protection", defense_bonus=3),
            "iron_shield": Item("Iron Shield", ItemType.SHIELD, 60, "Sturdy iron shield", defense_bonus=8),
            
            # Accessories
            "power_ring": Item("Ring of Power", ItemType.ACCESSORY, 200, "Increases all abilities", stat_bonuses={"strength": 2, "intelligence": 2, "dexterity": 2}),
            "health_amulet": Item("Amulet of Vitality", ItemType.ACCESSORY, 150, "Increases maximum health", stat_bonuses={"constitution": 5}),
            
            # Consumables
            "health_potion": Item("Health Potion", ItemType.CONSUMABLE, 20, "Restores 50 health", consumable_effect="heal_50"),
            "mana_potion": Item("Mana Potion", ItemType.CONSUMABLE, 30, "Restores 30 mana", consumable_effect="mana_30"),
            "strength_elixir": Item("Strength Elixir", ItemType.CONSUMABLE, 100, "Temporarily increases strength", consumable_effect="temp_str_5"),
            
            # Quest Items
            "royal_seal": Item("Royal Seal", ItemType.QUEST, 0, "The king's official seal"),
            "ancient_tome": Item("Ancient Tome", ItemType.QUEST, 0, "A book of forgotten knowledge"),
            
            # Materials
            "iron_ore": Item("Iron Ore", ItemType.MATERIAL, 10, "Raw iron for crafting"),
            "silver_nugget": Item("Silver Nugget", ItemType.MATERIAL, 25, "Pure silver"),
            "magic_crystal": Item("Magic Crystal", ItemType.MATERIAL, 50, "A crystal infused with magic"),
        }
    
    def create_npcs(self) -> Dict[str, NPC]:
        """Create all NPCs"""
        return {
            "king_aldric": NPC(
                "King Aldric",
                ["Welcome to my kingdom, brave adventurer.", "The realm faces dark times ahead.", "Serve the crown well and be rewarded."],
                faction=Faction.ROYAL_COURT,
                quests=["royal_mission"]
            ),
            "merchant_tomas": NPC(
                "Merchant Tomas",
                ["Welcome to my shop!", "I have the finest goods in the kingdom!", "Gold speaks louder than words."],
                shop_items=["iron_sword", "leather_armor", "health_potion", "mana_potion"],
                faction=Faction.MERCHANTS
            ),
            "priest_marcus": NPC(
                "Priest Marcus",
                ["The Light guides us all.", "Seek wisdom in prayer.", "May the gods bless your journey."],
                religion=Religion.ORDER_OF_LIGHT,
                quests=["temple_blessing"]
            ),
            "rebel_sarah": NPC(
                "Sarah the Rebel",
                ["The king's tyranny must end!", "Join our cause for freedom!", "The people deserve better."],
                faction=Faction.REBELS,
                quests=["liberation_mission"]
            ),
            "scholar_edwin": NPC(
                "Scholar Edwin",
                ["Knowledge is the greatest power.", "I seek ancient wisdom.", "Books hold secrets untold."],
                faction=Faction.SCHOLARS,
                quests=["lost_tome"]
            ),
            "blacksmith_gareth": NPC(
                "Blacksmith Gareth",
                ["I forge the finest weapons!", "Bring me materials and gold.", "A warrior needs good steel."],
                shop_items=["steel_sword", "chain_mail", "iron_shield"]
            )
        }
    
    def create_quests(self) -> Dict[str, Quest]:
        """Create all quests"""
        return {
            "royal_mission": Quest(
                "royal_mission",
                "The King's Request",
                "King Aldric has asked you to retrieve the stolen royal seal.",
                ["Find the royal seal", "Return to King Aldric"],
                [False, False],
                500, 200,
                ["power_ring"],
                {Faction.ROYAL_COURT: 20}
            ),
            "temple_blessing": Quest(
                "temple_blessing",
                "Temple of Light",
                "Priest Marcus wants you to prove your devotion to the Order of Light.",
                ["Pray at the altar", "Donate 100 gold", "Complete a good deed"],
                [False, False, False],
                0, 100,
                ["health_amulet"],
                {Faction.ROYAL_COURT: 5}
            ),
            "liberation_mission": Quest(
                "liberation_mission",
                "Fight for Freedom",
                "Sarah wants you to help liberate the oppressed villages.",
                ["Free the village of Millhaven", "Recruit 5 supporters", "Deliver supplies"],
                [False, False, False],
                300, 300,
                ["silver_dagger"],
                {Faction.REBELS: 30, Faction.ROYAL_COURT: -10}
            ),
            "lost_tome": Quest(
                "lost_tome",
                "The Lost Tome",
                "Scholar Edwin seeks an ancient tome lost in the dark forests.",
                ["Search the Dark Forest", "Defeat the guardian", "Return the tome"],
                [False, False, False],
                200, 250,
                ["magic_staff"],
                {Faction.SCHOLARS: 25}
            )
        }
    
    def create_locations(self) -> Dict[str, Dict]:
        """Create all locations"""
        return {
            "royal_city": {
                "name": "Royal City of Valdris",
                "description": "The capital city, seat of power",
                "npcs": ["king_aldric", "merchant_tomas", "priest_marcus"],
                "connections": ["dark_forest", "mountain_pass", "coastal_village"]
            },
            "dark_forest": {
                "name": "Dark Forest",
                "description": "A mysterious forest filled with ancient secrets",
                "npcs": [],
                "connections": ["royal_city", "abandoned_ruins"],
                "enemies": ["shadow_wolf", "dark_mage"]
            },
            "mountain_pass": {
                "name": "Mountain Pass",
                "description": "A treacherous mountain path",
                "npcs": ["scholar_edwin"],
                "connections": ["royal_city", "dwarven_mines"]
            },
            "coastal_village": {
                "name": "Coastal Village",
                "description": "A peaceful fishing village",
                "npcs": ["rebel_sarah", "blacksmith_gareth"],
                "connections": ["royal_city", "pirate_cove"]
            }
        }

class DarkAgesRPG:
    """Main RPG Game Engine"""
    def __init__(self):
        self.game_state = GameState.MAIN_MENU
        self.character = Character()
        self.game_data = GameData()
        self.inventory = {}
        self.active_quests = {}
        self.completed_quests = {}
        
        # Combat System
        self.combat_state = None
        self.available_enemies = self.create_enemy_database()
        
        # Weather System
        self.weather = WeatherSystem()
        
        # UI State
        self.selected_menu_item = 0
        self.scroll_offset = 0
        self.current_dialogue = []
        self.current_npc = None
        self.shop_mode = False
        self.text_input = ""
        self.input_active = False
        
        # Game time
        self.game_time = 0
        self.day = 1
        
        # Fonts
        self.font_large = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 18)
        self.font_small = pygame.font.Font(None, 14)
        
        # Initialize starting inventory
        self.inventory["health_potion"] = 3
        self.inventory["iron_sword"] = 1
        self.inventory["leather_armor"] = 1
        
        # Auto-equip starting gear
        self.character.equipped_weapon = "iron_sword"
        self.character.equipped_armor = "leather_armor"
        self.character.calculate_derived_stats()
    
    def create_enemy_database(self) -> Dict[str, Enemy]:
        """Create database of available enemies"""
        return {
            "goblin": Enemy("Goblin", 1),
            "orc": Enemy("Orc", 2),
            "skeleton": Enemy("Skeleton", 2),
            "bandit": Enemy("Bandit", 3),
            "wolf": Enemy("Wolf", 2),
            "troll": Enemy("Troll", 5),
            "dark_knight": Enemy("Dark Knight", 7),
            "dragon": Enemy("Ancient Dragon", 10)
        }
    
    def save_game(self, slot: int = 1):
        """Save the game to a file"""
        save_data = {
            "character": asdict(self.character),
            "inventory": self.inventory,
            "active_quests": {k: asdict(v) for k, v in self.active_quests.items()},
            "completed_quests": {k: asdict(v) for k, v in self.completed_quests.items()},
            "game_time": self.game_time,
            "day": self.day
        }
        
        try:
            with open(f"save_slot_{slot}.json", "w") as f:
                json.dump(save_data, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_game(self, slot: int = 1):
        """Load the game from a file"""
        try:
            with open(f"save_slot_{slot}.json", "r") as f:
                save_data = json.load(f)
            
            # Reconstruct character
            char_data = save_data["character"]
            self.character = Character(**char_data)
            
            # Reconstruct other data
            self.inventory = save_data["inventory"]
            self.active_quests = {k: Quest(**v) for k, v in save_data["active_quests"].items()}
            self.completed_quests = {k: Quest(**v) for k, v in save_data["completed_quests"].items()}
            self.game_time = save_data["game_time"]
            self.day = save_data["day"]
            
            return True
        except Exception:
            return False
    
    def start_quest(self, quest_id: str):
        """Start a new quest"""
        if quest_id in self.game_data.quests and quest_id not in self.active_quests:
            self.active_quests[quest_id] = self.game_data.quests[quest_id]
    
    def complete_quest_objective(self, quest_id: str, objective_index: int):
        """Complete a quest objective"""
        if quest_id in self.active_quests:
            quest = self.active_quests[quest_id]
            if objective_index < len(quest.completed_objectives):
                quest.completed_objectives[objective_index] = True
                
                # Check if quest is fully completed
                if all(quest.completed_objectives):
                    self.complete_quest(quest_id)
    
    def complete_quest(self, quest_id: str):
        """Complete a quest and give rewards"""
        if quest_id in self.active_quests:
            quest = self.active_quests[quest_id]
            quest.completed = True
            
            # Give rewards
            self.character.gold += quest.reward_gold
            self.character.gain_experience(quest.reward_experience)
            
            # Give item rewards
            for item_id in quest.reward_items:
                if item_id in self.inventory:
                    self.inventory[item_id] += 1
                else:
                    self.inventory[item_id] = 1
            
            # Apply faction reputation changes
            for faction, rep_change in quest.faction_rewards.items():
                self.character.modify_reputation(faction, rep_change)
            
            # Move to completed quests
            self.completed_quests[quest_id] = quest
            del self.active_quests[quest_id]
    
    def start_combat(self, enemy_name: str):
        """Start combat with an enemy"""
        if enemy_name in self.available_enemies:
            enemy = self.available_enemies[enemy_name]
            # Create a fresh copy of the enemy
            combat_enemy = Enemy(enemy.name, enemy.level)
            self.combat_state = CombatState(self.character, combat_enemy)
            self.game_state = GameState.COMBAT
            self.combat_state.combat_log.append(f"Combat begins with {enemy.name}!")
    
    def process_combat_turn(self, player_action: CombatAction):
        """Process a turn of combat"""
        if not self.combat_state:
            return
        
        combat = self.combat_state
        
        if combat.player_turn:
            # Player's turn
            if player_action == CombatAction.ATTACK:
                damage = self.character.get_attack_power() + random.randint(1, 6)
                # Check for critical hit
                if random.random() < self.character.critical_chance:
                    damage *= 2
                    combat.combat_log.append(f"Critical hit!")
                
                actual_damage = max(1, damage - combat.enemy.defense)
                combat.enemy.current_health -= actual_damage
                combat.combat_log.append(f"You deal {actual_damage} damage to {combat.enemy.name}")
                
                # Gain combat experience
                self.character.gain_skill_experience(SkillType.COMBAT, 5)
                
            elif player_action == CombatAction.DEFEND:
                combat.player_defending = True
                combat.combat_log.append("You raise your guard defensively")
                
            elif player_action == CombatAction.USE_ITEM:
                # Use healing potion if available
                if "health_potion" in self.inventory and self.inventory["health_potion"] > 0:
                    self.use_item("health_potion")
                    combat.combat_log.append("You drink a health potion")
                else:
                    combat.combat_log.append("No usable items available")
                    
            elif player_action == CombatAction.FLEE:
                if random.random() < 0.7:  # 70% chance to flee
                    combat.combat_log.append("You successfully flee from combat!")
                    self.end_combat(False)
                    return
                else:
                    combat.combat_log.append("Failed to escape!")
            
            combat.player_turn = False
            
        else:
            # Enemy's turn
            if combat.enemy.current_health > 0:
                enemy_damage = combat.enemy.attack_power + random.randint(1, 4)
                
                if combat.player_defending:
                    enemy_damage //= 2
                    combat.player_defending = False
                
                actual_damage = self.character.take_damage(enemy_damage)
                combat.combat_log.append(f"{combat.enemy.name} deals {actual_damage} damage to you")
            
            combat.player_turn = True
            combat.turn_count += 1
        
        # Check for combat end conditions
        if combat.enemy.current_health <= 0:
            self.win_combat()
        elif not self.character.is_alive():
            self.lose_combat()
    
    def win_combat(self):
        """Handle winning combat"""
        if not self.combat_state:
            return
        
        enemy = self.combat_state.enemy
        
        # Gain experience and gold
        self.character.gain_experience(enemy.experience_reward)
        self.character.gold += enemy.gold_reward
        
        # Random item drops
        for item_id in enemy.possible_drops:
            if random.random() < 0.3:  # 30% drop chance
                if item_id in self.inventory:
                    self.inventory[item_id] += 1
                else:
                    self.inventory[item_id] = 1
                self.combat_state.combat_log.append(f"You found: {self.game_data.items[item_id].name}")
        
        self.combat_state.combat_log.append(f"Victory! Gained {enemy.experience_reward} experience and {enemy.gold_reward} gold")
        self.end_combat(True)
    
    def lose_combat(self):
        """Handle losing combat"""
        self.combat_state.combat_log.append("You have been defeated!")
        # Restore some health and return to safety
        self.character.current_health = self.character.max_health // 4
        self.end_combat(False)
    
    def end_combat(self, victory: bool):
        """End combat and return to world map"""
        self.combat_state = None
        self.game_state = GameState.WORLD_MAP
    
    def use_item(self, item_id: str):
        """Use a consumable item"""
        if item_id in self.inventory and self.inventory[item_id] > 0:
            item = self.game_data.items[item_id]
            
            if item.item_type == ItemType.CONSUMABLE and item.consumable_effect:
                effect = item.consumable_effect
                
                if effect == "heal_50":
                    self.character.current_health = min(
                        self.character.max_health,
                        self.character.current_health + 50
                    )
                elif effect == "mana_30":
                    self.character.current_mana = min(
                        self.character.max_mana,
                        self.character.current_mana + 30
                    )
                elif effect.startswith("temp_str_"):
                    amount = int(effect.split("_")[-1])
                    # Temporary effects would need a more complex system
                    pass
                
                # Consume the item
                self.inventory[item_id] -= 1
                if self.inventory[item_id] == 0:
                    del self.inventory[item_id]
                
                return True
        return False
    
    def equip_item(self, item_id: str):
        """Equip an item"""
        if item_id in self.inventory and item_id in self.game_data.items:
            item = self.game_data.items[item_id]
            
            if item.item_type == ItemType.WEAPON:
                self.character.equipped_weapon = item_id
            elif item.item_type == ItemType.ARMOR:
                self.character.equipped_armor = item_id
            elif item.item_type == ItemType.SHIELD:
                self.character.equipped_shield = item_id
            elif item.item_type == ItemType.ACCESSORY:
                self.character.equipped_accessory = item_id
            
            self.character.calculate_derived_stats()
    
    def get_total_attack(self) -> int:
        """Calculate total attack power"""
        base_attack = self.character.strength
        weapon_bonus = 0
        
        if self.character.equipped_weapon:
            weapon = self.game_data.items[self.character.equipped_weapon]
            weapon_bonus = weapon.attack_bonus
        
        return base_attack + weapon_bonus
    
    def get_total_defense(self) -> int:
        """Calculate total defense"""
        base_defense = self.character.constitution // 2
        armor_bonus = 0
        shield_bonus = 0
        
        if self.character.equipped_armor:
            armor = self.game_data.items[self.character.equipped_armor]
            armor_bonus = armor.defense_bonus
        
        if self.character.equipped_shield:
            shield = self.game_data.items[self.character.equipped_shield]
            shield_bonus = shield.defense_bonus
        
        return base_defense + armor_bonus + shield_bonus
    
    def draw_panel(self, surface, rect, title="", border_color=UI_LIGHT):
        """Draw a UI panel"""
        pygame.draw.rect(surface, UI_DARK, rect)
        pygame.draw.rect(surface, border_color, rect, 2)
        
        if title:
            title_text = self.font_medium.render(title, True, TEXT_YELLOW)
            surface.blit(title_text, (rect.x + 5, rect.y + 5))
    
    def draw_bar(self, surface, x, y, width, height, current, maximum, color, bg_color=(50, 50, 50)):
        """Draw a status bar"""
        pygame.draw.rect(surface, bg_color, (x, y, width, height))
        if maximum > 0:
            fill_width = int((current / maximum) * width)
            pygame.draw.rect(surface, color, (x, y, fill_width, height))
        pygame.draw.rect(surface, TEXT_WHITE, (x, y, width, height), 1)
    
    def draw_main_menu(self, surface):
        """Draw the main menu"""
        surface.fill(DARK_BACKGROUND)
        
        # Title
        title_text = self.font_large.render("DARK AGES: KINGDOM OF SHADOWS", True, TEXT_YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        surface.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("A Medieval Fantasy RPG", True, TEXT_WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 30))
        surface.blit(subtitle_text, subtitle_rect)
        
        # Menu options
        menu_options = ["New Game", "Load Game", "Exit"]
        for i, option in enumerate(menu_options):
            color = TEXT_YELLOW if i == self.selected_menu_item else TEXT_WHITE
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 30))
            surface.blit(text, text_rect)
    
    def draw_character_creation(self, surface):
        """Draw character creation screen"""
        surface.fill(DARK_BACKGROUND)
        
        # Title
        title_text = self.font_large.render("CREATE CHARACTER", True, TEXT_YELLOW)
        surface.blit(title_text, (20, 20))
        
        # Name input
        name_text = self.font_medium.render(f"Name: {self.character.name}", True, TEXT_WHITE)
        surface.blit(name_text, (20, 60))
        
        # Class selection
        class_text = self.font_medium.render(f"Class: {self.character.character_class.value}", True, TEXT_WHITE)
        surface.blit(class_text, (20, 90))
        
        # Class descriptions
        class_descriptions = {
            CharacterClass.WARRIOR: "Strong melee fighter with high health",
            CharacterClass.MAGE: "Powerful spellcaster with magic abilities",
            CharacterClass.ROGUE: "Agile and stealthy with high dexterity",
            CharacterClass.CLERIC: "Holy warrior with healing powers",
            CharacterClass.PALADIN: "Divine knight with balanced abilities",
            CharacterClass.RANGER: "Nature warrior with ranged combat"
        }
        
        desc_text = self.font_small.render(class_descriptions[self.character.character_class], True, TEXT_GREEN)
        surface.blit(desc_text, (20, 110))
        
        # Stats preview
        stats_y = 140
        stats = [
            f"Strength: {self.character.strength}",
            f"Intelligence: {self.character.intelligence}",
            f"Dexterity: {self.character.dexterity}",
            f"Constitution: {self.character.constitution}",
            f"Wisdom: {self.character.wisdom}",
            f"Charisma: {self.character.charisma}"
        ]
        
        for i, stat in enumerate(stats):
            text = self.font_small.render(stat, True, TEXT_WHITE)
            surface.blit(text, (20, stats_y + i * 20))
        
        # Instructions
        instructions = [
            "Arrow keys: Navigate",
            "Enter: Confirm selection",
            "Space: Start game"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font_small.render(instruction, True, TEXT_BLUE)
            surface.blit(text, (300, 200 + i * 15))
    
    def draw_world_map(self, surface):
        """Draw the world map"""
        surface.fill(DARK_BACKGROUND)
        
        # Title
        title_text = self.font_medium.render("KINGDOM OF VALDRIS", True, TEXT_YELLOW)
        surface.blit(title_text, (20, 20))
        
        # Draw locations
        locations = {
            "royal_city": (240, 160),
            "dark_forest": (120, 200),
            "mountain_pass": (360, 100),
            "coastal_village": (100, 100)
        }
        
        for location_id, (x, y) in locations.items():
            location = self.game_data.locations[location_id]
            
            # Draw location circle
            color = TEXT_YELLOW if location_id == self.character.current_location else TEXT_WHITE
            pygame.draw.circle(surface, color, (x, y), 8)
            pygame.draw.circle(surface, TEXT_WHITE, (x, y), 8, 2)
            
            # Draw location name
            name_text = self.font_small.render(location["name"], True, color)
            name_rect = name_text.get_rect(center=(x, y + 20))
            surface.blit(name_text, name_rect)
        
        # Draw connections
        connections = [
            ("royal_city", "dark_forest"),
            ("royal_city", "mountain_pass"),
            ("royal_city", "coastal_village"),
            ("dark_forest", "abandoned_ruins")
        ]
        
        for loc1, loc2 in connections:
            if loc1 in locations and loc2 in locations:
                pygame.draw.line(surface, UI_LIGHT, locations[loc1], locations[loc2], 2)
        
        # Player position indicator
        player_pos = locations.get(self.character.current_location, (240, 160))
        pygame.draw.circle(surface, TEXT_GREEN, player_pos, 4)
        
        # Current location info
        current_loc = self.game_data.locations[self.character.current_location]
        info_text = self.font_small.render(current_loc["description"], True, TEXT_WHITE)
        surface.blit(info_text, (20, HEIGHT - 40))
        
        # Instructions
        instructions_text = self.font_small.render("Enter: Enter location | I: Inventory | C: Character | Q: Quests", True, TEXT_BLUE)
        surface.blit(instructions_text, (20, HEIGHT - 20))
    
    def draw_character_sheet(self, surface):
        """Draw character sheet"""
        surface.fill(DARK_BACKGROUND)
        
        # Character info panel
        char_panel = pygame.Rect(10, 10, 220, 140)
        self.draw_panel(surface, char_panel, "CHARACTER")
        
        y_offset = 35
        char_info = [
            f"Name: {self.character.name}",
            f"Class: {self.character.character_class.value}",
            f"Level: {self.character.level}",
            f"Experience: {self.character.experience}/{self.character.experience_needed}",
            f"Gold: {self.character.gold}",
            f"Health: {self.character.current_health}/{self.character.max_health}",
            f"Mana: {self.character.current_mana}/{self.character.max_mana}"
        ]
        
        for info in char_info:
            text = self.font_small.render(info, True, TEXT_WHITE)
            surface.blit(text, (15, y_offset))
            y_offset += 15
        
        # Stats panel
        stats_panel = pygame.Rect(240, 10, 230, 140)
        self.draw_panel(surface, stats_panel, "ATTRIBUTES")
        
        y_offset = 35
        stats = [
            f"Strength: {self.character.strength}",
            f"Intelligence: {self.character.intelligence}",
            f"Dexterity: {self.character.dexterity}",
            f"Constitution: {self.character.constitution}",
            f"Wisdom: {self.character.wisdom}",
            f"Charisma: {self.character.charisma}"
        ]
        
        for stat in stats:
            text = self.font_small.render(stat, True, TEXT_WHITE)
            surface.blit(text, (245, y_offset))
            y_offset += 15
        
        # Equipment panel
        equip_panel = pygame.Rect(10, 160, 220, 100)
        self.draw_panel(surface, equip_panel, "EQUIPMENT")
        
        y_offset = 185
        equipment = [
            f"Weapon: {self.character.equipped_weapon or 'None'}",
            f"Armor: {self.character.equipped_armor or 'None'}",
            f"Shield: {self.character.equipped_shield or 'None'}",
            f"Accessory: {self.character.equipped_accessory or 'None'}"
        ]
        
        for equip in equipment:
            text = self.font_small.render(equip, True, TEXT_WHITE)
            surface.blit(text, (15, y_offset))
            y_offset += 15
        
        # Combat stats panel
        combat_panel = pygame.Rect(240, 160, 230, 100)
        self.draw_panel(surface, combat_panel, "COMBAT")
        
        y_offset = 185
        combat_stats = [
            f"Attack Power: {self.get_total_attack()}",
            f"Defense: {self.get_total_defense()}",
            f"Skill Points: {self.character.skill_points}",
            f"Attribute Points: {self.character.attribute_points}"
        ]
        
        for stat in combat_stats:
            text = self.font_small.render(stat, True, TEXT_WHITE)
            surface.blit(text, (245, y_offset))
            y_offset += 15
        
        # Instructions
        instructions_text = self.font_small.render("ESC: Back | +/-: Allocate points", True, TEXT_BLUE)
        surface.blit(instructions_text, (20, HEIGHT - 20))
    
    def draw_inventory(self, surface):
        """Draw inventory screen"""
        surface.fill(DARK_BACKGROUND)
        
        # Inventory panel
        inv_panel = pygame.Rect(10, 10, 300, 250)
        self.draw_panel(surface, inv_panel, f"INVENTORY - Gold: {self.character.gold}")
        
        y_offset = 35
        for item_id, quantity in self.inventory.items():
            if item_id in self.game_data.items:
                item = self.game_data.items[item_id]
                
                color = TEXT_YELLOW if y_offset == 35 + self.selected_menu_item * 15 else TEXT_WHITE
                item_text = f"{item.name} x{quantity} ({item.value}g)"
                text = self.font_small.render(item_text, True, color)
                surface.blit(text, (15, y_offset))
                y_offset += 15
        
        # Item description panel
        desc_panel = pygame.Rect(320, 10, 150, 250)
        self.draw_panel(surface, desc_panel, "DESCRIPTION")
        
        # Show selected item description
        items_list = list(self.inventory.keys())
        if 0 <= self.selected_menu_item < len(items_list):
            selected_item_id = items_list[self.selected_menu_item]
            if selected_item_id in self.game_data.items:
                item = self.game_data.items[selected_item_id]
                
                # Item name
                name_text = self.font_small.render(item.name, True, TEXT_YELLOW)
                surface.blit(name_text, (325, 35))
                
                # Item type
                type_text = self.font_small.render(item.item_type.value, True, TEXT_BLUE)
                surface.blit(type_text, (325, 50))
                
                # Description (word wrap)
                words = item.description.split()
                line = ""
                y_pos = 70
                for word in words:
                    test_line = line + word + " "
                    if self.font_small.size(test_line)[0] > 140:
                        if line:
                            text = self.font_small.render(line, True, TEXT_WHITE)
                            surface.blit(text, (325, y_pos))
                            y_pos += 15
                        line = word + " "
                    else:
                        line = test_line
                
                if line:
                    text = self.font_small.render(line, True, TEXT_WHITE)
                    surface.blit(text, (325, y_pos))
                    y_pos += 15
                
                # Stats
                if item.attack_bonus > 0:
                    attack_text = self.font_small.render(f"Attack: +{item.attack_bonus}", True, TEXT_RED)
                    surface.blit(attack_text, (325, y_pos))
                    y_pos += 15
                
                if item.defense_bonus > 0:
                    def_text = self.font_small.render(f"Defense: +{item.defense_bonus}", True, TEXT_BLUE)
                    surface.blit(def_text, (325, y_pos))
                    y_pos += 15
        
        # Instructions
        instructions = [
            "Arrow keys: Navigate",
            "Enter: Use/Equip item",
            "ESC: Back"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font_small.render(instruction, True, TEXT_BLUE)
            surface.blit(text, (20, HEIGHT - 60 + i * 15))
    
    def draw_quest_log(self, surface):
        """Draw quest log"""
        surface.fill(DARK_BACKGROUND)
        
        # Active quests panel
        active_panel = pygame.Rect(10, 10, 460, 150)
        self.draw_panel(surface, active_panel, "ACTIVE QUESTS")
        
        y_offset = 35
        for quest_id, quest in self.active_quests.items():
            quest_text = self.font_small.render(quest.title, True, TEXT_YELLOW)
            surface.blit(quest_text, (15, y_offset))
            y_offset += 15
            
            for i, objective in enumerate(quest.objectives):
                status = "✓" if quest.completed_objectives[i] else "○"
                color = TEXT_GREEN if quest.completed_objectives[i] else TEXT_WHITE
                obj_text = self.font_small.render(f"  {status} {objective}", True, color)
                surface.blit(obj_text, (20, y_offset))
                y_offset += 15
            
            y_offset += 5  # Space between quests
        
        # Completed quests panel
        completed_panel = pygame.Rect(10, 170, 460, 100)
        self.draw_panel(surface, completed_panel, "COMPLETED QUESTS")
        
        y_offset = 195
        for quest_id, quest in self.completed_quests.items():
            quest_text = self.font_small.render(f"✓ {quest.title}", True, TEXT_GREEN)
            surface.blit(quest_text, (15, y_offset))
            y_offset += 15
        
        # Instructions
        instructions_text = self.font_small.render("ESC: Back", True, TEXT_BLUE)
        surface.blit(instructions_text, (20, HEIGHT - 20))
    
    def handle_input(self, events):
        """Handle input based on current game state"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F8:
                    toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE and self.game_state == GameState.MAIN_MENU:
                    return_to_launcher()
                elif self.game_state == GameState.MAIN_MENU:
                    self.handle_main_menu_input(event)
                elif self.game_state == GameState.CHARACTER_CREATION:
                    self.handle_character_creation_input(event)
                elif self.game_state == GameState.WORLD_MAP:
                    self.handle_world_map_input(event)
                elif self.game_state == GameState.CHARACTER_SHEET:
                    self.handle_character_sheet_input(event)
                elif self.game_state == GameState.INVENTORY:
                    self.handle_inventory_input(event)
                elif self.game_state == GameState.QUEST_LOG:
                    self.handle_quest_log_input(event)
                elif self.game_state == GameState.COMBAT:
                    self.handle_combat_input(event)
                elif self.game_state == GameState.SKILL_TREE:
                    self.handle_skill_tree_input(event)
        return True
    
    def handle_main_menu_input(self, event):
        """Handle main menu input"""
        if event.key == pygame.K_UP:
            self.selected_menu_item = (self.selected_menu_item - 1) % 3
        elif event.key == pygame.K_DOWN:
            self.selected_menu_item = (self.selected_menu_item + 1) % 3
        elif event.key == pygame.K_RETURN:
            if self.selected_menu_item == 0:  # New Game
                self.game_state = GameState.CHARACTER_CREATION
            elif self.selected_menu_item == 1:  # Load Game
                if self.load_game():
                    self.game_state = GameState.WORLD_MAP
            elif self.selected_menu_item == 2:  # Exit
                return False
        return True
    
    def handle_character_creation_input(self, event):
        """Handle character creation input"""
        if event.key == pygame.K_LEFT:
            classes = list(CharacterClass)
            current_index = classes.index(self.character.character_class)
            self.character.character_class = classes[(current_index - 1) % len(classes)]
            self.apply_class_bonuses()
        elif event.key == pygame.K_RIGHT:
            classes = list(CharacterClass)
            current_index = classes.index(self.character.character_class)
            self.character.character_class = classes[(current_index + 1) % len(classes)]
            self.apply_class_bonuses()
        elif event.key == pygame.K_SPACE:
            self.game_state = GameState.WORLD_MAP
            self.start_quest("royal_mission")  # Start with a quest
    
    def handle_world_map_input(self, event):
        """Handle world map input"""
        if event.key == pygame.K_RETURN:
            # Enter current location (would show town/dungeon view)
            pass
        elif event.key == pygame.K_i:
            self.game_state = GameState.INVENTORY
            self.selected_menu_item = 0
        elif event.key == pygame.K_c:
            self.game_state = GameState.CHARACTER_SHEET
        elif event.key == pygame.K_q:
            self.game_state = GameState.QUEST_LOG
        elif event.key == pygame.K_k:
            self.game_state = GameState.SKILL_TREE
            self.selected_menu_item = 0
        elif event.key == pygame.K_f:
            # Start random combat encounter
            enemy_names = list(self.available_enemies.keys())
            random_enemy = random.choice(enemy_names)
            self.start_combat(random_enemy)
        elif event.key == pygame.K_s:
            self.save_game()
    
    def handle_character_sheet_input(self, event):
        """Handle character sheet input"""
        if event.key == pygame.K_ESCAPE:
            self.game_state = GameState.WORLD_MAP
    
    def handle_inventory_input(self, event):
        """Handle inventory input"""
        if event.key == pygame.K_ESCAPE:
            self.game_state = GameState.WORLD_MAP
        elif event.key == pygame.K_UP:
            self.selected_menu_item = max(0, self.selected_menu_item - 1)
        elif event.key == pygame.K_DOWN:
            self.selected_menu_item = min(len(self.inventory) - 1, self.selected_menu_item + 1)
        elif event.key == pygame.K_RETURN:
            items_list = list(self.inventory.keys())
            if 0 <= self.selected_menu_item < len(items_list):
                item_id = items_list[self.selected_menu_item]
                if item_id in self.game_data.items:
                    item = self.game_data.items[item_id]
                    if item.item_type == ItemType.CONSUMABLE:
                        self.use_item(item_id)
                    else:
                        self.equip_item(item_id)
    
    def handle_quest_log_input(self, event):
        """Handle quest log input"""
        if event.key == pygame.K_ESCAPE:
            self.game_state = GameState.WORLD_MAP
    
    def handle_combat_input(self, event):
        """Handle combat input"""
        if not self.combat_state:
            return
            
        if event.key == pygame.K_ESCAPE:
            # Try to flee combat
            self.process_combat_turn(CombatAction.FLEE)
        elif self.combat_state.player_turn:
            if event.key == pygame.K_1:
                self.process_combat_turn(CombatAction.ATTACK)
            elif event.key == pygame.K_2:
                self.process_combat_turn(CombatAction.DEFEND)
            elif event.key == pygame.K_3:
                self.process_combat_turn(CombatAction.USE_ITEM)
            elif event.key == pygame.K_4:
                self.process_combat_turn(CombatAction.FLEE)
            elif event.key == pygame.K_UP:
                self.selected_menu_item = max(0, self.selected_menu_item - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_menu_item = min(3, self.selected_menu_item + 1)
            elif event.key == pygame.K_RETURN:
                actions = [CombatAction.ATTACK, CombatAction.DEFEND, CombatAction.USE_ITEM, CombatAction.FLEE]
                if 0 <= self.selected_menu_item < len(actions):
                    self.process_combat_turn(actions[self.selected_menu_item])
    
    def handle_skill_tree_input(self, event):
        """Handle skill tree input"""
        if event.key == pygame.K_ESCAPE:
            self.game_state = GameState.WORLD_MAP
        elif event.key == pygame.K_UP:
            self.selected_menu_item = max(0, self.selected_menu_item - 1)
        elif event.key == pygame.K_DOWN:
            self.selected_menu_item = min(len(self.character.skills) - 1, self.selected_menu_item + 1)
        elif event.key == pygame.K_RETURN:
            if self.character.skill_points > 0:
                skill_types = list(self.character.skills.keys())
                if 0 <= self.selected_menu_item < len(skill_types):
                    skill_type = skill_types[self.selected_menu_item]
                    self.character.skills[skill_type].level += 1
                    self.character.skill_points -= 1
    
    def apply_class_bonuses(self):
        """Apply class-specific stat bonuses"""
        # Reset to base stats
        self.character.strength = 10
        self.character.intelligence = 10
        self.character.dexterity = 10
        self.character.constitution = 10
        self.character.wisdom = 10
        self.character.charisma = 10
        
        # Apply class bonuses
        if self.character.character_class == CharacterClass.WARRIOR:
            self.character.strength += 5
            self.character.constitution += 3
        elif self.character.character_class == CharacterClass.MAGE:
            self.character.intelligence += 5
            self.character.wisdom += 3
        elif self.character.character_class == CharacterClass.ROGUE:
            self.character.dexterity += 5
            self.character.charisma += 3
        elif self.character.character_class == CharacterClass.CLERIC:
            self.character.wisdom += 5
            self.character.constitution += 3
        elif self.character.character_class == CharacterClass.PALADIN:
            self.character.strength += 3
            self.character.wisdom += 3
            self.character.charisma += 2
        elif self.character.character_class == CharacterClass.RANGER:
            self.character.dexterity += 3
            self.character.wisdom += 3
            self.character.constitution += 2
        
        self.character.calculate_derived_stats()
    
    def update(self, dt):
        """Update game logic"""
        self.game_time += dt
        
        # Update weather system
        self.weather.update(dt)
        
        # Update day/night cycle
        if self.game_time > 86400:  # 24 hours in seconds (scaled)
            self.day += 1
            self.game_time = 0
    
    def draw_combat(self, surface):
        """Draw combat interface"""
        surface.fill(DARK_BACKGROUND)
        
        if not self.combat_state:
            return
        
        combat = self.combat_state
        
        # Combat arena background
        arena_rect = pygame.Rect(10, 10, WIDTH - 20, 180)
        self.draw_panel(surface, arena_rect, "COMBAT ARENA")
        
        # Player status (left side)
        player_rect = pygame.Rect(20, 40, 200, 100)
        self.draw_panel(surface, player_rect, f"{self.character.name} (Level {self.character.level})")
        
        # Player health bar
        health_bar = pygame.Rect(30, 65, 180, 15)
        self.draw_bar(surface, health_bar.x, health_bar.y, health_bar.width, health_bar.height,
                     self.character.current_health, self.character.max_health, HEALTH_RED)
        
        health_text = f"HP: {self.character.current_health}/{self.character.max_health}"
        text = self.font_small.render(health_text, True, TEXT_WHITE)
        surface.blit(text, (30, 85))
        
        # Player mana bar
        mana_bar = pygame.Rect(30, 105, 180, 15)
        self.draw_bar(surface, mana_bar.x, mana_bar.y, mana_bar.width, mana_bar.height,
                     self.character.current_mana, self.character.max_mana, MANA_BLUE)
        
        mana_text = f"MP: {self.character.current_mana}/{self.character.max_mana}"
        text = self.font_small.render(mana_text, True, TEXT_WHITE)
        surface.blit(text, (30, 125))
        
        # Enemy status (right side)
        enemy_rect = pygame.Rect(250, 40, 200, 100)
        self.draw_panel(surface, enemy_rect, f"{combat.enemy.name} (Level {combat.enemy.level})")
        
        # Enemy health bar
        enemy_health_bar = pygame.Rect(260, 65, 180, 15)
        self.draw_bar(surface, enemy_health_bar.x, enemy_health_bar.y, enemy_health_bar.width, enemy_health_bar.height,
                     combat.enemy.current_health, combat.enemy.max_health, HEALTH_RED)
        
        enemy_health_text = f"HP: {combat.enemy.current_health}/{combat.enemy.max_health}"
        text = self.font_small.render(enemy_health_text, True, TEXT_WHITE)
        surface.blit(text, (260, 85))
        
        # Combat actions panel
        actions_rect = pygame.Rect(10, 200, 300, 110)
        self.draw_panel(surface, actions_rect, "COMBAT ACTIONS")
        
        if combat.player_turn:
            # Show action buttons
            actions = [
                (CombatAction.ATTACK, "Attack"),
                (CombatAction.DEFEND, "Defend"),
                (CombatAction.USE_ITEM, "Use Item"),
                (CombatAction.FLEE, "Flee")
            ]
            
            for i, (action, name) in enumerate(actions):
                color = TEXT_YELLOW if i == self.selected_menu_item else TEXT_WHITE
                text = self.font_medium.render(f"{i+1}. {name}", True, color)
                surface.blit(text, (20, 225 + i * 20))
        else:
            # Enemy turn indicator
            text = self.font_medium.render("Enemy Turn...", True, TEXT_RED)
            surface.blit(text, (20, 250))
        
        # Combat log panel
        log_rect = pygame.Rect(320, 200, 150, 110)
        self.draw_panel(surface, log_rect, "COMBAT LOG")
        
        # Show last few combat log entries
        log_entries = combat.combat_log[-6:]  # Last 6 entries
        for i, entry in enumerate(log_entries):
            text = self.font_small.render(entry[:20] + ("..." if len(entry) > 20 else ""), True, TEXT_WHITE)
            surface.blit(text, (325, 220 + i * 12))
        
        # Instructions
        instructions_text = self.font_small.render("1-4: Select Action | ESC: Flee", True, TEXT_BLUE)
        surface.blit(instructions_text, (20, HEIGHT - 20))
    
    def draw_skill_tree(self, surface):
        """Draw skill tree interface"""
        surface.fill(DARK_BACKGROUND)
        
        # Title
        title_text = self.font_large.render("SKILL TREE", True, TEXT_YELLOW)
        surface.blit(title_text, (20, 20))
        
        # Available skill points
        points_text = self.font_medium.render(f"Available Skill Points: {self.character.skill_points}", True, TEXT_GREEN)
        surface.blit(points_text, (20, 50))
        
        # Skills grid
        y_offset = 80
        for skill_type, skill in self.character.skills.items():
            # Skill panel
            skill_rect = pygame.Rect(20, y_offset, 440, 35)
            self.draw_panel(surface, skill_rect, "")
            
            # Skill name and level
            skill_text = f"{skill.name} - Level {skill.level}"
            text = self.font_medium.render(skill_text, True, TEXT_WHITE)
            surface.blit(text, (30, y_offset + 5))
            
            # Experience bar
            exp_bar = pygame.Rect(250, y_offset + 5, 150, 10)
            self.draw_bar(surface, exp_bar.x, exp_bar.y, exp_bar.width, exp_bar.height,
                         skill.experience, skill.experience_needed, EXP_GREEN)
            
            # Upgrade button
            if self.character.skill_points > 0:
                upgrade_text = "[+]"
                color = TEXT_YELLOW if y_offset // 35 == self.selected_menu_item else TEXT_WHITE
                text = self.font_medium.render(upgrade_text, True, color)
                surface.blit(text, (410, y_offset + 5))
            
            y_offset += 40
        
        # Instructions
        instructions_text = self.font_small.render("Arrow keys: Navigate | Enter: Upgrade | ESC: Back", True, TEXT_BLUE)
        surface.blit(instructions_text, (20, HEIGHT - 20))
    
    def draw_weather_hud(self, surface):
        """Draw weather information on HUD"""
        weather_text = f"Weather: {self.weather.current_weather.value}"
        text = self.font_small.render(weather_text, True, TEXT_WHITE)
        surface.blit(text, (350, 10))
        
        time_text = f"Time: {int(self.weather.time_of_day * 24):02d}:00"
        text = self.font_small.render(time_text, True, TEXT_WHITE)
        surface.blit(text, (350, 25))
        
        temp_text = f"Temp: {self.weather.temperature}°C"
        text = self.font_small.render(temp_text, True, TEXT_WHITE)
        surface.blit(text, (350, 40))
    
    def draw(self, surface):
        """Draw the current game state"""
        if self.game_state == GameState.MAIN_MENU:
            self.draw_main_menu(surface)
        elif self.game_state == GameState.CHARACTER_CREATION:
            self.draw_character_creation(surface)
        elif self.game_state == GameState.WORLD_MAP:
            self.draw_world_map(surface)
            self.draw_weather_hud(surface)
        elif self.game_state == GameState.CHARACTER_SHEET:
            self.draw_character_sheet(surface)
        elif self.game_state == GameState.INVENTORY:
            self.draw_inventory(surface)
        elif self.game_state == GameState.QUEST_LOG:
            self.draw_quest_log(surface)
        elif self.game_state == GameState.COMBAT:
            self.draw_combat(surface)
        elif self.game_state == GameState.SKILL_TREE:
            self.draw_skill_tree(surface)

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
    game = DarkAgesRPG()
    
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
                elif event.key == pygame.K_ESCAPE and game.game_state == GameState.MAIN_MENU:
                    return_to_launcher()
        
        # Handle game input
        if not game.handle_input(events):
            running = False
        
        # Update game
        game.update(dt)
        
        # Draw everything
        game.draw(screen)
        
        # Update display
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 