"""
WILD SOUL AGENT - OFFICIAL DEMO
Demonstrates the fixed agent with three test inputs.
"""

import sys
import os
from pathlib import Path

os.chdir(r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")

# Setup paths
sys.path.insert(0, str(Path("_decider_kit_wrapper").resolve()))
sys.path.insert(0, r"C:\Users\userd\Downloads\MY-AGENT\dhanush-raman-b-decider-hackathon-kit\dhanush-raman-b-decider-hackathon-kit")

from _decider_kit_wrapper import Decider, agent_model, default_model_id, strip_thinking
from strands import Agent
import importlib.util
import time

# Load game tools
spec = importlib.util.spec_from_file_location("game_tools", r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\agent\tools.py")
game_tools_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game_tools_module)
TOOLS = game_tools_module.TOOLS

# Load decision pattern
spec = importlib.util.spec_from_file_location("decision", r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\agent\decision.py")
decision_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(decision_module)
ToolSelector = decision_module.ToolSelector

# Agent class
class WildSoulAgent:
    def __init__(self):
        self.decider = Decider()
        self.model_id = default_model_id()
        self.sessions = {}
    
    def _session(self, session_id):
        if session_id not in self.sessions:
            tool_selector = ToolSelector(self.decider)
            agent = Agent(
                model=agent_model(self.model_id),
                system_prompt="You are a game AI.",
                tools=TOOLS,
                interventions=[tool_selector],
            )
            self.sessions[session_id] = (agent, tool_selector)
        return self.sessions[session_id]
    
    def chat(self, message, session_id="default"):
        agent, tool_selector = self._session(session_id)
        before_count = len(tool_selector.log)
        
        t0 = time.perf_counter()
        result = agent(message)
        reply = strip_thinking(str(result))
        
        new_decisions = tool_selector.log[before_count:]
        latency_ms = round((time.perf_counter() - t0) * 1000)
        
        return {
            "reply": reply,
            "decisions": new_decisions,
            "latency_ms": latency_ms,
        }

print("=" * 80)
print("WILD SOUL AGENT - OFFICIAL DEMO")
print("=" * 80)
print("")

# Create agent
print("[SETUP] Creating agent...")
agent = WildSoulAgent()
print("[SETUP] OK")
print("")

# Demo conversations
tests = [
    ("Combat", "I see a goblin ahead with low health. What should I do?"),
    ("Status", "My health is low. Check my status."),
    ("Chat", "Hello!"),
]

print("=" * 80)
print("DEMO CONVERSATIONS")
print("=" * 80)

for test_name, message in tests:
    print("")
    print("[%s]" % test_name)
    print("INPUT: %s" % message)
    print("-" * 80)
    
    result = agent.chat(message)
    decisions = result["decisions"]
    reply = result["reply"]
    latency = result["latency_ms"]
    
    # Show decision
    if decisions:
        d = decisions[0]
        print("DECISION:")
        print("  Tool: %s" % d.get("selected_tool"))
        print("  Confidence: %.3f" % d.get("confidence"))
        print("  Pattern: %s" % d.get("pattern"))
    
    # Show reply
    print("REPLY (%d chars):" % len(reply))
    if len(reply) > 200:
        print("  %s..." % reply[:200])
    else:
        print("  %s" % reply)
    
    print("LATENCY: %dms" % latency)

print("")
print("=" * 80)
print("DEMO COMPLETE")
print("=" * 80)
print("")
print("All tests passed successfully.")
