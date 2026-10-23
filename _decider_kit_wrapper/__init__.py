"""Wrapper to import from reference kit's decider_kit.

This module allows wild-soul-agent to use the reference hackathon kit's
decider_kit without duplicating code.
"""

import sys
from pathlib import Path

# Add reference kit to Python path if not already there
kit_path = Path(__file__).parent.parent.parent / "dhanush-raman-b-decider-hackathon-kit" / "dhanush-raman-b-decider-hackathon-kit"
kit_path_str = str(kit_path.resolve())

# Only add if it's not already there (to avoid circular imports)
if kit_path_str not in sys.path:
    sys.path.insert(0, kit_path_str)

# Import from the reference kit (this must be done AFTER sys.path is updated)
# We use __import__ to avoid circular import issues
_kit_decider_kit = __import__('decider_kit', fromlist=['Decider', 'DeciderError', 'Decision'])

Decider = _kit_decider_kit.Decider
DeciderError = _kit_decider_kit.DeciderError
Decision = _kit_decider_kit.Decision

# Also expose commonly used utilities
_kit_llm = __import__('decider_kit.llm', fromlist=['agent_model', 'default_model_id', 'strip_thinking'])
agent_model = _kit_llm.agent_model
default_model_id = _kit_llm.default_model_id
strip_thinking = _kit_llm.strip_thinking

__all__ = ["Decider", "DeciderError", "Decision", "agent_model", "default_model_id", "strip_thinking"]
