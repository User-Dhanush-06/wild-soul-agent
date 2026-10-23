# WILD SOUL Agent - Final README

Autonomous game agent using Strands Decider 2B for tool selection and Amazon Bedrock for narrative responses.

## Key Features
- 5 game tools with clear interfaces
- #tool-selection decision pattern for tool classification
- Confidence-based fallback to safe action
- Session management and conversation history
- HackathonAgent interface for demo UI compatibility

## Installation
pip install strands-agents-sdk boto3

## Configuration
Export environment variables:
- AWS_REGION
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY  
- DECIDER_API_KEY

## Usage
from agent.agent import WildSoulAgent
agent = WildSoulAgent()
response = agent.chat("I see a goblin ahead")

## Built With
- AWS Strands Decider 2B (tool selection)
- Amazon Bedrock (narratives)
- Strands Agents SDK (orchestration)
- AWS User Group Madurai hackathon kit

## License
Apache 2.0
