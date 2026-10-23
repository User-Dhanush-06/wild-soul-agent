"""WILD SOUL Agent - autonomous game player using Strands Decider 2B for tool selection.

Built with the AWS User Group Madurai Strands Decider hackathon kit.
"""

# Only export tools to avoid import-time Strands SDK dependency
from .tools import TOOLS

__all__ = ["TOOLS"]
