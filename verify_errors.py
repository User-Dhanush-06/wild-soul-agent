import sys
sys.path.insert(0, r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")

print("=== Error Handling Verification ===\n")

from agent.tools import manage_inventory, interact_npc, explore_area, combat_action, check_status

# Test 1: Invalid inventory action
print("1. Testing error handling in manage_inventory...")
result = manage_inventory("invalid_action", "health_potion")
assert result["success"] == False, "Should reject invalid action"
assert "message" in result, "Should include error message"
print(f"   PASS: Invalid action handled - '{result['message']}'")

# Test 2: Invalid item
result = manage_inventory("examine", "nonexistent_item")
assert result["success"] == False, "Should reject nonexistent item"
print(f"   PASS: Invalid item handled - '{result['message']}'")

# Test 3: Invalid status type
print("\n2. Testing error handling in check_status...")
result = check_status("invalid_status")
assert result["success"] == False, "Should reject invalid status type"
print(f"   PASS: Invalid status type handled - '{result['message']}'")

# Test 4: Invalid NPC
print("\n3. Testing error handling in interact_npc...")
result = interact_npc("nonexistent_npc", "talk")
assert result["success"] == False, "Should reject nonexistent NPC"
print(f"   PASS: Invalid NPC handled - '{result['message']}'")

# Test 5: Invalid interaction type
result = interact_npc("merchant_garrick", "invalid_type")
assert result["success"] == False, "Should reject invalid interaction"
print(f"   PASS: Invalid interaction handled - '{result['message']}'")

# Test 6: Invalid combat action
print("\n4. Testing error handling in combat_action...")
result = combat_action("invalid_action", "goblin")
assert result["success"] == False, "Should reject invalid action"
print(f"   PASS: Invalid combat action handled - '{result['message']}'")

# Test 7: Attack without target
result = combat_action("attack")
assert result["success"] == False, "Should require target for attack"
print(f"   PASS: Missing target handled - '{result['message']}'")

# Test 8: Invalid explore action
print("\n5. Testing error handling in explore_area...")
result = explore_area(action="invalid_action")
assert result["success"] == False, "Should reject invalid action"
print(f"   PASS: Invalid explore action handled - '{result['message']}'")

print("\n=== Error handling verified ===")
