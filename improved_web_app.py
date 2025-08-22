#!/usr/bin/env python3
"""
Improved Agentic AI Focus Group Workflow - Professional Web Application
Features: Persona editing, Natural language outputs, Separate pages, Professional UI
"""

from flask import Flask, request, jsonify, render_template_string, session
from flask_cors import CORS
import json
import logging
from datetime import datetime
import os
from workflow_orchestrator import WorkflowOrchestrator
from config import Config

app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY
CORS(app)

# Initialize workflow orchestrator
orchestrator = WorkflowOrchestrator()
logger = logging.getLogger(__name__)

def format_personas_natural(personas_data):
    """Convert personas to natural language"""
    if not personas_data.get("success"):
        return "Failed to generate participants."
    
    personas = personas_data["personas"]
    output = f"# ✅ Generated {len(personas)} Research Participants\n\n"
    
    for i, persona in enumerate(personas, 1):
        output += f"## {persona['name']}\n"
        output += f"**Age:** {persona['age']} | **Occupation:** {persona['occupation']}\n\n"
        output += f"**Background:** {persona.get('background', '')}\n\n"
        
        if persona.get('personality_traits'):
            traits = persona['personality_traits'] if isinstance(persona['personality_traits'], list) else [persona['personality_traits']]
            output += f"**Personality Traits:** {', '.join(traits)}\n\n"
        
        if persona.get('motivations'):
            motivations = persona['motivations'] if isinstance(persona['motivations'], list) else [persona['motivations']]
            output += f"**Key Motivations:** {', '.join(motivations)}\n\n"
        
        output += "---\n\n"
    
    if personas_data.get("group_dynamics_prediction"):
        output += f"## 🔮 Expected Group Dynamics\n\n{personas_data['group_dynamics_prediction']}"
    
    return output

def format_schema_natural(schema_data):
    """Convert schema to natural language"""
    if not schema_data.get("success"):
        return "Failed to create discussion framework."
    
    schema = schema_data["schema"]
    output = f"# ✅ Discussion Framework: {schema.get('topic', 'Research Topic')}\n\n"
    output += f"**Total Duration:** {schema.get('total_duration_minutes', 60)} minutes\n"
    output += f"**Discussion Phases:** {len(schema.get('phases', []))}\n\n"
    
    for i, phase in enumerate(schema.get('phases', []), 1):
        output += f"## Phase {i}: {phase['phase_name']}\n"
        output += f"**Duration:** {phase.get('duration_minutes', 'N/A')} minutes\n"
        output += f"**Objective:** {phase['objective']}\n\n"
        
        if phase.get('sample_prompts'):
            output += "**Key Discussion Questions:**\n"
            for prompt in phase['sample_prompts']:
                output += f"• {prompt}\n"
            output += "\n"
        
        if phase.get('moderator_guidance'):
            output += f"**Moderator Notes:** {phase['moderator_guidance']}\n\n"
        
        output += "---\n\n"
    
    return output

