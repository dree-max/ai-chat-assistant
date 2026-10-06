"""
Guardrail layer for the AI chat assistant.

When a prompt is blocked by validation, the assistant should respond with a safe, consistent refusal instead of sending the prompt to the AI model. This prevents the model from being exposed to potentially harmful or malicious input.
"""

from __future__ import annotations

def safe_refusal(reason: str) -> str:
    """Return a safe refusal message for blocked prompts.

    Args:
        reason (str): The reason the prompt was blocked.

    Returns:
        A fixed, user-facing refusal message that does not expose the model to the blocked prompt.
    """
    return (
        "This request cannot be processed due to security concerns. "
        "Please rephrase your message and avoid including any instructions that could compromise the assistant's safety or integrity."
    )

