# Design Document

## Introduction

This document describes the architecture and design of the WILD SOUL Agent, an autonomous game agent that plays the WILD SOUL game using Strands Decider 2B for intelligent tool selection. The agent follows the hackathon kit's `HackathonAgent` interface contract while implementing a specialized game-playing decision system using the #tool-selection pattern.

## Overview

The WILD SOUL Agent is an autonomous AI agent that analyzes game state and selects the most appropriate action from five available game tools. It uses Amazon Bedrock (Amazon Nova Pro by default) for conversation and reasoning, with Strands Decider 2B making real-time decisions about which game action to take.

**Core Capabilities:**
- Session-based game state management
- Intelligent tool selection using #tool-selection pattern
- Configurable LLM and decider endpoints
- Compatible with demo UI, benchmark, and AWS deployment pipeline

**Decision Pattern:** #tool-selection

The agent hands the following decision to Strands Decider 2B:
- **Question Type:** `choice` - Select one tool from five options plus "none"
- **State:** Conversation history + game context
- **Options:** Five game tools, each described by their one-line docstring

**Why a Decision Model is Appropriate:**
- Five distinct action types require classification, not generation
- Real-time game play needs fast, consistent decisions
- Calibrated confidence enables intelligent fallback behavior
- Lower cost and latency than LLM-only tool selection

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              WILD SOUL Agent                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────────────────────────────────────┐│
│  │   chat(msg)     │    │              Session Manager                     ││
│  │                 │───▶│  ┌─────────────┐  ┌──────────────────────────┐  ││
│  │  - message      │    │  │ session_id  │  │ conversation_history     │  ││
│  │  - session_id   │    │  │ agent inst. │  │ (per-session state)      │  ││
│  │  - images       │    │  └─────────────┘  └──────────────────────────┘  ││
│  └────────┬────────┘    └─────────────────────────────────────────────────┘│
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                         Strands Agent                                   ││
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐ ││
│  │  │ Amazon Bedrock  │  │ Tool Selection  │  │    Game Tools           │ ││
│  │  │ (Nova Pro)      │  │ Decision Pattern│  │ ┌─────┐ ┌─────┐        │ ││
│  │  │                 │  │                 │  │ │Mgmt.│ │Inter│        │ ││
│  │  │ - Conversation  │  │ #tool-selection │  │ │Inv. │ │NPC  │        │ ││
│  │  │ - Reasoning     │  │ Decider.choice  │  │ └─────┘ └─────┘        │ ││
│  │  │                 │  │                 │  │ ┌─────┐ ┌─────┐        │ ││
│  │  │                 │  │ Strands Decider │  │ │Explr│ │Combat│        │ ││
│  │  │                 │  │ 2B              │  │ │Area │ │Act. │        │ ││
│  │  │                 │  │                 │  │ └─────┘ └─────┘        │ ││
│  │  │                 │  │                 │  │ ┌─────┐                │ ││
│  │  │                 │  │                 │  │ │Check│                │ ││
│  │  │                 │  │                 │  │ │Stat.│                │ ││
│  │  │                 │  │                 │  │ └─────┘                │ ││
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                      Response Builder                                   ││
│  │  {                                                                       ││
│  │    "reply": string,                                                      ││
│  │    "decisions": [ToolSelectionLog],                                     ││
│  │    "model_id": string,                                                   ││
│  │    "latency_ms": number,                                                 ││
│  │    "agent": "WILD SOUL Agent"                                           ││
│  │  }                                                                       ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

### Architecture Layers

| Layer | Component | Responsibility |
|-------|-----------|----------------|
| Interface | `WildSoulAgent.chat()` | API endpoint, session management, response formatting |
| Reasoning | Strands Agent + Bedrock | Conversation, reasoning, tool orchestration |
| Decision | Tool Selection Pattern | Classify game state, select appropriate tool |
| Action | Game Tools | Execute game actions (inventory, NPC, explore, combat, status) |
| Infrastructure | Configuration | Environment-based settings, AgentCore integration |

