from typing import Dict, Any, List
import json
import random
import time
from datetime import datetime
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from tinytroupe import control
from .base_agent import BaseAgent
from config import Config

class DynamicFocusGroupAgent(BaseAgent):
    """Agent that orchestrates dynamic focus group discussions using TinyTroupe"""
    
    def __init__(self):
        system_prompt = """You are a focus group orchestration specialist. You manage realistic 
        group discussions by coordinating multiple AI personas, ensuring natural conversation flow, 
        and capturing authentic group dynamics.
        
        Your expertise includes:
        1. Managing natural conversation timing and flow
        2. Encouraging authentic persona interactions
        3. Facilitating spontaneous reactions and interruptions
        4. Maintaining discussion focus while allowing organic development
        5. Capturing nuanced group dynamics and insights"""
        
        super().__init__("DynamicFocusGroup", "Focus Group Orchestrator", system_prompt)
        self.current_session = None
        self.participants = []
        self.world = None
        self.moderator = None
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run complete focus group discussion"""
        
        personas = input_data.get("personas", [])
        discussion_schema = input_data.get("discussion_schema", {})
        session_config = input_data.get("session_config", {})
        
        try:
            # Initialize session
            session_id = f"focus_group_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.current_session = session_id
            
            # Set up TinyTroupe environment
            control.begin(f"{Config.TINYTROUPE_CACHE_DIR}/{session_id}.cache.json")
            
            # Create participants
            self.participants = self._create_tinytroupe_personas(personas)
            
            # Create environment
            self.world = TinyWorld("Focus Group Discussion Room", self.participants)
            
            # Create moderator
            self.moderator = self._create_moderator(discussion_schema)
            
            # Run discussion
            discussion_results = self._run_discussion(discussion_schema)
            
            # Clean up
            control.end()
            
            return {
                "success": True,
                "session_id": session_id,
                "transcript": discussion_results["transcript"],
                "group_dynamics": discussion_results["group_dynamics"],
                "spontaneous_moments": discussion_results["spontaneous_moments"],
                "participation_stats": discussion_results["participation_stats"],
                "insights": discussion_results["insights"]
            }
            
        except Exception as e:
            self.logger.error(f"Focus group execution error: {e}")
            if self.current_session:
                try:
                    control.end()
                except:
                    pass
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_tinytroupe_personas(self, personas: List[Dict]) -> List[TinyPerson]:
        """Convert persona data to TinyTroupe TinyPerson objects"""
        
        tiny_personas = []
        
        for persona_data in personas:
            person = TinyPerson(persona_data["name"])
            
            # Define all persona attributes
            for key, value in persona_data.items():
                if key != "name":
                    person.define(key, value)
            
            # Create comprehensive persona prompt
            persona_prompt = f"""You are {persona_data['name']}, a {persona_data.get('age', 'young adult')} 
            year old {persona_data.get('occupation', 'person')} from {persona_data.get('location', 'India')}.
            
            Background: {persona_data.get('background', '')}
            Personality: {', '.join(persona_data.get('personality_traits', []))}
            Communication style: {persona_data.get('communication_style', 'natural')}
            
            In discussions, you:
            - Speak authentically based on your background and experiences
            - Share specific examples and personal stories
            - React naturally to others' comments
            - Show your personality through your responses
            - Stay true to your economic and social context
            
            Backstory: {persona_data.get('backstory', '')}"""
            
            person.define("persona_prompt", persona_prompt)
            tiny_personas.append(person)
        
        return tiny_personas
    
    def _create_moderator(self, discussion_schema: Dict) -> TinyPerson:
        """Create a dynamic moderator based on discussion schema"""
        
        moderator = TinyPerson("Moderator")
        moderator.define("role", "Professional Focus Group Moderator")
        
        moderator_prompt = f"""You are an experienced focus group moderator. Your discussion plan:
        
        {json.dumps(discussion_schema, indent=2)}
        
        Your moderation style:
        1. Ask open-ended questions that encourage detailed responses
        2. Allow natural conversation flow while gently guiding
        3. Encourage participation from quieter members
        4. Manage dominant personalities tactfully
        5. Create safe space for honest opinions
        6. Build on participant responses with follow-up questions
        7. Maintain energy and engagement throughout
        
        Use natural, conversational language and be genuinely curious about participants' perspectives."""
        
        moderator.define("moderation_approach", moderator_prompt)
        return moderator
    
    def _run_discussion(self, discussion_schema: Dict) -> Dict[str, Any]:
        """Execute the actual focus group discussion"""
        
        transcript = []
        group_dynamics = []
        spontaneous_moments = []
        participation_stats = {p.name: 0 for p in self.participants}
        
        phases = discussion_schema.get("phases", [])
        
        for phase_idx, phase in enumerate(phases):
            phase_name = phase["phase_name"]
            objective = phase["objective"]
            prompts = phase.get("sample_prompts", [])
            
            self.logger.info(f"Starting phase: {phase_name}")
            
            # Moderator introduces phase
            moderator_intro = self._generate_phase_introduction(phase)
            transcript.append({
                "speaker": "Moderator",
                "content": moderator_intro,
                "phase": phase_name,
                "timestamp": datetime.now().isoformat(),
                "type": "moderation"
            })
            
            # Run prompts for this phase
            for prompt_idx, prompt in enumerate(prompts):
                
                # Moderator asks question
                transcript.append({
                    "speaker": "Moderator",
                    "content": prompt,
                    "phase": phase_name,
                    "timestamp": datetime.now().isoformat(),
                    "type": "question"
                })
                
                # Get responses from participants
                responses = self._get_participant_responses(prompt, phase)
                
                for response_data in responses:
                    transcript.append(response_data)
                    participation_stats[response_data["speaker"]] += 1
                
                # Generate spontaneous interactions
                spontaneous = self._generate_spontaneous_interactions(prompt, phase)
                spontaneous_moments.extend(spontaneous)
                transcript.extend(spontaneous)
                
                # Capture group dynamics
                dynamics = self._analyze_current_dynamics(responses)
                group_dynamics.append({
                    "phase": phase_name,
                    "prompt": prompt,
                    "dynamics": dynamics,
                    "timestamp": datetime.now().isoformat()
                })
        
        # Generate final insights
        insights = self._extract_discussion_insights(transcript, group_dynamics)
        
        return {
            "transcript": transcript,
            "group_dynamics": group_dynamics,
            "spontaneous_moments": spontaneous_moments,
            "participation_stats": participation_stats,
            "insights": insights
        }
    
    def _generate_phase_introduction(self, phase: Dict) -> str:
        """Generate natural moderator introduction for each phase"""
        
        prompt = f"""As a professional moderator, create a natural introduction for this discussion phase:
        
        Phase: {phase['phase_name']}
        Objective: {phase['objective']}
        
        Create a warm, engaging 1-2 sentence introduction that transitions smoothly into this phase.
        Be conversational and encouraging."""
        
        try:
            return self.call_llm(prompt, temperature=0.7, max_tokens=200)
        except:
            return f"Let's move into our {phase['phase_name'].lower()} phase where we'll {phase['objective'].lower()}."
    
    def _get_participant_responses(self, prompt: str, phase: Dict) -> List[Dict]:
        """Get responses from all participants to a prompt"""
        
        responses = []
        
        # Randomize response order for natural flow
        response_order = random.sample(self.participants, len(self.participants))
        
        for participant in response_order:
            try:
                # Create context-aware prompt for participant
                participant_prompt = f"""
                The moderator just asked: "{prompt}"
                
                Phase context: {phase['objective']}
                
                Respond naturally as your persona. Share specific experiences, opinions, and examples.
                Be authentic to your background and personality. Keep responses conversational (2-4 sentences).
                """
                
                participant.listen(participant_prompt)
                response = participant.act()
                
                if response:
                    responses.append({
                        "speaker": participant.name,
                        "content": response,
                        "phase": phase["phase_name"],
                        "timestamp": datetime.now().isoformat(),
                        "type": "response"
                    })
                
                # Small delay for realism
                time.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Error getting response from {participant.name}: {e}")
                
        return responses
    
    def _generate_spontaneous_interactions(self, prompt: str, phase: Dict) -> List[Dict]:
        """Generate natural spontaneous interactions between participants"""
        
        interactions = []
        
        # 40% chance of spontaneous interaction per prompt
        if random.random() > 0.6:
            return interactions
        
        # Select random participants for interaction
        if len(self.participants) >= 2:
            interacting_participants = random.sample(self.participants, 2)
            initiator, responder = interacting_participants
            
            try:
                # Generate spontaneous comment
                spontaneous_prompt = f"""
                Based on the current discussion about "{prompt}", create a brief spontaneous 
                comment or reaction as {initiator.name}. This should feel natural and unscripted,
                like something you'd naturally want to add or respond to. Keep it short (1-2 sentences).
                """
                
                initiator.listen(spontaneous_prompt)
                spontaneous_comment = initiator.act()
                
                if spontaneous_comment:
                    interactions.append({
                        "speaker": initiator.name,
                        "content": spontaneous_comment,
                        "phase": phase["phase_name"],
                        "timestamp": datetime.now().isoformat(),
                        "type": "spontaneous"
                    })
                    
                    # Potential follow-up response
                    if random.random() > 0.5:
                        followup_prompt = f"""
                        {initiator.name} just said: "{spontaneous_comment}"
                        
                        As {responder.name}, respond briefly if this resonates with you or 
                        if you have a different perspective. Keep it natural and conversational.
                        """
                        
                        responder.listen(followup_prompt)
                        followup = responder.act()
                        
                        if followup:
                            interactions.append({
                                "speaker": responder.name,
                                "content": followup,
                                "phase": phase["phase_name"],
                                "timestamp": datetime.now().isoformat(),
                                "type": "spontaneous_response"
                            })
                
            except Exception as e:
                self.logger.error(f"Error generating spontaneous interaction: {e}")
        
        return interactions
    
    def _analyze_current_dynamics(self, responses: List[Dict]) -> Dict[str, Any]:
        """Analyze group dynamics from current responses"""
        
        return {
            "response_count": len(responses),
            "speakers": [r["speaker"] for r in responses],
            "avg_response_length": sum(len(r["content"]) for r in responses) / len(responses) if responses else 0,
            "engagement_level": "high" if len(responses) >= len(self.participants) * 0.8 else "moderate"
        }
    
    def _extract_discussion_insights(self, transcript: List[Dict], dynamics: List[Dict]) -> Dict[str, Any]:
        """Extract key insights from the discussion"""
        
        # Compile transcript for analysis
        full_discussion = "\n".join([
            f"{entry['speaker']}: {entry['content']}" 
            for entry in transcript 
            if entry['type'] in ['response', 'spontaneous', 'spontaneous_response']
        ])
        
        insights_prompt = f"""
        Analyze this focus group discussion and extract key insights:
        
        {full_discussion}
        
        Provide insights in these categories:
        1. Key themes that emerged
        2. Participant perspectives and differences
        3. Consensus areas and disagreements
        4. Unexpected insights or surprising revelations
        5. Group dynamics observations
        6. Actionable takeaways
        
        Format as a structured analysis with specific examples from the discussion.
        """
        
        try:
            insights = self.call_llm(insights_prompt, temperature=0.6)
            return {
                "analysis": insights,
                "discussion_length": len(transcript),
                "unique_speakers": len(set(entry["speaker"] for entry in transcript)),
                "phases_completed": len(set(entry["phase"] for entry in transcript if "phase" in entry))
            }
        except Exception as e:
            self.logger.error(f"Insights extraction error: {e}")
            return {"error": str(e)}