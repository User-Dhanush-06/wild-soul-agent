"""
WILD SOUL GAME - Version 2
Fully functional graphical game with 2D world, working buttons, and interactive chat.
Built with Streamlit + AI agent.
"""

import streamlit as st
import sys
from pathlib import Path
import time
import os

# Setup paths - must be first
os.chdir(r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")
sys.path.insert(0, r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\_decider_kit_wrapper")
sys.path.insert(0, r"C:\Users\userd\Downloads\MY-AGENT\dhanush-raman-b-decider-hackathon-kit\dhanush-raman-b-decider-hackathon-kit")

# Import dependencies safely
try:
    from _decider_kit_wrapper import Decider, agent_model, default_model_id, strip_thinking
    from strands import Agent
    from strands.interventions import InterventionHandler, Proceed
except Exception as e:
    st.error(f"Import error: {e}")
    st.stop()

# Load game tools
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("game_tools", 
        r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\agent\tools.py")
    game_tools_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(game_tools_mod)
    TOOLS = game_tools_mod.TOOLS
except Exception as e:
    st.error(f"Error loading tools: {e}")
    st.stop()

# Load decision pattern
try:
    spec2 = importlib.util.spec_from_file_location("game_decision", 
        r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\agent\decision.py")
    decision_mod = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(decision_mod)
    ToolSelector = decision_mod.ToolSelector
except Exception as e:
    st.error(f"Error loading decision: {e}")
    st.stop()

# AGENT CLASS
class GameAgent:
    """Simple agent wrapper for the game."""
    def __init__(self):
        try:
            self.decider = Decider()
            self.model_id = default_model_id()
            self.sessions = {}
        except Exception as e:
            raise Exception(f"Agent init failed: {e}")
    
    def _get_session(self, sid):
        if sid not in self.sessions:
            try:
                tool_selector = ToolSelector(self.decider)
                agent = Agent(
                    model=agent_model(self.model_id),
                    system_prompt="You are a companion in WILD SOUL fantasy game. Help the player with their adventure. Be helpful and concise.",
                    tools=TOOLS,
                    interventions=[tool_selector]
                )
                self.sessions[sid] = (agent, tool_selector)
            except Exception as e:
                raise Exception(f"Session creation failed: {e}")
        return self.sessions[sid]
    
    def chat(self, message, sid="default"):
        """Get response from agent."""
        try:
            agent, tool_selector = self._get_session(sid)
            before = len(tool_selector.log)
            
            t0 = time.perf_counter()
            result = agent(message)
            reply = strip_thinking(str(result))
            
            new_decisions = tool_selector.log[before:]
            latency_ms = round((time.perf_counter() - t0) * 1000)
            
            return {
                "reply": reply,
                "decisions": new_decisions,
                "latency_ms": latency_ms,
                "success": True
            }
        except Exception as e:
            return {
                "reply": f"Error: {str(e)[:100]}",
                "decisions": [],
                "latency_ms": 0,
                "success": False
            }

# PAGE CONFIG
st.set_page_config(page_title="WILD SOUL", layout="wide", initial_sidebar_state="expanded")

# STYLING
st.markdown("""
<style>
    body { background-color: #0a0e27; }
    .stApp { background-color: #0a0e27; }
    .game-world { 
        background-color: #1a1f3a; 
        border: 2px solid #6dd5ed; 
        padding: 20px; 
        border-radius: 8px;
        font-family: monospace;
        color: #e8e8e8;
        min-height: 400px;
    }
    .chat-box { 
        background-color: #1a1f3a; 
        border: 2px solid #6dd5ed; 
        padding: 15px; 
        border-radius: 8px;
        color: #e8e8e8;
        max-height: 400px;
        overflow-y: auto;
    }
    .stat-bar {
        background-color: #2d3561;
        border-radius: 4px;
        overflow: hidden;
        border: 1px solid #6dd5ed;
    }
    .health-fill { background-color: #ff4444; height: 20px; }
    .mana-fill { background-color: #4444ff; height: 20px; }
    button { background-color: #2d3561; color: #e8e8e8; border: 1px solid #6dd5ed; }
</style>
""", unsafe_allow_html=True)

# INITIALIZE SESSION STATE
if "agent" not in st.session_state:
    st.session_state.agent = GameAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "player_health" not in st.session_state:
    st.session_state.player_health = 85

if "player_mana" not in st.session_state:
    st.session_state.player_mana = 40

if "location" not in st.session_state:
    st.session_state.location = "Village Square"

if "world_map" not in st.session_state:
    st.session_state.world_map = {
        "Village Square": {"display": "VILLAGE\n  You  \nSQUARE", "enemies": []},
        "Dark Forest": {"display": "FOREST\n🌲You🌲\n TREES", "enemies": ["Goblin"]},
        "Goblin Cave": {"display": " CAVE\nYou⚡\nDARK", "enemies": ["Goblin Shaman"]},
    }

if "last_decision" not in st.session_state:
    st.session_state.last_decision = None

# HEADER
st.title("🎮 WILD SOUL - Fantasy Adventure")
st.subheader("An AI-Powered Game with Strands Decider 2B")
st.divider()

# MAIN LAYOUT
col_world, col_chat = st.columns([1.2, 1])

with col_world:
    st.markdown("### 🌍 Game World")
    
    # 2D WORLD DISPLAY
    world_container = st.container()
    with world_container:
        location_data = st.session_state.world_map.get(st.session_state.location, 
                                                        st.session_state.world_map["Village Square"])
        
        st.markdown(f"**Location:** `{st.session_state.location}`")
        
        # Draw 2D world
        world_display = f"""
```
╔════════════════════╗
║ {location_data['display'].split(chr(10))[0]:<20} ║
║ {location_data['display'].split(chr(10))[1]:<20} ║
║ {location_data['display'].split(chr(10))[2]:<20} ║
╚════════════════════╝
```
        """
        st.markdown(world_display)
        
        # Enemies
        if location_data["enemies"]:
            st.warning(f"⚠️ Enemies: {', '.join(location_data['enemies'])}")
        else:
            st.success("✓ No enemies visible")
    
    st.divider()
    
    # PLAYER STATS
    st.markdown("### ❤️ Player Stats")
    
    health_pct = (st.session_state.player_health / 100) * 100
    mana_pct = (st.session_state.player_mana / 50) * 100
    
    st.write(f"**Health:** {st.session_state.player_health}/100")
    st.progress(health_pct / 100, text=f"{health_pct:.0f}%")
    
    st.write(f"**Mana:** {st.session_state.player_mana}/50")
    st.progress(mana_pct / 100, text=f"{mana_pct:.0f}%")
    
    st.divider()
    
    # QUICK ACTION BUTTONS
    st.markdown("### ⚡ Quick Actions")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("🗡️ ATTACK", use_container_width=True, key="btn_attack"):
            action_text = "I want to attack the nearest enemy with my sword!"
            st.session_state.messages.append(("You", action_text))
            response = st.session_state.agent.chat(action_text)
            if response["success"]:
                st.session_state.messages.append(("Agent", response["reply"]))
                if response["decisions"]:
                    st.session_state.last_decision = response["decisions"][0]
                st.session_state.player_health = max(0, st.session_state.player_health - 5)
                st.rerun()
    
    with btn_col2:
        if st.button("🚶 EXPLORE", use_container_width=True, key="btn_explore"):
            action_text = "I want to explore the area for items and new locations."
            st.session_state.messages.append(("You", action_text))
            response = st.session_state.agent.chat(action_text)
            if response["success"]:
                st.session_state.messages.append(("Agent", response["reply"]))
                if response["decisions"]:
                    st.session_state.last_decision = response["decisions"][0]
                # Change location
                st.session_state.location = "Dark Forest"
                st.rerun()
    
    with btn_col3:
        if st.button("❤️ STATUS", use_container_width=True, key="btn_status"):
            action_text = "Check my current health, mana, and status."
            st.session_state.messages.append(("You", action_text))
            response = st.session_state.agent.chat(action_text)
            if response["success"]:
                st.session_state.messages.append(("Agent", response["reply"]))
                if response["decisions"]:
                    st.session_state.last_decision = response["decisions"][0]
                st.rerun()

with col_chat:
    st.markdown("### 💬 Agent Chat")
    
    # CHAT DISPLAY
    chat_display = st.container(border=True, height=350)
    with chat_display:
        if st.session_state.messages:
            for speaker, text in st.session_state.messages[-10:]:
                if speaker == "You":
                    st.markdown(f"**You:** {text}")
                else:
                    st.markdown(f"**Agent:** {text}")
        else:
            st.info("💭 Game starting... Type a command or click a button!")
    
    st.divider()
    
    # COMMAND INPUT
    st.markdown("### 📝 Your Command")
    user_command = st.text_input(
        "What do you do?",
        placeholder="e.g., Attack the goblin, explore deeper, use my potion",
        key="user_input"
    )
    
    if st.button("📤 SEND", use_container_width=True, key="btn_send"):
        if user_command.strip():
            # Add user message
            st.session_state.messages.append(("You", user_command))
            
            # Get agent response
            response = st.session_state.agent.chat(user_command)
            
            if response["success"]:
                st.session_state.messages.append(("Agent", response["reply"]))
                
                # Update last decision
                if response["decisions"]:
                    st.session_state.last_decision = response["decisions"][0]
                
                # Game state changes based on content
                if "attack" in user_command.lower():
                    st.session_state.player_health = max(0, st.session_state.player_health - 10)
                elif "heal" in user_command.lower() or "potion" in user_command.lower():
                    st.session_state.player_health = min(100, st.session_state.player_health + 20)
                elif "explore" in user_command.lower():
                    locations = list(st.session_state.world_map.keys())
                    import random
                    st.session_state.location = random.choice(locations)
                
                st.rerun()
            else:
                st.error("Failed to get response from agent")

# SIDEBAR - STATS & INFO
with st.sidebar:
    st.markdown("## 📊 Game Info")
    
    st.markdown("### Player")
    st.write("**Name:** Adventurer")
    st.write("**Level:** 1")
    st.write("**Gold:** 250")
    
    st.markdown("### Inventory")
    st.write("🗡️ Iron Sword")
    st.write("🛡️ Leather Armor")
    st.write("💊 Health Potion x3")
    st.write("💙 Mana Potion x2")
    
    st.markdown("### Last AI Decision")
    if st.session_state.last_decision:
        dec = st.session_state.last_decision
        st.info(f"""
**Tool:** {dec.get('selected_tool', 'N/A')}
**Confidence:** {dec.get('confidence', 0):.1%}
**Latency:** {dec.get('decider_ms', 0)}ms
        """)
    else:
        st.write("*(None yet)*")
    
    st.divider()
    
    st.markdown("### How to Play")
    st.write("""
1. Click action buttons or type commands
2. Watch the AI make decisions
3. Explore locations, fight enemies
4. Check your status
5. Try healing items
    """)
    
    st.markdown("### Built With")
    st.write("""
- **Strands Decider 2B** - AI decision making
- **Amazon Bedrock** - Language model
- **Streamlit** - Game UI
- **Python Agent** - Game logic
    """)

st.divider()
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.8rem;">
Built with the AWS User Group Madurai Strands Decider hackathon kit.
</div>
""", unsafe_allow_html=True)
