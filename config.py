from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    api_key: str
    base_url: str
    model: str


def load_settings() -> Settings:
    return Settings(
        api_key=os.getenv("LLM_API_KEY", ""),
        base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
    )

