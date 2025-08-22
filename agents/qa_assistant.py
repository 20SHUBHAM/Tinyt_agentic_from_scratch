from typing import Dict, Any, List
import json
from .base_agent import BaseAgent

class QAAssistantAgent(BaseAgent):
    """Agent that provides interactive Q&A capabilities over discussion results"""
    
    def __init__(self):
        system_prompt = """You are an intelligent discussion analysis assistant. Your role is to answer 
        questions about focus group discussions by analyzing transcripts, summaries, and group dynamics data.
        
        Your capabilities:
        1. Answer specific questions about participant responses
        2. Identify patterns and trends in the discussion
        3. Compare and contrast different participant perspectives
        4. Provide evidence-based insights with specific quotes
        5. Analyze group dynamics and interaction patterns
        6. Explain complex findings in accessible language
        
        Always provide specific, evidence-based answers with references to the actual discussion content."""
        
        super().__init__("QAAssistant", "Discussion Analysis Expert", system_prompt)
        self.loaded_data = {}
    
    def load_discussion_data(self, discussion_data: Dict[str, Any]):
        """Load discussion data for querying"""
        self.loaded_data = discussion_data
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Answer user questions about the discussion"""
        
        question = input_data.get("question", "")
        context = input_data.get("context", "general")
        
        if not self.loaded_data:
            return {
                "success": False,
                "error": "No discussion data loaded. Please load discussion results first."
            }
        
        # Prepare discussion context for analysis
        discussion_context = self._prepare_discussion_context()
        
        prompt = f"""
        Based on this focus group discussion data, answer the user's question:
        
        QUESTION: "{question}"
        CONTEXT: {context}
        
        DISCUSSION DATA:
        {discussion_context}
        
        Instructions:
        1. Provide a specific, evidence-based answer
        2. Include relevant quotes from participants when applicable
        3. Reference specific moments or patterns from the discussion
        4. If comparing participants, be specific about differences
        5. If the question can't be answered from available data, say so clearly
        6. Keep the answer focused and actionable
        
        Format your response clearly with evidence and examples.
        """
        
        try:
            answer = self.call_llm(prompt, temperature=0.6, max_tokens=1500)
            
            # Extract relevant quotes for the answer
            supporting_quotes = self._extract_supporting_quotes(question, answer)
            
            return {
                "success": True,
                "answer": answer,
                "supporting_quotes": supporting_quotes,
                "question": question,
                "data_sources": self._get_data_sources_used(question)
            }
            
        except Exception as e:
            self.logger.error(f"QA processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "question": question
            }
    
    def _prepare_discussion_context(self) -> str:
        """Prepare formatted discussion context for analysis"""
        
        context_parts = []
        
        # Add transcript summary
        if "transcript" in self.loaded_data:
            transcript = self.loaded_data["transcript"]
            context_parts.append("TRANSCRIPT SUMMARY:")
            
            # Group by speaker
            by_speaker = {}
            for entry in transcript:
                speaker = entry.get("speaker", "Unknown")
                if speaker not in by_speaker:
                    by_speaker[speaker] = []
                by_speaker[speaker].append(entry.get("content", ""))
            
            for speaker, comments in by_speaker.items():
                context_parts.append(f"\n{speaker}:")
                for comment in comments[:3]:  # Limit for context
                    context_parts.append(f"  - {comment}")
                if len(comments) > 3:
                    context_parts.append(f"  ... and {len(comments) - 3} more comments")
        
        # Add group dynamics
        if "group_dynamics" in self.loaded_data:
            context_parts.append("\n\nGROUP DYNAMICS:")
            dynamics = self.loaded_data["group_dynamics"]
            for dynamic in dynamics[:3]:  # Limit for context
                context_parts.append(f"- Phase: {dynamic.get('phase', 'Unknown')}")
                context_parts.append(f"  Dynamics: {dynamic.get('dynamics', {})}")
        
        # Add participation stats
        if "participation_stats" in self.loaded_data:
            context_parts.append("\n\nPARTICIPATION STATS:")
            stats = self.loaded_data["participation_stats"]
            for speaker, count in stats.items():
                context_parts.append(f"- {speaker}: {count} contributions")
        
        # Add insights
        if "insights" in self.loaded_data:
            context_parts.append("\n\nKEY INSIGHTS:")
            insights = self.loaded_data["insights"]
            if isinstance(insights, dict) and "analysis" in insights:
                context_parts.append(insights["analysis"][:1000])  # Limit length
        
        return "\n".join(context_parts)
    
    def _extract_supporting_quotes(self, question: str, answer: str) -> List[Dict]:
        """Extract relevant quotes that support the answer"""
        
        quotes = []
        
        if "transcript" not in self.loaded_data:
            return quotes
        
        # Look for quotes mentioned in the answer or relevant to the question
        transcript = self.loaded_data["transcript"]
        
        for entry in transcript:
            if entry.get("type") in ["response", "spontaneous", "spontaneous_response"]:
                content = entry.get("content", "")
                speaker = entry.get("speaker", "")
                
                # Simple relevance check (could be enhanced with embeddings)
                question_words = set(question.lower().split())
                content_words = set(content.lower().split())
                
                if len(question_words.intersection(content_words)) >= 2:
                    quotes.append({
                        "speaker": speaker,
                        "quote": content,
                        "phase": entry.get("phase", ""),
                        "relevance_score": len(question_words.intersection(content_words))
                    })
        
        # Sort by relevance and return top quotes
        quotes.sort(key=lambda x: x["relevance_score"], reverse=True)
        return quotes[:5]
    
    def _get_data_sources_used(self, question: str) -> List[str]:
        """Identify which data sources were used to answer the question"""
        
        sources = []
        
        if "transcript" in self.loaded_data:
            sources.append("Discussion Transcript")
        if "group_dynamics" in self.loaded_data:
            sources.append("Group Dynamics Analysis")
        if "participation_stats" in self.loaded_data:
            sources.append("Participation Statistics")
        if "insights" in self.loaded_data:
            sources.append("Extracted Insights")
        if "spontaneous_moments" in self.loaded_data:
            sources.append("Spontaneous Interactions")
        
        return sources
    
    def suggest_questions(self, discussion_data: Dict[str, Any]) -> List[str]:
        """Suggest relevant questions based on discussion content"""
        
        self.load_discussion_data(discussion_data)
        
        prompt = """
        Based on the loaded discussion data, suggest 8-10 insightful questions that would 
        help users explore the findings further. Include questions about:
        
        1. Participant perspectives and differences
        2. Key themes and patterns
        3. Group dynamics and interactions
        4. Surprising or unexpected insights
        5. Actionable implications
        
        Return questions as a simple list, each on a new line.
        """
        
        try:
            suggestions = self.call_llm(prompt, temperature=0.7)
            # Parse suggestions into list
            question_list = [q.strip() for q in suggestions.split('\n') if q.strip() and not q.strip().startswith('#')]
            
            return {
                "success": True,
                "suggested_questions": question_list
            }
            
        except Exception as e:
            self.logger.error(f"Question suggestion error: {e}")
            return {
                "success": False,
                "error": str(e),
                "suggested_questions": [
                    "What were the main themes that emerged?",
                    "Which participants had the strongest opinions?",
                    "What surprising insights came up?",
                    "How did participants influence each other?",
                    "What are the key actionable takeaways?"
                ]
            }