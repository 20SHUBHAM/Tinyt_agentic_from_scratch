from __future__ import annotations

import asyncio
from typing import Any, Dict

from flask import Flask, jsonify, request, send_from_directory

from agents.base_agent import LLMClient
from agents import (
    PersonaGeneratorAgent,
    ContextSchemaGenerator,
    DynamicFocusGroupAgent,
    SummaryAgent,
    QAAssistantAgent,
)
from config import load_settings
from workflow_orchestrator import WorkflowOrchestrator


class HttpTransport:
    async def chat_completions(self, base_url: str, api_key: str, payload: Dict[str, Any]) -> str:
        import aiohttp

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{base_url}/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
                json=payload,
                timeout=120,
            ) as resp:
                text = await resp.text()
                if resp.status >= 400:
                    raise RuntimeError(f"LLM error {resp.status}: {text}")
                data = await resp.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")


def create_app() -> Flask:
    settings = load_settings()
    llm = LLMClient(settings.api_key, settings.base_url, settings.model, HttpTransport())
    orchestrator = WorkflowOrchestrator(
        persona_agent=PersonaGeneratorAgent(llm),
        framework_agent=ContextSchemaGenerator(llm),
        sim_agent=DynamicFocusGroupAgent(llm),
        summary_agent=SummaryAgent(llm),
        qa_agent=QAAssistantAgent(llm),
    )

    app = Flask(__name__, static_folder="static", static_url_path="/static")

    @app.post("/api/personas")
    def personas():
        data = request.get_json(force=True)
        description = data.get("description", "")
        count = int(data.get("count", 5))
        result = asyncio.run(orchestrator.generate_personas(description, count))
        return jsonify(result)

    @app.post("/api/framework")
    def framework():
        data = request.get_json(force=True)
        topic = data.get("topic", "")
        goals = data.get("goals", "")
        duration = int(data.get("duration", 30))
        phases = data.get("phases", "")
        personas = data.get("personas", [])
        result = asyncio.run(orchestrator.generate_framework(topic, goals, duration, phases, personas))
        return jsonify(result)

    @app.post("/api/simulate")
    def simulate():
        data = request.get_json(force=True)
        personas = data.get("personas", [])
        framework = data.get("framework", {})
        result = asyncio.run(orchestrator.simulate(personas, framework))
        return jsonify(result)

    @app.post("/api/summary")
    def summary():
        data = request.get_json(force=True)
        schema = data.get("schema", "{}")
        transcript = data.get("transcript", {})
        result = asyncio.run(orchestrator.summarize(schema, transcript))
        return jsonify(result)

    @app.post("/api/qa")
    def qa():
        data = request.get_json(force=True)
        question = data.get("question", "")
        transcript = data.get("transcript", {})
        result = asyncio.run(orchestrator.ask(question, transcript))
        return jsonify(result)

    @app.get("/")
    def index() -> Any:
        return send_from_directory(app.static_folder, "index.html")

    @app.get("/health")
    def health() -> Any:
        return {"status": "ok"}

    return app

