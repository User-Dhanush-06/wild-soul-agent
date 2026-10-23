"""The WILD SOUL Agent: plays the game using Strands Decider 2B for tool selection.

Built with the AWS User Group Madurai Strands Decider hackathon kit.

The agent follows the HackathonAgent interface contract for compatibility with demo UI,
benchmark, and AWS deployment pipeline.
"""

from __future__ import annotations

import time
from typing import Any

from strands import Agent

from _decider_kit_wrapper import Decider, agent_model, default_model_id, strip_thinking

from .decision import ToolSelector
from .tools import TOOLS

NAME = "WILD SOUL Agent"
SYSTEM_PROMPT = """You are an intelligent companion navigating the world of WILD SOUL, a fantasy game.
You can manage your inventory, interact with NPCs, explore the world, engage in combat, and check your status.
Be strategic, descriptive, and engaged with the game world. Respond to player commands and narrate your actions."""


class WildSoulAgent:
    """
    Autonomous game agent that plays WILD SOUL using Strands Decider 2B
    for intelligent tool selection.
    
    Implements the HackathonAgent interface contract for compatibility with
    demo UI, benchmark, and AWS deployment pipeline.
    """
    
    def __init__(self, decider: Decider | None = None, model_id: str | None = None, eager: bool | None = None):
        """
        Initialize agent with optional decider and model configuration.
        
        Args:
            decider: Strands Decider instance (created if None)
            model_id: Bedrock model ID (default: from env or BEDROCK_MODEL_ID)
            eager: Demo mode that acts without asking questions (default: False from env)
        """
        import os
        
        self.decider = decider or Decider()
        self.eager = eager if eager is not None else os.environ.get("DEMO_EAGER") == "1"
        self.model_id = model_id or default_model_id()
        self.sessions: dict[str, tuple[Agent, ToolSelector]] = {}
    
    def _session(self, session_id: str) -> tuple[Agent, ToolSelector]:
        """Get or create agent instance for a session."""
        if session_id not in self.sessions:
            tool_selector = ToolSelector(self.decider)
            agent = Agent(
                model=agent_model(self.model_id),
                system_prompt=SYSTEM_PROMPT,
                tools=TOOLS,
                interventions=[tool_selector],
                callback_handler=None
            )
            self.sessions[session_id] = (agent, tool_selector)
        return self.sessions[session_id]
    
    def chat(self, message: str, session_id: str = "default", images: list[Any] | None = None) -> dict[str, Any]:
        """
        Process a game state message and return action response.
        
        Args:
            message: Game state description or player input
            session_id: Unique identifier for the game session
            images: Optional game screenshots (for multimodal analysis)
            
        Returns:
            Dictionary containing:
                - reply: Agent's response to the game state
                - decisions: List of tool selection decision records
                - model_id: Bedrock model identifier
                - latency_ms: Response latency in milliseconds
                - agent: Agent name identifier
                - eager: Whether running in eager mode
        """
        agent, tool_selector = self._session(session_id)
        
        # Record decisions made before this chat
        before_decision_count = len(tool_selector.log)
        
        # Measure latency
        t0 = time.perf_counter()
        
        # Invoke the agent
        result = agent(message)
        
        # Extract reply and strip thinking tags
        reply = strip_thinking(str(result))
        
        # Get decisions made during this chat
        new_decisions = tool_selector.log[before_decision_count:]
        
        # Calculate latency
        latency_ms = round((time.perf_counter() - t0) * 1000)
        
        return {
            "reply": reply,
            "decisions": new_decisions,
            "model_id": self.model_id,
            "latency_ms": latency_ms,
            "agent": NAME,
            "eager": self.eager
        }


if __name__ == "__main__":
    import json
    import sys
    
    a = WildSoulAgent()
    for msg in sys.argv[1:] or ["I see a goblin ahead. What should I do?", "My health is low. Check my status."]:
        print(json.dumps(a.chat(msg), indent=1, default=str))
