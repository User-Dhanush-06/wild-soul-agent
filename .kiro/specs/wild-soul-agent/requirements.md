# Requirements Document

## Introduction

WILD SOUL is an autonomous game agent that plays the WILD SOUL game using Strands Decider 2B for intelligent tool selection. The agent analyzes the game state and selects the most appropriate action from five available game tools, using the #tool-selection decision pattern. The agent runs on Amazon Bedrock AgentCore Runtime with the decider making real-time decisions about which game action to take based on contextual analysis of the current game state.

## Glossary

- **WILD SOUL Agent**: An autonomous AI agent that plays the WILD SOUL game by selecting and executing game actions
- **Strands Decider 2B**: A 2-billion-parameter decision model that classifies states and returns calibrated probabilities
- **Tool Selection Pattern (#tool-selection)**: A decision pattern where the decider chooses which tool the agent should use based on the current context
- **Game State**: The current state of the WILD SOUL game including player status, inventory, location, NPCs, and combat situations
- **ManageInventory**: Tool for managing player inventory items (equip, use, drop, or examine items)
- **InteractNPC**: Tool for interacting with non-player characters (talk, trade, quest interactions)
- **ExploreArea**: Tool for moving through the game world and discovering new locations
- **CombatAction**: Tool for engaging in combat with enemies (attack, defend, use abilities)
- **CheckStatus**: Tool for checking player status (health, mana, buffs, debuffs, quest progress)
- **Amazon Bedrock**: The generative AI service providing the conversation and reasoning capabilities
- **AgentCore Runtime**: The AWS deployment platform for running the agent

## Requirements

### Requirement 1: Core Agent Implementation

**User Story:** As a game developer, I want an autonomous game agent that can play WILD SOUL, so that players can have an intelligent AI companion or opponent.

#### Acceptance Criteria

1. THE WILD SOUL Agent SHALL implement a `WildSoulAgent` class with a `chat` method accepting a game state message and returning a response with the selected action
2. THE WILD SOUL Agent SHALL use Amazon Bedrock (Amazon Nova Pro by default) for generative conversation and reasoning
3. THE WILD SOUL Agent SHALL integrate Strands Decider 2B for tool selection decisions
4. THE WILD SOUL Agent SHALL return a response dictionary containing `reply`, `decisions`, `model_id`, `latency_ms`, and `agent` fields
5. THE WILD SOUL Agent SHALL maintain session state to track conversation history within a game session
6. THE WILD SOUL Agent SHALL follow the `HackathonAgent` interface contract for compatibility with the demo UI, benchmark, and deployment pipeline

### Requirement 2: Game Tool Definitions

**User Story:** As a game system, I need five distinct game tools for the agent to choose from, so that the agent can perform different actions in the game world.

#### Acceptance Criteria

1. THE WILD SOUL Agent SHALL provide a ManageInventory tool for managing inventory items with operations for equip, use, drop, and examine
2. THE WILD SOUL Agent SHALL provide an InteractNPC tool for interacting with non-player characters with operations for talk, trade, and quest
3. THE WILD SOUL Agent SHALL provide an ExploreArea tool for navigation with operations for move, search, and discover
4. THE WILD SOUL Agent SHALL provide a CombatAction tool for combat encounters with operations for attack, defend, and ability use
5. THE WILD SOUL Agent SHALL provide a CheckStatus tool for checking player status including health, mana, buffs, debuffs, and quest progress
6. EACH tool SHALL have a clear one-line docstring describing its purpose for the decider to read during tool selection

### Requirement 3: Tool Selection Decision Pattern

**User Story:** As the agent's decision system, I need to select the most appropriate game tool based on the current context, so that the agent acts intelligently in the game world.

#### Acceptance Criteria

1. WHEN a game action is proposed, THE Tool Selection Pattern SHALL use Strands Decider 2B to classify which tool best fits the current game state
2. THE Tool Selection Pattern SHALL use the `Decider.choice` question type with five options corresponding to the five game tools
3. THE Tool Selection Pattern SHALL include a state description containing the conversation history and proposed action context
4. THE Tool Selection Pattern SHALL provide meaningful option descriptions for each tool to guide the decider's classification
5. THE Tool Selection Pattern SHALL handle low confidence cases (below 0.6-0.7) by falling back to a default safe action or asking for clarification
6. THE Tool Selection Pattern SHALL log each decision with the selected tool, confidence score, and latency

### Requirement 4: Configuration and Infrastructure

**User Story:** As a developer, I want the agent to use configurable LLM and decider endpoints, so that I can develop locally and deploy to AWS without code changes.

#### Acceptance Criteria

1. THE WILD SOUL Agent SHALL read configuration from environment variables following the `.env.example` pattern
2. THE WILD SOUL Agent SHALL support `LLM_PROVIDER` values of `bedrock`, `local`, and `ugmdu` for different deployment scenarios
3. THE WILD SOUL Agent SHALL support `DECIDER_MODE` values of `local`, `ugmdu`, and `custom` for the decision model endpoint
4. THE WILD SOUL Agent SHALL use Amazon Bedrock model ids from environment variables without hardcoding defaults in code
5. THE WILD SOUL Agent SHALL never expose API keys or credentials in logs, responses, or commits
6. THE WILD SOUL Agent SHALL follow the `agentcore.py` pattern for optional integration with AgentCore Memory and Gateway features

### Requirement 5: Testing and Evaluation

**User Story:** As a developer, I need test cases and demo scripts to validate and showcase the agent's decision-making abilities.

#### Acceptance Criteria

1. THE WILD SOUL Agent SHALL include an `eval_cases.jsonl` file with labelled test cases for benchmarking tool selection accuracy
2. EACH test case in `eval_cases.jsonl` SHALL contain a `state` field with the game context, an `expected` field with the correct tool selection, and an optional `split` field for tune/test separation
3. THE WILD SOUL Agent SHALL include a `demo_script.yaml` file defining turns for recording the demo video
4. THE demo_script.yaml SHALL include a title, pitch, features, intro, turns with `say` and `narrate` fields, and an outro
5. THE test cases SHALL cover diverse game scenarios including combat, exploration, inventory management, NPC interaction, and status checking
6. THE test cases SHALL include edge cases where the appropriate action is ambiguous to test the decider's confidence handling

### Requirement 6: Submission Materials

**User Story:** As a hackathon participant, I need complete submission materials including code, article, and video, so that my entry meets all judging requirements.

#### Acceptance Criteria

1. THE WILD SOUL Agent SHALL be in a separate `wild-soul-agent/` directory with the same structure as the reference kit
2. THE WILD SOUL Agent SHALL have an OSI-approved license (Apache-2.0) in the repository
3. THE WILD SOUL Agent SHALL include a `decision.py` file with a clearly labelled reusable decision pattern containing `PATTERN_TAG`, `QUESTIONS`, and the wiring class
4. THE WILD SOUL Agent SHALL include an `AGENT.md` file describing the use case, the decision handed to Strands Decider 2B, and why a decision model is appropriate
5. THE WILD SOUL Agent SHALL credit the AWS User Group Madurai Strands Decider hackathon kit in all generated materials
6. THE WILD SOUL Agent SHALL use exactly two tags for submission: `#strands-decider-2b` and `#tool-selection`
