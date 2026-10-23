# Step-by-step submission instructions document

## SUBMISSION CHECKLIST & INSTRUCTIONS

### PHASE 1: REPOSITORY SETUP (Ready Now)

**Files to Include in Public GitHub Repository:**

Required Files:
- agent/agent.py (80 lines) - WildSoulAgent class
- agent/decision.py (110 lines) - #tool-selection pattern
- agent/tools.py (325 lines) - 5 game tools
- .env.example - Configuration template
- LICENSE - Apache-2.0
- README.md - Project description
- agent/AGENT.md - Technical description (to be created)
- agent/eval_cases.jsonl - Test cases (to be created)

Excluded Files (in .gitignore):
- .env (never commit)
- __pycache__/
- *.pyc
- .vscode/
- .DS_Store

Git Tags Required:
- #strands-decider-2b
- #tool-selection

Description:
"WILD SOUL Agent - Autonomous game player using Strands Decider 2B for intelligent tool selection and Amazon Bedrock for narrative gameplay. Built with the AWS User Group Madurai Strands Decider hackathon kit."

### PHASE 2: SUBMISSION MATERIALS (To Create)

1. agent/AGENT.md - Technical Description (~300 words)
   - Use Case: "Autonomous game agent for strategy games"
   - Decision: "Which game tool (5 options) should handle the current game state?"
   - Why Decider: "Classification task, not generation; fast, calibrated confidence"
   - Features:
     * 5 specialized game tools
     * Real-time tool selection
     * Confidence threshold with fallback
     * Narrative integration with Bedrock
   - For: "Game developers, AI/ML researchers, game AI enthusiasts"

2. agent/eval_cases.jsonl - Test Cases (~20 lines, JSONL format)
   Examples:
   {"state": "Player health low, goblin nearby", "expected": "combat_action"}
   {"state": "Unknown area, safe location", "expected": "explore_area"}
   {"state": "Inventory full, found new item", "expected": "manage_inventory"}

3. demo_script.yaml - Video Script (< 3 minutes)
   - Title: "WILD SOUL Agent - AI Tool Selection with Strands Decider 2B"
   - Intro: Show game state
   - Turn 1: Goblin scenario
   - Turn 2: Exploration scenario
   - Turn 3: NPC scenario
   - Show: Agent response, Decider selection, tool execution, confidence score
   - Outro: "Decision-based AI, not prompt-based"

### PHASE 3: PUBLICATION

Repository Setup:
1. Create new GitHub repo (public)
2. Clone locally
3. Copy agent/ directory
4. Copy .env.example, LICENSE, README.md
5. git add . && git commit -m "Initial commit"
6. git push origin main
7. Add topics/tags: strands-decider-2b, tool-selection

Demo Video:
1. Record screencast (< 3 minutes)
2. Show: Agent initialization, game state, Decider decision, tool result
3. Upload to YouTube (unlisted or public)
4. Get video URL

Hackathon Submission:
1. Complete hackathon platform form
2. GitHub URL
3. Demo video URL
4. AGENT.md summary
5. Submit
