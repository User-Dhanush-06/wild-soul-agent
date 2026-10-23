"""Direct E2E test of WILD SOUL agent code."""

import sys
import os

os.chdir(r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")

# Only add wild-soul paths, NOT kit
sys.path.insert(0, r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")
sys.path.insert(0, r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\_decider_kit_wrapper")
sys.path.insert(0, r"C:\Users\userd\Downloads\MY-AGENT\dhanush-raman-b-decider-hackathon-kit\dhanush-raman-b-decider-hackathon-kit")

print("=" * 80)
print("WILD SOUL AGENT - END-TO-END VALIDATION")
print("=" * 80)

print("\n[SETUP] Importing dependencies...")

from _decider_kit_wrapper import Decider, agent_model, default_model_id, strip_thinking
from strands import Agent

print("✓ Core dependencies OK")

# Load game tools
print("\n[TOOLS] Loading game tools...")
import importlib.util
spec = importlib.util.spec_from_file_location("game_tools", r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\agent\tools.py")
game_tools_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game_tools_module)
TOOLS = game_tools_module.TOOLS
print(f"✓ {len(TOOLS)} game tools loaded")

# Load decision pattern
print("\n[DECISION] Loading decision pattern...")
spec = importlib.util.spec_from_file_location("decision", r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\agent\decision.py")
decision_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(decision_module)
ToolSelector = decision_module.ToolSelector
PATTERN_TAG = decision_module.PATTERN_TAG
print(f"✓ Decision pattern OK ({PATTERN_TAG})")

# Manually create agent class
print("\n[AGENT] Creating agent class...")

class WildSoulAgent:
    """Minimal agent for testing."""
    def __init__(self):
        import time
        self.decider = Decider()
        self.model_id = default_model_id()
        self.sessions = {}
    
    def _session(self, session_id):
        if session_id not in self.sessions:
            tool_selector = ToolSelector(self.decider)
            agent = Agent(
                model=agent_model(self.model_id),
                system_prompt="You are a game AI. Respond helpfully.",
                tools=TOOLS,
                interventions=[tool_selector],
                callback_handler=None
            )
            self.sessions[session_id] = (agent, tool_selector)
        return self.sessions[session_id]
    
    def chat(self, message, session_id="default", images=None):
        agent, tool_selector = self._session(session_id)
        
        before_count = len(tool_selector.log)
        import time
        t0 = time.perf_counter()
        
        result = agent(message)
        reply = strip_thinking(str(result))
        
        new_decisions = tool_selector.log[before_count:]
        latency_ms = round((time.perf_counter() - t0) * 1000)
        
        return {
            "reply": reply,
            "decisions": new_decisions,
            "model_id": self.model_id,
            "latency_ms": latency_ms,
            "agent": "WILD SOUL Agent",
        }

print("✓ Agent class created")

print("\n[INSTANTIATE] Creating agent instance...")
try:
    agent = WildSoulAgent()
    print("✓ Agent instantiated")
except Exception as e:
    print(f"✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("RUNNING TEST INPUTS")
print("=" * 80)

tests = [
    ("I see a goblin ahead with low health. What should I do?", "combat"),
    ("My health is low. Check my status.", "status"),
    ("Hello!", "chat"),
]

for message, label in tests:
    print(f"\n▶ TEST: {label}")
    print(f"  Input: {message}")
    print("  " + "-" * 76)
    
    try:
        result = agent.chat(message, session_id="default")
        
        decisions = result["decisions"]
        reply = result["reply"]
        latency = result["latency_ms"]
        
        # Verify structure
        assert isinstance(reply, str), "Reply not string"
        assert isinstance(decisions, list), "Decisions not list"
        
        # Check decisions
        if len(decisions) == 0:
            print(f"  ⚠ No decisions (Decider endpoint unavailable)")
        elif len(decisions) == 1:
            d = decisions[0]
            print(f"  ✓ 1 decision")
            print(f"    - selected_tool: {d.get('selected_tool')}")
            print(f"    - confidence: {d.get('confidence')}")
            if d.get("fallback"):
                print(f"    - fallback: YES")
        else:
            print(f"  ✗ {len(decisions)} decisions (expected 1)")
        
        # Check reply
        if reply:
            if "blocked" in reply.lower() or "filter" in reply.lower():
                print(f"  ✗ Content filter error in reply")
            else:
                print(f"  ✓ Reply: {len(reply)} chars")
                print(f"    '{reply[:80]}...'")
        else:
            print(f"  ✗ Empty reply")
        
        print(f"  ✓ Latency: {latency}ms")
        
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 80)
print("VALIDATION COMPLETE")
print("=" * 80)
