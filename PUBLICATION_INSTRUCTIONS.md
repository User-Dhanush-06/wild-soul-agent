# STEP-BY-STEP PUBLICATION INSTRUCTIONS

## APPROVAL REQUIRED BEFORE PROCEEDING

User must explicitly approve each step before execution.

---

## STEP 1: CREATE PUBLIC GITHUB REPOSITORY

### Prerequisites
- GitHub account (https://github.com)
- Git installed locally
- Access to code at: c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent

### Instructions

1. Go to https://github.com/new
2. Fill in repository details:
   - **Repository name**: wild-soul-agent
   - **Description**: "WILD SOUL Agent - Autonomous game player using Strands Decider 2B for intelligent tool selection and Amazon Bedrock for narrative responses. Built with the AWS User Group Madurai Strands Decider hackathon kit."
   - **Visibility**: Public (required for hackathon)
   - **Initialize repository**: None (we'll push existing code)
3. Click "Create repository"
4. Copy the repository URL (e.g., https://github.com/USERNAME/wild-soul-agent.git)

### Push Code to GitHub

In PowerShell:

cd c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent
git init
git add .
git commit -m "Initial commit: WILD SOUL Agent with Strands Decider 2B tool selection"
git branch -M main
git remote add origin https://github.com/USERNAME/wild-soul-agent.git
git push -u origin main

### Add GitHub Topics/Tags

On GitHub repository page:
1. Go to repository "Settings"
2. Find "Topics" section (or directly: click gear icon, look for "About")
3. Add topics: strands-decider-2b, tool-selection
4. Save

### Verify Files

Check GitHub shows:
- agent/ directory with all .py files
- agent/AGENT.md
- agent/eval_cases.jsonl
- agent/demo_script.yaml
- LICENSE
- README.md
- .env.example
- .gitignore

Do NOT see:
- .env (should be in .gitignore)
- __pycache__/ (should be in .gitignore)

---

## STEP 2: RECORD DEMO VIDEO (< 3 minutes)

### Prerequisites
- Screencast software (OBS Studio free, or ScreenFlow/SnapSnap)
- Audio setup (built-in mic OK)
- Script: agent/demo_script.yaml (ready)

### Video Content Checklist

Show the following (use demo_script.yaml as guide):

[ ] Introduction
    - "WILD SOUL Agent uses Strands Decider 2B to select game tools"
    - "Classification model, not LLM generation"

[ ] Agent Initialization
    - Code: rom agent.agent import WildSoulAgent
    - Code: gent = WildSoulAgent()

[ ] Scenario 1: Combat
    - Input: "I see a goblin ahead with low health"
    - Show: Decider selects combat_action
    - Show: Confidence score (0.92 in script)
    - Show: Tool executes

[ ] Scenario 2: Status Check
    - Input: "Check my status before battle"
    - Show: Decider selects check_status
    - Show: Status output

[ ] Scenario 3: Exploration
    - Input: "Explore the north area"
    - Show: Decider selects explore_area
    - Show: Exploration result

[ ] Decision Log
    - Show: pattern, tool, confidence, probabilities, latency
    - Explain: Low confidence triggers fallback to check_status

[ ] Conclusion
    - "Decider makes real-time decisions"
    - "Fast, calibrated, with fallback behavior"
    - "Credit: Built with AWS User Group Madurai hackathon kit"

### Recording Tips

- 720p minimum resolution
- Speak clearly, explain as you go
- Total duration: 2-3 minutes
- Show code execution, not just terminal
- Emphasize: Decision model classifies, doesn't generate

### Upload Video

1. Create unlisted YouTube video (or use Vimeo, AWS Media)
2. Get public URL
3. Do NOT require password or special access

Example URL format:
- YouTube: https://www.youtube.com/watch?v=XXXXXXX
- Vimeo: https://vimeo.com/XXXXXXX

---

## STEP 3: WRITE BUILDER CENTER ARTICLE

### Article Structure

**Title**: "Using Strands Decider 2B for Game AI Tool Selection"

**Introduction** (100 words)
- Problem: Game AI must decide which action to take
- Traditional approach: LLM does decision + generation (slow, not calibrated)
- Our approach: Classifier for decision, LLM for generation (fast, calibrated)
- Benefit: Real-time decisions with confidence-based fallback

**Use Case** (200 words)
- From agent/AGENT.md - Strategy games need fast decisions
- 5 distinct action types: inventory, NPC, explore, combat, status
- Player says "I see a goblin" - need to decide: attack? check health? explore? etc.

**Decision Pattern** (300 words)
- What decision: "Which game tool handles this situation?"
- Why Decider: Classification not generation, calibrated confidence
- Options: 5 tools + none
- Confidence threshold: 0.6
- Fallback: check_status (safe action)

**Implementation** (400 words)
- Code samples from agent.py, decision.py, tools.py
- How #tool-selection pattern works
- How ToolSelector intervention wires into Strands Agent
- Error handling and edge cases

**Results** (200 words)
- eval_cases.jsonl test coverage
- Tool selection accuracy
- Latency measurements
- Comparison with LLM baseline (if available)

**Reusability** (100 words)
- Pattern can be used in other domains
- Copy decision.py to new project
- Adapt QUESTIONS for your tools
- Same ToolSelector logic applies

**Conclusion** (100 words)
- Decision models for classification, not generation
- Faster, more predictable, better calibrated
- Credit: Built with AWS User Group Madurai hackathon kit

**Word count**: ~1400 total

### Submission Format

AWS Builder Center expects:
- Title
- Subtitle/Description
- Cover image (optional)
- Author bio
- Body text (Markdown supported)
- Code snippets (from agent.py, decision.py)
- Links to GitHub repository
- Tags: strands, decider, aws, game-ai

---

## STEP 4: COMPLETE HACKATHON SUBMISSION

### Find Hackathon Portal

URL (approximate): builder.aws.com/build/hackathons/.../agent-experience-hackathon-strands-decider

### Form Fields to Complete

**Field 1: Project Title**
`
WILD SOUL Agent - Autonomous Game AI with Strands Decider 2B
`

**Field 2: Project Description**
`
Autonomous game agent that uses Strands Decider 2B for intelligent tool selection 
and Amazon Bedrock for narrative responses. Demonstrates how to use a classification 
model for game AI decisions instead of relying on LLM generation alone.
`

**Field 3: GitHub Repository URL**
`
https://github.com/USERNAME/wild-soul-agent
`

**Field 4: Demo Video URL**
`
https://www.youtube.com/watch?v=XXXXXXX
(or your video platform URL)
`

**Field 5: Builder Center Article URL**
`
https://builder.aws.com/build/posts/[article-id]
(or direct link after publication)
`

**Field 6: Technologies Used**
`
- Strands Decider 2B
- Amazon Bedrock (Nova Pro)
- Strands Agents SDK
- Python 3.11
`

**Field 7: Tags**
`
#strands-decider-2b
#tool-selection
`

**Field 8: License**
`
Apache License 2.0
`

**Field 9: Credit Line** (if required)
`
Built with the AWS User Group Madurai Strands Decider hackathon kit
`

### Submit

Click "Submit" button and wait for confirmation.

---

## FULL PUBLICATION WORKFLOW

### Day of Submission

**Morning (30 minutes)**
1. Create GitHub repository
2. Push code
3. Add tags

**Midday (20 minutes)**
4. Verify GitHub repo is public and complete

**Afternoon (30 minutes)**
5. Record demo video
6. Upload to YouTube (or Vimeo)

**Evening (30 minutes)**
7. Write Builder Center article
8. Submit to AWS Builder Center

**Before Deadline (10 minutes)**
9. Complete hackathon submission form
10. Submit to hackathon portal

**Total Time**: ~2 hours

### Deadline

**October 23, 2026, 11:59 PM Pacific Time**

Recommend submitting by 11:00 PM PT to allow for any last-minute platform issues.

---

## SUCCESS CRITERIA

After publication, verify:

[ ] GitHub repository is public and discovers
[ ] All required files visible on GitHub (except .env)
[ ] Tags #strands-decider-2b and #tool-selection present
[ ] Demo video is viewable and under 3 minutes
[ ] Demo shows: agent, decision, tool execution, confidence
[ ] Builder Center article published and visible
[ ] Hackathon submission confirmed

---

## SUPPORT LINKS

- GitHub: https://github.com
- YouTube: https://youtube.com
- AWS Builder Center: https://builder.aws.com
- Hackathon Platform: [specific URL from organizers]

---

## READY FOR PUBLICATION

All materials are complete.
Code is verified and working.
No credentials or secrets in repository.
Awaiting user approval to execute these steps.
