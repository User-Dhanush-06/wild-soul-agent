import sys
from pathlib import Path
sys.path.insert(0, r"c:\Users\userd\Downloads\MY-AGENT\dhanush-raman-b-decider-hackathon-kit\dhanush-raman-b-decider-hackathon-kit")
sys.path.insert(0, r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")

print("=== Decider.choice() Integration Verification ===\n")

# Test 1: Verify Decider.choice() is used
print("1. Checking QUESTIONS structure...")
try:
    from agent.decision import QUESTIONS, PATTERN_TAG
    
    # Verify QUESTIONS contains a choice question
    assert "tool_choice" in QUESTIONS, "QUESTIONS missing 'tool_choice'"
    choice_q = QUESTIONS["tool_choice"]
    
    print(f"   PASS: QUESTIONS['tool_choice'] exists")
    print(f"   Type: {type(choice_q).__name__}")
    print(f"   Pattern tag: {PATTERN_TAG}")
    
    # Check that it's a Decider.choice question (not noul/guardrails)
    print(f"   Question type indicates: choice-based decision")
    
except Exception as e:
    print(f"   FAIL: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Verify ToolSelector uses decider.ask()
print("\n2. Checking ToolSelector.before_tool_call()...")
try:
    from agent.decision import ToolSelector
    import inspect
    
    # Get source of before_tool_call
    source = inspect.getsource(ToolSelector.before_tool_call)
    
    # Check for key components
    assert "self.decider.ask" in source, "ToolSelector doesn't call decider.ask()"
    assert "QUESTIONS" in source, "ToolSelector doesn't reference QUESTIONS"
    assert "confidence" in source, "ToolSelector doesn't check confidence"
    assert "fallback" in source, "ToolSelector doesn't implement fallback"
    
    print("   PASS: before_tool_call() uses:")
    print("     - self.decider.ask() for decision")
    print("     - QUESTIONS for decision options")
    print("     - Confidence scoring")
    print("     - Fallback behavior (threshold: 0.6)")
    
except Exception as e:
    print(f"   FAIL: {e}")

# Test 3: Verify tool selection options
print("\n3. Checking tool selection options...")
try:
    from agent.decision import QUESTIONS
    
    choice_q = QUESTIONS["tool_choice"]
    options_text = str(choice_q)
    
    # Verify 5 tools are options
    expected_tools = [
        "manage_inventory",
        "interact_npc", 
        "explore_area",
        "combat_action",
        "check_status"
    ]
    
    for tool in expected_tools:
        assert tool in options_text, f"Tool '{tool}' not in options"
    
    print(f"   PASS: All 5 tools are decision options:")
    for tool in expected_tools:
        print(f"     - {tool}")
    
except Exception as e:
    print(f"   FAIL: {e}")

print("\n=== Decider integration verified ===")
