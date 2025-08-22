from typing import Dict, Any, List
import json
from .base_agent import BaseAgent

class SummaryAgent(BaseAgent):
    """Agent responsible for generating custom summaries based on user-defined schemas"""
    
    def __init__(self):
        system_prompt = """You are an expert research analyst specializing in qualitative data synthesis. 
        Your role is to transform raw discussion transcripts into structured, actionable reports based on 
        custom user schemas.
        
        Key capabilities:
        1. Extract meaningful patterns from conversational data
        2. Organize insights according to custom report structures
        3. Identify verbatim quotes that support key findings
        4. Synthesize complex discussions into clear, actionable insights
        5. Maintain objectivity while highlighting important nuances
        
        Always follow the exact schema provided by the user and ensure your output is well-structured and actionable."""
        
        super().__init__("SummaryAgent", "Research Analysis Specialist", system_prompt)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary based on transcript and user schema"""
        
        transcript = input_data.get("transcript", [])
        user_schema = input_data.get("summary_schema", "")
        group_dynamics = input_data.get("group_dynamics", [])
        additional_context = input_data.get("additional_context", {})
        
        # Convert transcript to readable format
        formatted_transcript = self._format_transcript(transcript)
        
        prompt = f"""
        Analyze this focus group discussion and create a summary following the user's custom schema.
        
        TRANSCRIPT:
        {formatted_transcript}
        
        GROUP DYNAMICS:
        {json.dumps(group_dynamics, indent=2)}
        
        ADDITIONAL CONTEXT:
        {json.dumps(additional_context, indent=2)}
        
        USER'S CUSTOM SUMMARY SCHEMA:
        "{user_schema}"
        
        Instructions:
        1. Follow the user's schema EXACTLY as specified
        2. Extract relevant insights from the transcript for each section
        3. Include specific verbatim quotes where appropriate
        4. Ensure all sections requested in the schema are addressed
        5. Make insights actionable and specific
        6. Maintain objectivity while highlighting key patterns
        
        If the user schema is in natural language (not JSON), interpret it and create 
        appropriate sections. For example:
        - "Executive Summary" → High-level overview
        - "Key Insights" → Main findings and patterns
        - "Recommendations" → Actionable next steps
        - "Verbatim Quotes" → Supporting quotes from participants
        
        Return a well-structured summary that follows the user's schema.
        """
        
        try:
            summary = self.call_llm(prompt, temperature=0.6, max_tokens=3000)
            
            return {
                "success": True,
                "summary": summary,
                "schema_used": user_schema,
                "source_data": {
                    "transcript_length": len(transcript),
                    "participants": list(set(entry.get("speaker", "") for entry in transcript)),
                    "discussion_phases": list(set(entry.get("phase", "") for entry in transcript if entry.get("phase")))
                }
            }
            
        except Exception as e:
            self.logger.error(f"Summary generation error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _format_transcript(self, transcript: List[Dict]) -> str:
        """Format transcript for analysis"""
        
        formatted_lines = []
        current_phase = ""
        
        for entry in transcript:
            # Add phase headers
            if entry.get("phase") and entry["phase"] != current_phase:
                current_phase = entry["phase"]
                formatted_lines.append(f"\n=== {current_phase.upper()} ===")
            
            # Format entry based on type
            speaker = entry.get("speaker", "Unknown")
            content = entry.get("content", "")
            entry_type = entry.get("type", "")
            
            if entry_type == "question":
                formatted_lines.append(f"\nMODERATOR: {content}")
            elif entry_type in ["response", "spontaneous", "spontaneous_response"]:
                prefix = "↳" if entry_type.startswith("spontaneous") else ""
                formatted_lines.append(f"{prefix}{speaker}: {content}")
            else:
                formatted_lines.append(f"{speaker}: {content}")
        
        return "\n".join(formatted_lines)
    
    def generate_multiple_formats(self, input_data: Dict[str, Any], formats: List[str]) -> Dict[str, Any]:
        """Generate summaries in multiple formats"""
        
        results = {}
        
        for format_name in formats:
            format_input = input_data.copy()
            format_input["summary_schema"] = self._get_format_schema(format_name)
            
            result = self.process(format_input)
            results[format_name] = result
        
        return {
            "success": True,
            "multiple_summaries": results,
            "formats_generated": formats
        }
    
    def _get_format_schema(self, format_name: str) -> str:
        """Get predefined schema for common summary formats"""
        
        schemas = {
            "executive": "Executive Summary, Key Findings, Strategic Recommendations, Next Steps",
            "research": "Research Objectives, Methodology, Key Findings, Participant Insights, Verbatim Quotes, Limitations, Recommendations",
            "business": "Business Impact Summary, Market Insights, Customer Segments, Opportunity Areas, Risk Factors, Action Items",
            "academic": "Abstract, Introduction, Methodology, Results, Discussion, Conclusions, Future Research",
            "marketing": "Campaign Insights, Target Audience Profiles, Message Resonance, Channel Preferences, Creative Direction, Budget Implications"
        }
        
        return schemas.get(format_name, "Summary, Key Points, Insights, Recommendations")