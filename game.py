"""
WILD SOUL - Graphical Game Interface
A Streamlit-based graphical game for the WILD SOUL AI agent.
"""

import streamlit as st
import sys
import os
from pathlib import Path
import time

# Setup paths for wrapper and kit
sys.path.insert(0, str(Path("_decider_kit_wrapper").resolve()))
sys.path.insert(0, r"C:\Users\userd\Downloads\MY-AGENT\dhanush-raman-b-decider-hackathon-kit\dhanush-raman-b-decider-hackathon-kit")

# Import dependencies
from _decider_kit_wrapper import Decider, agent_model, default_model_id, strip_thinking
from strands import Agent
from strands.interventions import InterventionHandler, Proceed, Guide

# Load game tools directly
import importlib.util
spec = importlib.util.spec_from_file_location("game_tools", r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\agent\tools.py")
game_tools_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game_tools_mod)
TOOLS = game_tools_mod.TOOLS

# Load decision pattern directly
spec2 = importlib.util.spec_from_file_location("game_decision", r"C:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\agent\decision.py")
decision_mod = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(decision_mod)
ToolSelector = decision_mod.ToolSelector

# Define agent inline
class WildSoulAgent:
    def __init__(self):
        self.decider = Decider()
        self.model_id = default_model_id()
        self.sessions = {}
    
    def _session(self, session_id):
        if session_id not in self.sessions:
            tool_selector = ToolSelector(self.decider)
            agent = Agent(
                model=agent_model(self.model_id),
                system_prompt="You are a companion in WILD SOUL. Help the player.",
                tools=TOOLS,
                interventions=[tool_selector],
                callback_handler=None
            )
            self.sessions[session_id] = (agent, tool_selector)
        return self.sessions[session_id]
    
    def chat(self, message, session_id="default"):
        agent, tool_selector = self._session(session_id)
        before_count = len(tool_selector.log)
        
        t0 = time.perf_counter()
        result = agent(message)
        reply = strip_thinking(str(result))
        
        new_decisions = tool_selector.log[before_count:]
        latency_ms = round((time.perf_counter() - t0) * 1000)
        
        return {
            "reply": reply,
            "decisions": new_decisions,
            "latency_ms": latency_ms
        }

