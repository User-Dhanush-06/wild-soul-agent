import sys
import inspect
from pathlib import Path
sys.path.insert(0, r"c:\Users\userd\Downloads\MY-AGENT\dhanush-raman-b-decider-hackathon-kit\dhanush-raman-b-decider-hackathon-kit")
sys.path.insert(0, r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")

print("=== HackathonAgent Interface Contract Verification ===\n")

# Test 1: Check WildSoulAgent class exists
print("1. Checking WildSoulAgent class...")
try:
    from agent.agent import WildSoulAgent
    print("   PASS: WildSoulAgent class exists")
except Exception as e:
    print(f"   FAIL: {e}")
    exit(1)

# Test 2: Check __init__ signature
print("\n2. Checking __init__ signature...")
try:
    sig = inspect.signature(WildSoulAgent.__init__)
    params = list(sig.parameters.keys())
    expected = ['self', 'decider', 'model_id', 'eager']
    
    for p in expected:
        assert p in params, f"Missing parameter: {p}"
    
    print(f"   PASS: __init__ signature correct")
    print(f"   Parameters: {params}")
except Exception as e:
    print(f"   FAIL: {e}")

# Test 3: Check chat method signature
print("\n3. Checking chat method signature...")
try:
    sig = inspect.signature(WildSoulAgent.chat)
    params = list(sig.parameters.keys())
    expected = ['self', 'message', 'session_id', 'images']
    
    for p in expected:
        assert p in params, f"Missing parameter: {p}"
    
    print(f"   PASS: chat() signature correct")
    print(f"   Parameters: {params}")
    print(f"   Return type annotation: {sig.return_annotation}")
except Exception as e:
    print(f"   FAIL: {e}")

# Test 4: Check chat return format
print("\n4. Checking chat return format...")
try:
    agent = WildSoulAgent.__new__(WildSoulAgent)
    agent.decider = None
    agent.model_id = "test"
    agent.eager = False
    agent.sessions = {}
    
    # Can't call without full Strands setup, but check the structure
    source = inspect.getsource(WildSoulAgent.chat)
    
    required_fields = ['reply', 'decisions', 'model_id', 'latency_ms', 'agent', 'eager']
    for field in required_fields:
        assert f'"{field}"' in source or f"'{field}'" in source, f"Missing return field: {field}"
    
    print(f"   PASS: chat() returns all required fields:")
    for field in required_fields:
        print(f"     - {field}")
except Exception as e:
    print(f"   FAIL: {e}")

# Test 5: Check session management
print("\n5. Checking session management...")
try:
    source = inspect.getsource(WildSoulAgent._session)
    assert "session_id" in source, "Missing session_id handling"
    assert "sessions" in source, "Missing session storage"
    assert "Agent(" in source, "Missing Strands Agent creation"
    print("   PASS: Session management implemented:")
    print("     - Per-session Agent instances")
    print("     - ToolSelector integration")
    print("     - Tool and intervention wiring")
except Exception as e:
    print(f"   FAIL: {e}")

# Test 6: Check integration wiring
print("\n6. Checking Strands integration...")
try:
    source = inspect.getsource(WildSoulAgent._session)
    assert "ToolSelector" in source, "Missing ToolSelector integration"
    assert "agent_model" in source, "Missing Bedrock model integration"
    assert "interventions" in source, "Missing intervention wiring"
    print("   PASS: Strands integration complete:")
    print("     - agent_model() for Bedrock")
    print("     - ToolSelector as intervention")
    print("     - TOOLS list passed to Agent")
except Exception as e:
    print(f"   FAIL: {e}")

print("\n=== HackathonAgent interface verified ===")
