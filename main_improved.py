#!/usr/bin/env python3
"""
Improved Agentic AI Focus Group Workflow - Main Entry Point
Features: Persona editing, Natural language outputs, Professional UI
"""

import os
import sys
import logging
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from improved_web_app import app
from config import Config

def setup_logging():
    """Set up application logging"""
    log_level = logging.DEBUG if Config.FLASK_DEBUG else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(f'app_{datetime.now().strftime("%Y%m%d")}.log')
        ]
    )

def create_directories():
    """Create necessary directories"""
    directories = [
        Config.TINYTROUPE_CACHE_DIR,
        'logs',
        'exports',
        'templates'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directory ready: {directory}")

def main():
    """Main application entry point"""
    print("🚀 Starting Improved Agentic AI Focus Group Workflow")
    print("=" * 60)
    print("✨ Features: Persona Editing, Natural Language Outputs, Professional UI")
    print("=" * 60)
    
    try:
        # Setup
        setup_logging()
        create_directories()
        
        # Validate configuration
        Config.validate()
        print("✅ Configuration validated")
        
        print(f"🌐 Starting professional web interface on port {Config.FLASK_PORT}")
        print(f"🔗 Access the application at: http://localhost:{Config.FLASK_PORT}")
        print("=" * 60)
        print("🎯 Key Improvements:")
        print("   • ✏️  Inline persona editing with click-to-edit functionality")
        print("   • 📝 Natural language outputs instead of JSON")
        print("   • 🎨 Professional business-focused UI design")
        print("   • 📱 Responsive design for all devices")
        print("   • 🚀 Smooth tabbed workflow navigation")
        print("=" * 60)
        
        # Start Flask application
        app.run(
            host='0.0.0.0',
            port=Config.FLASK_PORT,
            debug=Config.FLASK_DEBUG
        )
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please check your .env file and ensure all required variables are set.")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()