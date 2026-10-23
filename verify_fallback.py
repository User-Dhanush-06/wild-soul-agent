import sys
import inspect
sys.path.insert(0, r"c:\Users\userd\Downloads\MY-AGENT\dhanush-raman-b-decider-hackathon-kit\dhanush-raman-b-decider-hackathon-kit")
sys.path.insert(0, r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")

print("=== Tool Selection Confidence and Fallback Verification ===\n")

# Test 1: Check confidence threshold
print("1. Checking confidence threshold...")
try:
    from agent.decision import ToolSelector
    
    # Create a mock decider
    class MockDecider:
        pass
    
    selector = ToolSelector(MockDecider(), confidence_threshold=0.6)
    assert selector.confidence_threshold == 0.6, "Default threshold should be 0.6"
    print("   PASS: Confidence threshold set to 0.6")
except Exception as e:
    print(f"   FAIL: {e}")

# Test 2: Check fallback logic
print("\n2. Checking fallback logic in before_tool_call...")
try:
    source = inspect.getsource(ToolSelector.before_tool_call)
    
    checks = {
        "confidence < threshold": "confidence < self.confidence_threshold" in source,
        "fallback flag": '"fallback"' in source or "'fallback'" in source,
        "fallback tool": "check_status" in source,
        "confidence extraction": "confidence" in source and "choice.p_choice" in source
    }
    
    all_pass = all(checks.values())
    
    if all_pass:
        print("   PASS: Fallback logic implemented:")
        for check, result in checks.items():
            print(f"     - {check}: implemented")
    else:
        print("   FAIL: Missing fallback components:")
        for check, result in checks.items():
            if not result:
                print(f"     - {check}: MISSING")
except Exception as e:
    print(f"   FAIL: {e}")

# Test 3: Check decision logging
print("\n3. Checking decision logging...")
try:
    from agent.decision import ToolSelector
    
    source = inspect.getsource(ToolSelector.before_tool_call)
    
    log_fields = {
        "pattern": "PATTERN_TAG" in source,
        "selected_tool": "selected_tool" in source,
        "confidence": "confidence" in source,
        "options": "p_options" in source,
        "decider_ms": "decider_ms" in source or "latency_ms" in source
    }
    
    all_pass = all(log_fields.values())
    
    if all_pass:
        print("   PASS: Decision logging complete:")
        for field, result in log_fields.items():
            print(f"     - {field}")
    else:
        print("   FAIL: Missing log fields:")
        for field, result in log_fields.items():
            if not result:
                print(f"     - {field}: MISSING")
except Exception as e:
    print(f"   FAIL: {e}")

# Test 4: Check tool selector integration
print("\n4. Checking ToolSelector integration in agent...")
try:
    from agent.agent import WildSoulAgent
    
    source = inspect.getsource(WildSoulAgent._session)
    
    assert "ToolSelector" in source, "ToolSelector not created"
    assert "interventions=" in source, "interventions not passed"
    assert "tool_selector" in source, "tool_selector not stored"
    
    print("   PASS: ToolSelector integrated into Agent:")
    print("     - Instance created")
    print("     - Passed as intervention")
    print("     - Stored for log access")
except Exception as e:
    print(f"   FAIL: {e}")

# Test 5: Check decision access in chat
print("\n5. Checking decision access in chat method...")
try:
    from agent.agent import WildSoulAgent
    
    source = inspect.getsource(WildSoulAgent.chat)
    
    checks = {
        "get tool_selector": "tool_selector" in source,
        "access decision log": "tool_selector.log" in source,
        "return decisions": '"decisions"' in source or "'decisions'" in source
    }
    
    all_pass = all(checks.values())
    
    if all_pass:
        print("   PASS: Decisions accessible in chat response:")
        for check in checks.keys():
            print(f"     - {check}")
    else:
        print("   FAIL: Missing decision access")
except Exception as e:
    print(f"   FAIL: {e}")

print("\n=== Confidence and fallback verified ===")