# Professional HTML Template with Tabbed Interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic AI Research Platform</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --success: #059669;
            --error: #dc2626;
            --warning: #d97706;
            --background: #f8fafc;
            --surface: #ffffff;
            --text: #1e293b;
            --text-light: #64748b;
            --border: #e2e8f0;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--background);
            color: var(--text);
            line-height: 1.6;
        }

        .container { max-width: 1100px; margin: 0 auto; padding: 20px; }
        
        .header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 3rem 0;
            text-align: center;
            margin-bottom: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(37, 99, 235, 0.3);
        }
        
        .header h1 { 
            font-size: 3rem; 
            font-weight: 700; 
            margin-bottom: 0.5rem; 
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .header p { 
            font-size: 1.3rem; 
            opacity: 0.9; 
            margin-bottom: 1rem;
        }

        .nav-tabs {
            display: flex;
            background: var(--surface);
            border-radius: 16px;
            padding: 8px;
            margin-bottom: 3rem;
            border: 1px solid var(--border);
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }

        .nav-tab {
            flex: 1;
            padding: 16px 20px;
            text-align: center;
            background: transparent;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 600;
            font-size: 15px;
            transition: all 0.3s ease;
            color: var(--text-light);
        }

        .nav-tab.active {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            box-shadow: 0 4px 16px rgba(37, 99, 235, 0.3);
            transform: translateY(-2px);
        }

        .nav-tab:hover:not(.active):not(:disabled) {
            background: rgba(37, 99, 235, 0.1);
            color: var(--primary);
            transform: translateY(-1px);
        }

        .nav-tab:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .workflow-step {
            background: var(--surface);
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 6px 30px rgba(0,0,0,0.08);
            border: 1px solid var(--border);
            transition: all 0.3s ease;
        }

        .step-header {
            text-align: center;
            margin-bottom: 2.5rem;
        }

        .step-title { 
            font-size: 2rem; 
            font-weight: 700; 
            color: var(--text);
            margin-bottom: 0.5rem;
        }

        .step-subtitle {
            font-size: 1.1rem;
            color: var(--text-light);
        }

        .form-group { margin-bottom: 2rem; }
        
        .form-label { 
            display: block; 
            margin-bottom: 0.75rem; 
            font-weight: 600; 
            color: var(--text);
            font-size: 1.1rem;
        }

        .form-input, .form-textarea, .form-select {
            width: 100%;
            padding: 18px 24px;
            border: 2px solid var(--border);
            border-radius: 12px;
            font-size: 16px;
            transition: all 0.3s ease;
            font-family: inherit;
            background: var(--surface);
        }

        .form-input:focus, .form-textarea:focus, .form-select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
            transform: translateY(-2px);
        }

        .form-textarea { 
            min-height: 160px; 
            resize: vertical; 
        }

        .btn {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 18px 36px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.3);
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.4);
        }

        .btn:disabled {
            background: #cbd5e1;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        .btn-secondary {
            background: linear-gradient(135deg, #64748b 0%, #475569 100%);
            box-shadow: 0 6px 20px rgba(100, 116, 139, 0.3);
        }

        .btn-success {
            background: linear-gradient(135deg, var(--success) 0%, #047857 100%);
            box-shadow: 0 6px 20px rgba(5, 150, 105, 0.3);
        }

        .btn-small {
            padding: 10px 20px;
            font-size: 14px;
        }

        .result-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2.5rem;
            margin-top: 2rem;
            white-space: pre-wrap;
            line-height: 1.8;
            font-size: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        }

        .success {
            border-left: 6px solid var(--success);
            background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
        }

        .error {
            border-left: 6px solid var(--error);
            background: linear-gradient(135deg, #fef2f2 0%, #fef7f7 100%);
        }

        .loading {
            text-align: center;
            padding: 4rem;
            color: var(--text-light);
        }

        .spinner {
            width: 60px;
            height: 60px;
            border: 6px solid var(--border);
            border-top: 6px solid var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 1.5rem;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .persona-card {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border: 2px solid var(--border);
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
            transition: all 0.3s ease;
        }

        .persona-card:hover {
            border-color: var(--primary);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transform: translateY(-3px);
        }

        .persona-name {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 0.75rem;
        }

        .editable {
            background: transparent;
            border: 2px solid transparent;
            padding: 8px 12px;
            border-radius: 8px;
            transition: all 0.3s ease;
            cursor: text;
            display: inline-block;
            min-width: 120px;
        }

        .editable:hover {
            background: rgba(37, 99, 235, 0.05);
            border-color: var(--primary);
        }

        .editable:focus {
            background: white;
            border-color: var(--primary);
            outline: none;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
        }

        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }

        .progress-indicator {
            background: var(--border);
            height: 8px;
            border-radius: 4px;
            margin: 2rem 0;
            overflow: hidden;
        }

        .progress-fill {
            background: linear-gradient(90deg, var(--primary) 0%, var(--success) 100%);
            height: 100%;
            transition: width 0.5s ease;
        }

        .question-suggestion {
            background: #eff6ff;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 10px;
            cursor: pointer;
            border: 1px solid #dbeafe;
            transition: all 0.2s;
        }

        .question-suggestion:hover {
            background: #dbeafe;
            transform: translateX(5px);
        }

        @media (max-width: 768px) {
            .grid-2 { grid-template-columns: 1fr; }
            .header h1 { font-size: 2.2rem; }
            .container { padding: 15px; }
            .workflow-step { padding: 2rem; }
            .nav-tabs { flex-direction: column; gap: 5px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Agentic AI Research Platform</h1>
            <p>Professional Focus Group Simulation with Dynamic AI Agents</p>
            <div id="session-indicator"></div>
        </div>

        <!-- Progress Bar -->
        <div class="progress-indicator">
            <div class="progress-fill" id="progress-bar" style="width: 0%"></div>
        </div>

        <!-- Navigation Tabs -->
        <div class="nav-tabs">
            <button class="nav-tab active" onclick="showTab('personas', 1)">1. Create Participants</button>
            <button class="nav-tab" onclick="showTab('discussion', 2)" id="tab-discussion" disabled>2. Design Discussion</button>
            <button class="nav-tab" onclick="showTab('simulation', 3)" id="tab-simulation" disabled>3. Run Simulation</button>
            <button class="nav-tab" onclick="showTab('analysis', 4)" id="tab-analysis" disabled>4. Generate Report</button>
            <button class="nav-tab" onclick="showTab('results', 5)" id="tab-results" disabled>5. Analyze Results</button>
        </div>

        <!-- Tab 1: Personas -->
        <div id="content-personas" class="tab-content active">
            <div class="workflow-step">
                <div class="step-header">
                    <div class="step-title">Create Research Participants</div>
                    <div class="step-subtitle">Describe your ideal participants and our AI will create diverse, authentic personas</div>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Describe your ideal research participants:</label>
                    <textarea id="persona-description" class="form-textarea" 
                        placeholder="Example: Young professionals in Indian metros (age 22-32) who actively use digital banking and fintech apps. Include both tech-savvy early adopters and more cautious traditional users with different income levels and banking preferences.">Young professionals in Indian metros interested in sustainable lifestyle products</textarea>
                    <div style="font-size: 0.9rem; color: var(--text-light); margin-top: 0.5rem;">
                        💡 Be specific about demographics, behaviors, and context for more authentic participants
                    </div>
                </div>
                
                <div class="grid-2">
                    <div class="form-group">
                        <label class="form-label">Number of participants:</label>
                        <select id="num-personas" class="form-select">
                            <option value="3">3 participants</option>
                            <option value="4">4 participants</option>
                            <option value="5" selected>5 participants</option>
                            <option value="6">6 participants</option>
                            <option value="8">8 participants</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Research context:</label>
                        <select id="context" class="form-select">
                            <option value="focus group" selected>Focus Group Discussion</option>
                            <option value="user interview">User Interview Session</option>
                            <option value="market research">Market Research Study</option>
                            <option value="product feedback">Product Feedback Session</option>
                        </select>
                    </div>
                </div>
                
                <div style="text-align: center;">
                    <button class="btn" onclick="generatePersonas()">🎯 Generate Participants</button>
                </div>
                
                <div id="persona-results"></div>
                
                <!-- Editable Personas Section -->
                <div id="personas-editor" style="display: none; margin-top: 3rem;">
                    <h3 style="margin-bottom: 2rem; color: var(--primary); text-align: center;">✏️ Review & Edit Your Participants</h3>
                    <div id="personas-list"></div>
                    <div style="margin-top: 2rem; text-align: center;">
                        <button class="btn btn-success" onclick="approvePersonas()">✅ Approve Participants & Continue</button>
                        <button class="btn btn-secondary" onclick="addPersona()">➕ Add Participant</button>
                        <button class="btn btn-secondary" onclick="regeneratePersonas()">🔄 Regenerate All</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 2: Discussion -->
        <div id="content-discussion" class="tab-content">
            <div class="workflow-step">
                <div class="step-header">
                    <div class="step-title">Design Discussion Framework</div>
                    <div class="step-subtitle">Define your research topic and our AI will create a structured discussion plan</div>
                </div>
                
                <div class="form-group">
                    <label class="form-label">What should your participants discuss?</label>
                    <textarea id="discussion-topic" class="form-textarea" 
                        placeholder="Example: User experience challenges and improvement suggestions for digital banking platforms. Focus on daily usage scenarios, pain points, security concerns, and feature requests.">Barriers to adopting sustainable lifestyle products and what motivates eco-friendly purchasing decisions</textarea>
                    <div style="font-size: 0.9rem; color: var(--text-light); margin-top: 0.5rem;">
                        💡 Be specific about what insights you want to gather from the discussion
                    </div>
                </div>
                
                <div class="grid-2">
                    <div class="form-group">
                        <label class="form-label">Discussion duration:</label>
                        <select id="duration" class="form-select">
                            <option value="30">30 minutes - Quick insights</option>
                            <option value="45">45 minutes - Balanced discussion</option>
                            <option value="60" selected>60 minutes - Deep exploration</option>
                            <option value="90">90 minutes - Comprehensive analysis</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Discussion style:</label>
                        <select id="discussion-type" class="form-select">
                            <option value="focus group" selected>Focus Group (Interactive)</option>
                            <option value="structured interview">Structured Interview</option>
                            <option value="open discussion">Open Discussion</option>
                        </select>
                    </div>
                </div>
                
                <div style="text-align: center;">
                    <button class="btn" onclick="generateSchema()">🎯 Create Discussion Framework</button>
                </div>
                
                <div id="schema-results"></div>
                
                <div style="margin-top: 2rem; text-align: center;">
                    <button class="btn btn-success" onclick="approveSchema()" id="approve-schema-btn" style="display: none;">✅ Approve Framework & Continue</button>
                </div>
            </div>
        </div>

        <!-- Tab 3: Simulation -->
        <div id="content-simulation" class="tab-content">
            <div class="workflow-step">
                <div class="step-header">
                    <div class="step-title">Run Focus Group Simulation</div>
                    <div class="step-subtitle">Watch as your AI participants engage in realistic discussion</div>
                </div>
                
                <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); padding: 2.5rem; border-radius: 16px; margin-bottom: 2rem; text-align: center;">
                    <h3 style="color: var(--primary); margin-bottom: 1rem; font-size: 1.5rem;">🎭 Ready for Simulation</h3>
                    <p style="color: var(--text-light); margin-bottom: 2rem; font-size: 1.1rem;">Your AI participants will engage in a realistic discussion with natural group dynamics. This typically takes 3-5 minutes.</p>
                    <div id="participants-preview"></div>
                </div>
                
                <div style="text-align: center;">
                    <button class="btn" onclick="runFocusGroup()" style="font-size: 18px; padding: 20px 40px;">🚀 Start Focus Group Discussion</button>
                </div>
                
                <div id="discussion-results"></div>
            </div>
        </div>

        <!-- Tab 4: Analysis -->
        <div id="content-analysis" class="tab-content">
            <div class="workflow-step">
                <div class="step-header">
                    <div class="step-title">Generate Research Report</div>
                    <div class="step-subtitle">Create a custom report tailored to your specific needs</div>
                </div>
                
                <div class="form-group">
                    <label class="form-label">What should your report include?</label>
                    <textarea id="summary-schema" class="form-textarea" 
                        placeholder="Describe what sections and insights you want in your report. Example: Executive Summary, Key Insights, Participant Perspectives, Barriers Identified, Motivating Factors, Recommendations, Supporting Quotes">Executive Summary, Key Insights, Participant Perspectives, Barriers Identified, Motivating Factors, Recommendations, Supporting Quotes</textarea>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Report style:</label>
                    <select id="report-style" class="form-select">
                        <option value="business" selected>Business Report - Professional analysis</option>
                        <option value="executive">Executive Summary - High-level insights</option>
                        <option value="academic">Academic Research - Detailed methodology</option>
                        <option value="marketing">Marketing Insights - Consumer behavior focus</option>
                    </select>
                </div>
                
                <div style="text-align: center;">
                    <button class="btn" onclick="generateSummary()">📊 Generate Custom Report</button>
                </div>
                
                <div id="summary-results"></div>
            </div>
        </div>

        <!-- Tab 5: Results -->
        <div id="content-results" class="tab-content">
            <div class="workflow-step">
                <div class="step-header">
                    <div class="step-title">Interactive Research Analysis</div>
                    <div class="step-subtitle">Ask questions about your research and get AI-powered insights</div>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Ask questions about your research results:</label>
                    <input type="text" id="qa-question" class="form-input" 
                        placeholder="Example: Who was most enthusiastic about the topic? What were the main concerns? Which insights surprised you most?">
                </div>
                
                <div style="text-align: center; margin-bottom: 2rem;">
                    <button class="btn" onclick="askQuestion()">🤔 Ask Question</button>
                    <button class="btn btn-secondary" onclick="getSuggestedQuestions()">💡 Get Question Suggestions</button>
                </div>
                
                <div id="suggested-questions"></div>
                <div id="qa-results"></div>
                
                <div style="margin-top: 3rem; text-align: center; padding-top: 2rem; border-top: 2px solid var(--border);">
                    <h3 style="margin-bottom: 1rem; color: var(--primary);">🎉 Research Complete!</h3>
                    <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                        <button class="btn btn-success" onclick="exportSession()">💾 Export Complete Results</button>
                        <button class="btn btn-secondary" onclick="viewSessionSummary()">📊 View Session Summary</button>
                        <button class="btn btn-secondary" onclick="resetSession()">🔄 Start New Research</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentPersonas = [];
        let sessionProgress = 0;

        // Tab Management
        function showTab(tabName, step) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active from all nav tabs
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(`content-${tabName}`).classList.add('active');
            
            // Activate nav tab
            event.target.classList.add('active');
            
            // Update progress
            updateProgress(step);
        }

        function updateProgress(step) {
            sessionProgress = step;
            const progress = (step / 5) * 100;
            document.getElementById('progress-bar').style.width = `${progress}%`;
        }

        function enableTab(tabId) {
            const tab = document.getElementById(tabId);
            tab.disabled = false;
            tab.style.opacity = '1';
        }

        async function apiCall(endpoint, data = {}) {
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                return await response.json();
            } catch (error) {
                return { success: false, error: error.message };
            }
        }

        function showLoading(elementId, message = 'Processing...') {
            document.getElementById(elementId).innerHTML = 
                `<div class="loading"><div class="spinner"></div><strong>🤖 ${message}</strong></div>`;
        }

        function showResult(elementId, content, isError = false) {
            const className = isError ? 'result-box error' : 'result-box success';
            document.getElementById(elementId).innerHTML = 
                `<div class="${className}">${content}</div>`;
        }

        // Persona Management with Editing
        async function generatePersonas() {
            const description = document.getElementById('persona-description').value;
            const numPersonas = parseInt(document.getElementById('num-personas').value);
            const context = document.getElementById('context').value;

            if (!description.trim()) {
                showResult('persona-results', '❌ Please provide a description of your participants', true);
                return;
            }

            showLoading('persona-results', 'Creating authentic participants with unique personalities...');
            
            const result = await apiCall('/api/generate-personas', {
                persona_description: description,
                num_personas: numPersonas,
                context: context
            });
            
            if (result.success) {
                currentPersonas = result.personas;
                
                // Show natural language description
                const naturalOutput = formatPersonasForDisplay(result);
                showResult('persona-results', naturalOutput);
                
                // Show editable interface
                displayEditablePersonas(result.personas);
                
                updateProgress(1);
                
            } else {
                showResult('persona-results', `❌ Failed to generate participants: ${result.error}`, true);
            }
        }

        function formatPersonasForDisplay(result) {
            const personas = result.personas;
            let output = `# ✅ Created ${personas.length} Authentic Research Participants\\n\\n`;
            
            personas.forEach((persona, index) => {
                output += `## ${persona.name}\\n`;
                output += `**Profile:** ${persona.age} years old, ${persona.occupation}\\n\\n`;
                output += `**Background:** ${persona.background}\\n\\n`;
                
                if (persona.personality_traits) {
                    const traits = Array.isArray(persona.personality_traits) ? 
                        persona.personality_traits.join(', ') : persona.personality_traits;
                    output += `**Personality:** ${traits}\\n\\n`;
                }
                
                output += '---\\n\\n';
            });
            
            if (result.group_dynamics_prediction) {
                output += `## 🔮 Expected Group Dynamics\\n\\n${result.group_dynamics_prediction}\\n\\n`;
                output += `*These participants are designed to create authentic, engaging discussions with natural group dynamics.*`;
            }
            
            return output;
        }

        function displayEditablePersonas(personas) {
            const container = document.getElementById('personas-list');
            const editor = document.getElementById('personas-editor');
            
            let html = '';
            personas.forEach((persona, index) => {
                html += `
                    <div class="persona-card" data-index="${index}">
                        <div class="persona-name">
                            <span class="editable" contenteditable="true" onblur="updatePersona(${index}, 'name', this.textContent)">${persona.name}</span>
                        </div>
                        <div style="margin: 1rem 0; color: var(--text-light); font-size: 1.05rem;">
                            <strong>Age:</strong> <span class="editable" contenteditable="true" onblur="updatePersona(${index}, 'age', this.textContent)">${persona.age}</span> | 
                            <strong>Occupation:</strong> <span class="editable" contenteditable="true" onblur="updatePersona(${index}, 'occupation', this.textContent)">${persona.occupation}</span>
                        </div>
                        <div style="margin: 1.5rem 0;">
                            <strong style="color: var(--text);">Background:</strong><br>
                            <div class="editable" contenteditable="true" onblur="updatePersona(${index}, 'background', this.textContent)" style="margin-top: 0.75rem; min-height: 80px; line-height: 1.6;">${persona.background}</div>
                        </div>
                        <div style="text-align: right; margin-top: 1.5rem;">
                            <button class="btn btn-secondary btn-small" onclick="duplicatePersona(${index})">📋 Duplicate</button>
                            <button class="btn btn-secondary btn-small" onclick="removePersona(${index})" style="background: var(--error);">🗑️ Remove</button>
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = html;
            editor.style.display = 'block';
            
            // Scroll to editor
            editor.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        function updatePersona(index, field, value) {
            if (currentPersonas[index]) {
                currentPersonas[index][field] = value;
                
                // Visual feedback
                const card = document.querySelector(`[data-index="${index}"]`);
                card.style.background = 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)';
                card.style.borderColor = var(--success);
                setTimeout(() => {
                    card.style.background = '';
                    card.style.borderColor = '';
                }, 1500);
            }
        }

        function duplicatePersona(index) {
            const original = currentPersonas[index];
            const duplicate = { 
                ...original, 
                name: original.name + ' (Copy)'
            };
            
            currentPersonas.push(duplicate);
            displayEditablePersonas(currentPersonas);
        }

        function removePersona(index) {
            if (currentPersonas.length <= 2) {
                alert('You need at least 2 participants for a meaningful discussion');
                return;
            }
            
            if (confirm('Are you sure you want to remove this participant?')) {
                currentPersonas.splice(index, 1);
                displayEditablePersonas(currentPersonas);
            }
        }

        function addPersona() {
            const newPersona = {
                name: 'New Participant',
                age: 25,
                occupation: 'Professional',
                background: 'Click here to add background details, personality traits, and motivations...',
                personality_traits: ['Thoughtful', 'Analytical'],
                motivations: ['Quality', 'Value']
            };
            
            currentPersonas.push(newPersona);
            displayEditablePersonas(currentPersonas);
        }

        function regeneratePersonas() {
            if (confirm('This will create completely new participants. Continue?')) {
                generatePersonas();
            }
        }

        function approvePersonas() {
            if (currentPersonas.length === 0) {
                alert('Please generate participants first');
                return;
            }
            
            showResult('persona-results', '# ✅ Participants Approved!\\n\\nYour research participants are ready. Moving to discussion design...');
            enableTab('tab-discussion');
            updateProgress(2);
            
            setTimeout(() => {
                document.getElementById('tab-discussion').click();
            }, 2000);
        }

        // Schema Management
        async function generateSchema() {
            const topic = document.getElementById('discussion-topic').value;
            
            if (!topic.trim()) {
                showResult('schema-results', '❌ Please provide a discussion topic', true);
                return;
            }
            
            showLoading('schema-results', 'Designing structured discussion framework...');
            
            const result = await apiCall('/api/generate-schema', {
                topic: topic,
                discussion_type: document.getElementById('discussion-type').value,
                duration_minutes: parseInt(document.getElementById('duration').value)
            });
            
            if (result.success) {
                const naturalOutput = formatSchemaForDisplay(result);
                showResult('schema-results', naturalOutput);
                
                document.getElementById('approve-schema-btn').style.display = 'inline-flex';
                updateProgress(2.5);
            } else {
                showResult('schema-results', `❌ Failed to create framework: ${result.error}`, true);
            }
        }

        function formatSchemaForDisplay(result) {
            const schema = result.schema;
            let output = `# ✅ Discussion Framework Created\\n\\n`;
            output += `**Research Topic:** ${schema.topic}\\n`;
            output += `**Total Duration:** ${schema.total_duration_minutes} minutes\\n`;
            output += `**Discussion Structure:** ${schema.phases.length} carefully designed phases\\n\\n`;
            
            schema.phases.forEach((phase, index) => {
                output += `## Phase ${index + 1}: ${phase.phase_name}\\n`;
                output += `**Duration:** ${phase.duration_minutes} minutes\\n`;
                output += `**Objective:** ${phase.objective}\\n\\n`;
                
                if (phase.sample_prompts && phase.sample_prompts.length > 0) {
                    output += `**Key Discussion Questions:**\\n`;
                    phase.sample_prompts.forEach(prompt => {
                        output += `• ${prompt}\\n`;
                    });
                    output += '\\n';
                }
                
                output += '---\\n\\n';
            });
            
            output += `*This framework is designed to facilitate natural, engaging discussions that yield valuable insights.*`;
            
            return output;
        }

        function approveSchema() {
            showResult('schema-results', '# ✅ Discussion Framework Approved!\\n\\nYour discussion structure is ready. Proceeding to simulation...');
            enableTab('tab-simulation');
            updateProgress(3);
            
            setTimeout(() => {
                document.getElementById('tab-simulation').click();
                showParticipantsPreview();
            }, 2000);
        }

        function showParticipantsPreview() {
            if (currentPersonas.length > 0) {
                let preview = `<div style="background: white; padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border: 1px solid var(--border);">`;
                preview += `<h4 style="color: var(--primary); margin-bottom: 1rem;">Your ${currentPersonas.length} Research Participants:</h4>`;
                preview += `<div style="display: flex; flex-wrap: wrap; gap: 1rem;">`;
                
                currentPersonas.forEach(persona => {
                    preview += `<div style="background: var(--background); padding: 0.75rem 1rem; border-radius: 8px; border: 1px solid var(--border);">
                        <strong>${persona.name}</strong><br>
                        <small style="color: var(--text-light);">${persona.age}, ${persona.occupation}</small>
                    </div>`;
                });
                
                preview += `</div></div>`;
                document.getElementById('participants-preview').innerHTML = preview;
            }
        }

        // Discussion Simulation
        async function runFocusGroup() {
            showLoading('discussion-results', 'AI participants are engaging in realistic discussion... This may take 3-5 minutes');
            
            const result = await apiCall('/api/run-focus-group');
            
            if (result.success) {
                const summary = `# ✅ Focus Group Discussion Successfully Completed!\\n\\n` +
                    `## Session Overview\\n` +
                    `**Session ID:** ${result.session_id}\\n` +
                    `**Total Conversation Exchanges:** ${result.transcript_length}\\n` +
                    `**Active Participants:** ${result.participants}\\n` +
                    `**Spontaneous Interactions:** ${result.spontaneous_interactions}\\n\\n` +
                    `## Discussion Quality\\n` +
                    `Your AI participants engaged in authentic discussions with realistic group dynamics. ` +
                    `The conversation included natural interruptions, agreements, disagreements, and spontaneous reactions - ` +
                    `just like a real focus group!\\n\\n` +
                    `*The discussion data is now ready for analysis and custom reporting.*`;
                
                showResult('discussion-results', summary);
                enableTab('tab-analysis');
                updateProgress(4);
                
            } else {
                showResult('discussion-results', `❌ Focus group simulation failed: ${result.error}`, true);
            }
        }

        // Summary Generation
        async function generateSummary() {
            const schema = document.getElementById('summary-schema').value;
            
            if (!schema.trim()) {
                showResult('summary-results', '❌ Please describe what you want in your report', true);
                return;
            }
            
            showLoading('summary-results', 'Generating your custom research report...');
            
            const result = await apiCall('/api/generate-summary', {
                summary_schema: schema,
                format_type: document.getElementById('report-style').value
            });
            
            if (result.success) {
                showResult('summary-results', result.summary);
                enableTab('tab-results');
                updateProgress(5);
                
                // Auto-scroll to results
                setTimeout(() => {
                    document.getElementById('tab-results').click();
                }, 3000);
                
            } else {
                showResult('summary-results', `❌ Failed to generate report: ${result.error}`, true);
            }
        }

        // Interactive Q&A
        async function askQuestion() {
            const question = document.getElementById('qa-question').value;
            if (!question.trim()) return;
            
            showLoading('qa-results', 'Analyzing discussion data for insights...');
            
            const result = await apiCall('/api/ask-question', {
                question: question
            });
            
            if (result.success) {
                const formatted = `## 🤔 ${question}\\n\\n${result.answer}`;
                showResult('qa-results', formatted);
            } else {
                showResult('qa-results', `❌ Analysis failed: ${result.error}`, true);
            }
            
            document.getElementById('qa-question').value = '';
        }

        async function getSuggestedQuestions() {
            showLoading('suggested-questions', 'Generating relevant analytical questions...');
            
            const result = await apiCall('/api/suggested-questions');
            
            if (result.success) {
                let html = '<h3 style="color: var(--primary); margin-bottom: 1.5rem;">💡 AI-Suggested Questions</h3>';
                html += '<div style="margin-bottom: 1rem; color: var(--text-light);">Click any question to get instant insights:</div>';
                
                result.suggested_questions.forEach(q => {
                    html += `<div class="question-suggestion" onclick="useQuestion('${q.replace(/'/g, "\\'")}')">❓ ${q}</div>`;
                });
                
                document.getElementById('suggested-questions').innerHTML = html;
            } else {
                showResult('suggested-questions', `❌ ${result.error}`, true);
            }
        }

        function useQuestion(question) {
            document.getElementById('qa-question').value = question;
            askQuestion();
        }

        // Session Management
        async function exportSession() {
            showLoading('qa-results', 'Exporting your complete research session...');
            
            const result = await apiCall('/api/export-session');
            if (result.success) {
                showResult('qa-results', `# ✅ Research Export Complete!\\n\\n` +
                    `Your complete research session has been exported successfully.\\n\\n` +
                    `**Export File:** ${result.filename || 'session_export.json'}\\n\\n` +
                    `**Includes:**\\n` +
                    `• All participant profiles and backgrounds\\n` +
                    `• Complete discussion transcript with natural interactions\\n` +
                    `• Custom analysis and insights\\n` +
                    `• Q&A responses and supporting evidence\\n\\n` +
                    `*Your research data is now ready for presentation or further analysis.*`);
            } else {
                showResult('qa-results', `❌ Export failed: ${result.error}`, true);
            }
        }

        async function viewSessionSummary() {
            const result = await apiCall('/api/session-status');
            if (result.success) {
                const summary = `# 📊 Research Session Summary\\n\\n` +
                    `**Session ID:** ${result.session_id}\\n` +
                    `**Current Stage:** ${result.current_stage}\\n` +
                    `**Completed Steps:** ${result.completed_stages ? result.completed_stages.length : 0}/5\\n` +
                    `**Session Status:** ${result.session_active ? 'Active' : 'Inactive'}\\n\\n` +
                    `*This session contains your complete research workflow and results.*`;
                
                showResult('qa-results', summary);
            }
        }

        async function resetSession() {
            if (confirm('Start a new research session? All current progress will be lost.')) {
                await apiCall('/api/reset-session');
                location.reload();
            }
        }

        // Initialize Application
        window.onload = async function() {
            const result = await apiCall('/api/start-session');
            if (result.success) {
                document.getElementById('session-indicator').innerHTML = 
                    `<div style="background: rgba(255,255,255,0.25); padding: 1rem 2rem; border-radius: 30px; display: inline-block; font-weight: 600; margin-top: 1rem;">⚡ Professional Research Session Active</div>`;
            }
        };

        // Keyboard shortcuts
        document.addEventListener('DOMContentLoaded', function() {
            // Enter key for Q&A
            document.getElementById('qa-question').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') askQuestion();
            });
            
            // Tab navigation with arrow keys
            document.addEventListener('keydown', function(e) {
                if (e.ctrlKey || e.metaKey) {
                    if (e.key === 'ArrowRight') {
                        // Next tab
                        const currentTab = document.querySelector('.nav-tab.active');
                        const nextTab = currentTab.nextElementSibling;
                        if (nextTab && !nextTab.disabled) {
                            nextTab.click();
                        }
                    } else if (e.key === 'ArrowLeft') {
                        // Previous tab
                        const currentTab = document.querySelector('.nav-tab.active');
                        const prevTab = currentTab.previousElementSibling;
                        if (prevTab) {
                            prevTab.click();
                        }
                    }
                }
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the professional web interface"""
    return render_template_string(HTML_TEMPLATE)

# Enhanced API Routes
@app.route('/api/start-session', methods=['POST'])
def start_session():
    """Start new research session"""
    try {
        session_config = request.json or {}
        session_id = orchestrator.start_new_session(session_config)
        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "Professional research session initialized"
        })
    except Exception as e:
        logger.error(f"Session start error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/generate-personas', methods=['POST'])
def generate_personas():
    """Generate personas with natural language output"""
    try {
        data = request.json
        result = orchestrator.step1_generate_personas(
            data.get('persona_description', ''),
            data.get('num_personas', 5),
            data.get('context', 'focus group')
        )
        
        if result["success"]:
            # Add natural language formatting
            result["natural_language"] = format_personas_natural(result)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Persona generation error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/generate-schema', methods=['POST'])
def generate_schema():
    """Generate discussion schema with natural language output"""
    try {
        data = request.json
        result = orchestrator.step2_generate_discussion_schema(
            data.get('topic', ''),
            data.get('discussion_type', 'focus group'),
            data.get('duration_minutes', 60)
        )
        
        if result["success"]:
            # Add natural language formatting
            result["natural_language"] = format_schema_natural(result)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Schema generation error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/run-focus-group', methods=['POST'])
def run_focus_group():
    """Execute focus group simulation"""
    try {
        result = orchestrator.step3_run_focus_group()
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Focus group execution error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/generate-summary', methods=['POST'])
def generate_summary():
    """Generate custom summary"""
    try {
        data = request.json
        result = orchestrator.step4_generate_summary(
            data.get('summary_schema', ''),
            data.get('format_type', 'custom')
        )
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Summary generation error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/ask-question', methods=['POST'])
def ask_question():
    """Interactive Q&A"""
    try {
        data = request.json
        result = orchestrator.step5_ask_question(
            data.get('question', ''),
            data.get('context', 'general')
        )
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Q&A error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/suggested-questions', methods=['POST'])
def suggested_questions():
    """Get AI-suggested questions"""
    try {
        result = orchestrator.get_suggested_questions()
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Suggested questions error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/session-status', methods=['POST'])
def session_status():
    """Get current session status"""
    try {
        result = orchestrator.get_session_status()
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Session status error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/export-session', methods=['POST'])
def export_session():
    """Export session data"""
    try {
        result = orchestrator.export_session_data()
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Export error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reset-session', methods=['POST'])
def reset_session():
    """Reset current session"""
    try {
        orchestrator.reset_session()
        return jsonify({"success": True, "message": "Session reset successfully"})
        
    except Exception as e:
        logger.error(f"Reset error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "session_active": orchestrator.current_session is not None
    })

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )