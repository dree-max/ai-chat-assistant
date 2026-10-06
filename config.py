"""Configuration helpers for the ai-chat-assistant lab.

This file keeps environment variables and other configuration settings in one place.
The app defaults to Ollama so it can be run locally without an OpenAI API key. If you want to use OpenAI, add your API key to a .env file in the root of this repo.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).parent
SYSTEM_PROMPT = PROJECT_DIR / "prompts" / "system_prompt.txt"

DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."

@dataclass(frozen=True)
class AppConfig:
    """Configuration settings for the ai-chat-assistant."""

    app_title: str = "ai-chat-assistant"
    provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    openai_model: str = "gpt-3.5-turbo"
    openai_api_key: str = ""
    system_prompt: str = DEFAULT_SYSTEM_PROMPT

def _read_system_prompt() -> str:
    """Read the system prompt from the prompts/system_prompt.txt file."""
    if SYSTEM_PROMPT.exists():
        return SYSTEM_PROMPT.read_text(encoding="utf-8").strip()
    
    return "You are a helpful assistant."    


def load_config() -> AppConfig:
    """Load configuration settings from environment variables and the .env file."""
    load_dotenv(PROJECT_DIR / ".env")  # Load environment variables from .env file if it exists

    provider = os.environ.get("AI_PROVIDER", "ollama").strip().lower()
    if provider not in ("ollama", "openai"):
        raise ValueError(f"Invalid provider: {provider}. Must be 'ollama' or 'openai'.")
    
    return AppConfig(
        app_title=os.getenv("APP_TITLE", "ai-chat-assistant"),
        provider=provider,
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama2"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        system_prompt=_read_system_prompt(),
    )