"""
Utility functions for input validation and data sanitization
"""

import re
import json
from typing import Dict, Any, List, Optional, Union
import jsonschema

class ValidationError(Exception):
    """Custom validation error"""
    pass

class InputValidator:
    """Validates and sanitizes user inputs"""
    
    @staticmethod
    def validate_persona_description(description: str) -> str:
        """Validate and sanitize persona description"""
        if not description or not description.strip():
            raise ValidationError("Persona description cannot be empty")
        
        # Remove potentially harmful content
        description = description.strip()
        
        # Check length limits
        if len(description) > 1000:
            raise ValidationError("Persona description too long (max 1000 characters)")
        
        if len(description) < 10:
            raise ValidationError("Persona description too short (min 10 characters)")
        
        return description
    
    @staticmethod
    def validate_num_personas(num_personas: Union[int, str]) -> int:
        """Validate number of personas"""
        try:
            num = int(num_personas)
        except (ValueError, TypeError):
            raise ValidationError("Number of personas must be a valid integer")
        
        if num < 2:
            raise ValidationError("Minimum 2 personas required")
        
        if num > 10:
            raise ValidationError("Maximum 10 personas allowed")
        
        return num
    
    @staticmethod
    def validate_discussion_topic(topic: str) -> str:
        """Validate discussion topic"""
        if not topic or not topic.strip():
            raise ValidationError("Discussion topic cannot be empty")
        
        topic = topic.strip()
        
        if len(topic) > 500:
            raise ValidationError("Discussion topic too long (max 500 characters)")
        
        if len(topic) < 5:
            raise ValidationError("Discussion topic too short (min 5 characters)")
        
        return topic
    
    @staticmethod
    def validate_duration(duration: Union[int, str]) -> int:
        """Validate discussion duration"""
        try:
            duration_int = int(duration)
        except (ValueError, TypeError):
            raise ValidationError("Duration must be a valid integer")
        
        if duration_int < 15:
            raise ValidationError("Minimum duration is 15 minutes")
        
        if duration_int > 180:
            raise ValidationError("Maximum duration is 180 minutes")
        
        return duration_int
    
    @staticmethod
    def validate_summary_schema(schema: str) -> str:
        """Validate summary schema"""
        if not schema or not schema.strip():
            raise ValidationError("Summary schema cannot be empty")
        
        schema = schema.strip()
        
        if len(schema) > 1000:
            raise ValidationError("Summary schema too long (max 1000 characters)")
        
        return schema
    
    @staticmethod
    def validate_question(question: str) -> str:
        """Validate Q&A question"""
        if not question or not question.strip():
            raise ValidationError("Question cannot be empty")
        
        question = question.strip()
        
        if len(question) > 500:
            raise ValidationError("Question too long (max 500 characters)")
        
        if len(question) < 3:
            raise ValidationError("Question too short (min 3 characters)")
        
        return question
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Basic text sanitization"""
        if not isinstance(text, str):
            return str(text)
        
        # Remove potentially harmful characters
        text = re.sub(r'[<>"\']', '', text)
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text

class OutputValidator:
    """Validates agent outputs"""
    
    @staticmethod
    def validate_persona_output(output: Dict[str, Any]) -> bool:
        """Validate persona generation output"""
        required_fields = ["success", "personas"]
        
        for field in required_fields:
            if field not in output:
                return False
        
        if not output["success"]:
            return "error" in output
        
        personas = output["personas"]
        if not isinstance(personas, list) or len(personas) == 0:
            return False
        
        # Validate each persona
        required_persona_fields = ["name", "age", "occupation"]
        for persona in personas:
            if not isinstance(persona, dict):
                return False
            
            for field in required_persona_fields:
                if field not in persona:
                    return False
        
        return True
    
    @staticmethod
    def validate_schema_output(output: Dict[str, Any]) -> bool:
        """Validate schema generation output"""
        required_fields = ["success", "schema"]
        
        for field in required_fields:
            if field not in output:
                return False
        
        if not output["success"]:
            return "error" in output
        
        schema = output["schema"]
        if not isinstance(schema, dict):
            return False
        
        # Validate schema structure
        if "phases" not in schema or not isinstance(schema["phases"], list):
            return False
        
        # Validate each phase
        required_phase_fields = ["phase_name", "objective", "sample_prompts"]
        for phase in schema["phases"]:
            if not isinstance(phase, dict):
                return False
            
            for field in required_phase_fields:
                if field not in phase:
                    return False
        
        return True
    
    @staticmethod
    def validate_discussion_output(output: Dict[str, Any]) -> bool:
        """Validate focus group discussion output"""
        required_fields = ["success", "transcript", "group_dynamics", "participation_stats"]
        
        for field in required_fields:
            if field not in output:
                return False
        
        if not output["success"]:
            return "error" in output
        
        # Validate transcript
        transcript = output["transcript"]
        if not isinstance(transcript, list):
            return False
        
        # Validate participation stats
        stats = output["participation_stats"]
        if not isinstance(stats, dict):
            return False
        
        return True

class SchemaValidator:
    """JSON schema validation utilities"""
    
    PERSONA_SCHEMA = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "age": {"type": "integer", "minimum": 1, "maximum": 100},
            "occupation": {"type": "string", "minLength": 1},
            "background": {"type": "string"},
            "personality_traits": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["name", "age", "occupation", "background"]
    }
    
    DISCUSSION_PHASE_SCHEMA = {
        "type": "object",
        "properties": {
            "phase_name": {"type": "string", "minLength": 1},
            "duration_minutes": {"type": "integer", "minimum": 1},
            "objective": {"type": "string", "minLength": 1},
            "sample_prompts": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1
            }
        },
        "required": ["phase_name", "objective", "sample_prompts"]
    }
    
    @classmethod
    def validate_persona(cls, persona: Dict[str, Any]) -> bool:
        """Validate single persona against schema"""
        try:
            jsonschema.validate(persona, cls.PERSONA_SCHEMA)
            return True
        except jsonschema.ValidationError:
            return False
    
    @classmethod
    def validate_discussion_phase(cls, phase: Dict[str, Any]) -> bool:
        """Validate discussion phase against schema"""
        try:
            jsonschema.validate(phase, cls.DISCUSSION_PHASE_SCHEMA)
            return True
        except jsonschema.ValidationError:
            return False
    
    @classmethod
    def validate_personas_list(cls, personas: List[Dict[str, Any]]) -> List[str]:
        """Validate list of personas and return errors"""
        errors = []
        
        for i, persona in enumerate(personas):
            if not cls.validate_persona(persona):
                errors.append(f"Persona {i+1} ({persona.get('name', 'Unknown')}) has invalid structure")
        
        return errors