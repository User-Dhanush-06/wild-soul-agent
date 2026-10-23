"""Game tools for WILD SOUL Agent - the agent's capabilities in the game world.

Each tool has a clear one-line docstring: the decider reads it during tool selection.
Built with the AWS User Group Madurai Strands Decider hackathon kit.
"""

from __future__ import annotations
from strands import tool
import random

# --- Game State Data ---

PLAYER_INVENTORY = {
    "health_potion": {"quantity": 3, "type": "consumable", "stats": {"heal": 50}, "equipped": False},
    "mana_potion": {"quantity": 2, "type": "consumable", "stats": {"restore_mana": 30}, "equipped": False},
    "iron_sword": {"quantity": 1, "type": "weapon", "stats": {"damage": 15, "range": "melee"}, "equipped": True},
    "leather_armor": {"quantity": 1, "type": "armor", "stats": {"defense": 10}, "equipped": False},
    "wooden_shield": {"quantity": 1, "type": "shield", "stats": {"block": 5}, "equipped": False},
    "magic_scroll": {"quantity": 1, "type": "consumable", "stats": {"damage": 100}, "equipped": False},
    "gold_coin": {"quantity": 250, "type": "currency", "stats": {}, "equipped": False},
}

EQUIPMENT_SLOTS = ["head", "chest", "legs", "feet", "main_hand", "off_hand", "necklace", "ring"]

PLAYER_STATE = {
    "health": 85,
    "max_health": 100,
    "mana": 40,
    "max_mana": 50,
    "attack": 20,
    "defense": 15,
    "buffs": ["strength (+10 damage)", "haste (+15% speed)"],
    "debuffs": ["poison (5 hp/sec)"],
}

GAME_WORLD = {
    "current_location": "village_square",
    "locations": {
        "village_square": {"description": "A bustling village square", "exits": ["north_forest", "east_market"], "entities": ["merchant_garrick"]},
        "north_forest": {"description": "A dense forest north of the village", "exits": ["village_square", "goblin_cave"], "entities": []},
        "goblin_cave": {"description": "A dark cave with goblin activity", "exits": ["north_forest"], "entities": ["goblin", "goblin", "goblin_shaman"]},
        "east_market": {"description": "A bustling marketplace", "exits": ["village_square", "tavern"], "entities": ["merchant_garrick", "bard"]},
        "tavern": {"description": "A cozy tavern with locals", "exits": ["east_market"], "entities": ["bartender"]},
    }
}

NPCS = {
    "merchant_garrick": {"name": "Merchant Garrick", "type": "merchant", "location": "village_square"},
    "bard": {"name": "Bard", "type": "performer", "location": "east_market"},
    "bartender": {"name": "Bartender", "type": "npc", "location": "tavern"},
    "goblin_shaman": {"name": "Goblin Shaman", "type": "enemy", "location": "goblin_cave"},
}

# --- Tool Implementation ---

@tool
def manage_inventory(action: str, item_name: str, target_slot: str | None = None) -> dict:
    """Manage player inventory: equip, use, drop, or examine items."""
    action = action.lower().strip()
    item_name = item_name.lower().strip()
    
    if action not in {"equip", "use", "drop", "examine"}:
        return {"success": False, "message": f"Invalid action: {action}", "operation": action, "inventory": list(PLAYER_INVENTORY.keys())}
    
    if item_name not in PLAYER_INVENTORY:
        return {"success": False, "message": f"Item not found: {item_name}", "operation": action, "inventory": list(PLAYER_INVENTORY.keys())}
    
    item = PLAYER_INVENTORY[item_name]
    
    if action == "examine":
        return {"success": True, "message": f"{item_name}: {item['type']}, stats={item['stats']}", "operation": "examine", "item": item}
    elif action == "use":
        if item["type"] != "consumable":
            return {"success": False, "message": f"Cannot use {item_name} (not consumable)", "operation": "use", "item": item}
        item["quantity"] -= 1
        if item["quantity"] <= 0:
            del PLAYER_INVENTORY[item_name]
        return {"success": True, "message": f"Used {item_name}", "operation": "use", "item": item}
    elif action == "drop":
        del PLAYER_INVENTORY[item_name]
        return {"success": True, "message": f"Dropped {item_name}", "operation": "drop", "item": item}
    elif action == "equip":
        item["equipped"] = True
        return {"success": True, "message": f"Equipped {item_name}", "operation": "equip", "item": item}


