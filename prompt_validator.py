""""
Prompt validation logic for the AI Chat Assistant

Checks user input for known prompt injection patterns before the message is ever sent to the AI model
"""

from __future__ import annotations

# Known prompt injection / jailbreak phrases. Matched ah=gainst lowercase input.

BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "ignore previous directions",   
    "forget your rules",
    "forget your instructions",
    "reveal your system prompt",
    "show your system prompt",
    "hidden instructions",
    "developer mindeset",
    "developer mode",
    "system instructions",
    "system prompt",
    "unrestricted assistant",
    "bypass rules",
    "disable safety",
    "jailbreak",
]

BLOCKED_MESSAGE = "This request contains a prompt injection attempt and cannot be processed. Please rephrase your message."

def validate_prompt(user_input: str) -> tuple[bool, str]:
    """Validate user input for known prompt injection patterns.

    Args:
        user_input (str): The user's input message.

        Returns:
        (False, BLOCKED_MESSAGE) if a blocked pattern is found, otherwise (True, user_input).
    """
    lowered = user_input.lower()

    for pattern in BLOCKED_PATTERNS:
        if pattern in lowered:
            return False, BLOCKED_MESSAGE

    return True, user_input
