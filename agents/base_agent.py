from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    def __init__(self, llm_client: Any) -> None:
        self.llm = llm_client

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:  # pragma: no cover - interface
        raise NotImplementedError


class LLMClient:
    """Minimal OpenAI-compatible client; supports base_url, api_key, model.

    The concrete transport is injected to ease testing and vendor swaps.
    """

    def __init__(self, api_key: str, base_url: str, model: str, transport: Any) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.transport = transport

    async def complete(self, system_prompt: str, user_prompt: str, **opts: Any) -> str:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": opts.get("temperature", 0.7),
        }
        return await self.transport.chat_completions(self.base_url, self.api_key, payload)

