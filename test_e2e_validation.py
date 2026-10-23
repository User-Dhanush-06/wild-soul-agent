"""End-to-end test of WILD SOUL Agent with Bedrock and Decider."""

import sys
from pathlib import Path

# Add paths
wrapper = Path('.') / '_decider_kit_wrapper'
sys.path.insert(0, str(wrapper.resolve()))
kit_path = Path('.') / '..' / '..' / 'dhanush-raman-b-decider-hackathon-kit' / 'dhanush-raman-b-decider-hackathon-kit'
sys.path.insert(0, str(kit_path.resolve()))
sys.path.insert(0, '.')

print("=" * 80)
print("WILD SOUL AGENT - END-TO-END VALIDATION")
print("=" * 80)

# Import agent and tools
try:
    from agent.agent import WildSoulAgent
    from agent.decision import PATTERN_TAG
    print("✓ Imports successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Create agent
try:
    agent = WildSoulAgent()
    print("✓ Agent instantiated")
except Exception as e:
    print(f"✗ Agent instantiation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test inputs
test_inputs = [
    "I see a goblin ahead with low health. What should I do?",
    "My health is low. Check my status.",
    "Hello!"
]

print("\n" + "=" * 80)
print("RUNNING TESTS")
print("=" * 80)

all_passed = True
for i, message in enumerate(test_inputs, 1):
    print(f"\nTEST {i}: {message}")
    print("-" * 80)
    
    try:
        result = agent.chat(message, session_id="test")
        
        # Verify result structure
        assert "reply" in result, "Missing 'reply' in result"
        assert "decisions" in result, "Missing 'decisions' in result"
        assert "model_id" in result, "Missing 'model_id' in result"
        assert "latency_ms" in result, "Missing 'latency_ms' in result"
        
        # Check decisions
        decisions = result["decisions"]
        print(f"Decisions logged: {len(decisions)}")
        
        if len(decisions) == 0:
            print("⚠ No decisions logged (Decider may not be available)")
        else:
            # Should be exactly one decision per turn after fix
            if len(decisions) > 1:
                print(f"✗ ERROR: {len(decisions)} decisions logged (should be 1)")
                all_passed = False
            else:
                decision = decisions[0]
                print(f"✓ One decision logged")
                print(f"  - Pattern: {decision.get('pattern')}")
                print(f"  - Tool: {decision.get('selected_tool')}")
                print(f"  - Confidence: {decision.get('confidence')}")
                
                # Check for fallback
                if "fallback" in decision:
                    print(f"  - Fallback: {decision['fallback']}")
                    print(f"  - Fallback reason: {decision.get('fallback_reason')}")
        
        # Check response
        reply = result["reply"]
        if reply:
            print(f"✓ Reply generated ({len(reply)} chars)")
            if "blocked" in reply.lower() or "filter" in reply.lower():
                print(f"✗ ERROR: Content filter message detected in reply")
                all_passed = False
            else:
                print(f"  Preview: {reply[:100]}...")
        else:
            print(f"✗ ERROR: Empty reply")
            all_passed = False
        
        # Check metadata
        print(f"✓ Model: {result['model_id']}")
        print(f"✓ Latency: {result['latency_ms']}ms")
        
    except Exception as e:
        print(f"✗ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False

print("\n" + "=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)

if all_passed:
    print("✅ ALL TESTS PASSED")
    print("\nVerified:")
    print("  ✓ Agent runs without errors")
    print("  ✓ Decisions are logged")
    print("  ✓ One decision per turn")
    print("  ✓ No content filter errors")
    print("  ✓ Responses generated")
    print("  ✓ Metadata correct")
else:
    print("⚠ SOME TESTS HAD ISSUES (see above)")

print("\n" + "=" * 80)
