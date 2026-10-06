""" Provider layer for the ai-chat-assistant,

The streamlit app calls one function: get_assistant_response.
This file decides whether to use Ollama or OpenAI based on the environment variable LLM_PROVIDER.

"""

from __future__ import annotations

from typing import Literal

import requests
from openai import OpenAI

from config import AppConfig

ProviderName = Literal["ollama", "openai"]

class LLMServiceError(RuntimeError):
    """Raised when the selected model provider fails to return a response."""


def _format_messages(system_prompt:str, chat_history:list[dict[str, str]], user_message:str) -> list[dict[str, str]]:
    """Builds the messages list for the LLM API call, including system prompt, chat history, and user message."""

    return [
        {"role": "system", "content": system_prompt},
        *chat_history,
        {"role": "user", "content": user_message},
    ]

def _call_ollama(config: AppConfig, chat_history: list[dict[str, str]], user_message: str) -> str:
    """Call the local ollama chat endpoint."""

    url = f"{config.ollama_base_url}/api/chat"
    payload = {
        "model": config.ollama_model,
        "messages": _format_messages(config.system_prompt, chat_history, user_message),
        "stream": False,
    }

    try: 
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise LLMServiceError(
            "Could not reach Ollama. Make sure Ollama is running and the model is pulled."
            f"Try: ollama pull {config.ollama_model} " 
            
        ) from exc

    data = response.json()
    message = data.get("message", {})
    content = message.get("content", "").strip()

    if not content:
        raise LLMServiceError("Ollama returned an empty response.")

    return content


def _call_openai(config: AppConfig, chat_history: list[dict[str, str]], user_message: str) -> str:
    """Call OpenAI using the official OpenAI Python SDK."""

    if not config.openai_api_key:
        raise LLMServiceError(
            "OpenAI is selected but the API key is not set. Add it to your .env file."
        )
    client = OpenAI(api_key=config.openai_api_key)

    try:
        response = client.chat.completions.create(
            model=config.openai_model,
            messages=_format_messages(config.system_prompt, chat_history, user_message),
            temperature=0.3,

        )
    except Exception as exc: #OpenAI raises serveral typed errors; keep lab begineer friendly,
        raise LLMServiceError(
            f"OpenAI request failed: {exc}"
        ) from exc

    content = response.choices[0].message.content

    if not content:
        raise LLMServiceError("OpenAI returned an empty response.")

    return content.strip()


def get_assistant_response(
        provider: ProviderName, config: AppConfig, chat_history: list[dict[str, str]], user_message: str) -> str:
    """Return the assistant's response based on the selected provider and chat history."""
    if provider == "openai":
        return _call_openai(config, chat_history, user_message)

    return _call_ollama(config, chat_history, user_message)