"""
WILD SOUL AGENT - Interactive CLI App
Allows real-time conversation with the game agent.
"""

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
            agent = Agent(
                model=agent_model(self.model_id),
                system_prompt="You are a companion in the WILD SOUL fantasy game. Help the player with their adventure.",
                tools=TOOLS,
                interventions=[ts],
            )
            self.sessions[sid] = (agent, ts)
        return self.sessions[sid]
    
    def chat(self, msg, sid="default"):
        agent, ts = self._session(sid)
        before = len(ts.log)
        t0 = time.perf_counter()
        try:
            result = agent(msg)
            reply = strip_thinking(str(result))
        except Exception as e:
            reply = "Error: %s" % str(e)
        
        new_decisions = ts.log[before:]
        latency_ms = round((time.perf_counter() - t0) * 1000)
        return {
            "reply": reply,
            "decisions": new_decisions,
            "latency_ms": latency_ms
        }

def main():
    print("=" * 80)
    print("WILD SOUL AGENT - Interactive CLI")
    print("=" * 80)
    print("")
    print("Welcome to WILD SOUL!")
    print("Type 'quit' or 'exit' to end the game.")
    print("Type 'help' for example commands.")
    print("")
    
    agent = WildSoulAgent()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit"]:
                print("Goodbye!")
                break
            
            if user_input.lower() == "help":
                print("")
                print("Example commands:")
                print("  - I see a goblin ahead with low health. What should I do?")
                print("  - My health is low. Check my status.")
                print("  - Let me explore the area.")
                print("  - Talk to the merchant.")
                print("  - Use my health potion.")
                print("")
                continue
            
            print("")
            print("Agent: Processing...")
            result = agent.chat(user_input)
            
            decisions = result["decisions"]
            reply = result["reply"]
            latency = result["latency_ms"]
            
            if decisions:
                d = decisions[0]
                tool = d.get("selected_tool", "none")
                conf = d.get("confidence", 0.0)
                print("[Decision: tool=%s, confidence=%.3f]" % (tool, conf))
            
            print("")
            print("Agent: %s" % reply)
            print("")
            print("[Latency: %dms]" % latency)
            print("")
            
        except KeyboardInterrupt:
            print("")
            print("Game interrupted.")
            break
        except Exception as e:
            print("Error: %s" % str(e))
            print("")

if __name__ == "__main__":
    main()
