from typing import Dict, Any, List
import json
from .base_agent import BaseAgent

class ContextSchemaGenerator(BaseAgent):
    """Agent responsible for generating dynamic discussion schemas and frameworks"""
    
    def __init__(self):
        system_prompt = """You are an expert discussion framework designer. Your role is to create 
        structured, engaging discussion schemas that facilitate meaningful group conversations.
        
        Key principles:
        1. Create natural conversation flows that feel organic
        2. Design phases that build upon each other logically
        3. Include prompts that encourage authentic sharing
        4. Consider group dynamics and participation patterns
        5. Ensure discussions yield actionable insights
        
        Always output valid JSON with clear, actionable discussion structures."""
        
        super().__init__("ContextSchemaGenerator", "Discussion Framework Specialist", system_prompt)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate discussion schema based on topic and context"""
        
        topic = input_data.get("topic", "")
        discussion_type = input_data.get("discussion_type", "focus group")
        duration_minutes = input_data.get("duration_minutes", 60)
        num_participants = input_data.get("num_participants", 5)
        
        prompt = f"""
        Create a dynamic discussion schema for: "{topic}"
        
        Context:
        - Discussion type: {discussion_type}
        - Duration: {duration_minutes} minutes
        - Participants: {num_participants} people
        
        Requirements:
        1. Create 4-6 discussion phases that flow naturally
        2. Each phase should have clear objectives and sample prompts
        3. Include timing estimates for each phase
        4. Design prompts that encourage authentic, detailed responses
        5. Consider natural conversation dynamics and group interaction
        6. Include moderator guidance for managing the discussion
        
        Return ONLY a valid JSON object with this exact structure:
        {{
            "discussion_schema": {{
                "topic": "string",
                "total_duration_minutes": "integer",
                "phases": [
                    {{
                        "phase_name": "string",
                        "duration_minutes": "integer",
                        "objective": "string",
                        "moderator_guidance": "string",
                        "sample_prompts": ["array of prompts"],
                        "expected_outcomes": ["array of outcomes"],
                        "transition_cues": ["array of natural transitions"]
                    }}
                ],
                "group_dynamic_considerations": {{
                    "ice_breakers": ["array of ice breakers"],
                    "energy_boosters": ["array of energy boosters"],
                    "conflict_resolution": ["array of techniques"],
                    "participation_encouragers": ["array of techniques"]
                }},
                "success_metrics": ["array of success indicators"]
            }}
        }}
        """
        
        try:
            response = self.call_llm(prompt, temperature=0.8)
            
            # Clean response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            result = json.loads(response)
            
            # Validate structure
            if "discussion_schema" not in result:
                raise ValueError("Invalid schema structure")
            
            schema = result["discussion_schema"]
            if "phases" not in schema or not isinstance(schema["phases"], list):
                raise ValueError("Invalid phases structure")
            
            return {
                "success": True,
                "schema": schema,
                "metadata": {
                    "topic": topic,
                    "phases_count": len(schema["phases"]),
                    "total_duration": schema.get("total_duration_minutes", duration_minutes)
                }
            }
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parsing error: {e}")
            return {
                "success": False,
                "error": "Failed to generate valid schema JSON",
                "raw_response": response
            }
        except Exception as e:
            self.logger.error(f"Schema generation error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def customize_schema(self, schema: Dict, user_modifications: str) -> Dict[str, Any]:
        """Customize schema based on user feedback"""
        
        prompt = f"""
        Current discussion schema:
        {json.dumps(schema, indent=2)}
        
        User modifications requested: "{user_modifications}"
        
        Update the schema based on the user's modifications while maintaining the same JSON structure.
        Ensure the discussion flow remains logical and engaging.
        
        Return the updated schema in the same JSON format.
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
                "schema": result.get("discussion_schema", result),
                "modifications_applied": True
            }
            
        except Exception as e:
            self.logger.error(f"Schema customization error: {e}")
            return {
                "success": False,
                "error": str(e),
                "schema": schema  # Return original on error
            }