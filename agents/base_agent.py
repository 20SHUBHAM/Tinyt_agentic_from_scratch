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
        
        # Check if we're in mock mode
        if Config.is_mock_mode():
            return self._get_mock_response(prompt)
        
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
    
    def _get_mock_response(self, prompt: str) -> str:
        """Generate mock response for testing without API calls"""
        
        # Mock responses based on agent type
        if "PersonaGenerator" in self.name:
            return '''
            {
                "personas": [
                    {
                        "name": "Alex Chen",
                        "age": 28,
                        "gender": "Non-binary",
                        "occupation": "Software Developer",
                        "background": "Tech-savvy millennial with strong environmental values",
                        "personality_traits": ["analytical", "environmentally conscious", "collaborative"],
                        "motivations": ["sustainability", "innovation", "work-life balance"],
                        "economic_status": "middle-class",
                        "location": "San Francisco, CA"
                    },
                    {
                        "name": "Maria Rodriguez",
                        "age": 34,
                        "gender": "Female", 
                        "occupation": "Marketing Manager",
                        "background": "Business professional focused on consumer trends",
                        "personality_traits": ["creative", "data-driven", "social"],
                        "motivations": ["career growth", "family security", "community impact"],
                        "economic_status": "upper-middle-class",
                        "location": "Austin, TX"
                    }
                ],
                "group_dynamics_prediction": "This group will likely have engaging discussions with Alex bringing technical insights and Maria contributing market perspectives. Both are professionally minded and will create productive dialogue."
            }
            '''
        elif "ContextSchema" in self.name:
            return '''
            {
                "topic": "Product Feedback Discussion",
                "total_duration_minutes": 60,
                "phases": [
                    {
                        "phase_name": "Introduction & Warm-up",
                        "duration_minutes": 10,
                        "objective": "Get participants comfortable and establish rapport",
                        "sample_prompts": ["Tell us about yourself", "What brings you here today?"],
                        "moderator_guidance": "Keep energy light and welcoming"
                    },
                    {
                        "phase_name": "Core Discussion",
                        "duration_minutes": 40,
                        "objective": "Deep dive into the main topic",
                        "sample_prompts": ["What are your thoughts on...", "How does this impact you?"],
                        "moderator_guidance": "Encourage detailed responses and follow-up questions"
                    },
                    {
                        "phase_name": "Wrap-up & Next Steps",
                        "duration_minutes": 10,
                        "objective": "Summarize insights and gather final thoughts",
                        "sample_prompts": ["Any final thoughts?", "What would you like to see happen next?"],
                        "moderator_guidance": "Synthesize key themes and thank participants"
                    }
                ]
            }
            '''
        elif "Summary" in self.name:
            return '''
            # Focus Group Summary
            
            ## Key Insights
            - Participants showed strong interest in sustainability features
            - Price sensitivity was a major concern across demographics
            - User experience expectations are high for mobile interfaces
            
            ## Recommendations
            1. Prioritize eco-friendly product features
            2. Consider tiered pricing models
            3. Invest in mobile-first design approach
            
            ## Next Steps
            - Conduct follow-up survey with larger sample
            - Prototype key features identified
            - Schedule stakeholder review meeting
            '''
        elif "QA" in self.name:
            return '''
            Based on the focus group discussion, here are the key points regarding your question:
            
            The participants generally agreed that user experience is the top priority, with sustainability features being a close second. Price sensitivity varied by demographic, with younger participants more willing to pay premium for eco-friendly options.
            
            This suggests a strategy focused on highlighting both UX excellence and environmental benefits could be most effective.
            '''
        else:
            return '''
            {
                "discussion_transcript": "Mock focus group discussion would appear here with realistic participant interactions and insights.",
                "key_themes": ["user experience", "sustainability", "pricing"],
                "participant_engagement": "High engagement with diverse perspectives shared",
                "notable_quotes": ["This feature would really help my daily workflow", "I care about environmental impact"],
                "moderator_notes": "Group dynamics were positive with good participation from all members"
            }
            '''
    
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