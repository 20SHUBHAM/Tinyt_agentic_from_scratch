from __future__ import annotations

from typing import Any, List

from .base_agent import BaseAgent


class PersonaGeneratorAgent(BaseAgent):
    async def run(self, description: str, count: int) -> List[dict[str, Any]]:
        system = (
            "You create diverse, realistic personas with distinct backgrounds, motivations,"
            " constraints, and personalities. Output a strict JSON array."
        )
        user = (
            f"Description: {description}\nCount: {count}\n"
            "Return fields: id (uuid), name, age, occupation, background, motivations[],"
            " constraints[], personality."
        )
        content = await self.llm.complete(system, user)
        return _safe_json(content)


def _safe_json(text: str):
    import json, re

    try:
        return json.loads(text)
    except Exception:
        fence = re.search(r"```[a-zA-Z]*\n([\s\S]*?)```", text)
        if fence:
            try:
                return json.loads(fence.group(1))
            except Exception:
                pass
        first, last = text.find("["), text.rfind("]")
        if first != -1 and last != -1 and last > first:
            return json.loads(text[first : last + 1])
        first, last = text.find("{"), text.rfind("}")
        if first != -1 and last != -1 and last > first:
            return json.loads(text[first : last + 1])
        raise ValueError("Agent did not return valid JSON array")

