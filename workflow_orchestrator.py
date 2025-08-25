from __future__ import annotations

from typing import Any, Dict, List

from agents import (
    BaseAgent,
    PersonaGeneratorAgent,
    ContextSchemaGenerator,
    DynamicFocusGroupAgent,
    SummaryAgent,
    QAAssistantAgent,
)


class WorkflowOrchestrator:
    def __init__(
        self,
        persona_agent: PersonaGeneratorAgent,
        framework_agent: ContextSchemaGenerator,
        sim_agent: DynamicFocusGroupAgent,
        summary_agent: SummaryAgent,
        qa_agent: QAAssistantAgent,
    ) -> None:
        self.persona_agent = persona_agent
        self.framework_agent = framework_agent
        self.sim_agent = sim_agent
        self.summary_agent = summary_agent
        self.qa_agent = qa_agent

    async def generate_personas(self, description: str, count: int) -> List[dict]:
        return await self.persona_agent.run(description, count)

    async def generate_framework(self, topic: str, goals: str, duration_minutes: int, phases_csv: str, personas: List[dict]) -> Dict[str, Any]:
        return await self.framework_agent.run(topic, goals, duration_minutes, phases_csv, personas)

    async def simulate(self, personas: List[dict], framework: Dict[str, Any]) -> Dict[str, Any]:
        return await self.sim_agent.run(personas, framework)

    async def summarize(self, schema_json: str, transcript: Dict[str, Any]) -> Dict[str, Any]:
        return await self.summary_agent.run(schema_json, transcript)

    async def ask(self, question: str, transcript: Dict[str, Any]) -> Dict[str, Any]:
        return await self.qa_agent.run(question, transcript)

