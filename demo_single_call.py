"""Single demo call to WILD SOUL agent."""

import sys
from pathlib import Path
import os
import time

os.chdir(r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")
sys.path.insert(0, str(Path("_decider_kit_wrapper").resolve()))
sys.path.insert(0, r"C:\Users\userd\Downloads\MY-AGENT\dhanush-raman-b-decider-hackathon-kit\dhanush-raman-b-decider-hackathon-kit")

from _decider_kit_wrapper import Decider, agent_model, default_model_id, strip_thinking
from strands import Agent
import importlib.util

# Load modules
spec = importlib.util.spec_from_file_location("game_tools", r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\agent\tools.py")
game_tools_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game_tools_module)
TOOLS = game_tools_module.TOOLS

spec = importlib.util.spec_from_file_location("decision", r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\agent\decision.py")
decision_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(decision_module)
ToolSelector = decision_module.ToolSelector

class WildSoulAgent:
    def __init__(self):
        self.decider = Decider()
        self.model_id = default_model_id()
        self.sessions = {}
    
    def _session(self, sid):
        if sid not in self.sessions:
            ts = ToolSelector(self.decider)
            agent = Agent(model=agent_model(self.model_id), system_prompt="You are a game AI.", tools=TOOLS, interventions=[ts])
            self.sessions[sid] = (agent, ts)
        return self.sessions[sid]
    
    def chat(self, msg, sid="default"):
        agent, ts = self._session(sid)
        before = len(ts.log)
        t0 = time.perf_counter()
        result = agent(msg)
        reply = strip_thinking(str(result))
        new_decisions = ts.log[before:]
        latency_ms = round((time.perf_counter() - t0) * 1000)
        return {"reply": reply, "decisions": new_decisions, "latency_ms": latency_ms}

print("WILD SOUL AGENT - DEMO")
print("-" * 80)
print("Input: I see a goblin ahead with low health. What should I do?")
print()

agent = WildSoulAgent()
result = agent.chat("I see a goblin ahead with low health. What should I do?")

d = result["decisions"][0] if result["decisions"] else {}
print("DECISION:")
print("  Tool: %s" % d.get("selected_tool"))
print("  Confidence: %.3f" % d.get("confidence", 0))
print()
print("RESPONSE:")
print("  %s" % result["reply"][:150])
print()
print("Latency: %dms" % result["latency_ms"])
print()
print("SUCCESS - Demo ran successfully!")
