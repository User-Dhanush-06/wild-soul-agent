# HACKATHON SUBMISSION CHECKLIST

## ✅ PHASE 1: MATERIALS READY

- [x] **Agent Code**
  - agent/agent.py (80 lines)
  - agent/decision.py (110 lines, #tool-selection pattern)
  - agent/tools.py (325 lines, 5 game tools)
  - agent/__init__.py

- [x] **Documentation**
  - README.md (project overview)
  - agent/AGENT.md (technical description)
  - LICENSE (Apache-2.0)

- [x] **Test Cases & Configuration**
  - agent/eval_cases.jsonl (10 test scenarios)
  - agent/demo_script.yaml (video script outline)
  - agent/features.yaml (feature list)

- [x] **Game Application**
  - game_v2.py (Streamlit-based playable game)
  - app.py (CLI version)

- [x] **Test Suite (16/16 passing)**
  - test_bug_fixes.py (7 tests)
  - test_game_functionality.py (4 tests)
  - test_detailed_validation.py (3 tests)
  - test_final_proof.py (2 tests)

---

## 🎬 PHASE 2: VIDEO & ARTICLE

### Video Production

- [ ] **Record Demo Video**
  - [ ] Use RECORDING_GUIDE.md (step-by-step)
  - [ ] Start game: \streamlit run game_v2.py\
  - [ ] Narrate using VIDEO_NARRATION_SCRIPT.md
  - [ ] Target length: 2:55 (under 3 minutes)
  - [ ] Format: MP4, 1280x720, H.264 + AAC
  - [ ] Save as: \WILD_SOUL_DEMO_VIDEO.mp4\

- [ ] **Upload to YouTube**
  - [ ] Create YouTube account (if needed)
  - [ ] Upload video (unlisted or public)
  - [ ] Add title: "WILD SOUL Agent - Autonomous Game AI with Strands Decider 2B"
  - [ ] Add description (include kit credit and GitHub link)
  - [ ] Add tags: #strands-decider-2b, #tool-selection, #aws
  - [ ] Copy video URL

### Article Publication

- [ ] **Technical Article**
  - [x] Draft written (ARTICLE_WILD_SOUL_TECHNICAL_DEEP_DIVE.md)
  - [ ] Review for clarity and accuracy
  - [ ] Prepare for AWS Builder Center or Medium

**Article Details:**
- Title: "WILD SOUL Agent: Intelligent Tool Selection with Strands Decider 2B"
- Length: ~1,800 words (5-7 min read)
- Topics: Classification vs. generation, #tool-selection pattern, evaluation results
- Tags: #AWS, #ML, #GameAI, #AgentDesign

**Submission Platforms:**
- AWS Builder Center (preferred)
- Medium
- Dev.to
- Your own blog

---

## 📋 PHASE 3: GITHUB SETUP

- [ ] **Create GitHub Repository**
  - [ ] Go to github.com, create new public repo
  - [ ] Name: \wild-soul-agent\ (or preferred name)
  - [ ] Description: "Autonomous game agent using Strands Decider 2B for tool selection. Built with AWS User Group Madurai hackathon kit."
  - [ ] License: Apache-2.0
  - [ ] Initialize: No (we'll push existing files)

- [ ] **Prepare Local Files**
  - [ ] Copy to temp directory:
    - agent/agent.py
    - agent/decision.py
    - agent/tools.py
    - agent/AGENT.md
    - agent/eval_cases.jsonl
    - agent/demo_script.yaml
    - README.md
    - LICENSE
    - .env.example
    - .gitignore

- [ ] **Push to GitHub**
  \\\ash
  git clone https://github.com/YOUR_USERNAME/wild-soul-agent.git
  cd wild-soul-agent
  # Copy files here
  git add .
  git commit -m "Initial commit: WILD SOUL Agent with #tool-selection pattern"
  git push origin main
  \\\

- [ ] **Add Repository Topics**
  - Go to Settings → Topics
  - Add: \strands-decider-2b\, \	ool-selection\, \ws\, \game-ai\, \gent\

- [ ] **Get Repository URL**
  - Copy HTTPS URL (e.g., https://github.com/YOUR_USERNAME/wild-soul-agent)

---

## 🏁 PHASE 4: HACKATHON SUBMISSION

Go to: [Strands Decider Hackathon Portal](https://builder.aws.com/build/hackathons/4f50957c-1d08-37ab-b11c-97516b9adeb4)

### Submission Form Fields

| Field | Value | Status |
|-------|-------|--------|
| **Project Name** | WILD SOUL Agent | [ ] |
| **Short Description** | Autonomous game player using Strands Decider 2B for intelligent tool selection | [ ] |
| **GitHub Repository URL** | https://github.com/YOUR_USERNAME/wild-soul-agent | [ ] |
| **Video URL** | https://youtube.com/watch?v=YOUR_VIDEO_ID | [ ] |
| **Article/Blog URL** | https://aws.amazon.com/blogs/... (or Medium link) | [ ] |
| **Pattern Tag** | #tool-selection | [ ] |
| **Bedrock Integration** | Yes (Amazon Nova for narrative) | [ ] |
| **Strands Decider 2B Used** | Yes | [ ] |

---

## 📝 FINAL CHECKLIST (Before Submission)

- [ ] Video is exactly <3 minutes (2:55 target)
- [ ] Video narration is clear and professional
- [ ] Video shows 3 game scenarios + fallback behavior
- [ ] GitHub repo is public and has all required files
- [ ] README mentions AWS User Group Madurai kit credit
- [ ] Article is published or ready to publish
- [ ] All URLs are working and public-facing
- [ ] Video description includes GitHub + article links
- [ ] Tags (#strands-decider-2b + #tool-selection) are on repo and video

---

## 🚀 SUBMISSION DEADLINE

**October 23, 2026 - 11:59 PM PT**

**Time to submit**: ~2 hours of work
1. Record video: 15-20 min
2. Upload to YouTube: 5 min
3. Create GitHub repo: 10 min
4. Push code: 5 min
5. Publish article: 10-30 min (depending on platform)
6. Fill hackathon form: 10 min

---

## ✨ BONUS: After Submission

- [ ] Share video link on Twitter/LinkedIn (tag @AWS, @AWSMadurai)
- [ ] Comment on hackathon portal with additional insights
- [ ] Ask for community feedback on #tool-selection pattern
- [ ] Consider writing a follow-up article on lessons learned
- [ ] Open issues on GitHub if community has questions

---

## RESOURCES

- **Kit Documentation**: https://github.com/Vivek0712/decider-hackathon-kit
- **Strands Agents SDK**: https://strands.com/agents
- **AWS Bedrock Docs**: https://aws.amazon.com/bedrock
- **Decider 2B Info**: https://aws.amazon.com/bedrock/models (search "Decider")
- **Builder Center**: https://aws.amazon.com/blogs

---

**Status**: All materials ready for submission. Estimated time to finalize: 2-3 hours.

Good luck! 🎮✨
