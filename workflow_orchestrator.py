from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime
from agents.persona_generator import PersonaGeneratorAgent
from agents.context_schema_generator import ContextSchemaGenerator
from agents.dynamic_focus_group import DynamicFocusGroupAgent
from agents.summary_agent import SummaryAgent
from agents.qa_assistant import QAAssistantAgent
from config import Config

class WorkflowOrchestrator:
    """Main orchestrator for the agentic AI workflow"""
    
    def __init__(self):
        # Validate configuration
        Config.validate()
        
        # Initialize all agents
        self.persona_agent = PersonaGeneratorAgent()
        self.schema_agent = ContextSchemaGenerator()
        self.focus_group_agent = DynamicFocusGroupAgent()
        self.summary_agent = SummaryAgent()
        self.qa_agent = QAAssistantAgent()
        
        # Workflow state
        self.current_session = None
        self.session_data = {}
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("WorkflowOrchestrator")
        
    def start_new_session(self, session_config: Optional[Dict[str, Any]] = None) -> str:
        """Start a new workflow session"""
        
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.current_session = session_id
        
        self.session_data = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "config": session_config or {},
            "stages": {},
            "current_stage": "persona_creation",
            "status": "active"
        }
        
        self.logger.info(f"Started new session: {session_id}")
        return session_id
    
    def step1_generate_personas(self, persona_description: str, num_personas: int = 5, context: str = "focus group") -> Dict[str, Any]:
        """Step 1: Generate personas based on user description"""
        
        if not self.current_session:
            return {"success": False, "error": "No active session. Start a new session first."}
        
        self.logger.info("Step 1: Generating personas")
        
        input_data = {
            "persona_description": persona_description,
            "num_personas": num_personas,
            "context": context
        }
        
        result = self.persona_agent.process(input_data)
        
        if result["success"]:
            self.session_data["stages"]["persona_creation"] = {
                "completed_at": datetime.now().isoformat(),
                "input": input_data,
                "output": result,
                "status": "completed"
            }
            self.session_data["current_stage"] = "schema_creation"
        
        return result
    
    def step1_refine_personas(self, user_feedback: str) -> Dict[str, Any]:
        """Refine personas based on user feedback"""
        
        if "persona_creation" not in self.session_data.get("stages", {}):
            return {"success": False, "error": "No personas to refine. Generate personas first."}
        
        current_personas = self.session_data["stages"]["persona_creation"]["output"]["personas"]
        result = self.persona_agent.refine_personas(current_personas, user_feedback)
        
        if result["success"]:
            # Update session data with refined personas
            self.session_data["stages"]["persona_creation"]["output"]["personas"] = result["personas"]
            self.session_data["stages"]["persona_creation"]["refined_at"] = datetime.now().isoformat()
        
        return result
    
    def step2_generate_discussion_schema(self, topic: str, discussion_type: str = "focus group", duration_minutes: int = 60) -> Dict[str, Any]:
        """Step 2: Generate discussion schema and framework"""
        
        if not self.current_session:
            return {"success": False, "error": "No active session. Start a new session first."}
        
        self.logger.info("Step 2: Generating discussion schema")
        
        # Get number of personas from previous step
        num_participants = 5
        if "persona_creation" in self.session_data.get("stages", {}):
            personas = self.session_data["stages"]["persona_creation"]["output"].get("personas", [])
            num_participants = len(personas)
        
        input_data = {
            "topic": topic,
            "discussion_type": discussion_type,
            "duration_minutes": duration_minutes,
            "num_participants": num_participants
        }
        
        result = self.schema_agent.process(input_data)
        
        if result["success"]:
            self.session_data["stages"]["schema_creation"] = {
                "completed_at": datetime.now().isoformat(),
                "input": input_data,
                "output": result,
                "status": "completed"
            }
            self.session_data["current_stage"] = "discussion_execution"
        
        return result
    
    def step2_customize_schema(self, user_modifications: str) -> Dict[str, Any]:
        """Customize discussion schema based on user feedback"""
        
        if "schema_creation" not in self.session_data.get("stages", {}):
            return {"success": False, "error": "No schema to customize. Generate schema first."}
        
        current_schema = self.session_data["stages"]["schema_creation"]["output"]["schema"]
        result = self.schema_agent.customize_schema(current_schema, user_modifications)
        
        if result["success"]:
            # Update session data with customized schema
            self.session_data["stages"]["schema_creation"]["output"]["schema"] = result["schema"]
            self.session_data["stages"]["schema_creation"]["customized_at"] = datetime.now().isoformat()
        
        return result
    
    def step3_run_focus_group(self, additional_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Step 3: Execute the dynamic focus group discussion"""
        
        if not self.current_session:
            return {"success": False, "error": "No active session."}
        
        # Validate prerequisites
        stages = self.session_data.get("stages", {})
        if "persona_creation" not in stages or "schema_creation" not in stages:
            return {"success": False, "error": "Complete persona creation and schema creation first."}
        
        self.logger.info("Step 3: Running focus group discussion")
        
        # Prepare input data
        personas = stages["persona_creation"]["output"]["personas"]
        discussion_schema = stages["schema_creation"]["output"]["schema"]
        
        input_data = {
            "personas": personas,
            "discussion_schema": discussion_schema,
            "session_config": additional_config or {}
        }
        
        result = self.focus_group_agent.process(input_data)
        
        if result["success"]:
            self.session_data["stages"]["discussion_execution"] = {
                "completed_at": datetime.now().isoformat(),
                "input": input_data,
                "output": result,
                "status": "completed"
            }
            self.session_data["current_stage"] = "summary_generation"
            
            # Load data into QA agent for interactive queries
            self.qa_agent.load_discussion_data(result)
        
        return result
    
    def step4_generate_summary(self, summary_schema: str, format_type: str = "custom") -> Dict[str, Any]:
        """Step 4: Generate custom summary based on user schema"""
        
        if "discussion_execution" not in self.session_data.get("stages", {}):
            return {"success": False, "error": "No discussion results to summarize. Run focus group first."}
        
        self.logger.info("Step 4: Generating summary")
        
        discussion_results = self.session_data["stages"]["discussion_execution"]["output"]
        
        input_data = {
            "transcript": discussion_results.get("transcript", []),
            "group_dynamics": discussion_results.get("group_dynamics", []),
            "summary_schema": summary_schema,
            "additional_context": {
                "session_id": self.current_session,
                "participants": [p["name"] for p in self.session_data["stages"]["persona_creation"]["output"]["personas"]],
                "topic": self.session_data["stages"]["schema_creation"]["input"]["topic"]
            }
        }
        
        result = self.summary_agent.process(input_data)
        
        if result["success"]:
            self.session_data["stages"]["summary_generation"] = {
                "completed_at": datetime.now().isoformat(),
                "input": input_data,
                "output": result,
                "status": "completed"
            }
            self.session_data["current_stage"] = "interactive_qa"
        
        return result
    
    def step5_ask_question(self, question: str, context: str = "general") -> Dict[str, Any]:
        """Step 5: Ask questions about the discussion results"""
        
        if "discussion_execution" not in self.session_data.get("stages", {}):
            return {"success": False, "error": "No discussion results available for Q&A."}
        
        self.logger.info(f"Step 5: Processing question - {question}")
        
        input_data = {
            "question": question,
            "context": context
        }
        
        result = self.qa_agent.process(input_data)
        
        # Store Q&A in session data
        if "interactive_qa" not in self.session_data["stages"]:
            self.session_data["stages"]["interactive_qa"] = {
                "questions": [],
                "status": "active"
            }
        
        self.session_data["stages"]["interactive_qa"]["questions"].append({
            "question": question,
            "answer": result,
            "timestamp": datetime.now().isoformat()
        })
        
        return result
    
    def get_suggested_questions(self) -> Dict[str, Any]:
        """Get AI-suggested questions based on discussion results"""
        
        if "discussion_execution" not in self.session_data.get("stages", {}):
            return {"success": False, "error": "No discussion results available."}
        
        discussion_results = self.session_data["stages"]["discussion_execution"]["output"]
        return self.qa_agent.suggest_questions(discussion_results)
    
    def get_session_status(self) -> Dict[str, Any]:
        """Get current session status and progress"""
        
        if not self.current_session:
            return {"session_active": False}
        
        return {
            "session_active": True,
            "session_id": self.current_session,
            "current_stage": self.session_data.get("current_stage", "not_started"),
            "completed_stages": list(self.session_data.get("stages", {}).keys()),
            "session_data": self.session_data,
            "agent_status": {
                "persona_generator": self.persona_agent.get_status(),
                "schema_generator": self.schema_agent.get_status(),
                "focus_group": self.focus_group_agent.get_status(),
                "summary_agent": self.summary_agent.get_status(),
                "qa_assistant": self.qa_agent.get_status()
            }
        }
    
    def export_session_data(self, format: str = "json") -> Dict[str, Any]:
        """Export complete session data"""
        
        if not self.current_session:
            return {"success": False, "error": "No active session to export."}
        
        export_data = {
            "metadata": {
                "session_id": self.current_session,
                "exported_at": datetime.now().isoformat(),
                "format": format
            },
            "session_data": self.session_data
        }
        
        if format == "json":
            filename = f"session_export_{self.current_session}.json"
            try:
                with open(filename, 'w') as f:
                    json.dump(export_data, f, indent=2)
                
                return {
                    "success": True,
                    "filename": filename,
                    "data": export_data
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Export failed: {e}",
                    "data": export_data
                }
        
        return {"success": True, "data": export_data}
    
    def reset_session(self):
        """Reset current session"""
        self.current_session = None
        self.session_data = {}
        self.logger.info("Session reset")