### Data Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           Tool Selection Flow                                 │
└──────────────────────────────────────────────────────────────────────────────┘

  1. User Input
     ┌─────────────────┐
     │ Game State Msg  │  "I see a goblin ahead and my health is low"
     └────────┬────────┘
              │
              ▼
  2. Session Lookup
     ┌─────────────────┐
     │ Get/Create      │
     │ Agent Instance  │
     │ for session_id  │
     └────────┬────────┘
              │
              ▼
  3. State Construction
     ┌─────────────────────────────────────────────────────────────────────────┐
     │ State = {                                                               │
     │   "conversation": [...history...],                                      │
     │   "current_message": "I see a goblin...",                               │
     │   "game_context": {player_status, location, nearby_entities}            │
     │ }                                                                       │
     └────────┬────────────────────────────────────────────────────────────────┘
              │
              ▼
  4. Decider Classification
     ┌─────────────────────────────────────────────────────────────────────────┐
     │ Decider.choice(state, QUESTIONS["tool"])                               │
     │                                                                         │
     │ Options:                                                                │
     │   - manage_inventory: 0.05                                              │
     │   - interact_npc: 0.02                                                  │
     │   - explore_area: 0.03                                                  │
     │   - combat_action: 0.75  ◀── SELECTED (confidence > 0.6)               │
     │   - check_status: 0.12                                                  │
     │   - none: 0.03                                                          │
     └────────┬────────────────────────────────────────────────────────────────┘
              │
              ▼
  5. Confidence Check
     ┌─────────────────┐     ┌─────────────────┐
     │ confidence >=   │ YES │ Proceed with    │
     │ threshold?      │────▶│ selected tool   │
     └────────┬────────┘     └─────────────────┘
              │ NO
              ▼
     ┌─────────────────┐
     │ Fallback to     │
     │ safe action     │
     │ (check_status)  │
     └────────┬────────┘
              │
              ▼
  6. Tool Execution
     ┌─────────────────────────────────────────────────────────────────────────┐
     │ combat_action(action="attack", target="goblin")                         │
     │                                                                         │
     │ Returns: {"damage_dealt": 15, "combat_log": [...]}                     │
     └────────┬────────────────────────────────────────────────────────────────┘
              │
              ▼
  7. Response Building
     ┌─────────────────────────────────────────────────────────────────────────┐
     │ {                                                                       │
     │   "reply": "I attacked the goblin for 15 damage...",                   │
     │   "decisions": [{                                                       │
     │     "tool": "combat_action",                                            │
     │     "confidence": 0.75,                                                 │
     │     "probabilities": {...},                                             │
     │     "decider_ms": 180                                                   │
     │   }],                                                                   │
     │   "model_id": "us.amazon.nova-pro-v1:0",                               │
     │   "latency_ms": 1250                                                    │
     │ }                                                                       │
     └─────────────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### WildSoulAgent Class

The main entry point implementing the `HackathonAgent` interface contract.

```python
class WildSoulAgent:
    """
    Autonomous game agent that plays WILD SOUL using Strands Decider 2B
    for intelligent tool selection.
    
    Implements the HackathonAgent interface for compatibility with the
    demo UI, benchmark, and AWS deployment pipeline.
    """
    
    def __init__(
        self,
        decider: Decider | None = None,
        model_id: str | None = None,
        eager: bool | None = None
    ):
        """
        Initialize agent with optional decider and model configuration.
        
        Args:
            decider: Strands Decider instance (created from DECIDER_MODE if None)
            model_id: Bedrock model ID (default: from BEDROCK_MODEL_ID env var)
            eager: Demo mode that acts without asking questions (default: False)
        """
        
    def chat(
        self,
        message: str,
        session_id: str = "default",
        images: list[Any] | None = None
    ) -> dict[str, Any]:
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
        
    def _session(self, session_id: str) -> tuple[Agent, GameToolSelector]:
        """Get or create agent instance for a session."""
```

### Game Tools Module

Five specialized tools for game actions, each with a clear one-line docstring for decider classification.

#### ManageInventory Tool

