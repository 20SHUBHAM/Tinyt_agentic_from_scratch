#!/usr/bin/env python3
"""
Demonstration scenarios for the Agentic AI Focus Group Workflow
Showcases different use cases and capabilities
"""

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_client import AgenticWorkflowClient

class DemoScenarios:
    """Collection of demonstration scenarios"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.client = AgenticWorkflowClient(base_url)
    
    def scenario_1_fintech_ux_research(self):
        """Scenario 1: FinTech UX Research"""
        
        print("🏦 Scenario 1: FinTech UX Research")
        print("=" * 40)
        print("Use Case: Understanding user pain points in digital banking apps")
        print("Target: Product managers, UX designers, developers")
        
        return self.client.run_complete_workflow(
            persona_description="""Young working professionals in Indian metros (age 22-32) who actively use 
            digital banking, UPI payments, and fintech apps. Mix of tech-savvy early adopters and cautious 
            traditional users. Include different income levels and banking preferences.""",
            
            topic="""User experience challenges, frustrations, and improvement suggestions for digital 
            banking platforms and fintech apps. Focus on daily usage scenarios, pain points, 
            and feature requests.""",
            
            num_personas=6,
            duration_minutes=55,
            
            summary_schema="""Executive Summary, Critical UX Pain Points, Most Requested Features, 
            User Behavior Patterns, Security Concerns, Mobile vs Desktop Preferences, 
            Implementation Priority Matrix, Verbatim User Quotes, Actionable Recommendations"""
        )
    
    def scenario_2_ecommerce_market_research(self):
        """Scenario 2: E-commerce Market Research"""
        
        print("🛒 Scenario 2: E-commerce Market Research")
        print("=" * 40)
        print("Use Case: Understanding shopping behavior for new marketplace entry")
        print("Target: Business strategists, marketing teams, investors")
        
        return self.client.run_complete_workflow(
            persona_description="""Small to medium business owners and individual sellers across 
            tier-1 and tier-2 Indian cities. Include both experienced online sellers and traditional 
            retailers considering digital transition. Mix of product categories.""",
            
            topic="""E-commerce platform preferences, selling challenges, commission structures, 
            marketing support needs, and factors influencing platform choice for online selling.""",
            
            num_personas=5,
            duration_minutes=50,
            
            summary_schema="""Market Landscape Overview, Platform Switching Drivers, Commission Sensitivity, 
            Marketing Support Requirements, Technology Adoption Barriers, Seller Segment Profiles, 
            Competitive Advantages Sought, Business Impact Priorities, Strategic Recommendations"""
        )
    
    def scenario_3_edtech_product_validation(self):
        """Scenario 3: EdTech Product Validation"""
        
        print("📚 Scenario 3: EdTech Product Validation")
        print("=" * 40)
        print("Use Case: Validating new online learning platform concept")
        print("Target: EdTech entrepreneurs, investors, product teams")
        
        return self.client.run_complete_workflow(
            persona_description="""College students and young professionals (age 18-28) from various 
            educational backgrounds pursuing skill development. Include engineering students, 
            commerce graduates, arts students, and working professionals seeking upskilling.""",
            
            topic="""Online learning preferences, course selection criteria, pricing sensitivity, 
            certification value, and factors that influence completion rates in digital education.""",
            
            num_personas=6,
            duration_minutes=60,
            
            summary_schema="""Learning Behavior Insights, Price Sensitivity Analysis, Content Format Preferences, 
            Certification Importance, Completion Motivators, Platform Feature Priorities, 
            Marketing Message Resonance, Competitive Positioning, Product Development Roadmap"""
        )
    
    def scenario_4_healthcare_app_feedback(self):
        """Scenario 4: Healthcare App User Feedback"""
        
        print("🏥 Scenario 4: Healthcare App User Feedback")
        print("=" * 40)
        print("Use Case: Gathering feedback on telemedicine and health tracking apps")
        print("Target: Healthcare startups, digital health teams, investors")
        
        return self.client.run_complete_workflow(
            persona_description="""Urban residents aged 25-45 with varying health awareness levels. 
            Include busy professionals, parents, elderly care providers, and health-conscious individuals. 
            Mix of tech comfort levels and healthcare engagement patterns.""",
            
            topic="""Telemedicine adoption barriers, health app usage patterns, privacy concerns, 
            doctor consultation preferences, and features that would increase engagement 
            with digital health platforms.""",
            
            num_personas=5,
            duration_minutes=45,
            
            summary_schema="""Digital Health Adoption Patterns, Privacy and Trust Factors, 
            Consultation Preferences, App Feature Priorities, Engagement Barriers, 
            Age-based Usage Differences, Healthcare Decision Influencers, 
            Technology Comfort Levels, Actionable Product Improvements"""
        )
    
    def scenario_5_sustainability_consumer_insights(self):
        """Scenario 5: Sustainability Consumer Insights"""
        
        print("🌱 Scenario 5: Sustainability Consumer Insights")
        print("=" * 40)
        print("Use Case: Understanding consumer attitudes toward sustainable products")
        print("Target: FMCG brands, sustainability consultants, marketing agencies")
        
        return self.client.run_complete_workflow(
            persona_description="""Urban consumers across age groups (22-45) with varying levels of 
            environmental consciousness. Include budget-conscious families, premium product users, 
            millennials, Gen Z, and traditional shoppers from different economic backgrounds.""",
            
            topic="""Sustainable product adoption motivations, price premium tolerance, 
            greenwashing concerns, brand trust factors, and behavior change triggers 
            for eco-friendly purchasing decisions.""",
            
            num_personas=7,
            duration_minutes=65,
            
            summary_schema="""Sustainability Motivation Spectrum, Price Premium Thresholds, 
            Trust and Authenticity Factors, Behavior Change Triggers, Demographic Differences, 
            Brand Communication Preferences, Purchase Decision Influencers, 
            Greenwashing Detection Patterns, Marketing Strategy Recommendations"""
        )

def run_demo_scenarios():
    """Run all demonstration scenarios"""
    
    print("🎭 Agentic AI Focus Group Workflow - Demo Scenarios")
    print("=" * 60)
    print("These scenarios demonstrate real-world applications of the workflow")
    print()
    
    scenarios = DemoScenarios()
    
    available_scenarios = [
        ("FinTech UX Research", scenarios.scenario_1_fintech_ux_research),
        ("E-commerce Market Research", scenarios.scenario_2_ecommerce_market_research),
        ("EdTech Product Validation", scenarios.scenario_3_edtech_product_validation),
        ("Healthcare App Feedback", scenarios.scenario_4_healthcare_app_feedback),
        ("Sustainability Consumer Insights", scenarios.scenario_5_sustainability_consumer_insights)
    ]
    
    print("Available scenarios:")
    for i, (name, _) in enumerate(available_scenarios, 1):
        print(f"{i}. {name}")
    
    print("0. Run all scenarios")
    
    try:
        choice = input("\nSelect scenario (0-5): ").strip()
        
        if choice == "0":
            # Run all scenarios
            results = {}
            for name, scenario_func in available_scenarios:
                print(f"\n🚀 Running: {name}")
                try:
                    result = scenario_func()
                    results[name] = {
                        "success": result.get("success", False),
                        "session_id": result.get("session_id"),
                        "completed_at": datetime.now().isoformat()
                    }
                    status = "✅" if result.get("success") else "❌"
                    print(f"{status} {name}: {'Completed' if result.get('success') else 'Failed'}")
                except Exception as e:
                    results[name] = {"success": False, "error": str(e)}
                    print(f"❌ {name}: Failed - {e}")
            
            # Summary
            print(f"\n📊 Results Summary:")
            successful = sum(1 for r in results.values() if r.get("success"))
            print(f"Successful: {successful}/{len(available_scenarios)}")
            
            return results
            
        elif choice in ["1", "2", "3", "4", "5"]:
            idx = int(choice) - 1
            name, scenario_func = available_scenarios[idx]
            
            print(f"\n🚀 Running: {name}")
            result = scenario_func()
            
            if result.get("success"):
                print(f"✅ {name} completed successfully!")
                print(f"Session ID: {result.get('session_id')}")
                
                # Show sample insights
                if "steps" in result and "summary" in result["steps"]:
                    summary = result["steps"]["summary"].get("summary", "")
                    if summary:
                        print(f"\n📋 Sample Summary (first 300 chars):")
                        print(summary[:300] + "..." if len(summary) > 300 else summary)
            else:
                print(f"❌ {name} failed: {result.get('error')}")
            
            return result
            
        else:
            print("Invalid choice")
            return None
            
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted")
        return None
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("\nMake sure:")
        print("1. The workflow server is running: python main.py")
        print("2. Your OpenAI API key is set correctly")
        print("3. You have sufficient OpenAI credits")
        return None

def interactive_demo():
    """Interactive demo with step-by-step guidance"""
    
    print("🎯 Interactive Demo - Custom Focus Group")
    print("=" * 40)
    print("Create your own focus group discussion!")
    
    try:
        # Get user inputs
        print("\n📝 Step 1: Define Your Participants")
        persona_desc = input("Describe your ideal participants: ").strip()
        if not persona_desc:
            persona_desc = "Young professionals interested in technology products"
        
        print("\n🗣️ Step 2: Set Your Discussion Topic") 
        topic = input("What topic should they discuss? ").strip()
        if not topic:
            topic = "Technology adoption challenges and preferences"
        
        print("\n⏱️ Step 3: Configuration")
        try:
            num_personas = int(input("Number of participants (3-8): ") or "5")
        except:
            num_personas = 5
        
        try:
            duration = int(input("Discussion duration in minutes (30-90): ") or "45")
        except:
            duration = 45
        
        print("\n📊 Step 4: Summary Format")
        summary_schema = input("What should the summary include? ").strip()
        if not summary_schema:
            summary_schema = "Executive Summary, Key Insights, Recommendations, Verbatim Quotes"
        
        # Run workflow
        print(f"\n🚀 Running your custom focus group...")
        print("⏳ This will take a few minutes...")
        
        client = AgenticWorkflowClient()
        result = client.run_complete_workflow(
            persona_description=persona_desc,
            topic=topic,
            num_personas=num_personas,
            duration_minutes=duration,
            summary_schema=summary_schema
        )
        
        if result.get("success"):
            print(f"\n🎉 Your focus group completed successfully!")
            print(f"Session ID: {result['session_id']}")
            
            # Interactive Q&A
            print(f"\n❓ Ask questions about your results:")
            while True:
                question = input("\nYour question (or 'done' to finish): ").strip()
                if question.lower() in ['done', 'exit', 'quit']:
                    break
                
                if question:
                    qa_result = client.ask_question(question)
                    if qa_result.get("success"):
                        print(f"\n💡 Answer: {qa_result['answer']}")
                    else:
                        print(f"❌ Error: {qa_result.get('error')}")
            
            print("\n✨ Demo completed! Check the exported files for full results.")
            
        else:
            print(f"\n❌ Focus group failed: {result.get('error')}")
        
        return result
        
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled")
        return None

if __name__ == "__main__":
    print("🎭 Agentic AI Focus Group Workflow - Demonstrations")
    print("=" * 60)
    
    print("\nChoose demo type:")
    print("1. Pre-built scenarios (business use cases)")
    print("2. Interactive demo (create your own)")
    print("3. Quick health check")
    
    try:
        demo_choice = input("\nEnter choice (1-3): ").strip()
        
        if demo_choice == "1":
            run_demo_scenarios()
            
        elif demo_choice == "2":
            interactive_demo()
            
        elif demo_choice == "3":
            print("\n🏥 Quick Health Check...")
            client = AgenticWorkflowClient()
            health = client.health_check()
            
            if health.get("status") == "healthy":
                print("✅ System is healthy and ready!")
                print("You can now run scenarios or use the web interface.")
            else:
                print("❌ System health check failed")
                print("Make sure the server is running: python main.py")
            
        else:
            print("Invalid choice")
            
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure the server is running: python main.py")
        print("2. Check your OpenAI API key is set")
        print("3. Verify you have internet connectivity")