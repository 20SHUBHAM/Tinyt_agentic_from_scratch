# 🤖 Agentic AI Focus Group Workflow

A production-ready, multi-agent AI system for dynamic group discussion simulation using TinyTroupe. This system creates realistic focus group discussions with zero hardcoding - everything is generated dynamically by specialized AI agents.

## 🌟 Key Features

- **Fully Dynamic**: No hardcoded personas, topics, or schemas
- **Multi-Agent Architecture**: 5 specialized agents working in orchestration
- **TinyTroupe Integration**: Realistic group dynamics and conversations
- **User-Interactive**: Minimal user input triggers complex AI workflows
- **Production Ready**: Deployed on Replit with proper error handling
- **Modular Design**: Each component is independently testable and replaceable

## 🏗️ Architecture Overview

```
User Input → PersonaGenerator → SchemaGenerator → FocusGroupAgent → SummaryAgent → QAAssistant
     ↓              ↓               ↓               ↓              ↓            ↓
  Description   Personas      Discussion      Transcript    Custom      Interactive
                             Framework                     Summary        Q&A
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd agentic-focus-group-workflow
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
FLASK_SECRET_KEY=your_secret_key_here
```

### 3. Run Locally

```bash
python main.py
```

Access at: `http://localhost:5000`

### 4. Deploy to Replit

1. Import this repository to Replit
2. Set environment variables in Replit Secrets
3. Click "Run" - Replit will handle the rest!

## 🎯 Workflow Steps

### Step 1: Dynamic Persona Creation
- **Input**: Free-text description (e.g., "College students interested in fitness apps")
- **Agent**: PersonaGeneratorAgent
- **Output**: Detailed, diverse personas with backgrounds, motivations, constraints
- **User Action**: Review and optionally refine personas

### Step 2: Discussion Framework Generation
- **Input**: Discussion topic and parameters
- **Agent**: ContextSchemaGenerator  
- **Output**: Structured discussion phases with prompts and timing
- **User Action**: Review and optionally customize framework

### Step 3: Focus Group Simulation
- **Input**: Personas + Discussion Framework
- **Agent**: DynamicFocusGroupAgent (powered by TinyTroupe)
- **Output**: Complete transcript with natural interactions and group dynamics
- **Features**: Spontaneous reactions, interruptions, authentic conversations

### Step 4: Custom Summary Generation
- **Input**: User-defined summary schema
- **Agent**: SummaryAgent
- **Output**: Structured report following exact user specifications
- **Flexibility**: Any format from "Executive Summary" to custom business reports

### Step 5: Interactive Q&A
- **Input**: User questions about the discussion
- **Agent**: QAAssistantAgent
- **Output**: Evidence-based answers with supporting quotes
- **Features**: Suggested questions, pattern analysis, participant comparisons

## 🔧 Agent Specifications

### PersonaGeneratorAgent
- Creates authentic, diverse personas from natural language descriptions
- Considers cultural context, economic constraints, psychological profiles
- Ensures distinct voices and perspectives for engaging discussions

### ContextSchemaGenerator
- Designs natural conversation flows and discussion phases
- Creates moderator guidance and transition cues
- Optimizes for authentic sharing and meaningful insights

### DynamicFocusGroupAgent
- Orchestrates TinyTroupe-powered group discussions
- Manages natural conversation timing and spontaneous interactions
- Captures realistic group dynamics and authentic responses

### SummaryAgent
- Transforms raw transcripts into structured, actionable reports
- Follows custom user schemas exactly
- Extracts patterns, quotes, and insights with objectivity

### QAAssistantAgent
- Provides intelligent analysis of discussion results
- Answers specific questions with evidence and quotes
- Suggests relevant follow-up questions for deeper exploration

## 📁 Project Structure

```
agentic-focus-group-workflow/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py           # Abstract base class
│   ├── persona_generator.py    # Step 1: Persona creation
│   ├── context_schema_generator.py  # Step 2: Discussion framework
│   ├── dynamic_focus_group.py  # Step 3: TinyTroupe simulation
│   ├── summary_agent.py        # Step 4: Custom summaries
│   └── qa_assistant.py         # Step 5: Interactive Q&A
├── config.py                   # Configuration management
├── workflow_orchestrator.py    # Main workflow coordination
├── web_interface.py           # Flask web application
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .replit                    # Replit configuration
├── replit.nix                # Nix environment setup
├── pyproject.toml            # Modern Python packaging
└── README.md                 # This file
```

## 🌐 API Endpoints

- `POST /api/start-session` - Initialize new workflow session
- `POST /api/generate-personas` - Create dynamic personas
- `POST /api/refine-personas` - Refine personas with feedback
- `POST /api/generate-schema` - Create discussion framework
- `POST /api/customize-schema` - Modify discussion schema
- `POST /api/run-focus-group` - Execute focus group simulation
- `POST /api/generate-summary` - Create custom summary
- `POST /api/ask-question` - Interactive Q&A
- `POST /api/suggested-questions` - Get AI-suggested questions
- `POST /api/session-status` - Check workflow progress
- `POST /api/export-session` - Export complete session data
- `GET /health` - Health check endpoint

## 💡 Usage Examples

### Example 1: Tech Product Research
```
Step 1: "Young professionals in Bangalore who use fintech apps"
Step 2: "User experience challenges with digital banking"
Step 3: [Automated focus group with realistic participants]
Step 4: "Executive Summary, UX Pain Points, Feature Requests, Implementation Priority"
Step 5: "Which features were most requested?" "What frustrated users most?"
```

### Example 2: Market Research
```
Step 1: "Small business owners in tier-2 Indian cities"
Step 2: "Digital marketing adoption challenges and opportunities"
Step 3: [Natural group discussion with authentic business perspectives]
Step 4: "Market Insights, Adoption Barriers, Opportunity Areas, Budget Considerations"
Step 5: "What drives digital marketing adoption?" "Which channels show most promise?"
```

## 🎨 Key Innovations

1. **Zero Hardcoding**: Everything generated dynamically by AI agents
2. **Natural Group Dynamics**: TinyTroupe creates realistic interruptions and reactions
3. **Custom Output Formats**: User defines exactly what they want in summaries
4. **Interactive Analysis**: Ask any question about the discussion results
5. **Production Ready**: Proper error handling, logging, and deployment configuration

## 🔒 Security & Production Considerations

- Environment variable management for API keys
- Input validation and sanitization
- Error handling and graceful degradation
- Logging for debugging and monitoring
- Rate limiting considerations for API calls
- Session management and data isolation

## 🚀 Deployment Options

### Replit (Recommended)
1. Import repository to Replit
2. Set environment variables in Secrets
3. Click Run - automatic deployment!

### Local Development
```bash
python main.py
```

### Docker (Optional)
```bash
docker build -t agentic-focus-group .
docker run -p 5000:5000 --env-file .env agentic-focus-group
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the logs in the web interface
2. Verify environment variables are set correctly
3. Ensure OpenAI API key has sufficient credits
4. Check Replit deployment logs if using Replit

## 🎯 Roadmap

- [ ] Advanced persona refinement with user feedback loops
- [ ] Multi-language support for global discussions
- [ ] Integration with external data sources for persona enrichment
- [ ] Advanced analytics and pattern recognition
- [ ] Export to multiple formats (PDF, Word, PowerPoint)
- [ ] Real-time collaboration features
- [ ] API rate limiting and caching optimization