import sys
from pathlib import Path
sys.path.insert(0, r"c:\Users\userd\Downloads\MY-AGENT\dhanush-raman-b-decider-hackathon-kit\dhanush-raman-b-decider-hackathon-kit")
sys.path.insert(0, r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent")

# Test 6: Configuration loading (fixed)
print("6. Testing configuration loading...")
try:
    from decider_kit.config import load_dotenv, settings
    load_dotenv(Path(r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\.env"))
    s = settings()
    print("   PASS: Configuration loaded successfully")
    print(f"   Decider mode: {s.decider_mode}")
    print(f"   AWS Region: {s.aws_region}")
    print(f"   Bedrock model: {s.bedrock_model}")
except Exception as e:
    print(f"   FAIL: {e}")
    import traceback
    traceback.print_exc()
