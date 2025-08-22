from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import logging
from workflow_orchestrator import WorkflowOrchestrator
from config import Config
from datetime import datetime

app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY
CORS(app)

# Initialize workflow orchestrator
orchestrator = WorkflowOrchestrator()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HTML Template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic AI Focus Group Workflow</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f7fa; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; text-align: center; }
        .workflow-step { background: white; border-radius: 10px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .step-header { display: flex; align-items: center; margin-bottom: 20px; }
        .step-number { background: #667eea; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 15px; }
        .step-title { font-size: 1.4em; font-weight: 600; color: #333; }
        .form-group { margin-bottom: 20px; }
        .form-label { display: block; margin-bottom: 8px; font-weight: 500; color: #555; }
        .form-input, .form-textarea { width: 100%; padding: 12px; border: 2px solid #e1e5e9; border-radius: 6px; font-size: 14px; }
        .form-textarea { min-height: 100px; resize: vertical; }
        .btn { background: #667eea; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500; transition: background 0.3s; }
        .btn:hover { background: #5a6fd8; }
        .btn:disabled { background: #ccc; cursor: not-allowed; }
        .btn-secondary { background: #6c757d; }
        .btn-secondary:hover { background: #5a6268; }
        .result-box { background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 6px; padding: 15px; margin-top: 15px; }
        .success { border-left: 4px solid #28a745; background: #f8fff9; }
        .error { border-left: 4px solid #dc3545; background: #fff8f8; }
        .loading { text-align: center; padding: 20px; color: #666; }
        .persona-card { background: #f8f9fa; border-radius: 6px; padding: 15px; margin: 10px 0; border-left: 4px solid #667eea; }
        .qa-section { margin-top: 20px; }
        .question-item { background: #e3f2fd; padding: 10px; margin: 5px 0; border-radius: 4px; cursor: pointer; }
        .question-item:hover { background: #bbdefb; }
        .status-indicator { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }
        .status-completed { background: #28a745; }
        .status-active { background: #ffc107; }
        .status-pending { background: #6c757d; }
        .json-viewer { background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 6px; font-family: 'Courier New', monospace; font-size: 12px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Agentic AI Focus Group Workflow</h1>
            <p>Dynamic, Multi-Agent Group Discussion Simulation</p>
            <div id="session-status"></div>
        </div>

        <!-- Step 1: Persona Generation -->
        <div class="workflow-step">
            <div class="step-header">
                <div class="step-number">1</div>
                <div class="step-title">Dynamic Persona Creation</div>
            </div>
            
            <div class="form-group">
                <label class="form-label">Describe your desired participants:</label>
                <textarea id="persona-description" class="form-textarea" 
                    placeholder="e.g., College students in India, Gen Z, who are enthusiastic about fitness apps">College students in India, Gen Z, who are enthusiastic about fitness apps</textarea>
            </div>
            
            <div class="form-group">
                <label class="form-label">Number of personas:</label>
                <input type="number" id="num-personas" class="form-input" value="5" min="3" max="8">
            </div>
            
            <button class="btn" onclick="generatePersonas()">Generate Personas</button>
            <div id="persona-results"></div>
        </div>

        <!-- Step 2: Discussion Schema -->
        <div class="workflow-step">
            <div class="step-header">
                <div class="step-number">2</div>
                <div class="step-title">Discussion Framework Creation</div>
            </div>
            
            <div class="form-group">
                <label class="form-label">Discussion topic:</label>
                <textarea id="discussion-topic" class="form-textarea" 
                    placeholder="e.g., Challenges in adopting fitness apps">Challenges in adopting fitness apps</textarea>
            </div>
            
            <div class="form-group">
                <label class="form-label">Duration (minutes):</label>
                <input type="number" id="duration" class="form-input" value="60" min="30" max="120">
            </div>
            
            <button class="btn" onclick="generateSchema()" disabled id="schema-btn">Generate Discussion Framework</button>
            <div id="schema-results"></div>
        </div>

        <!-- Step 3: Focus Group Execution -->
        <div class="workflow-step">
            <div class="step-header">
                <div class="step-number">3</div>
                <div class="step-title">Dynamic Focus Group Simulation</div>
            </div>
            
            <p>Execute the focus group discussion with your generated personas and framework.</p>
            <button class="btn" onclick="runFocusGroup()" disabled id="discussion-btn">Run Focus Group Discussion</button>
            <div id="discussion-results"></div>
        </div>

        <!-- Step 4: Custom Summary -->
        <div class="workflow-step">
            <div class="step-header">
                <div class="step-number">4</div>
                <div class="step-title">Custom Summary Generation</div>
            </div>
            
            <div class="form-group">
                <label class="form-label">Summary schema (describe what you want):</label>
                <textarea id="summary-schema" class="form-textarea" 
                    placeholder="e.g., Executive Summary, Key Insights, Recommendations, and Verbatim Quotes">Executive Summary, Key Insights, Recommendations, and Verbatim Quotes</textarea>
            </div>
            
            <button class="btn" onclick="generateSummary()" disabled id="summary-btn">Generate Summary</button>
            <div id="summary-results"></div>
        </div>

        <!-- Step 5: Interactive Q&A -->
        <div class="workflow-step">
            <div class="step-header">
                <div class="step-number">5</div>
                <div class="step-title">Interactive Q&A</div>
            </div>
            
            <div class="form-group">
                <label class="form-label">Ask questions about your discussion:</label>
                <input type="text" id="qa-question" class="form-input" 
                    placeholder="e.g., Who was the most positive? What common barriers emerged?">
            </div>
            
            <button class="btn" onclick="askQuestion()" disabled id="qa-btn">Ask Question</button>
            <button class="btn btn-secondary" onclick="getSuggestedQuestions()" disabled id="suggest-btn">Get Suggested Questions</button>
            
            <div id="suggested-questions"></div>
            <div id="qa-results"></div>
        </div>

        <!-- Session Management -->
        <div class="workflow-step">
            <div class="step-header">
                <div class="step-number">📊</div>
                <div class="step-title">Session Management</div>
            </div>
            
            <button class="btn btn-secondary" onclick="getSessionStatus()">View Session Status</button>
            <button class="btn btn-secondary" onclick="exportSession()">Export Session Data</button>
            <button class="btn btn-secondary" onclick="resetSession()">Reset Session</button>
            
            <div id="session-management-results"></div>
        </div>
    </div>

    <script>
        let sessionActive = false;

        // Initialize session on page load
        window.onload = function() {
            startNewSession();
        };

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

        function showLoading(elementId) {
            document.getElementById(elementId).innerHTML = '<div class="loading">🤖 Processing...</div>';
        }

        function showResult(elementId, result, isError = false) {
            const className = isError ? 'result-box error' : 'result-box success';
            const content = typeof result === 'object' ? JSON.stringify(result, null, 2) : result;
            document.getElementById(elementId).innerHTML = 
                `<div class="${className}"><pre>${content}</pre></div>`;
        }

        async function startNewSession() {
            const result = await apiCall('/api/start-session');
            if (result.success) {
                sessionActive = true;
                updateSessionStatus();
            }
        }

        async function generatePersonas() {
            showLoading('persona-results');
            
            const result = await apiCall('/api/generate-personas', {
                persona_description: document.getElementById('persona-description').value,
                num_personas: parseInt(document.getElementById('num-personas').value)
            });
            
            if (result.success) {
                showResult('persona-results', result);
                document.getElementById('schema-btn').disabled = false;
                
                // Display personas in a user-friendly way
                let personaHtml = '<h4>Generated Personas:</h4>';
                result.personas.forEach(persona => {
                    personaHtml += `
                        <div class="persona-card">
                            <strong>${persona.name}</strong> (${persona.age}, ${persona.occupation})<br>
                            <small>${persona.background}</small>
                        </div>
                    `;
                });
                document.getElementById('persona-results').innerHTML = personaHtml;
                
            } else {
                showResult('persona-results', result, true);
            }
        }

        async function generateSchema() {
            showLoading('schema-results');
            
            const result = await apiCall('/api/generate-schema', {
                topic: document.getElementById('discussion-topic').value,
                duration_minutes: parseInt(document.getElementById('duration').value)
            });
            
            if (result.success) {
                showResult('schema-results', result);
                document.getElementById('discussion-btn').disabled = false;
            } else {
                showResult('schema-results', result, true);
            }
        }

        async function runFocusGroup() {
            showLoading('discussion-results');
            
            const result = await apiCall('/api/run-focus-group');
            
            if (result.success) {
                showResult('discussion-results', result);
                document.getElementById('summary-btn').disabled = false;
                document.getElementById('qa-btn').disabled = false;
                document.getElementById('suggest-btn').disabled = false;
            } else {
                showResult('discussion-results', result, true);
            }
        }

        async function generateSummary() {
            showLoading('summary-results');
            
            const result = await apiCall('/api/generate-summary', {
                summary_schema: document.getElementById('summary-schema').value
            });
            
            if (result.success) {
                showResult('summary-results', result);
            } else {
                showResult('summary-results', result, true);
            }
        }

        async function askQuestion() {
            const question = document.getElementById('qa-question').value;
            if (!question.trim()) return;
            
            showLoading('qa-results');
            
            const result = await apiCall('/api/ask-question', {
                question: question
            });
            
            if (result.success) {
                showResult('qa-results', result);
            } else {
                showResult('qa-results', result, true);
            }
            
            // Clear question input
            document.getElementById('qa-question').value = '';
        }

        async function getSuggestedQuestions() {
            showLoading('suggested-questions');
            
            const result = await apiCall('/api/suggested-questions');
            
            if (result.success) {
                let questionsHtml = '<h4>Suggested Questions:</h4>';
                result.suggested_questions.forEach(q => {
                    questionsHtml += `<div class="question-item" onclick="useQuestion('${q.replace(/'/g, "\\'")}')">${q}</div>`;
                });
                document.getElementById('suggested-questions').innerHTML = questionsHtml;
            } else {
                showResult('suggested-questions', result, true);
            }
        }

        function useQuestion(question) {
            document.getElementById('qa-question').value = question;
        }

        async function getSessionStatus() {
            const result = await apiCall('/api/session-status');
            showResult('session-management-results', result);
        }

        async function exportSession() {
            const result = await apiCall('/api/export-session');
            showResult('session-management-results', result);
        }

        async function resetSession() {
            if (confirm('Are you sure you want to reset the session? All progress will be lost.')) {
                const result = await apiCall('/api/reset-session');
                if (result.success) {
                    location.reload();
                }
            }
        }

        function updateSessionStatus() {
            document.getElementById('session-status').innerHTML = 
                sessionActive ? '<span class="status-indicator status-active"></span>Session Active' : 
                '<span class="status-indicator status-pending"></span>No Session';
        }

        // Allow Enter key for question input
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('qa-question').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    askQuestion();
                }
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/start-session', methods=['POST'])
def start_session():
    """Start a new workflow session"""
    try:
        session_config = request.json or {}
        session_id = orchestrator.start_new_session(session_config)
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "New session started successfully"
        })
    except Exception as e:
        logger.error(f"Session start error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/generate-personas', methods=['POST'])
def generate_personas():
    """Step 1: Generate personas"""
    try:
        data = request.json
        persona_description = data.get('persona_description', '')
        num_personas = data.get('num_personas', 5)
        context = data.get('context', 'focus group')
        
        result = orchestrator.step1_generate_personas(persona_description, num_personas, context)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Persona generation error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/refine-personas', methods=['POST'])
def refine_personas():
    """Refine personas based on user feedback"""
    try:
        data = request.json
        user_feedback = data.get('feedback', '')
        
        result = orchestrator.step1_refine_personas(user_feedback)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Persona refinement error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/generate-schema', methods=['POST'])
def generate_schema():
    """Step 2: Generate discussion schema"""
    try:
        data = request.json
        topic = data.get('topic', '')
        discussion_type = data.get('discussion_type', 'focus group')
        duration_minutes = data.get('duration_minutes', 60)
        
        result = orchestrator.step2_generate_discussion_schema(topic, discussion_type, duration_minutes)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Schema generation error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/customize-schema', methods=['POST'])
def customize_schema():
    """Customize discussion schema"""
    try:
        data = request.json
        modifications = data.get('modifications', '')
        
        result = orchestrator.step2_customize_schema(modifications)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Schema customization error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/run-focus-group', methods=['POST'])
def run_focus_group():
    """Step 3: Execute focus group discussion"""
    try:
        data = request.json or {}
        additional_config = data.get('config', {})
        
        result = orchestrator.step3_run_focus_group(additional_config)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Focus group execution error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/generate-summary', methods=['POST'])
def generate_summary():
    """Step 4: Generate custom summary"""
    try:
        data = request.json
        summary_schema = data.get('summary_schema', '')
        format_type = data.get('format_type', 'custom')
        
        result = orchestrator.step4_generate_summary(summary_schema, format_type)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Summary generation error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/ask-question', methods=['POST'])
def ask_question():
    """Step 5: Interactive Q&A"""
    try:
        data = request.json
        question = data.get('question', '')
        context = data.get('context', 'general')
        
        result = orchestrator.step5_ask_question(question, context)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Q&A error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/suggested-questions', methods=['POST'])
def suggested_questions():
    """Get AI-suggested questions"""
    try:
        result = orchestrator.get_suggested_questions()
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Suggested questions error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/session-status', methods=['POST'])
def session_status():
    """Get current session status"""
    try:
        result = orchestrator.get_session_status()
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Session status error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/export-session', methods=['POST'])
def export_session():
    """Export session data"""
    try:
        data = request.json or {}
        format_type = data.get('format', 'json')
        
        result = orchestrator.export_session_data(format_type)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Export error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reset-session', methods=['POST'])
def reset_session():
    """Reset current session"""
    try:
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