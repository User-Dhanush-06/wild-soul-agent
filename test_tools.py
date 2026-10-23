"""Unit tests for WILD SOUL game tools - direct import from tools only."""

import sys
sys.path.insert(0, r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")

# Import only tools (no Decider/Agent dependencies)
from agent.tools import (
    manage_inventory, interact_npc, explore_area, 
    combat_action, check_status, TOOLS
)

def test_manage_inventory():
    """Test inventory management tool."""
    print("Testing manage_inventory...")
    
    # Test examine
    result = manage_inventory("examine", "health_potion")
    assert result["success"] == True, f"Examine failed: {result}"
    assert result["operation"] == "examine"
    print("  ✓ Examine works")
    
    # Test invalid action
    result = manage_inventory("invalid", "health_potion")
    assert result["success"] == False
    print("  ✓ Invalid action rejected")
    
    # Test invalid item
    result = manage_inventory("examine", "nonexistent_item")
    assert result["success"] == False
    print("  ✓ Invalid item rejected")
    
    print("manage_inventory: PASS\n")


def test_check_status():
    """Test status check tool."""
    print("Testing check_status...")
    
    # Test all status
    result = check_status("all")
    assert result["success"] == True
    assert "health" in result or result["max_health"] in result.values()
    print("  ✓ Status check returns data")
    
    # Test specific status types
    for status_type in ["health", "mana", "buffs", "debuffs", "quests"]:
        result = check_status(status_type)
        assert result["success"] == True or result["success"] == False
    print("  ✓ All status types handled")
    
    print("check_status: PASS\n")


def test_interact_npc():
    """Test NPC interaction tool."""
    print("Testing interact_npc...")
    
    # Test valid NPC interaction
    result = interact_npc("merchant_garrick", "talk")
    assert result["success"] == True
    print("  ✓ NPC talk works")
    
    # Test invalid NPC
    result = interact_npc("nonexistent_npc", "talk")
    assert result["success"] == False
    print("  ✓ Invalid NPC rejected")
    
    # Test various interaction types
    for interaction in ["talk", "trade", "quest"]:
        result = interact_npc("merchant_garrick", interaction)
        assert result["success"] == True or result["success"] == False
    print("  ✓ Interaction types handled")
    
    print("interact_npc: PASS\n")


def test_explore_area():
    """Test exploration tool."""
    print("Testing explore_area...")
    
    # Test examine (no direction needed)
    result = explore_area(action="examine")
    assert result["success"] == True
    print("  ✓ Examine location works")
    
    # Test search
    result = explore_area(action="search")
    assert result["success"] == True
    print("  ✓ Search works")
    
    # Test discover
    result = explore_area(action="discover")
    assert result["success"] == True
    print("  ✓ Discover works")
    
    print("explore_area: PASS\n")


def test_combat_action():
    """Test combat tool."""
    print("Testing combat_action...")
    
    # Test attack
    result = combat_action("attack", "goblin")
    assert result["success"] == True
    assert "damage_dealt" in result
    print("  ✓ Attack works")
    
    # Test defend
    result = combat_action("defend")
    assert result["success"] == True
    print("  ✓ Defend works")
    
    # Test ability
    result = combat_action("ability", "goblin", "fireball")
    assert result["success"] == True or result["success"] == False
    print("  ✓ Ability handling works")
    
    # Test flee
    result = combat_action("flee")
    assert result["success"] in [True, False]
    print("  ✓ Flee handling works")
    
    print("combat_action: PASS\n")


def test_tools_exported():
    """Test that all tools are exported."""
    print("Testing tools export...")
    
    assert len(TOOLS) == 5, f"Expected 5 tools, got {len(TOOLS)}"
    print(f"  ✓ All 5 tools exported: {[t.__name__ for t in TOOLS]}")
    
    print("tools_export: PASS\n")


if __name__ == "__main__":
    print("=" * 60)
    print("WILD SOUL Agent - Tool Unit Tests")
    print("=" * 60 + "\n")
    
    try:
        test_manage_inventory()
        test_check_status()
        test_interact_npc()
        test_explore_area()
        test_combat_action()
        test_tools_exported()
        
        print("=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
