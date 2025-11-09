"""
Application configuration via Pydantic settings.
"""
from __future__ import annotations

from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Environment-driven configuration for CalmMind.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "CalmMind"
    api_prefix: str = "/api"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"
    ollama_timeout_seconds: float = 60.0

    database_url: str = "sqlite+aiosqlite:///./calmmind.db"
    redis_url: str = "redis://localhost:6379/0"

    risk_keywords: List[str] = [
        "suicide",
        "kill myself",
        "can't go on",
        "hurt myself",
        "ending it",
    ]
    sentiment_threshold: float = -0.4

    allowed_origins: Optional[List[str]] = ["http://localhost:5173", "http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings loader for dependency injection.
    """
    return Settings()


