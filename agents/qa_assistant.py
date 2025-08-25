from __future__ import annotations

from typing import Any, Dict

from .base_agent import BaseAgent


class QAAssistantAgent(BaseAgent):
    async def run(self, question: str, transcript: dict[str, Any]) -> Dict[str, Any]:
        system = (
            "Answer questions about the transcript with evidence quotes."
            " Output JSON: { answer, quotes: [{speaker, quote}], confidence: 0-1 }"
        )
        user = f"Question: {question}\nTranscript: {transcript}"
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

