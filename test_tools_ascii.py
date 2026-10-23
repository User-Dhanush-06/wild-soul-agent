import sys
sys.path.insert(0, r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")

from agent.tools import (
    manage_inventory, interact_npc, explore_area, 
    combat_action, check_status, TOOLS
)

# Test 1: manage_inventory
print("TEST 1: manage_inventory")
result = manage_inventory("examine", "health_potion")
assert result["success"] == True
print("  PASS: examine works")

result = manage_inventory("invalid", "health_potion")
assert result["success"] == False
print("  PASS: invalid action rejected")

# Test 2: check_status
print("\nTEST 2: check_status")
result = check_status("all")
assert result["success"] == True
print("  PASS: status check works")

# Test 3: interact_npc
print("\nTEST 3: interact_npc")
result = interact_npc("merchant_garrick", "talk")
assert result["success"] == True
print("  PASS: NPC interaction works")

# Test 4: explore_area
print("\nTEST 4: explore_area")
result = explore_area(action="examine")
assert result["success"] == True
print("  PASS: explore works")

# Test 5: combat_action
print("\nTEST 5: combat_action")
result = combat_action("attack", "goblin")
assert result["success"] == True
print("  PASS: combat works")

# Test 6: tools export
print("\nTEST 6: tools_export")
assert len(TOOLS) == 5
print("  PASS: all 5 tools exported")

print("\nALL TESTS PASSED")
