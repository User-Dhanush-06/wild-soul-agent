"""REUSABLE DECISION PATTERN: tool selection for game actions (#tool-selection)

Built with the AWS User Group Madurai Strands Decider hackathon kit.

This pattern demonstrates how to use Strands Decider 2B to meaningfully influence
tool selection in a game agent. Key behaviors:

1. ONE decision per user turn (asked in before_invocation)
2. Decision is ENFORCED via Guide intervention in before_tool_call
3. Low-confidence decisions FALLBACK to check_status
4. Decision record MATCHES the actual tool that runs
5. If Decider selects "none", the agent responds without tools

The decision meaningfully influences the agent's behavior.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from _decider_kit_wrapper import Decider

try:
    from strands.interventions import InterventionHandler, Proceed, Guide
except ImportError:
    # Fallback for testing without Strands
    class InterventionHandler:
        pass

    class Proceed:
        pass

    class Guide:
        def __init__(self, feedback, reason):
            self.feedback = feedback
            self.reason = reason

from _decider_kit_wrapper import Decider

PATTERN_TAG = "#tool-selection"

QUESTIONS = {
    "tool_choice": Decider.choice(
        "Which game tool should handle this situation?",
        {
            "manage_inventory": (
                "Manage player inventory: equip, use, drop, or examine items"
            ),
            "interact_npc": (
                "Interact with NPCs: talk, trade, accept quests, or gather information"
            ),
            "explore_area": (
                "Navigate the game world: move between locations, search, or discover secrets"
            ),
            "combat_action": (
                "Engage in combat: attack enemies, defend, or use special abilities"
            ),
            "check_status": (
                "Check player status: health, mana, buffs, debuffs, or quests"
            ),
            "none": (
                "No tool needed; respond with conversational guidance"
            ),
        },
    )
}


class ToolSelector(InterventionHandler):
    """
    Intervention handler that uses Strands Decider 2B to select the appropriate
    game tool based on the current game state context.

    Decision lifecycle:
    1. before_invocation: Ask Decider once per user message, store decision
    2. before_tool_call: If tool proposal matches decision, Proceed()
                        If tool proposal differs, Guide to the Decider choice
                        If Decider chose "none", Guide against tool use
    """

    name = "game-tool-selector"

    def __init__(
        self,
        decider: Decider,
        confidence_threshold: float = 0.6,
    ):
        self.decider = decider
        self.confidence_threshold = confidence_threshold
        self.log: list[dict[str, Any]] = []
        self._last_decision: dict[str, Any] | None = None

    def before_invocation(self, event, **kwargs):
        """
        Ask the Decider once at the start of each user message.
        Store the decision to be enforced in before_tool_call.
        """
        self._last_decision = None

        # Extract the latest user message from the conversation
        messages = event.messages or []
        latest_message = ""

        if messages:
            message = messages[-1]
            content = message.get("content", "")
            if isinstance(content, list):
                # Multi-part content (e.g., text + images)
                latest_message = " ".join(
                    str(part.get("text", ""))
                    for part in content
                    if isinstance(part, dict) and part.get("text")
                )
            else:
                latest_message = str(content)

        # Build state for the Decider
        state = (
            "Choose the best tool for the player's latest request.\n"
            "Use only facts stated in the request. Do not invent game events.\n"
            f"Player request: {latest_message}"
        )

        # Ask the Decider
        started = time.perf_counter()
        result = self.decider.ask(state, QUESTIONS)
        elapsed_ms = round((time.perf_counter() - started) * 1000)

        # Extract the choice
        choice = result["tool_choice"]
        selected = choice.label or "none"
        confidence = float(choice.confidence)

        # Build the decision record
        record = {
            "pattern": PATTERN_TAG,
            "selected_tool": selected,
            "confidence": round(confidence, 3),
            "options": {
                key: round(float(value), 3)
                for key, value in choice.probabilities.items()
            },
            "decider_ms": elapsed_ms,
        }

        # Handle low confidence: fallback to check_status
        if confidence < self.confidence_threshold and selected != "none":
            record["fallback"] = True
            record["fallback_reason"] = f"confidence {round(confidence, 3)} < threshold {self.confidence_threshold}"
            selected = "check_status"
            record["selected_tool"] = selected

        # Log and store
        self.log.append(record)
        self._last_decision = record

        return Proceed()

    def before_tool_call(self, event, **kwargs):
        """
        Enforce the Decider's decision.

        If tool proposal matches the decision, allow it.
        If it differs, guide the agent back to the Decider choice.
        If Decider chose "none", guide against tool use.
        """
        decision = self._last_decision
        if not decision:
            # No decision made yet; let the agent decide
            return Proceed()

        proposed = event.selected_tool
        if proposed is None:
            # No tool proposed; fine
            return Proceed()

        # Extract the proposed tool name
        proposed_name = (
            getattr(proposed, "tool_name", None)
            or getattr(proposed, "name", None)
            or str(proposed)
        )

        selected = decision["selected_tool"]

        # If Decider said "none", guide against tool use
        if selected == "none":
            return Guide(
                feedback=(
                    "The Decider determined no tool is needed for this request. "
                    "Respond conversationally based on the player's message, "
                    "using only the facts they stated."
                ),
                reason="Decider selected no tool",
            )

        # If proposed tool matches the decision, allow it
        if proposed_name == selected:
            return Proceed()

        # Tool mismatch: guide back to the Decider choice
        return Guide(
            feedback=(
                f"The Decider analysis selected the '{selected}' tool as most appropriate. "
                f"Use that tool with valid arguments. Do not invent game state."
            ),
            reason=f"Align tool choice: Decider selected '{selected}', agent proposed '{proposed_name}'",
        )