# Page configuration
st.set_page_config(
    page_title="WILD SOUL - Game",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    body {
        background-color: #0a0e27;
        color: #e8e8e8;
    }
    .stApp {
        background-color: #0a0e27;
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #1a1f3a;
        color: #e8e8e8;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #2d3561;
        color: #6dd5ed;
    }
    .health-bar {
        height: 30px;
        background-color: #2d3561;
        border-radius: 5px;
        overflow: hidden;
        border: 2px solid #6dd5ed;
    }
    .health-fill {
        height: 100%;
        background-color: #ff4444;
        width: {health_percent}%;
        transition: width 0.3s;
    }
    .mana-fill {
        height: 100%;
        background-color: #4444ff;
        width: {mana_percent}%;
        transition: width 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = WildSoulAgent()

if "game_log" not in st.session_state:
    st.session_state.game_log = []

if "player_health" not in st.session_state:
    st.session_state.player_health = 85

if "player_max_health" not in st.session_state:
    st.session_state.player_max_health = 100

if "player_mana" not in st.session_state:
    st.session_state.player_mana = 40

if "player_max_mana" not in st.session_state:
    st.session_state.player_max_mana = 50

if "current_location" not in st.session_state:
    st.session_state.current_location = "Village Square"

if "enemies_present" not in st.session_state:
    st.session_state.enemies_present = []

if "last_decision" not in st.session_state:
    st.session_state.last_decision = None

# Header
st.markdown("# 🎮 WILD SOUL - Fantasy Adventure")
st.markdown("*An AI-powered fantasy game using Strands Decider 2B*")
st.divider()

# Three column layout: Game world (left), Chat (right), Stats (sidebar)
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.markdown("## 🌍 Game World")
    
    # Location display
    st.markdown(f"**Location:** {st.session_state.current_location}")
    
    # Placeholder for game world (ASCII art style)
    if "Forest" in st.session_state.current_location:
        st.text("🌲🌲🌲🌲🌲\n🌲   You  🌲\n🌲🌲🌲🌲🌲")
    elif "Dungeon" in st.session_state.current_location:
        st.text("█████████\n█   You  █\n█████████")
    else:
        st.text("████░░████\n░░░░You░░░░\n████░░████")
    
    # Enemies display
    if st.session_state.enemies_present:
        st.markdown("**Enemies:**")
        for enemy in st.session_state.enemies_present:
            st.warning(f"⚔️ {enemy}")
    else:
        st.info("✓ No enemies visible")
    
    # Player stats bars
    st.markdown("### Player Stats")
    
    health_percent = (st.session_state.player_health / st.session_state.player_max_health) * 100
    st.markdown(f"**Health: {st.session_state.player_health}/{st.session_state.player_max_health}**")
    st.progress(health_percent / 100)
    
    mana_percent = (st.session_state.player_mana / st.session_state.player_max_mana) * 100
    st.markdown(f"**Mana: {st.session_state.player_mana}/{st.session_state.player_max_mana}**")
    st.progress(mana_percent / 100)
    
    # Quick action buttons
    st.markdown("### Quick Actions")
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        if st.button("🗡️ Attack"):
            message = "Attack the nearest enemy with my sword!"
            st.session_state.player_health = max(0, st.session_state.player_health - 10)
            st.session_state.enemies_present = []
            process_message(message)
    
    with col_btn2:
        if st.button("🚶 Explore"):
            message = "Explore the area to find items or enemies."
            process_message(message)
    
    with col_btn3:
        if st.button("❤️ Status"):
            message = "Check my current status and inventory."
            process_message(message)

with col_right:
    st.markdown("## 💬 Agent Chat")
    
    # Display game log
    chat_container = st.container(border=True)
    with chat_container:
        if st.session_state.game_log:
            for log_entry in st.session_state.game_log[-10:]:  # Show last 10 entries
                if log_entry["type"] == "player":
                    st.markdown(f"**You:** {log_entry['text']}")
                else:
                    st.markdown(f"**Agent:** {log_entry['text']}")
                    if log_entry.get("decision"):
                        st.caption(f"🤖 Tool: {log_entry['decision']}, Latency: {log_entry.get('latency', 0)}ms")
        else:
            st.markdown("*Game starting... Type a command or click an action button.*")
    
    # Input area
    st.markdown("### Your Command")
    user_input = st.text_input("What do you do?", placeholder="e.g., Attack the goblin, Check my health, Explore the forest")
    
    if st.button("Send", key="send_button"):
        if user_input.strip():
            process_message(user_input)
            st.rerun()

# Sidebar - Inventory and Stats
with st.sidebar:
    st.markdown("## 📊 Stats & Inventory")
    
    st.markdown("### Character")
    st.write(f"**Name:** Adventurer")
    st.write(f"**Level:** 1")
    st.write(f"**Experience:** 0 / 100")
    
    st.markdown("### Inventory")
    inventory_items = [
        "🗡️ Iron Sword",
        "🛡️ Leather Armor",
        "💊 Health Potion x3",
        "💙 Mana Potion x2",
        "💰 Gold Coins x250"
    ]
    for item in inventory_items:
        st.write(item)
    
    st.markdown("### Last Decision")
    if st.session_state.last_decision:
        dec = st.session_state.last_decision
        st.info(f"""
**Tool:** {dec.get('tool', 'unknown')}
**Confidence:** {dec.get('confidence', 0):.1%}
**Pattern:** {dec.get('pattern', 'N/A')}
        """)
    else:
        st.write("*(None yet)*")
    
    st.markdown("### About")
    st.write("""
WILD SOUL is an AI-powered fantasy game using:
- **Strands Decider 2B** for tool selection
- **Amazon Bedrock** for narrative
- **AI agent** for gameplay decisions
    """)

def process_message(user_message: str):
    """Process user message through the agent."""
    # Add user message to log
    st.session_state.game_log.append({
        "type": "player",
        "text": user_message
    })
    
    # Get agent response
    with st.spinner("🤔 Agent thinking..."):
        try:
            result = st.session_state.agent.chat(user_message)
            reply = result["reply"]
            decisions = result.get("decisions", [])
            latency = result.get("latency_ms", 0)
            
            # Extract decision info
            if decisions:
                decision = decisions[0]
                st.session_state.last_decision = {
                    "tool": decision.get("selected_tool", "unknown"),
                    "confidence": decision.get("confidence", 0),
                    "pattern": decision.get("pattern", "N/A")
                }
            
            # Add agent response to log
            st.session_state.game_log.append({
                "type": "agent",
                "text": reply,
                "decision": st.session_state.last_decision.get("tool") if st.session_state.last_decision else None,
                "latency": latency
            })
            
            # Simulate game state changes based on keywords
            if "goblin" in user_message.lower():
                st.session_state.enemies_present = ["Goblin (Low Health)"]
            elif "explore" in user_message.lower():
                st.session_state.current_location = "Dark Forest"
            elif "health" in user_message.lower() or "status" in user_message.lower():
                st.session_state.player_health = 85
                st.session_state.player_mana = 40
            
        except Exception as e:
            error_msg = f"Error: {str(e)[:100]}"
            st.session_state.game_log.append({
                "type": "agent",
                "text": error_msg
            })
            st.error(error_msg)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem;">
Built with the AWS User Group Madurai Strands Decider hackathon kit.
</div>
""", unsafe_allow_html=True)
