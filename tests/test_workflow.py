#!/usr/bin/env python3
"""
Test suite for the Agentic AI Focus Group Workflow
"""

import unittest
import sys
import os
import json
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow_orchestrator import WorkflowOrchestrator
from agents.persona_generator import PersonaGeneratorAgent
from agents.context_schema_generator import ContextSchemaGenerator

class TestWorkflowOrchestrator(unittest.TestCase):
    """Test the main workflow orchestrator"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock the Config.validate method to avoid requiring real API keys
        with patch('config.Config.validate', return_value=True):
            with patch('config.Config.OPENAI_API_KEY', 'test-key'):
                self.orchestrator = WorkflowOrchestrator()
    
    def test_session_management(self):
        """Test session creation and management"""
        # Test session creation
        session_id = self.orchestrator.start_new_session()
        self.assertIsNotNone(session_id)
        self.assertIsNotNone(self.orchestrator.current_session)
        
        # Test session status
        status = self.orchestrator.get_session_status()
        self.assertTrue(status["session_active"])
        self.assertEqual(status["session_id"], session_id)
        
        # Test session reset
        self.orchestrator.reset_session()
        reset_status = self.orchestrator.get_session_status()
        self.assertFalse(reset_status["session_active"])

class TestPersonaGenerator(unittest.TestCase):
    """Test persona generation agent"""
    
    def setUp(self):
        """Set up test environment"""
        with patch('config.Config.OPENAI_API_KEY', 'test-key'):
            self.agent = PersonaGeneratorAgent()
    
    @patch('agents.persona_generator.PersonaGeneratorAgent.call_llm')
    def test_persona_generation_structure(self, mock_llm):
        """Test persona generation output structure"""
        # Mock LLM response
        mock_response = json.dumps({
            "personas": [
                {
                    "name": "Test Person",
                    "age": 25,
                    "occupation": "Software Developer",
                    "background": "Test background"
                }
            ],
            "group_dynamics_prediction": "Test prediction"
        })
        mock_llm.return_value = mock_response
        
        # Test input
        input_data = {
            "persona_description": "Test description",
            "num_personas": 1,
            "context": "test"
        }
        
        result = self.agent.process(input_data)
        
        # Verify structure
        self.assertTrue(result["success"])
        self.assertIn("personas", result)
        self.assertIsInstance(result["personas"], list)
        self.assertEqual(len(result["personas"]), 1)

class TestContextSchemaGenerator(unittest.TestCase):
    """Test discussion schema generation agent"""
    
    def setUp(self):
        """Set up test environment"""
        with patch('config.Config.OPENAI_API_KEY', 'test-key'):
            self.agent = ContextSchemaGenerator()
    
    @patch('agents.context_schema_generator.ContextSchemaGenerator.call_llm')
    def test_schema_generation_structure(self, mock_llm):
        """Test schema generation output structure"""
        # Mock LLM response
        mock_response = json.dumps({
            "discussion_schema": {
                "topic": "Test Topic",
                "total_duration_minutes": 60,
                "phases": [
                    {
                        "phase_name": "Opening",
                        "duration_minutes": 15,
                        "objective": "Test objective",
                        "sample_prompts": ["Test prompt"]
                    }
                ]
            }
        })
        mock_llm.return_value = mock_response
        
        # Test input
        input_data = {
            "topic": "Test topic",
            "duration_minutes": 60,
            "num_participants": 5
        }
        
        result = self.agent.process(input_data)
        
        # Verify structure
        self.assertTrue(result["success"])
        self.assertIn("schema", result)
        self.assertIn("phases", result["schema"])
        self.assertIsInstance(result["schema"]["phases"], list)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow"""
    
    def setUp(self):
        """Set up integration test environment"""
        with patch('config.Config.validate', return_value=True):
            with patch('config.Config.OPENAI_API_KEY', 'test-key'):
                self.orchestrator = WorkflowOrchestrator()
    
    def test_workflow_state_progression(self):
        """Test that workflow progresses through states correctly"""
        # Start session
        session_id = self.orchestrator.start_new_session()
        
        # Check initial state
        status = self.orchestrator.get_session_status()
        self.assertEqual(status["current_stage"], "persona_creation")
        
        # Mock persona generation
        with patch.object(self.orchestrator.persona_agent, 'process') as mock_persona:
            mock_persona.return_value = {
                "success": True,
                "personas": [{"name": "Test", "age": 25}]
            }
            
            result = self.orchestrator.step1_generate_personas("test description")
            self.assertTrue(result["success"])
            
            # Check state progression
            status = self.orchestrator.get_session_status()
            self.assertEqual(status["current_stage"], "schema_creation")
            self.assertIn("persona_creation", status["completed_stages"])

def run_tests():
    """Run all tests"""
    print("🧪 Running Agentic AI Workflow Tests")
    print("=" * 40)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestWorkflowOrchestrator))
    suite.addTest(unittest.makeSuite(TestPersonaGenerator))
    suite.addTest(unittest.makeSuite(TestContextSchemaGenerator))
    suite.addTest(unittest.makeSuite(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return True
    else:
        print(f"\n❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)