```python
@tool
def manage_inventory(action: str, item_name: str, target_slot: str | None = None) -> dict:
    """
    Manage player inventory items: equip, use, drop, or examine items in the player's bag.
    
    Args:
        action: One of 'equip', 'use', 'drop', 'examine'
        item_name: Name of the item to act upon
        target_slot: Target equipment slot for 'equip' action (optional)
        
    Returns:
        {"success": bool, "message": str, "inventory": list}
    """
```

#### InteractNPC Tool

```python
@tool
def interact_npc(npc_name: str, interaction_type: str, dialogue_option: str | None = None) -> dict:
    """
    Interact with non-player characters: talk, trade, accept quests, or get information.
    
    Args:
        npc_name: Name or identifier of the NPC
        interaction_type: One of 'talk', 'trade', 'quest', 'ask'
        dialogue_option: Specific dialogue choice (optional)
        
    Returns:
        {"success": bool, "response": str, "quest_id": str | None}
    """
```

#### ExploreArea Tool

```python
@tool
def explore_area(direction: str | None = None, action: str = "move") -> dict:
    """
    Navigate the game world: move between locations, search areas, or discover secrets.
    
    Args:
        direction: Cardinal direction or location name for movement
        action: One of 'move', 'search', 'discover', 'examine'
        
    Returns:
        {"success": bool, "location": str, "description": str, "encounters": list}
    """
```

#### CombatAction Tool

```python
@tool
def combat_action(action: str, target: str | None = None, ability_name: str | None = None) -> dict:
    """
    Engage in combat encounters: attack enemies, defend against attacks, or use special abilities.
    
    Args:
        action: One of 'attack', 'defend', 'ability', 'flee'
        target: Enemy name or identifier for targeted actions
        ability_name: Specific ability to use (for 'ability' action)
        
    Returns:
        {"success": bool, "damage_dealt": int, "damage_taken": int, "combat_log": list}
    """
```

#### CheckStatus Tool

```python
@tool
def check_status(status_type: str = "all") -> dict:
    """
    Check player status: health, mana, active buffs/debuffs, or quest progress.
    
    Args:
        status_type: One of 'all', 'health', 'mana', 'buffs', 'debuffs', 'quests'
        
    Returns:
        {
            "health": {"current": int, "max": int},
            "mana": {"current": int, "max": int},
            "buffs": list,
            "debuffs": list,
            "active_quests": list
        }
    """
```

### Tool Selection Decision Pattern

The reusable decision pattern in `decision.py` implementing #tool-selection.

```python
# decision.py

PATTERN_TAG = "#tool-selection"

QUESTIONS = {
    "tool": Decider.choice(
        "Which game action tool should handle the current game state?",
        {
            "manage_inventory": "Manage player inventory items: equip, use, drop, or examine items",
            "interact_npc": "Interact with non-player characters: talk, trade, or handle quests",
            "explore_area": "Navigate the game world: move between locations, search, or discover",
            "combat_action": "Engage in combat: attack enemies, defend, or use abilities",
            "check_status": "Check player status: health, mana, buffs, debuffs, or quest progress",
            "none": "No tool needed; respond directly to the player's message"
        }
    )
}

class GameToolSelector(InterventionHandler):
    """
    Intervention handler that uses Strands Decider 2B to select the appropriate
    game tool based on the current game state context.
    
    Wiring:
        Agent(..., interventions=[GameToolSelector(decider)])
    
    Attributes:
        name: Handler identifier for logging
        log: List of decision records for debugging/analysis
    """
    
    name = "game-tool-selector"
    
    def __init__(
        self,
        decider: Decider,
        threshold: float = 0.6,
        fallback_tool: str = "check_status"
    ):
        """
        Initialize the tool selector.
        
        Args:
            decider: Strands Decider instance for classification
            threshold: Confidence threshold for tool selection (default 0.6)
            fallback_tool: Safe default tool when confidence is low
        """
        
    def before_invocation(self, event, **kwargs) -> Proceed:
        """Reset guided calls for new user message."""
        
    def before_tool_call(self, event, **kwargs) -> Proceed | Guide | Confirm:
        """Evaluate proposed tool calls and guide/confirm/proceed based on context."""
```

