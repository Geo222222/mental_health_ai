"""
Async client for interacting with the local Ollama server.
"""
from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from typing import AsyncGenerator, Dict

import httpx

from app.core.config import get_settings


class OllamaClient:
    """
    Thin wrapper around the Ollama HTTP API with streaming support.
    """

    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.ollama_base_url.rstrip("/")
        self.model = settings.ollama_model
        self.timeout = settings.ollama_timeout_seconds
        self._client = httpx.AsyncClient(timeout=self.timeout)

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        """
        Generate a single non-streaming response.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
        }
        response = await self._client.post(f"{self.base_url}/api/generate", json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")

    async def stream(self, prompt: str, system_prompt: str = "") -> AsyncIterator[str]:
        """
        Stream tokens from Ollama as they arrive.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": True,
        }
        async with self._client.stream(
            "POST", f"{self.base_url}/api/generate", json=payload
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line:
                    continue
                chunk = httpx.Response(200, text=line).json()
                token = chunk.get("response")
                if token:
                    yield token

    async def close(self) -> None:
        await self._client.aclose()


async def stream_ollama_reply(prompt: str, system_prompt: str = "") -> AsyncGenerator[str, None]:
    """
    Convenience generator for FastAPI streaming responses.
    """
    client = OllamaClient()
    try:
        async for token in client.stream(prompt, system_prompt):
            yield token
            await asyncio.sleep(0)  # let event loop breathe
    finally:
        await client.close()


