"""Direct E2E test without path conflicts."""

import sys
import os

# Work from wild-soul-agent directory
os.chdir(r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")

# Add ONLY wild-soul paths
sys.path.insert(0, r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")
sys.path.insert(0, r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\_decider_kit_wrapper")
sys.path.insert(0, r"C:\Users\userd\Downloads\MY-AGENT\dhanush-raman-b-decider-hackathon-kit\dhanush-raman-b-decider-hackathon-kit")

print("=" * 80)
print("WILD SOUL AGENT - E2E VALIDATION")
print("=" * 80)

# Test 1: Import checks
print("\n[1] IMPORT CHECKS")
print("-" * 80)

try:
    from _decider_kit_wrapper import Decider, agent_model, default_model_id, strip_thinking
    print("✓ decider_kit_wrapper")
except Exception as e:
    print(f"✗ decider_kit_wrapper: {e}")
    sys.exit(1)

try:
    from strands import Agent
    print("✓ strands.Agent")
except Exception as e:
    print(f"✗ strands: {e}")
    sys.exit(1)

# Test 2: Import wild-soul modules
print("\n[2] WILD SOUL MODULES")
print("-" * 80)

try:
    # Load tools module directly
    import importlib.util
    spec = importlib.util.spec_from_file_location("tools", r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\agent\tools.py")
    tools_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tools_module)
    TOOLS = tools_module.TOOLS
    check_status = tools_module.check_status
    print(f"✓ agent.tools ({len(TOOLS)} tools)")
except Exception as e:
    print(f"✗ agent.tools: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from agent.decision import ToolSelector, PATTERN_TAG
    print(f"✓ agent.decision (pattern: {PATTERN_TAG})")
except Exception as e:
    print(f"✗ agent.decision: {e}")
    sys.exit(1)

try:
    from agent.agent import WildSoulAgent, NAME
    print(f"✓ agent.agent ({NAME})")
except Exception as e:
    print(f"✗ agent.agent: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Agent instantiation
print("\n[3] AGENT INSTANTIATION")
print("-" * 80)

try:
    agent = WildSoulAgent()
    print(f"✓ Agent created")
except Exception as e:
    print(f"✗ Agent creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Run test inputs
print("\n[4] TEST INPUTS")
print("-" * 80)

tests = [
    ("I see a goblin ahead with low health. What should I do?", "combat scenario"),
    ("My health is low. Check my status.", "status check"),
    ("Hello!", "conversational"),
]

for message, desc in tests:
    print(f"\n▶ {desc}: {message}")
    
    try:
        result = agent.chat(message, session_id="default")
        
        # Validate result structure
        assert isinstance(result, dict), "Result not dict"
        assert "reply" in result, "No reply"
        assert "decisions" in result, "No decisions"
        
        decisions = result["decisions"]
        reply = result["reply"]
        
        # Check decision count
        if len(decisions) == 0:
            print(f"  ⚠ 0 decisions logged (Decider endpoint may be unavailable)")
        elif len(decisions) == 1:
            d = decisions[0]
            print(f"  ✓ 1 decision logged")
            print(f"    Tool: {d.get('selected_tool')}")
            print(f"    Confidence: {d.get('confidence'):.3f}")
            if "fallback" in d and d["fallback"]:
                print(f"    Fallback: YES ({d.get('fallback_reason')})")
            else:
                print(f"    Fallback: NO")
        else:
            print(f"  ✗ {len(decisions)} decisions (expected 0 or 1)")
        
        # Check reply
        if reply and len(reply) > 0:
            print(f"  ✓ Reply: {len(reply)} chars")
            if "blocked" in reply.lower() or "filter" in reply.lower():
                print(f"  ✗ Content filter detected in reply")
            else:
                preview = reply[:80] + "..." if len(reply) > 80 else reply
                print(f"    '{preview}'")
        else:
            print(f"  ✗ Empty reply")
        
        print(f"  ✓ Latency: {result.get('latency_ms')}ms")
        
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 80)
print("E2E VALIDATION COMPLETE")
print("=" * 80)