### Configuration Module

```python
class WildSoulSettings:
    """
    Environment-based configuration for WILD SOUL Agent.
    
    Reads from environment variables following the .env.example pattern.
    """
    
    # LLM Configuration
    llm_provider: Literal["bedrock", "local", "ugmdu"]
    model_id: str
    
    # Decider Configuration
    decider_mode: Literal["local", "ugmdu", "custom"]
    decider_url: str
    
    # AWS Configuration
    aws_region: str
```

## Data Models

### Request Model

```python
@dataclass
class ChatRequest:
    """Input to the WildSoulAgent.chat() method."""
    
    message: str                          # Game state description or player input
    session_id: str = "default"           # Session identifier for state management
    images: list[bytes | str] | None = None  # Optional game screenshots
```

### Response Model

```python
@dataclass
class ChatResponse:
    """Output from the WildSoulAgent.chat() method."""
    
    reply: str                            # Agent's conversational response
    decisions: list[DecisionRecord]       # Tool selection decision log
    model_id: str                         # Bedrock model identifier
    latency_ms: int                       # Total response latency in milliseconds
    agent: str                            # Agent name: "WILD SOUL Agent"
    eager: bool                           # Whether running in eager (demo) mode
```

### Decision Record Model

```python
@dataclass
class DecisionRecord:
    """A single tool selection decision record."""
    
    pattern: str                          # Pattern tag (e.g., "#tool-selection")
    tool: str                             # Selected tool name
    confidence: float                     # Confidence score (0.0 to 1.0)
    probabilities: dict[str, float]       # Full probability distribution
    decider_ms: int                       # Decider latency in milliseconds
    narrowed: bool                        # Whether tools were narrowed
```

### Game Tool Schemas

#### ManageInventory Schema
```python
@dataclass
class ManageInventoryInput:
    action: Literal["equip", "use", "drop", "examine"]
    item_name: str
    target_slot: str | None = None

@dataclass
class ManageInventoryOutput:
    success: bool
    message: str
    inventory: list[dict]
```

#### InteractNPC Schema
```python
@dataclass
class InteractNPCInput:
    npc_name: str
    interaction_type: Literal["talk", "trade", "quest", "ask"]
    dialogue_option: str | None = None

@dataclass
class InteractNPCOutput:
    success: bool
    response: str
    quest_id: str | None = None
```

#### ExploreArea Schema
```python
@dataclass
class ExploreAreaInput:
    direction: str | None = None
    action: Literal["move", "search", "discover", "examine"] = "move"

@dataclass
class ExploreAreaOutput:
    success: bool
    location: str
    description: str
    encounters: list[dict]
```

#### CombatAction Schema
```python
@dataclass
class CombatActionInput:
    action: Literal["attack", "defend", "ability", "flee"]
    target: str | None = None
    ability_name: str | None = None

@dataclass
class CombatActionOutput:
    success: bool
    damage_dealt: int
    damage_taken: int
    combat_log: list[dict]
```

#### CheckStatus Schema
```python
@dataclass
class CheckStatusInput:
    status_type: Literal["all", "health", "mana", "buffs", "debuffs", "quests"] = "all"

@dataclass
class CheckStatusOutput:
    health: dict[str, int]
    mana: dict[str, int]
    buffs: list[dict]
    debuffs: list[dict]
    active_quests: list[dict]
```

### Session State Model

```python
@dataclass
class SessionState:
    """Internal session state for a game session."""
    
    session_id: str
    agent: Agent                          # Strands Agent instance
    tool_selector: GameToolSelector       # Decision handler
    conversation_history: list[dict]      # Message history
    created_at: datetime
    last_activity: datetime
```

## Error Handling

### Error Categories

| Category | Examples | Recovery Strategy |
|----------|----------|-------------------|
| Configuration | Missing env vars, invalid provider | Raise descriptive error on init |
| Decider | Low confidence, timeout, unavailable | Fallback to safe action or LLM |
| Tool Execution | Invalid args, tool not found | Return error in response |
| Session | Invalid session_id, timeout | Create new session |

### Error Response Format

