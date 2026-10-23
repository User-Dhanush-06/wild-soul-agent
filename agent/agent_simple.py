"""Simplified WILD SOUL Agent for demonstration and testing."""

from __future__ import annotations

import sys
import time
import json
from typing import Any
from pathlib import Path

# Add reference kit to path for decider_kit imports
kit_path = Path(r"c:\Users\userd\Downloads\MY-AGENT\dhanush-raman-b-decider-hackathon-kit\dhanush-raman-b-decider-hackathon-kit")
if str(kit_path) not in sys.path:
    sys.path.insert(0, str(kit_path))

from .tools import TOOLS

NAME = "WILD SOUL Agent"


class WildSoulAgentSimple:
    """
    Simplified WILD SOUL Agent for demonstration.
    Real Bedrock and Decider integration comes later.
    """
    
    def __init__(self, model_id: str | None = None, eager: bool = False):
        """Initialize the agent."""
        self.model_id = model_id or "us.amazon.nova-pro-v1:0"
        self.eager = eager
        self.sessions: dict[str, list[dict]] = {}
        self.tools_by_name = {tool.__name__: tool for tool in TOOLS}
    
    def _get_session_history(self, session_id: str) -> list[dict]:
        """Get or create session history."""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]
    
    def chat(self, message: str, session_id: str = "default", images: list[Any] | None = None) -> dict[str, Any]:
        """
        Process a game state message.
        
        For now, this demonstrates the interface contract.
        Real implementation integrates Bedrock and Decider.
        """
        session_history = self._get_session_history(session_id)
        t0 = time.perf_counter()
        
        # Add user message to history
        session_history.append({"role": "user", "content": message})
        
        # Simulate a response (real version uses Bedrock + Decider)
        reply = f"I understand you said: {message[:50]}..."
        
        # Simulate a tool selection decision
        decisions = [
            {
                "pattern": "#tool-selection",
                "selected_tool": "check_status",
                "confidence": 0.75,
                "decider_ms": 150
            }
        ]
        
        # Add assistant response to history
        session_history.append({"role": "assistant", "content": reply})
        
        latency_ms = round((time.perf_counter() - t0) * 1000)
        
        return {
            "reply": reply,
            "decisions": decisions,
            "model_id": self.model_id,
            "latency_ms": latency_ms,
            "agent": NAME,
            "eager": self.eager
        }


if __name__ == "__main__":
    import sys
    
    agent = WildSoulAgentSimple()
    
    test_messages = [
        "I see a goblin ahead. What should I do?",
        "My health is getting low.",
        "Let's explore the forest to the north."
    ]
    
    for msg in (sys.argv[1:] or test_messages):
        result = agent.chat(msg)
        print(json.dumps(result, indent=2, default=str))
        print()
