# WILD SOUL Agent - Technical Description

## Use Case

WILD SOUL Agent plays a fantasy game by making intelligent decisions about which action to take. In strategy games, the AI must:

1. **Understand the game state** - health, location, inventory, nearby entities
2. **Decide which action type** - inventory management, NPC interaction, exploration, combat, status check
3. **Execute the action** - use the tool and get results
4. **Narrate the action** - describe what happened to the player

Most AI agents ask the LLM to do all three. WILD SOUL Agent separates concerns:
- **Strands Decider 2B** decides which action (classification - fast, calibrated, consistent)
- **Tool chain** executes the action (deterministic)
- **Amazon Bedrock** narrates what happened (generation)

## Decision Handed to Strands Decider 2B

**Question**: "Which game tool should handle this situation?"

**Options**: 5 distinct tools
- manage_inventory: Equip, use, drop, or examine items
- interact_npc: Talk, trade, accept quests from NPCs
- explore_area: Move between locations, search, discover
- combat_action: Attack, defend, use abilities in combat
- check_status: Check health, mana, buffs, debuffs, quest progress

**Decision output**: Tool classification with confidence probability

**Fallback behavior**: If confidence < 0.6, use check_status (safe action)

## Why Strands Decider 2B is Appropriate

### Problem with LLM-Only Tool Selection
- LLMs are good at generation, not classification
- Tool selection is a classification problem (pick 1 of N options)
- LLMs have high latency for simple decisions
- Confidence is not calibrated - hard to implement fallback
- Expensive to run LLM just to pick a tool

### Advantages of Strands Decider 2B
1. **Optimized for classification**: Returns discrete choice with calibrated probabilities
2. **Fast**: Low latency for real-time game decisions
3. **Calibrated confidence**: Can implement threshold-based fallback
4. **Cost-effective**: Cheaper than running LLM for every decision
5. **Reliable**: Consistent, predictable behavior

### Architecture Benefits
- **Separation of concerns**: Decision logic separate from narrative logic
- **Testable**: Easy to evaluate tool selection accuracy
- **Composable**: Decision pattern can be reused in other projects
- **Game-appropriate**: Makes sense for turn-based decision scenarios

## Features

### 5 Game Tools with Clear Interfaces
Each tool has:
- Clear one-line docstring for Decider to read
- Input validation and error handling
- Consistent response format
- In-memory game state for demonstration

### Real #tool-selection Pattern
- Defined in gent/decision.py
- Uses Decider.choice() with 5 options
- Confidence threshold with fallback
- Logged with pattern tag, confidence, probabilities, latency
- Reusable - can be copied to other projects

### Session Management
- Per-session conversation history
- Separate Strands Agent per session
- ToolSelector intervention per session

### HackathonAgent Interface
- Compatible with demo UI, benchmark, deployment
- Standard response format across agents

## Implementation

- **Framework**: Strands Agents SDK
- **LLM**: Amazon Bedrock (Amazon Nova Pro)
- **Decision Model**: Strands Decider 2B
- **Language**: Python 3.11+
- **Lines of Code**: ~500 (agent.py, decision.py, tools.py)

## For Game Developers

This pattern is useful for any game where:
- You have 3-10 distinct action types
- You want to classify game state into actions
- You need fast, real-time decisions
- You want to log decision confidence and probabilities

## For AI/ML Researchers

The #tool-selection pattern demonstrates:
- How to use a classifier model (not generator) for decisions
- How to integrate Strands Decider 2B into agent workflows
- How to implement confidence-based fallback
- How to separate decision logic from narrative logic
