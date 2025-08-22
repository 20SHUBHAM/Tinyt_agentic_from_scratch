#!/usr/bin/env python3
"""
Command Line Interface for Agentic AI Focus Group Workflow
Advanced interface for power users and automation
"""

import argparse
import sys
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from workflow_orchestrator import WorkflowOrchestrator
from config import Config
from utils.validators import InputValidator, ValidationError

class CLIInterface:
    """Command line interface for the workflow"""
    
    def __init__(self):
        self.orchestrator = WorkflowOrchestrator()
        self.current_session = None
    
    def run_complete_workflow(self, args) -> bool:
        """Run complete workflow from command line arguments"""
        
        try:
            print("🚀 Starting Complete Agentic AI Workflow")
            print("=" * 50)
            
            # Validate inputs
            persona_desc = InputValidator.validate_persona_description(args.persona_description)
            num_personas = InputValidator.validate_num_personas(args.num_personas)
            topic = InputValidator.validate_discussion_topic(args.topic)
            duration = InputValidator.validate_duration(args.duration)
            
            # Step 1: Start session and generate personas
            print(f"\n📝 Step 1: Generating {num_personas} personas...")
            session_id = self.orchestrator.start_new_session({
                "cli_run": True,
                "args": vars(args)
            })
            self.current_session = session_id
            
            persona_result = self.orchestrator.step1_generate_personas(
                persona_description=persona_desc,
                num_personas=num_personas,
                context=args.context
            )
            
            if not persona_result["success"]:
                print(f"❌ Persona generation failed: {persona_result['error']}")
                return False
            
            print(f"✅ Generated {len(persona_result['personas'])} personas")
            if args.verbose:
                for persona in persona_result['personas']:
                    print(f"   • {persona['name']} - {persona['occupation']}")
            
            # Step 2: Generate discussion schema
            print(f"\n🗣️ Step 2: Creating discussion framework for '{topic}'...")
            schema_result = self.orchestrator.step2_generate_discussion_schema(
                topic=topic,
                discussion_type=args.discussion_type,
                duration_minutes=duration
            )
            
            if not schema_result["success"]:
                print(f"❌ Schema generation failed: {schema_result['error']}")
                return False
            
            schema = schema_result["schema"]
            print(f"✅ Generated framework with {len(schema['phases'])} phases")
            if args.verbose:
                for phase in schema['phases']:
                    print(f"   • {phase['phase_name']} ({phase.get('duration_minutes', 'N/A')}min)")
            
            # Step 3: Run focus group
            print(f"\n🎭 Step 3: Running focus group simulation...")
            print("⏳ This may take several minutes...")
            
            discussion_result = self.orchestrator.step3_run_focus_group()
            
            if not discussion_result["success"]:
                print(f"❌ Discussion failed: {discussion_result['error']}")
                return False
            
            transcript = discussion_result["transcript"]
            print(f"✅ Discussion completed!")
            print(f"   • Transcript entries: {len(transcript)}")
            print(f"   • Participants: {len(discussion_result['participation_stats'])}")
            print(f"   • Spontaneous interactions: {len(discussion_result['spontaneous_moments'])}")
            
            # Step 4: Generate summary
            print(f"\n📊 Step 4: Generating summary...")
            summary_result = self.orchestrator.step4_generate_summary(
                summary_schema=args.summary_schema
            )
            
            if not summary_result["success"]:
                print(f"❌ Summary generation failed: {summary_result['error']}")
                return False
            
            print("✅ Custom summary generated")
            
            # Export results
            print(f"\n💾 Exporting results...")
            export_result = self.orchestrator.export_session_data()
            
            if export_result["success"]:
                print(f"✅ Results exported to: {export_result['filename']}")
                
                # Also save summary separately if requested
                if args.output_file:
                    with open(args.output_file, 'w') as f:
                        json.dump({
                            "summary": summary_result["summary"],
                            "metadata": {
                                "session_id": session_id,
                                "topic": topic,
                                "participants": len(persona_result['personas']),
                                "generated_at": datetime.now().isoformat()
                            }
                        }, f, indent=2)
                    print(f"✅ Summary saved to: {args.output_file}")
            
            print(f"\n🎉 Workflow completed successfully!")
            print(f"Session ID: {session_id}")
            
            return True
            
        except ValidationError as e:
            print(f"❌ Validation error: {e}")
            return False
        except Exception as e:
            print(f"❌ Workflow error: {e}")
            return False
    
    def run_interactive_qa(self, args) -> bool:
        """Run interactive Q&A session"""
        
        if not args.session_file:
            print("❌ Session file required for Q&A mode")
            return False
        
        try:
            # Load session data
            with open(args.session_file, 'r') as f:
                session_data = json.load(f)
            
            # Load discussion results into QA agent
            if "session_data" in session_data and "stages" in session_data["session_data"]:
                stages = session_data["session_data"]["stages"]
                if "discussion_execution" in stages:
                    discussion_results = stages["discussion_execution"]["output"]
                    self.orchestrator.qa_agent.load_discussion_data(discussion_results)
                    print("✅ Session data loaded for Q&A")
                else:
                    print("❌ No discussion results found in session file")
                    return False
            else:
                print("❌ Invalid session file format")
                return False
            
            # Interactive Q&A loop
            print("\n❓ Interactive Q&A Mode")
            print("Type your questions (or 'quit' to exit)")
            print("-" * 40)
            
            while True:
                try:
                    question = input("\n🤔 Your question: ").strip()
                    
                    if question.lower() in ['quit', 'exit', 'q']:
                        break
                    
                    if not question:
                        continue
                    
                    # Validate question
                    question = InputValidator.validate_question(question)
                    
                    # Get answer
                    qa_result = self.orchestrator.step5_ask_question(question)
                    
                    if qa_result["success"]:
                        print(f"\n💡 Answer: {qa_result['answer']}")
                        
                        if qa_result.get("supporting_quotes") and args.verbose:
                            print("\n📝 Supporting quotes:")
                            for quote in qa_result["supporting_quotes"][:3]:
                                print(f"   • {quote['speaker']}: {quote['quote'][:100]}...")
                    else:
                        print(f"❌ Error: {qa_result['error']}")
                
                except ValidationError as e:
                    print(f"❌ Invalid question: {e}")
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"❌ Error processing question: {e}")
            
            print("\n👋 Q&A session ended")
            return True
            
        except FileNotFoundError:
            print(f"❌ Session file not found: {args.session_file}")
            return False
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in session file: {args.session_file}")
            return False
        except Exception as e:
            print(f"❌ Q&A session error: {e}")
            return False

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    
    parser = argparse.ArgumentParser(
        description="Agentic AI Focus Group Workflow - CLI Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete workflow
  python cli_interface.py workflow \\
    --persona-description "Young professionals interested in fintech" \\
    --topic "Digital banking adoption challenges" \\
    --num-personas 5 \\
    --duration 60

  # Interactive Q&A with existing session
  python cli_interface.py qa --session-file session_export_20240101_120000.json

  # Generate only personas
  python cli_interface.py personas \\
    --persona-description "College students in tier-2 cities" \\
    --num-personas 6
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Complete workflow command
    workflow_parser = subparsers.add_parser('workflow', help='Run complete workflow')
    workflow_parser.add_argument(
        '--persona-description', 
        required=True,
        help='Description of desired participants'
    )
    workflow_parser.add_argument(
        '--topic',
        required=True, 
        help='Discussion topic'
    )
    workflow_parser.add_argument(
        '--num-personas',
        type=int,
        default=5,
        help='Number of personas to generate (2-10)'
    )
    workflow_parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='Discussion duration in minutes (15-180)'
    )
    workflow_parser.add_argument(
        '--context',
        default='focus group',
        help='Discussion context type'
    )
    workflow_parser.add_argument(
        '--discussion-type',
        default='focus group',
        help='Type of discussion'
    )
    workflow_parser.add_argument(
        '--summary-schema',
        default='Executive Summary, Key Insights, Recommendations, Verbatim Quotes',
        help='Custom summary schema'
    )
    workflow_parser.add_argument(
        '--output-file',
        help='Output file for summary (JSON format)'
    )
    workflow_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    # Personas only command
    personas_parser = subparsers.add_parser('personas', help='Generate personas only')
    personas_parser.add_argument(
        '--persona-description',
        required=True,
        help='Description of desired participants'
    )
    personas_parser.add_argument(
        '--num-personas',
        type=int,
        default=5,
        help='Number of personas to generate'
    )
    personas_parser.add_argument(
        '--output-file',
        help='Output file for personas (JSON format)'
    )
    personas_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    # Q&A command
    qa_parser = subparsers.add_parser('qa', help='Interactive Q&A with existing session')
    qa_parser.add_argument(
        '--session-file',
        required=True,
        help='Session export file to analyze'
    )
    qa_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show supporting quotes and details'
    )
    
    # Schema generation command
    schema_parser = subparsers.add_parser('schema', help='Generate discussion schema only')
    schema_parser.add_argument(
        '--topic',
        required=True,
        help='Discussion topic'
    )
    schema_parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='Discussion duration in minutes'
    )
    schema_parser.add_argument(
        '--num-participants',
        type=int,
        default=5,
        help='Number of participants'
    )
    schema_parser.add_argument(
        '--output-file',
        help='Output file for schema (JSON format)'
    )
    
    return parser

