#!/usr/bin/env python3
"""
Basic Agentic AI Focus Group Workflow - Web Interface
Basic web application for the original main.py entry point
"""

from flask import Flask, request, jsonify, render_template_string
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

# Basic HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic AI Focus Group</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .step {
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px 5px;
        }
        button:hover {
            background: #0056b3;
        }
        textarea, input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin: 10px 0;
        }
        .result {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-top: 10px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Agentic AI Focus Group Workflow</h1>
        
        <div class="step">
            <h3>Step 1: Generate Personas</h3>
            <textarea id="persona-description" placeholder="Describe the type of participants you want (e.g., 'tech-savvy millennials interested in sustainability')"></textarea>
            <input type="number" id="num-personas" placeholder="Number of personas" value="5" min="1" max="10">
            <button onclick="generatePersonas()">Generate Personas</button>
            <div id="personas-result" class="result"></div>
        </div>

        <div class="step">
            <h3>Step 2: Create Discussion Schema</h3>
            <textarea id="discussion-topic" placeholder="Enter the discussion topic"></textarea>
            <input type="number" id="duration" placeholder="Duration in minutes" value="60" min="15" max="180">
            <button onclick="generateSchema()">Create Schema</button>
            <div id="schema-result" class="result"></div>
        </div>

        <div class="step">
            <h3>Step 3: Run Focus Group</h3>
            <button onclick="runFocusGroup()">Start Focus Group Simulation</button>
            <div id="focus-group-result" class="result"></div>
        </div>

        <div class="step">
            <h3>Step 4: Generate Summary</h3>
            <textarea id="summary-schema" placeholder="Describe what kind of summary you want"></textarea>
            <button onclick="generateSummary()">Generate Summary</button>
            <div id="summary-result" class="result"></div>
        </div>

        <div class="step">
            <h3>Step 5: Ask Questions</h3>
            <textarea id="question" placeholder="Ask a question about the focus group results"></textarea>
            <button onclick="askQuestion()">Ask Question</button>
            <div id="question-result" class="result"></div>
        </div>
    </div>

    <script>
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

        async function generatePersonas() {
            const description = document.getElementById('persona-description').value;
            const numPersonas = parseInt(document.getElementById('num-personas').value);
            
            document.getElementById('personas-result').innerHTML = 'Generating personas...';
            
            const result = await apiCall('/api/generate-personas', {
                persona_description: description,
                num_personas: numPersonas
            });
            
            document.getElementById('personas-result').innerHTML = 
                result.success ? JSON.stringify(result, null, 2) : `Error: ${result.error}`;
        }

        async function generateSchema() {
            const topic = document.getElementById('discussion-topic').value;
            const duration = parseInt(document.getElementById('duration').value);
            
            document.getElementById('schema-result').innerHTML = 'Creating schema...';
            
            const result = await apiCall('/api/generate-schema', {
                topic: topic,
                duration_minutes: duration
            });
            
            document.getElementById('schema-result').innerHTML = 
                result.success ? JSON.stringify(result, null, 2) : `Error: ${result.error}`;
        }

        async function runFocusGroup() {
            document.getElementById('focus-group-result').innerHTML = 'Running focus group simulation...';
            
            const result = await apiCall('/api/run-focus-group');
            
            document.getElementById('focus-group-result').innerHTML = 
                result.success ? JSON.stringify(result, null, 2) : `Error: ${result.error}`;
        }

        async function generateSummary() {
            const schema = document.getElementById('summary-schema').value;
            
            document.getElementById('summary-result').innerHTML = 'Generating summary...';
            
            const result = await apiCall('/api/generate-summary', {
                summary_schema: schema
            });
            
            document.getElementById('summary-result').innerHTML = 
                result.success ? JSON.stringify(result, null, 2) : `Error: ${result.error}`;
        }

        async function askQuestion() {
            const question = document.getElementById('question').value;
            
            document.getElementById('question-result').innerHTML = 'Processing question...';
            
            const result = await apiCall('/api/ask-question', {
                question: question
            });
            
            document.getElementById('question-result').innerHTML = 
                result.success ? JSON.stringify(result, null, 2) : `Error: ${result.error}`;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the basic web interface"""
    return render_template_string(HTML_TEMPLATE)

# Basic API Routes
@app.route('/api/generate-personas', methods=['POST'])
def generate_personas():
    """Generate personas"""
    try:
        data = request.json
        result = orchestrator.step1_generate_personas(
            data.get('persona_description', ''),
            data.get('num_personas', 5),
            data.get('context', 'focus group')
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Persona generation error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/generate-schema', methods=['POST'])
def generate_schema():
    """Generate discussion schema"""
    try:
        data = request.json
        result = orchestrator.step2_generate_discussion_schema(
            data.get('topic', ''),
            data.get('discussion_type', 'focus group'),
            data.get('duration_minutes', 60)
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Schema generation error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/run-focus-group', methods=['POST'])
def run_focus_group():
    """Execute focus group simulation"""
    try:
        result = orchestrator.step3_run_focus_group()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Focus group execution error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/generate-summary', methods=['POST'])
def generate_summary():
    """Generate custom summary"""
    try:
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
    try:
        data = request.json
        result = orchestrator.step5_ask_question(
            data.get('question', ''),
            data.get('context', 'general')
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Q&A error: {e}")
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