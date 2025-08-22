"""
Agentic AI Workflow Agents

This package contains specialized agents for the dynamic focus group workflow:
- PersonaGeneratorAgent: Creates dynamic personas from user descriptions
- ContextSchemaGenerator: Generates discussion frameworks and schemas
- DynamicFocusGroupAgent: Orchestrates TinyTroupe-based discussions
- SummaryAgent: Creates custom summaries based on user schemas
- QAAssistantAgent: Provides interactive Q&A over discussion results
"""

from .base_agent import BaseAgent
from .persona_generator import PersonaGeneratorAgent
from .context_schema_generator import ContextSchemaGenerator
from .dynamic_focus_group import DynamicFocusGroupAgent
from .summary_agent import SummaryAgent
from .qa_assistant import QAAssistantAgent

__all__ = [
    'BaseAgent',
    'PersonaGeneratorAgent', 
    'ContextSchemaGenerator',
    'DynamicFocusGroupAgent',
    'SummaryAgent',
    'QAAssistantAgent'
]