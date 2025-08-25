# Agentic Focus Group Workflow

End-to-end agentic focus group pipeline with LLM-powered agents and Flask API.

Project Structure
```text
agentic-focus-group-workflow/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── persona_generator.py
│   ├── context_schema_generator.py
│   ├── dynamic_focus_group.py
│   ├── summary_agent.py
│   └── qa_assistant.py
├── config.py
├── workflow_orchestrator.py
├── web_interface.py
├── main.py
├── requirements.txt
├── .replit
├── replit.nix
├── pyproject.toml
└── README.md
```

Quickstart
1) Create `.env` with:
```env
LLM_API_KEY=your_key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```
2) Install and run
```bash
pip install -r requirements.txt
python main.py
```
3) API endpoints
- POST `/api/personas` body: `{ "description": str, "count": int }`
- POST `/api/framework` body: `{ "topic": str, "goals": str, "duration": int, "phases": str, "personas": [] }`
- POST `/api/simulate` body: `{ "personas": [], "framework": {} }`
- POST `/api/summary` body: `{ "schema": json_string, "transcript": {} }`
- POST `/api/qa` body: `{ "question": str, "transcript": {} }`

Notes
- Agents use an OpenAI-compatible endpoint; swap base URL/model as needed.
- For TinyTroupe-style realism, use the simulation agent and your preferred model.