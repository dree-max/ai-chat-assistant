"""Prompt Filter for the AI chat assistant lab (Section 4, Lecture 5).

This module turns the risk analysis from Lecture 4 into a simple decision:

    low risk    -> allow  (assistant responds normally)
    medium risk -> warn   (assistant still responds, but we show a warning)
    high risk   -> block  (assistant is NOT called; show a safe block message)

It does NOT sanitize prompts, score risk, or call an LLM. It only reads the
risk analysis dictionary and returns a decision, so it is easy to explain.
"""

from __future__ import annotations


# Beginner-friendly messages for each decision. The block message intentionally
# avoids revealing hidden instructions, system/developer prompts, or internals.
WARN_MESSAGE = (
    "This prompt looks potentially risky, but it was allowed for this lab. "
    "In a real system you might add stricter handling here."
)

BLOCK_MESSAGE = (
    "This request was blocked because it appears to ask for protected "
    "instructions or attempts to bypass the assistant's rules. Please rephrase "
    "your request as a safe educational question."
)

ALLOW_MESSAGE = "This prompt looks safe and was allowed."


def filter_prompt(risk_analysis: dict) -> dict:
    """Convert a risk analysis into an allow / warn / block decision.

    Args:
        risk_analysis: The dictionary returned by analyze_prompt_risk(), which
            includes a "risk_level" of "low", "medium", or "high".

    Returns:
        A dictionary with keys:
            decision: "allow", "warn", or "block"
            allowed: True if the assistant may respond, False if blocked
            message: a short, user-facing message for this decision
    """
    # Read the risk level. Default to "low" if it is missing for any reason.
    risk_level = risk_analysis.get("risk_level", "low")

    if risk_level == "high":
        return {
            "decision": "block",
            "allowed": False,
            "message": BLOCK_MESSAGE,
        }

    if risk_level == "medium":
        return {
            "decision": "warn",
            "allowed": True,
            "message": WARN_MESSAGE,
        }

    # Anything else (including "low") is allowed.
    return {
        "decision": "allow",
        "allowed": True,
        "message": ALLOW_MESSAGE,
    }
