"""Prompt validation layer for the AI chat assistant lab.

Checks user input for known prompt-injection patterns before the message
is ever sent to the AI model.
"""

from __future__ import annotations


# Known prompt-injection / jailbreak phrases. Matched against lowercased input.
BLOCKED_PATTERNS: list[str] = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "forget your rules",
    "reveal your system prompt",
    "print your system prompt",
    "show your system prompt",
    "hidden instructions",
    "developer message",
    "developer mode",
    "system instructions",
    "system prompt",
    "unrestricted assistant",
    "bypass rules",
    "disable safety",
    "jailbreak",
]

BLOCKED_MESSAGE = "This request looks like a prompt injection attempt and was blocked."


def validate_prompt(user_input: str) -> tuple[bool, str]:
    """Validate a user prompt against known injection patterns.

    Returns:
        (False, BLOCKED_MESSAGE) if a blocked pattern is found.
        (True, "") if the prompt is allowed.
    """
    lowered = user_input.lower()

    for pattern in BLOCKED_PATTERNS:
        if pattern in lowered:
            return False, BLOCKED_MESSAGE

    return True, ""
