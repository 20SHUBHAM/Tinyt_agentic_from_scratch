#!/usr/bin/env python3
"""
Python API Client for Agentic AI Focus Group Workflow
Programmatic access to the workflow for integration with other systems
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

class AgenticWorkflowClient:
    """Python client for the Agentic AI Focus Group Workflow API"""
    
    def __init__(self, base_url: str = "http://localhost:5000", timeout: int = 300):
        """
        Initialize the API client
        
        Args:
            base_url: Base URL of the workflow API
            timeout: Request timeout in seconds (increased for AI operations)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.current_session_id = None
        
    def _make_request(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make API request with error handling"""
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            if data is not None:
                response = self.session.post(url, json=data, timeout=self.timeout)
            else:
                response = self.session.get(url, timeout=self.timeout)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timeout"}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Connection error"}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": f"HTTP error: {e}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def start_session(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Start a new workflow session"""
        
        result = self._make_request('/api/start-session', config or {})
        
        if result.get("success"):
            self.current_session_id = result.get("session_id")
        
        return result
    
    def generate_personas(self, persona_description: str, num_personas: int = 5, context: str = "focus group") -> Dict[str, Any]:
        """Generate dynamic personas"""
        
        data = {
            "persona_description": persona_description,
            "num_personas": num_personas,
            "context": context
        }
        
        return self._make_request('/api/generate-personas', data)
    
    def refine_personas(self, feedback: str) -> Dict[str, Any]:
        """Refine personas based on feedback"""
        
        data = {"feedback": feedback}
        return self._make_request('/api/refine-personas', data)
    
    def generate_discussion_schema(self, topic: str, discussion_type: str = "focus group", duration_minutes: int = 60) -> Dict[str, Any]:
        """Generate discussion framework"""
        
        data = {
            "topic": topic,
            "discussion_type": discussion_type,
            "duration_minutes": duration_minutes
        }
        
        return self._make_request('/api/generate-schema', data)
    
    def customize_schema(self, modifications: str) -> Dict[str, Any]:
        """Customize discussion schema"""
        
        data = {"modifications": modifications}
        return self._make_request('/api/customize-schema', data)
    
    def run_focus_group(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute focus group discussion"""
        
        return self._make_request('/api/run-focus-group', config or {})
    
    def generate_summary(self, summary_schema: str, format_type: str = "custom") -> Dict[str, Any]:
        """Generate custom summary"""
        
        data = {
            "summary_schema": summary_schema,
            "format_type": format_type
        }
        
        return self._make_request('/api/generate-summary', data)
    
    def ask_question(self, question: str, context: str = "general") -> Dict[str, Any]:
        """Ask question about discussion results"""
        
        data = {
            "question": question,
            "context": context
        }
        
        return self._make_request('/api/ask-question', data)
    
    def get_suggested_questions(self) -> Dict[str, Any]:
        """Get AI-suggested questions"""
        
        return self._make_request('/api/suggested-questions')
    
    def get_session_status(self) -> Dict[str, Any]:
        """Get current session status"""
        
        return self._make_request('/api/session-status')
    
    def export_session(self, format_type: str = "json") -> Dict[str, Any]:
        """Export session data"""
        
        data = {"format": format_type}
        return self._make_request('/api/export-session', data)
    
    def reset_session(self) -> Dict[str, Any]:
        """Reset current session"""
        
        result = self._make_request('/api/reset-session')
        if result.get("success"):
            self.current_session_id = None
        return result
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        
        return self._make_request('/health')
    
    def run_complete_workflow(self, 
                            persona_description: str,
                            topic: str,
                            num_personas: int = 5,
                            duration_minutes: int = 60,
                            summary_schema: str = "Executive Summary, Key Insights, Recommendations, Verbatim Quotes",
                            context: str = "focus group") -> Dict[str, Any]:
        """Run complete workflow with single method call"""
        
        workflow_results = {
            "started_at": datetime.now().isoformat(),
            "steps": {},
            "success": False
        }
        
        try:
            # Step 1: Start session
            session_result = self.start_session({"complete_workflow": True})
            if not session_result.get("success"):
                workflow_results["error"] = f"Session start failed: {session_result.get('error')}"
                return workflow_results
            
            workflow_results["session_id"] = session_result["session_id"]
            
            # Step 2: Generate personas
            persona_result = self.generate_personas(persona_description, num_personas, context)
            workflow_results["steps"]["personas"] = persona_result
            
            if not persona_result.get("success"):
                workflow_results["error"] = f"Persona generation failed: {persona_result.get('error')}"
                return workflow_results
            
            # Step 3: Generate schema
            schema_result = self.generate_discussion_schema(topic, "focus group", duration_minutes)
            workflow_results["steps"]["schema"] = schema_result
            
            if not schema_result.get("success"):
                workflow_results["error"] = f"Schema generation failed: {schema_result.get('error')}"
                return workflow_results
            
            # Step 4: Run focus group
            discussion_result = self.run_focus_group()
            workflow_results["steps"]["discussion"] = discussion_result
            
            if not discussion_result.get("success"):
                workflow_results["error"] = f"Discussion failed: {discussion_result.get('error')}"
                return workflow_results
            
            # Step 5: Generate summary
            summary_result = self.generate_summary(summary_schema)
            workflow_results["steps"]["summary"] = summary_result
            
            if not summary_result.get("success"):
                workflow_results["error"] = f"Summary generation failed: {summary_result.get('error')}"
                return workflow_results
            
            # Success!
            workflow_results["success"] = True
            workflow_results["completed_at"] = datetime.now().isoformat()
            
            return workflow_results
            
        except Exception as e:
            workflow_results["error"] = f"Workflow execution error: {e}"
            return workflow_results

# Example usage functions
def example_tech_product_research():
    """Example: Tech product user research"""
    
    client = AgenticWorkflowClient()
    
    result = client.run_complete_workflow(
        persona_description="Young professionals in Bangalore who use fintech apps and mobile banking",
        topic="User experience challenges and improvement suggestions for digital banking platforms",
        num_personas=6,
        duration_minutes=50,
        summary_schema="Executive Summary, UX Pain Points, Feature Requests, User Segments, Implementation Priority, Supporting Quotes"
    )
    
    return result

def example_market_research():
    """Example: Market research for new product"""
    
    client = AgenticWorkflowClient()
    
    result = client.run_complete_workflow(
        persona_description="Small business owners in tier-2 Indian cities with 10-50 employees",
        topic="Digital transformation challenges and technology adoption barriers",
        num_personas=5,
        duration_minutes=60,
        summary_schema="Market Insights, Adoption Barriers, Technology Preferences, Budget Considerations, Opportunity Areas, Action Items"
    )
    
    return result

def example_step_by_step():
    """Example: Step-by-step workflow execution with customization"""
    
    client = AgenticWorkflowClient()
    
    print("🚀 Step-by-step workflow example")
    
    # Start session
    session = client.start_session({"example": "step_by_step"})
    print(f"✅ Session: {session.get('session_id')}")
    
    # Generate personas
    personas = client.generate_personas(
        "College students interested in sustainable fashion",
        num_personas=4
    )
    print(f"✅ Personas: {len(personas.get('personas', []))} generated")
    
    # Generate schema
    schema = client.generate_discussion_schema(
        "Sustainable fashion adoption: barriers and motivations",
        duration_minutes=45
    )
    print(f"✅ Schema: {len(schema.get('schema', {}).get('phases', []))} phases")
    
    # Run discussion
    discussion = client.run_focus_group()
    print(f"✅ Discussion: {len(discussion.get('transcript', []))} transcript entries")
    
    # Generate summary
    summary = client.generate_summary(
        "Key Themes, Sustainability Drivers, Price Sensitivity, Brand Preferences, Recommendations"
    )
    print(f"✅ Summary: Generated")
    
    # Interactive Q&A
    qa1 = client.ask_question("What were the main barriers to sustainable fashion adoption?")
    print(f"✅ Q&A 1: {qa1.get('success')}")
    
    qa2 = client.ask_question("Which participant was most price-sensitive?")
    print(f"✅ Q&A 2: {qa2.get('success')}")
    
    # Export results
    export = client.export_session()
    print(f"✅ Export: {export.get('success')}")
    
    return {
        "session": session,
        "personas": personas,
        "schema": schema,
        "discussion": discussion,
        "summary": summary,
        "qa_examples": [qa1, qa2],
        "export": export
    }

if __name__ == "__main__":
    print("🤖 Agentic AI Workflow - API Client Examples")
    print("=" * 50)
    
    print("\nChoose an example:")
    print("1. Tech Product Research")
    print("2. Market Research") 
    print("3. Step-by-step Workflow")
    print("4. Health Check")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            print("\n🔍 Running Tech Product Research Example...")
            result = example_tech_product_research()
            print(f"Result: {result.get('success', False)}")
            
        elif choice == "2":
            print("\n📊 Running Market Research Example...")
            result = example_market_research()
            print(f"Result: {result.get('success', False)}")
            
        elif choice == "3":
            print("\n👣 Running Step-by-step Example...")
            result = example_step_by_step()
            print("All steps completed!")
            
        elif choice == "4":
            print("\n🏥 Running Health Check...")
            client = AgenticWorkflowClient()
            health = client.health_check()
            print(f"API Health: {health.get('status', 'unknown')}")
            
        else:
            print("Invalid choice")
            
    except KeyboardInterrupt:
        print("\n👋 Example interrupted")
    except Exception as e:
        print(f"❌ Example error: {e}")
        print("Make sure the workflow server is running: python main.py")