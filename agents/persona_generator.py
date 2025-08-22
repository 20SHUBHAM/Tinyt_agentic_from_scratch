from typing import Dict, Any, List
import json
from .base_agent import BaseAgent

class PersonaGeneratorAgent(BaseAgent):
    """Agent responsible for generating dynamic personas based on user descriptions"""
    
    def __init__(self):
        system_prompt = """You are an expert persona generation agent. Your role is to create detailed, 
        realistic personas based on user descriptions. You understand cultural nuances, economic contexts, 
        and psychological profiles.
        
        Key principles:
        1. Create diverse, authentic personas that feel real
        2. Include specific demographic and psychographic details
        3. Ensure personas have distinct voices and perspectives
        4. Consider economic constraints and cultural context
        5. Make personas relatable and engaging for discussions
        
        Always output valid JSON with the exact schema requested."""
        
        super().__init__("PersonaGenerator", "Persona Creation Specialist", system_prompt)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personas based on user description"""
        
        user_description = input_data.get("persona_description", "")
        num_personas = input_data.get("num_personas", 5)
        context = input_data.get("context", "general discussion")
        
        prompt = f"""
        Based on this description: "{user_description}"
        
        Create {num_personas} distinct personas for a {context}.
        
        Requirements:
        1. Each persona should be unique and authentic
        2. Include specific details about background, income, lifestyle
        3. Ensure diversity in perspectives and experiences
        4. Make them suitable for meaningful group discussions
        5. Include personality traits that will create natural dynamics
        
        Return ONLY a valid JSON object with this exact structure:
        {{
            "personas": [
                {{
                    "name": "string",
                    "age": "integer",
                    "gender": "string",
                    "occupation": "string",
                    "location": "string",
                    "income_level": "string",
                    "background": "string",
                    "personality_traits": ["array of traits"],
                    "communication_style": "string",
                    "motivations": ["array of motivations"],
                    "concerns": ["array of concerns"],
                    "backstory": "string"
                }}
            ],
            "group_dynamics_prediction": "string describing expected interactions"
        }}
        """
        
        try:
            response = self.call_llm(prompt, temperature=0.8)
            
            # Clean response to ensure valid JSON
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            result = json.loads(response)
            
            # Validate structure
            if "personas" not in result or not isinstance(result["personas"], list):
                raise ValueError("Invalid persona structure")
            
            return {
                "success": True,
                "personas": result["personas"],
                "group_dynamics_prediction": result.get("group_dynamics_prediction", ""),
                "metadata": {
                    "generated_count": len(result["personas"]),
                    "source_description": user_description,
                    "context": context
                }
            }
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parsing error: {e}")
            return {
                "success": False,
                "error": "Failed to generate valid persona JSON",
                "raw_response": response
            }
        except Exception as e:
            self.logger.error(f"Persona generation error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def refine_personas(self, personas: List[Dict], user_feedback: str) -> Dict[str, Any]:
        """Refine personas based on user feedback"""
        
        prompt = f"""
        Here are the current personas:
        {json.dumps(personas, indent=2)}
        
        User feedback: "{user_feedback}"
        
        Refine these personas based on the feedback. Maintain the same JSON structure
        and ensure all personas remain distinct and authentic.
        
        Return the updated personas in the same JSON format.
        """
        
        try:
            response = self.call_llm(prompt, temperature=0.7)
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            result = json.loads(response)
            
            return {
                "success": True,
                "personas": result.get("personas", personas),
                "refinement_applied": True
            }
            
        except Exception as e:
            self.logger.error(f"Persona refinement error: {e}")
            return {
                "success": False,
                "error": str(e),
                "personas": personas  # Return original on error
            }