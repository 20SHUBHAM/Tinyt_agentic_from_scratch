from __future__ import annotations

from typing import Any, Dict

from .base_agent import BaseAgent


class ContextSchemaGenerator(BaseAgent):
    async def run(self, topic: str, goals: str, duration_minutes: int, phases_csv: str, personas: list[dict]) -> Dict[str, Any]:
        system = (
            "Design a focus group framework with phases, prompts, timings, and moderator cues."
            " Output strict JSON: { phases: [{ name, minutes, prompts:[], moderatorCues:[] }], guidelines: [] }"
        )
        user = (
            f"Topic: {topic}\nGoals: {goals}\nDurationMinutes: {duration_minutes}\n"
            f"Phases: {phases_csv}\nParticipants: {personas}"
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
        first, last = text.find("{"), text.rfind("}")
        if first != -1 and last != -1 and last > first:
            return json.loads(text[first : last + 1])
        raise ValueError("Agent did not return valid JSON object")

