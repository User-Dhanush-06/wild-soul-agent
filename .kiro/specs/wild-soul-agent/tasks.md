# Implementation Plan: wild-soul-agent

## Overview

This implementation plan creates the WILD SOUL Agent - an autonomous game agent that plays the WILD SOUL game using Strands Decider 2B for intelligent tool selection. The agent will implement the HackathonAgent interface contract while providing specialized game-playing capabilities with five distinct game tools.

## Tasks

- [x] 1. Create project structure and configuration
  - [x] 1.1 Create wild-soul-agent directory structure matching the reference kit layout
    - Create agent/, decider_kit/ (optional for patterns), demo/, deploy/ directories
    - Create required __init__.py files for Python packages
    - _Requirements: 1.1, 1.6_
  
  - [x] 1.2 Create configuration files
    - Copy and modify .env.example for WILD SOUL configuration
    - Create .env file with appropriate values for the game context
    - _Requirements: 4.1, 4.2_

- [ ] 2. Implement five game tools
  - [-] 2.1 Implement ManageInventory tool
    - Create tool with operations: equip, use, drop, examine
    - Write one-line docstring for decider tool selection
    - _Requirements: 2.1_
  
  - [-] 2.2 Implement InteractNPC tool
    - Create tool with operations: talk, trade, quest
    - Write one-line docstring for decider tool selection
    - _Requirements: 2.2_
  
  - [-] 2.3 Implement ExploreArea tool
    - Create tool with operations: move, search, discover
    - Write one-line docstring for decider tool selection
    - _Requirements: 2.3_
  
  - [-] 2.4 Implement CombatAction tool
    - Create tool with operations: attack, defend, ability use
    - Write one-line docstring for decider tool selection
    - _Requirements: 2.4_
  
  - [ ] 2.5 Implement CheckStatus tool
    - Create tool with operations: check health, mana, buffs, debuffs, quest progress
    - Write one-line docstring for decider tool selection
    - _Requirements: 2.5_
  
  - [~] 2.6 Create TOOLS list and export all tools
    - Aggregate all five tools into a TOOLS list
    - Export tools for use by agent and testing
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 3. Implement WildSoulAgent class
  - [~] 3.1 Implement agent initialization
    - Initialize decider, model_id, eager mode, and sessions
    - Support optional decider and model_id parameters
    - _Requirements: 1.1, 1.3_
  
  - [~] 3.2 Implement session management
    - Create _session method to get or create Agent instances per session_id
    - Store conversation history within sessions
    - _Requirements: 1.5_
  
  - [~] 3.3 Implement chat method
    - Accept message, session_id, and images parameters
    - Use Amazon Bedrock for conversation and reasoning
    - Return response with reply, decisions, model_id, latency_ms, and agent fields
    - _Requirements: 1.1, 1.2, 1.4, 1.6_
  
  - [~] 3.4 Implement Strands Agent integration
    - Create Strands Agent instance with system prompt and tools
    - Wire in the tool selection decision pattern
    - _Requirements: 1.3, 3.1, 3.3_

- [ ] 4. Implement tool selection decision pattern
  - [~] 4.1 Create decision.py with #tool-selection pattern
    - Define PATTERN_TAG as "#tool-selection"
    - Create QUESTIONS dictionary with tool question
    - _Requirements: 3.1, 3.3, 6.3_
  
  - [~] 4.2 Implement ToolSelection pattern class
    - Create ToolSelection class extending InterventionHandler
    - Implement before_tool_call method for decision logic
    - Handle low confidence cases (below 0.6-0.7) with fallback to safe action
    - _Requirements: 3.1, 3.4, 3.5, 3.6_
  
  - [~] 4.3 Wire tool selection pattern to agent
    - Pass ToolSelection to Agent interventions
    - Log each decision with tool, confidence, and latency
    - _Requirements: 3.6_

- [ ] 5. Create evaluation cases
  - [~] 5.1 Create eval_cases.jsonl with diverse test cases
    - Include combat scenarios (goblin encounter, boss battle)
    - Include exploration scenarios (new area discovery, search)
    - Include inventory management (equipping items, using potions)
    - Include NPC interaction (talking, trading, quest acceptance)
    - Include status checking (low health, mana management)
    - Include edge cases with ambiguous appropriate actions
    - Each test case has state, expected tool selection, and optional split field
    - _Requirements: 5.1, 5.2, 5.5, 5.6_
  
  - [~] 5.2 Verify eval_cases coverage
    - Test all five tool types
    - Include edge cases for confidence handling
    - Cover diverse game scenarios
    - _Requirements: 5.1, 5.5, 5.6_

- [ ] 6. Create demo materials
  - [~] 6.1 Create demo_script.yaml
    - Define title for the demo video
    - Include pitch and features sections
    - Create turns with say and narrate fields
    - Include intro and outro sections
    - _Requirements: 5.3, 5.4_
  
  - [~] 6.2 Create or update demo server
    - Ensure demo server supports WILD SOUL Agent
    - Test with demo_script.yaml
    - _Requirements: 1.6_

- [ ] 7. Create documentation
  - [~] 7.1 Create AGENT.md
    - Describe the WILD SOUL use case
    - Explain the decision handed to Strands Decider 2B
    - Explain why a decision model is appropriate
    - Include pitch, who it's for, and features
    - _Requirements: 6.4, 6.5, 6.6_
  
  - [~] 7.2 Create decision.py documentation
    - Document the #tool-selection pattern
    - Explain the decision question and options
    - Document how to reuse the pattern
    - _Requirements: 6.3, 6.5, 6.6_
  
  - [~] 7.3 Update AGENTS.md for wild-soul-agent
    - Add WILD SOUL Agent documentation
    - Credit the AWS User Group Madurai hackathon kit
    - Include two tags: #strands-decider-2b and #tool-selection
    - _Requirements: 6.5, 6.6_

- [ ] 8. Create submission materials
  - [~] 8.1 Add Apache-2.0 license
    - Create LICENSE file with Apache-2.0 license text
    - _Requirements: 6.2_
  
  - [~] 8.2 Verify submission checklist
    - Check directory structure matches reference kit
    - Verify all required files exist
    - Confirm license is OSI-approved
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

- [~] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- The tool selection pattern (#tool-selection) is the core decision mechanism
- All tools must have clear one-line docstrings for decider tool selection
- The agent implements the HackathonAgent interface for compatibility with demo UI, benchmark, and AWS deployment pipeline
- Configuration is environment-based for local development and AWS deployment without code changes

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6"] },
    { "id": 2, "tasks": ["3.1", "3.2", "4.1", "4.2", "5.1", "6.1", "7.1"] },
    { "id": 3, "tasks": ["3.3", "3.4", "4.3", "5.2", "6.2", "7.2", "7.3", "8.1"] },
    { "id": 4, "tasks": ["8.2"] }
  ]
}
```