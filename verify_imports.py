import sys
sys.path.insert(0, r"c:\Users\userd\Downloads\MY-AGENT\dhanush-raman-b-decider-hackathon-kit\dhanush-raman-b-decider-hackathon-kit")
sys.path.insert(0, r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")

print("=== Import Verification ===\n")

# Test 1: Tools import
print("1. Testing tools.py imports...")
try:
    from agent.tools import TOOLS, manage_inventory, interact_npc, explore_area, combat_action, check_status
    print("   PASS: All tools import successfully")
    print(f"   Tools: {[t.__name__ for t in TOOLS]}")
except Exception as e:
    print(f"   FAIL: {e}")

# Test 2: Decision pattern imports
print("\n2. Testing decision.py imports...")
try:
    from agent.decision import PATTERN_TAG, QUESTIONS, ToolSelector
    print("   PASS: Decision pattern imports successfully")
    print(f"   Pattern tag: {PATTERN_TAG}")
except Exception as e:
    print(f"   FAIL: {e}")

# Test 3: Agent imports
print("\n3. Testing agent.py imports...")
try:
    from agent.agent import WildSoulAgent, NAME, SYSTEM_PROMPT
    print("   PASS: WildSoulAgent class imports successfully")
    print(f"   Agent name: {NAME}")
except Exception as e:
    print(f"   FAIL: {e}")

# Test 4: Decider kit imports
print("\n4. Testing decider_kit imports...")
try:
    from decider_kit import Decider
    print("   PASS: Decider imports successfully from reference kit")
except Exception as e:
    print(f"   FAIL: {e}")

# Test 5: LLM module imports
print("\n5. Testing llm module imports...")
try:
    from decider_kit.llm import agent_model, default_model_id, strip_thinking
    print("   PASS: LLM utilities import successfully")
except Exception as e:
    print(f"   FAIL: {e}")

# Test 6: Configuration loading
print("\n6. Testing configuration loading...")
try:
    from decider_kit.config import load_dotenv, settings
    load_dotenv(r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\.env")
    s = settings()
    print("   PASS: Configuration loaded successfully")
    print(f"   LLM Provider: {s.decider_mode}")
    print(f"   AWS Region: {s.aws_region}")
except Exception as e:
    print(f"   FAIL: {e}")

print("\n=== All imports verified ===")