```python
@dataclass
class ErrorResponse:
    """Error response format."""
    
    reply: str                            # User-friendly error message
    decisions: list[DecisionRecord]       # May contain error record
    model_id: str
    latency_ms: int
    agent: str = "WILD SOUL Agent"
    error: bool = True                    # Indicates error state
    error_type: str | None = None         # Error category
```

### Error Handling Flow

```
┌─────────────┐
│   Error     │
│  Detected   │
└──────┬──────┘
       │
       ├──────────────────────────────────┐
       │                                  │
       ▼                                  ▼
┌─────────────────┐              ┌─────────────────┐
│ Decider Error?  │              │ Tool Error?     │
└────────┬────────┘              └────────┬────────┘
         │                                │
    ┌────┴────┐                      ┌────┴────┐
    │         │                      │         │
    ▼         ▼                      ▼         ▼
┌────────┐ ┌────────┐            ┌────────┐ ┌────────┐
│ Low    │ │Timeout │            │ Invalid│ │ Exec   │
│Confid. │ │/Unavail│            │ Args   │ │ Failed │
└───┬────┘ └───┬────┘            └───┬────┘ └───┬────┘
    │          │                     │          │
    ▼          ▼                     ▼          ▼
┌────────┐ ┌────────┐            ┌────────┐ ┌────────┐
│Fallback│ │ LLM    │            │Error   │ │Error   │
│to safe │ │Fallback│            │Message │ │State   │
│action  │ │        │            │        │ │        │
└────────┘ └────────┘            └────────┘ └────────┘
```

### Fallback Configuration

```python
# Default fallback behavior
DECIDER_CONFIDENCE_THRESHOLD = 0.6  # Below this, use fallback
FALLBACK_TOOL = "check_status"       # Safe default action
LLM_FALLBACK_ENABLED = True          # Use LLM when decider unavailable
```

## Configuration Schema

### Environment Variables

```bash
# LLM Configuration
LLM_PROVIDER=bedrock              # bedrock | local | ugmdu
BEDROCK_MODEL_ID=us.amazon.nova-pro-v1:0
LLM_MODEL_ID=qwen3.5:4b           # For local/ugmdu providers
LLM_API_KEY=                      # For ugmdu provider

# Decider Configuration
DECIDER_MODE=local                # local | ugmdu | custom
DECIDER_URL=                      # Custom decider URL (for DECIDER_MODE=custom)
DECIDER_API_KEY=                  # For ugmdu provider

# AWS Configuration
AWS_REGION=us-east-1
AWS_PROFILE=default

# Optional: AgentCore Integration
# MEMORY_GAME_SESSION_ID=<memory-id>
# AGENTCORE_GATEWAY_GAME_TOOLS_URL=<gateway-url>
# AGENTCORE_GATEWAY_GAME_TOOLS_AUTH_TYPE=AWS_IAM

# Demo Mode
DEMO_EAGER=0                      # Set to 1 for demo mode (acts without asking)
```

### Settings Resolution