def main():
    """Main CLI entry point"""
    
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please check your .env file and ensure OPENAI_API_KEY is set")
        sys.exit(1)
    
    cli = CLIInterface()
    
    try:
        if args.command == 'workflow':
            success = cli.run_complete_workflow(args)
            
        elif args.command == 'personas':
            print("📝 Generating personas...")
            session_id = cli.orchestrator.start_new_session({"cli_personas_only": True})
            
            result = cli.orchestrator.step1_generate_personas(
                persona_description=args.persona_description,
                num_personas=args.num_personas,
                context="general"
            )
            
            if result["success"]:
                print(f"✅ Generated {len(result['personas'])} personas")
                
                if args.output_file:
                    with open(args.output_file, 'w') as f:
                        json.dump(result, f, indent=2)
                    print(f"💾 Saved to: {args.output_file}")
                
                if args.verbose:
                    for persona in result['personas']:
                        print(f"\n👤 {persona['name']}")
                        print(f"   Age: {persona['age']}")
                        print(f"   Occupation: {persona['occupation']}")
                        print(f"   Background: {persona['background'][:100]}...")
                
                success = True
            else:
                print(f"❌ Failed: {result['error']}")
                success = False
                
        elif args.command == 'schema':
            print("🗣️ Generating discussion schema...")
            session_id = cli.orchestrator.start_new_session({"cli_schema_only": True})
            
            result = cli.orchestrator.step2_generate_discussion_schema(
                topic=args.topic,
                duration_minutes=args.duration
            )
            
            if result["success"]:
                schema = result["schema"]
                print(f"✅ Generated schema with {len(schema['phases'])} phases")
                
                if args.output_file:
                    with open(args.output_file, 'w') as f:
                        json.dump(result, f, indent=2)
                    print(f"💾 Saved to: {args.output_file}")
                
                for phase in schema['phases']:
                    print(f"   • {phase['phase_name']}: {phase['objective']}")
                
                success = True
            else:
                print(f"❌ Failed: {result['error']}")
                success = False
                
        elif args.command == 'qa':
            success = cli.run_interactive_qa(args)
            
        else:
            print(f"❌ Unknown command: {args.command}")
            success = False
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n👋 Operation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ CLI error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()