@tool
def interact_npc(npc_name: str, interaction_type: str, dialogue_option: str | None = None) -> dict:
    """Interact with NPCs: talk, trade, accept quests, or gather information."""
    npc_name = npc_name.lower().strip()
    interaction_type = interaction_type.lower().strip()
    
    if npc_name not in NPCS:
        return {"success": False, "message": f"NPC not found: {npc_name}", "npc": None}
    
    if interaction_type not in {"talk", "trade", "quest", "ask"}:
        return {"success": False, "message": f"Invalid interaction: {interaction_type}", "npc": npc_name}
    
    npc = NPCS[npc_name]
    
    if interaction_type == "talk":
        dialogues = ["Greetings, adventurer!", "Nice to see you.", "Stay safe out there."]
        return {"success": True, "message": random.choice(dialogues), "npc": npc_name, "dialogue": True}
    elif interaction_type == "trade":
        return {"success": True, "message": f"Trading with {npc['name']}...", "npc": npc_name, "items_available": 5}
    elif interaction_type == "quest":
        return {"success": True, "message": f"{npc['name']} offers a quest.", "npc": npc_name, "quest_id": f"q_{random.randint(1, 100)}", "reward": random.randint(50, 500)}
    elif interaction_type == "ask":
        return {"success": True, "message": f"{npc['name']} shares information.", "npc": npc_name, "info": "useful"}


@tool
def explore_area(direction: str | None = None, action: str = "move") -> dict:
    """Navigate the game world: move between locations, search for items, or discover secrets."""
    action = action.lower().strip()
    
    if action not in {"move", "search", "discover", "examine"}:
        return {"success": False, "message": f"Invalid action: {action}"}
    
    current = GAME_WORLD["current_location"]
    location = GAME_WORLD["locations"].get(current, {})
    
    if action == "move":
        if not direction:
            return {"success": False, "message": "Direction required for move action"}
        exits = location.get("exits", [])
        if direction.lower() not in exits:
            return {"success": False, "message": f"Cannot move {direction}. Exits: {exits}"}
        GAME_WORLD["current_location"] = direction.lower()
        new_loc = GAME_WORLD["locations"].get(direction.lower(), {})
        return {"success": True, "message": f"Moved to {direction}", "location": direction, "description": new_loc.get("description", ""), "entities": new_loc.get("entities", [])}
    
    elif action == "search":
        loot = ["gold_coin", "health_potion", "ancient_rune"]
        found = random.choice(loot)
        return {"success": True, "message": f"Found {found}!", "location": current, "found": found}
    
    elif action == "discover":
        secrets = ["hidden passage", "treasure chest", "old map"]
        discovered = random.choice(secrets)
        return {"success": True, "message": f"Discovered: {discovered}!", "location": current, "discovered": discovered}
    
    elif action == "examine":
        return {"success": True, "message": location.get("description", "An unremarkable area"), "location": current, "exits": location.get("exits", [])}


@tool
def combat_action(action: str, target: str | None = None, ability_name: str | None = None) -> dict:
    """Engage in combat: attack enemies, defend against attacks, or use special abilities."""
    action = action.lower().strip()
    
    if action not in {"attack", "defend", "ability", "flee"}:
        return {"success": False, "message": f"Invalid combat action: {action}"}
    
    if action == "attack":
        if not target:
            return {"success": False, "message": "Target required for attack"}
        damage = random.randint(10, 25)
        return {"success": True, "message": f"Attacked {target} for {damage} damage", "damage_dealt": damage, "damage_taken": 0}
    
    elif action == "defend":
        mitigation = random.randint(5, 15)
        return {"success": True, "message": f"Assumed defensive stance, reducing damage by {mitigation}", "damage_dealt": 0, "damage_taken": 0}
    
    elif action == "ability":
        if not ability_name:
            return {"success": False, "message": "Ability name required"}
        damage = random.randint(30, 60)
        return {"success": True, "message": f"Used ability {ability_name} for {damage} damage", "damage_dealt": damage, "damage_taken": 0}
    
    elif action == "flee":
        success_chance = random.random()
        if success_chance > 0.3:
            return {"success": True, "message": "Fled from combat successfully!", "fled": True}
        else:
            return {"success": False, "message": "Failed to flee! You're caught in combat.", "fled": False}


@tool
def check_status(status_type: str = "all") -> dict:
    """Check player status: health, mana, buffs, debuffs, quests, or inventory."""
    status_type = status_type.lower().strip()
    
    if status_type not in {"all", "health", "mana", "buffs", "debuffs", "quests", "inventory"}:
        return {"success": False, "message": f"Invalid status type: {status_type}"}
    
    result = {
        "success": True,
        "status_type": status_type,
        "health": PLAYER_STATE["health"],
        "max_health": PLAYER_STATE["max_health"],
        "mana": PLAYER_STATE["mana"],
        "max_mana": PLAYER_STATE["max_mana"],
    }
    
    if status_type in {"all", "buffs"}:
        result["buffs"] = PLAYER_STATE["buffs"]
    if status_type in {"all", "debuffs"}:
        result["debuffs"] = PLAYER_STATE["debuffs"]
    if status_type in {"all", "quests"}:
        result["active_quests"] = ["Goblin Threat", "Lost Relic"]
    if status_type in {"all", "inventory"}:
        result["inventory_count"] = len(PLAYER_INVENTORY)
    
    return result


TOOLS = [manage_inventory, interact_npc, explore_area, combat_action, check_status]
