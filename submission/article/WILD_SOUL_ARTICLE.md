# WILD SOUL Agent: Autonomous Game AI with Strands Decider 2B

## The Problem: Tool Selection at Game Speed

Building an autonomous game agent seems straightforward: tell an LLM the current game state, ask which action to take, execute the tool, and narrate the result. In practice, this approach has a critical limitation—it treats tool selection as a **generation problem** when it is really a **classification problem**.

Large language models are powerful generators, but asking an LLM to pick 1 of 5 options is inefficient. The costs are real:

- **Latency**: 1–5 seconds per decision (too slow for responsive gameplay)
- **Unpredictable confidence**: No calibrated probabilities for fallback logic
- **Expense**: Paying for full token generation when you only need a choice
- **Over-specification**: Using a 70B model to do a 5-way classification

WILD SOUL Agent demonstrates a better approach: separate decision-making from storytelling.

## The Solution: Three-Phase Architecture

WILD SOUL uses a cleaner pipeline:

```
Game State → [Decider: Classify] → [Tool: Execute] → [Bedrock: Narrate] → Player
```

Each phase does one job:

1. **Strands Decider 2B** classifies the game state and selects which of 5 tools to use
2. **Deterministic tools** execute the choice and return structured results
3. **Amazon Bedrock** transforms the result into natural language for the player

This separation provides:

- **Fast decision-making**: Decider is optimized for classification, not generation
- **Safe fallback**: Calibrated confidence enables threshold-based decisions ("If confidence < 60%, use check_status")
- **Cost efficiency**: Decider costs less per decision than full LLM inference for classification
- **Reliability**: Deterministic tool execution; no hallucinated tool selection
- **Testability**: Tool selection accuracy can be measured against ground truth

## The #tool-selection Pattern

The `agent/decision.py` file defines a reusable pattern for tool selection. Here's the wiring:

```python
from _decider_kit_wrapper import Decider
from strands.interventions import Guide, Proceed

# Define the typed decision: 5 tools, each with a one-line docstring
QUESTIONS = {
    "tool_choice": Decider.choice(
        "Which game tool should handle this situation?",
        {
            "manage_inventory": "Equip, use, drop, or examine items",
            "interact_npc": "Talk, trade, accept quests from NPCs",
            "explore_area": "Move between locations, search, discover",
            "combat_action": "Attack, defend, use abilities in combat",
            "check_status": "Check health, mana, buffs, debuffs, quest progress",
        },
    )
}

# Wiring: Ask Decider once per turn, enforce the choice, fallback if low confidence
@before_invocation
def decide_tool_choice(agent: Agent) -> Guide | Proceed:
    game_state = agent.context.get("game_state", "")
    decision = Decider.ask(game_state, QUESTIONS)
    
    # Log the decision
    log_decision(choice=decision.verdict, confidence=decision.confidence)
    
    # Fallback: if confidence < 60%, force safe action
    if decision.confidence < 0.6:
        return Guide(
            feedback=f"Confidence too low. Use check_status.",
            reason="Confidence fallback"
        )
    
    return Proceed()
```

The key behaviors:

- **One decision per turn**: Asked in `before_invocation` (fires once per LLM invocation, not per tool call)
- **Enforced via intervention**: `Guide` overrides the tool choice if needed
- **Logged**: Every decision is recorded with choice, confidence, and latency
- **Truthful**: The logged decision matches the actual tool that executes

## Why This Matters for Game AI

Real-time games demand responsive AI. Tool selection is a core decision point. Strands Decider 2B is purpose-built for this:

- **Sub-100ms inference**: Designed for fast classification, not text generation
- **Confidence-based fallback**: Only take risky actions when the model is sure
- **Reproducible**: Same input produces the same decision (no probabilistic variation like LLMs)
- **Calibrated probabilities**: Enables meaningful fallback thresholds

For game developers building multiplayer systems, real-time strategy games, or narrative adventures, this pattern offers a way to make reliable, fast tool selection decisions.

## The #tool-selection Pattern: Reusable

The pattern is designed to be copied into your own projects. It works for any domain where you have 3–10 discrete options and need fast, reliable classification:

- **Game AI**: Tool selection, ability routing, NPC behavior classification
- **Task scheduling**: Route requests to the right handler
- **Customer service**: Classify inquiries for proper team routing
- **Autonomous vehicles**: Behavior selection (accelerate, brake, turn, yield)
- **Supply chain**: Warehouse or shipper selection
- **Fraud detection**: Transaction classification (approve, review, block)

To reuse it:

1. Define your 3–10 options with clear one-line docstrings
2. Create your typed questions using `Decider.choice()`
3. Wire the decision into your agent's `before_invocation` hook
4. Set your own confidence threshold based on your risk tolerance
5. Log decisions for monitoring and analysis

## The Implementation

WILD SOUL demonstrates the pattern with:

- **5 game tools**: `manage_inventory`, `interact_npc`, `explore_area`, `combat_action`, `check_status`
- **Per-session agent instances**: Each game session gets its own Strands Agent with tool integration
- **Decision logging**: Full telemetry of tool selection decisions recorded
- **Confidence-based fallback**: Decisions below 60% confidence fall back to safe action

The agent code spans ~500 lines of Python using:

- **Strands Agents SDK**: Open-source agent framework
- **Strands Decider 2B**: Decision classification model (2B parameters, Apache-2.0)
- **Amazon Bedrock**: Generative AI for narrative layer
- **Python 3.11+**: Clean, maintainable code
- **Apache-2.0 license**: Open source

## Next Steps

WILD SOUL Agent is published as open source. The pattern is reusable in any Python project that needs fast, reliable tool or action selection.

The #tool-selection pattern separates classification from generation, enabling game developers and autonomous systems builders to make decisions where it matters (via a specialized classifier) and narrate results where it matters (via a generative LLM).

Built with the AWS User Group Madurai Strands Decider hackathon kit.

---

**Tags**: `#strands-decider-2b` `#tool-selection` `#aws` `#gameai` `#agents`
