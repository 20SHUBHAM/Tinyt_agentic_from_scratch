#!/usr/bin/env python3
"""
Example usage of the Agentic AI Focus Group Workflow
This script demonstrates how to use the workflow programmatically
"""

import sys
import os
import json
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from workflow_orchestrator import WorkflowOrchestrator
from config import Config

def run_example_workflow():
    """Run a complete example workflow"""
    
    print("🚀 Starting Example Agentic AI Focus Group Workflow")
    print("=" * 60)
    
    try:
        # Initialize orchestrator
        orchestrator = WorkflowOrchestrator()
        
        # Step 1: Start session and generate personas
        print("\n📝 Step 1: Generating Dynamic Personas")
        print("-" * 40)
        
        session_id = orchestrator.start_new_session({
            "example_run": True,
            "purpose": "Demonstration of agentic workflow"
        })
        print(f"✅ Session started: {session_id}")
        
        persona_result = orchestrator.step1_generate_personas(
            persona_description="Young professionals in Indian metros who are interested in sustainable lifestyle products",
            num_personas=5,
            context="product feedback focus group"
        )
        
        if persona_result["success"]:
            print(f"✅ Generated {len(persona_result['personas'])} personas")
            for i, persona in enumerate(persona_result['personas'][:2], 1):  # Show first 2
                print(f"   {i}. {persona['name']} - {persona['occupation']}")
        else:
            print(f"❌ Persona generation failed: {persona_result['error']}")
            return
        
        # Step 2: Generate discussion schema
        print("\n🗣️ Step 2: Creating Discussion Framework")
        print("-" * 40)
        
        schema_result = orchestrator.step2_generate_discussion_schema(
            topic="Adoption barriers and motivations for sustainable lifestyle products",
            discussion_type="focus group",
            duration_minutes=45
        )
        
        if schema_result["success"]:
            schema = schema_result["schema"]
            print(f"✅ Generated discussion framework with {len(schema['phases'])} phases")
            for phase in schema['phases']:
                print(f"   • {phase['phase_name']} ({phase['duration_minutes']}min)")
        else:
            print(f"❌ Schema generation failed: {schema_result['error']}")
            return
        
        # Step 3: Run focus group discussion
        print("\n🎭 Step 3: Running Focus Group Simulation")
        print("-" * 40)
        print("⏳ This may take a few minutes as AI agents discuss...")
        
        discussion_result = orchestrator.step3_run_focus_group()
        
        if discussion_result["success"]:
            transcript = discussion_result["transcript"]
            print(f"✅ Discussion completed!")
            print(f"   • Transcript entries: {len(transcript)}")
            print(f"   • Participants: {len(discussion_result['participation_stats'])}")
            print(f"   • Spontaneous interactions: {len(discussion_result['spontaneous_moments'])}")
            
            # Show sample transcript entries
            print("\n📝 Sample Discussion Excerpts:")
            for entry in transcript[:3]:
                if entry.get('type') == 'response':
                    content = entry['content'][:100] + "..." if len(entry['content']) > 100 else entry['content']
                    print(f"   {entry['speaker']}: {content}")
        else:
            print(f"❌ Focus group execution failed: {discussion_result['error']}")
            return
        
        # Step 4: Generate custom summary
        print("\n📊 Step 4: Generating Custom Summary")
        print("-" * 40)
        
        summary_result = orchestrator.step4_generate_summary(
            summary_schema="Executive Summary, Key Adoption Barriers, Motivating Factors, Participant Segments, Actionable Recommendations, Supporting Quotes"
        )
        
        if summary_result["success"]:
            print("✅ Custom summary generated")
            print("   Summary follows user-defined schema exactly")
        else:
            print(f"❌ Summary generation failed: {summary_result['error']}")
            return
        
        # Step 5: Interactive Q&A examples
        print("\n❓ Step 5: Interactive Q&A Examples")
        print("-" * 40)
        
        example_questions = [
            "What were the main barriers to adoption mentioned?",
            "Which participant was most enthusiastic about sustainable products?",
            "What price sensitivity patterns emerged?"
        ]
        
        for question in example_questions:
            print(f"\n🤔 Question: {question}")
            qa_result = orchestrator.step5_ask_question(question)
            
            if qa_result["success"]:
                answer = qa_result["answer"][:200] + "..." if len(qa_result["answer"]) > 200 else qa_result["answer"]
                print(f"💡 Answer: {answer}")
            else:
                print(f"❌ Q&A failed: {qa_result['error']}")
        
        # Get suggested questions
        print("\n🎯 AI-Suggested Questions:")
        suggested = orchestrator.get_suggested_questions()
        if suggested["success"]:
            for i, q in enumerate(suggested["suggested_questions"][:3], 1):
                print(f"   {i}. {q}")
        
        # Export session data
        print("\n💾 Exporting Session Data")
        print("-" * 40)
        
        export_result = orchestrator.export_session_data()
        if export_result["success"]:
            print(f"✅ Session exported to: {export_result['filename']}")
        
        # Final status
        print("\n🎉 Example Workflow Completed Successfully!")
        print("=" * 60)
        
        status = orchestrator.get_session_status()
        print(f"Session ID: {status['session_id']}")
        print(f"Completed Stages: {', '.join(status['completed_stages'])}")
        print(f"Current Stage: {status['current_stage']}")
        
    except Exception as e:
        print(f"❌ Example workflow failed: {e}")
        return False
    
    return True

def run_api_example():
    """Example of using the workflow via API calls"""
    
    print("\n🌐 API Usage Example")
    print("-" * 30)
    print("For API usage, start the web server and make HTTP requests:")
    print()
    print("1. POST /api/start-session")
    print("2. POST /api/generate-personas")
    print("3. POST /api/generate-schema") 
    print("4. POST /api/run-focus-group")
    print("5. POST /api/generate-summary")
    print("6. POST /api/ask-question")
    print()
    print("See web_interface.py for detailed API documentation.")

if __name__ == "__main__":
    print("🎯 Agentic AI Focus Group Workflow - Example Usage")
    print("Choose an option:")
    print("1. Run complete workflow example")
    print("2. Show API usage example")
    
    try:
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            success = run_example_workflow()
            if success:
                print("\n✨ Example completed! Check the generated files and try the web interface.")
            else:
                print("\n⚠️  Example failed. Check your configuration and try again.")
        
        elif choice == "2":
            run_api_example()
        
        else:
            print("Invalid choice. Please run again and select 1 or 2.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Example interrupted by user.")
    except Exception as e:
        print(f"\n❌ Example error: {e}")
        print("Make sure you have:")
        print("1. Set OPENAI_API_KEY in your .env file")
        print("2. Installed all dependencies: pip install -r requirements.txt")
        print("3. Valid OpenAI API credits")