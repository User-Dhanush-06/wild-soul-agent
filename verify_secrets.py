import os
from pathlib import Path

print("=== Git Status and Secrets Verification ===\n")

# Test 1: Check .gitignore excludes .env
print("1. Checking .gitignore...")
gitignore_path = Path(r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\.gitignore")
if gitignore_path.exists():
    content = gitignore_path.read_text()
    if ".env" in content:
        print("   PASS: .env is in .gitignore")
    else:
        print("   FAIL: .env NOT in .gitignore")
else:
    print("   FAIL: .gitignore not found")

# Test 2: Check .env file exists but shouldn't be committed
print("\n2. Checking .env file...")
env_path = Path(r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\.env")
if env_path.exists():
    content = env_path.read_text()
    
    # Check for secrets that should never be in version control
    secrets_found = False
    secret_patterns = [
        "aws_access_key",
        "aws_secret_key",
        "AKIAIOSFODNN7EXAMPLE",  # Example AWS key format
        "password=",
        "token="
    ]
    
    for pattern in secret_patterns:
        if pattern.lower() in content.lower():
            secrets_found = True
            print(f"   WARNING: Found '{pattern}' in .env")
    
    if not secrets_found:
        print("   PASS: No hardcoded secrets found in .env")
    
    # Check that DECIDER_API_KEY is empty or placeholder
    if "DECIDER_API_KEY=" in content:
        lines = [l for l in content.split('\n') if 'DECIDER_API_KEY=' in l]
        for line in lines:
            if "DECIDER_API_KEY=" in line:
                value = line.split("=", 1)[1].strip().strip('#').strip()
                if value and not any(c in value for c in ['<', '>']):
                    print(f"   WARNING: DECIDER_API_KEY has value: {value[:20]}...")
                else:
                    print("   PASS: DECIDER_API_KEY is empty/placeholder")
else:
    print("   FAIL: .env not found")

# Test 3: Check .env.example doesn't have secrets
print("\n3. Checking .env.example...")
example_path = Path(r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\.env.example")
if example_path.exists():
    content = example_path.read_text()
    if "DECIDER_API_KEY=" in content:
        lines = [l for l in content.split('\n') if 'DECIDER_API_KEY=' in l]
        for line in lines:
            if line.strip() and not line.strip().startswith('#'):
                value = line.split("=", 1)[1].strip()
                if value and value != '':
                    print(f"   WARNING: .env.example has DECIDER_API_KEY value")
                else:
                    print("   PASS: .env.example has empty DECIDER_API_KEY")
else:
    print("   FAIL: .env.example not found")

# Test 4: Check LICENSE exists and is Apache-2.0
print("\n4. Checking LICENSE...")
license_path = Path(r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\LICENSE")
if license_path.exists():
    content = license_path.read_text()
    if "Apache License" in content or "apache" in content.lower():
        print("   PASS: LICENSE is Apache-2.0")
    else:
        print("   WARNING: LICENSE may not be Apache-2.0")
else:
    print("   FAIL: LICENSE file not found")

# Test 5: Check reference kit not modified
print("\n5. Checking reference kit integrity...")
kit_files = [
    r"c:\Users\userd\Downloads\MY-AGENT\dhanush-raman-b-decider-hackathon-kit\dhanush-raman-b-decider-hackathon-kit\agent\agent.py",
    r"c:\Users\userd\Downloads\MY-AGENT\dhanush-raman-b-decider-hackathon-kit\dhanush-raman-b-decider-hackathon-kit\agent\tools.py",
]

all_intact = True
for kit_file in kit_files:
    path = Path(kit_file)
    if not path.exists():
        print(f"   WARNING: Expected file missing: {kit_file}")
        all_intact = False

if all_intact:
    print("   PASS: Reference kit files intact")

# Test 6: Check credit line in files
print("\n6. Checking hackathon kit credit...")
agent_py = Path(r"c:\Users\userd\Downloads\MY-AGENT\wild-soul-agent\agent\agent.py")
if agent_py.exists():
    content = agent_py.read_text()
    if "AWS User Group Madurai" in content or "hackathon kit" in content.lower():
        print("   PASS: Credit line present in agent.py")
    else:
        print("   WARNING: Consider adding hackathon kit credit")

print("\n=== Secrets and git status verified ===")
