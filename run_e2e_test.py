"""Test runner with explicit path handling."""

import sys
import os
from pathlib import Path

# Change to wild-soul-agent directory
os.chdir(r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")

# Setup paths
wrapper_path = str(Path("_decider_kit_wrapper").resolve())
kit_path = str(Path("..\\..\\dhanush-raman-b-decider-hackathon-kit\\dhanush-raman-b-decider-hackathon-kit").resolve())
agent_path = str(Path(".").resolve())

sys.path.insert(0, wrapper_path)
sys.path.insert(0, kit_path)
sys.path.insert(0, agent_path)

print("=" * 80)
print("PATH SETUP")
print("=" * 80)
print(f"Working directory: {os.getcwd()}")
print(f"Agent path: {agent_path}")
print(f"Wrapper path: {wrapper_path}")
print(f"Kit path: {kit_path}")

print("\n" + "=" * 80)
print("IMPORTING MODULES")
print("=" * 80)

# Import in correct order
try:
    from _decider_kit_wrapper import Decider, agent_model, default_model_id, strip_thinking
    print("✓ _decider_kit_wrapper OK")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

try:
    from strands import Agent
    print("✓ Strands Agent OK")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

try:
    # Import directly from the wild-soul agent
    from agent.tools import TOOLS, check_status
    print(f"✓ Agent tools OK ({len(TOOLS)} tools)")
except Exception as e:
    print(f"✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from agent.decision import ToolSelector, PATTERN_TAG
    print("✓ Decision pattern OK")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

try:
    from agent.agent import WildSoulAgent, NAME
    print(f"✓ Agent OK: {NAME}")
except Exception as e:
    print(f"✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("AGENT INSTANTIATION")
print("=" * 80)

try:
    agent = WildSoulAgent()
    print("✓ Agent instance created")
except Exception as e:
    print(f"✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("RUNNING E2E TESTS")
print("=" * 80)

tests = [
    ("Combat scenario", "I see a goblin ahead with low health. What should I do?"),
    ("Status check", "My health is low. Check my status."),
    ("Conversational", "Hello!"),
]

for test_name, message in tests:
    print(f"\n{'=' * 80}")
    print(f"TEST: {test_name}")
    print(f"{'=' * 80}")
    print(f"Input: {message}")
    
    try:
        result = agent.chat(message, session_id="default")
        
        # Check structure
        assert "reply" in result, "Missing reply"
        assert "decisions" in result, "Missing decisions"
        assert "latency_ms" in result, "Missing latency"
        
        decisions = result["decisions"]
        reply = result["reply"]
        latency = result["latency_ms"]
        
        print(f"\n✓ Response received")
        print(f"  Decisions logged: {len(decisions)}")
        
        # Check decision count
        if len(decisions) > 1:
            print(f"  ⚠ WARNING: {len(decisions)} decisions (expected 1)")
        elif len(decisions) == 1:
            d = decisions[0]
            print(f"  ✓ Decision:")
            print(f"    - Tool: {d.get('selected_tool')}")
            print(f"    - Confidence: {d.get('confidence'):.3f}")
            if "fallback" in d:
                print(f"    - Fallback: {d['fallback']}")
                print(f"    - Reason: {d.get('fallback_reason')}")
        else:
            print(f"  ⚠ No decisions logged")
        
        print(f"\n  Reply ({len(reply)} chars):")
        if len(reply) > 200:
            print(f"    {reply[:200]}...")
        else:
            print(f"    {reply}")
        
        # Check for errors
        if "blocked" in reply.lower() or "filter" in reply.lower():
            print(f"  ⚠ WARNING: Content filter message detected")
        
        print(f"\n  Latency: {latency}ms")
        print(f"  Model: {result.get('model_id')}")
        
    except Exception as e:
        print(f"\n✗ Test failed with exception:")
        print(f"  {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 80)
print("END OF VALIDATION")
print("=" * 80)