```python
def resolve_settings() -> WildSoulSettings:
    """
    Resolve settings from environment with defaults.
    
    Priority:
        1. Explicit parameter
        2. Environment variable
        3. Default value
    """
    return WildSoulSettings(
        llm_provider=os.environ.get("LLM_PROVIDER", "bedrock"),
        model_id=(
            os.environ.get("BEDROCK_MODEL_ID") or
            settings().bedrock_model
        ),
        decider_mode=os.environ.get("DECIDER_MODE", "local"),
        decider_url=resolve_decider_url(),
        aws_region=settings().aws_region
    )
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Response Structure Validity

*For any* game state message processed by the WildSoulAgent, the response dictionary SHALL contain all required fields (`reply`, `decisions`, `model_id`, `latency_ms`, `agent`) with correct types.

**Validates: Requirements 1.1, 1.4**

### Property 2: Tool Selection Decision Completeness

*For any* game state message, the tool selection decision record SHALL contain the selected tool name, confidence score, full probability distribution, and decider latency.

**Validates: Requirements 3.1, 3.6**

### Property 3: Tool Docstring Presence

*For any* tool in the game tools list, the tool SHALL have a non-empty docstring describing its purpose, and this description SHALL be under 200 characters for optimal decider comprehension.

**Validates: Requirements 2.6, 3.4**

### Property 4: Session State Continuity

*For any* sequence of messages within the same session_id, the agent SHALL maintain conversation context, and subsequent messages SHALL have access to earlier conversation history.

**Validates: Requirements 1.5**

### Property 5: Low Confidence Fallback

*For any* game state where the decider returns confidence below the threshold (0.6), the system SHALL either fall back to the designated safe action (`check_status`) or request clarification.

**Validates: Requirements 3.5**

### Property 6: Decision State Context

*For any* tool selection decision, the state passed to the decider SHALL include the conversation history and the proposed action context.

**Validates: Requirements 3.3**

### Property 7: Credential Non-Exposure

*For any* response, log entry, or error message, the system SHALL NOT expose API keys, credentials, or secrets in plain text.

**Validates: Requirements 4.5**

### Property 8: Eval Case Format Validity

*For any* line in `eval_cases.jsonl`, the JSON object SHALL contain a `state` field with game context and an `expected` field with the correct tool selection.

**Validates: Requirements 5.2**

## Testing Strategy

### Unit Tests

Unit tests verify specific examples, edge cases, and error conditions:

1. **API Contract Tests**
   - Verify `WildSoulAgent.chat()` accepts correct parameters
   - Verify response structure matches specification
   - Verify error responses follow error format

2. **Tool Registration Tests**
   - Verify all five tools are registered
   - Verify each tool has required operations
   - Verify tool schemas are valid

3. **Configuration Tests**
   - Test each LLM_PROVIDER value
   - Test each DECIDER_MODE value
   - Test environment variable fallbacks

### Property-Based Tests

Property tests verify universal properties across generated inputs:

1. **Response Structure Property**
   - Generate random game state messages
   - Verify response always contains required fields with correct types

2. **Tool Selection Completeness Property**
   - Generate random game contexts
   - Verify decision log always contains tool, confidence, probabilities, latency

3. **Session Continuity Property**
   - Generate sequences of related messages
   - Verify conversation history grows within a session

4. **Low Confidence Fallback Property**
   - Generate ambiguous game states designed to produce low confidence
   - Verify fallback behavior triggers correctly

### Integration Tests

Integration tests verify end-to-end behavior:

1. **Full Game Scenario Tests**
   - Simulate complete game sessions with multiple turns
   - Verify tool selections are contextually appropriate

2. **Multi-Session Tests**
   - Verify session isolation
   - Verify multiple concurrent sessions work independently

### Configuration

- **Property tests**: Minimum 100 iterations per property
- **Test tags**: `**Feature: wild-soul-agent, Property {number}: {property_text}**`

## Implementation Notes

### Reusing Kit Patterns

The WILD SOUL Agent follows established patterns from the hackathon kit:

1. **Agent Class Structure** - Mirrors `HackathonAgent` from `agent/agent.py`
2. **Tool Definition Pattern** - Follows `@tool` decorator pattern from `agent/tools.py`
3. **Decision Pattern Structure** - Implements `#tool-selection` from `decider_kit/patterns/tool_selection.py`
4. **Configuration Pattern** - Uses `decider_kit/config.py` and `.env` approach

### Key Differences from Reference Kit

| Aspect | Reference Kit (Store Support) | WILD SOUL Agent |
|--------|-------------------------------|-----------------|
| Domain | E-commerce order management | Game playing |
| Tools | lookup_order, refund_order, cancel_order | manage_inventory, interact_npc, explore_area, combat_action, check_status |
| Decision Pattern | #guardrails (before tool execution) | #tool-selection (tool routing) |
| State Context | Customer conversation + order data | Game state + player context |

### Extensibility Points

1. **Additional Game Tools** - Add new tools by following the `@tool` pattern with clear docstrings
2. **Custom Decision Questions** - Extend QUESTIONS for domain-specific classification
3. **AgentCore Integration** - Enable Memory for game session history, Gateway for external game APIs
