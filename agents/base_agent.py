from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import json
import logging
from datetime import datetime
from openai import OpenAI
from config import Config

class BaseAgent(ABC):
    """Base class for all specialized agents in the workflow"""
    
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.logger = logging.getLogger(f"Agent.{name}")
        self.conversation_history = []
        
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def call_llm(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Make LLM call with error handling"""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            result = response.choices[0].message.content
            self.add_to_history("user", prompt)
            self.add_to_history("assistant", result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"LLM call failed: {e}")
            raise
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return structured output"""
        pass
    
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate agent output format"""
        return isinstance(output, dict)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "name": self.name,
            "role": self.role,
            "conversation_length": len(self.conversation_history),
            "last_activity": self.conversation_history[-1]["timestamp"] if self.conversation_history else None
        }