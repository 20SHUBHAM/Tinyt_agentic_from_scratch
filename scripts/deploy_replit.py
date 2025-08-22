#!/usr/bin/env python3
"""
Replit deployment helper script
Validates configuration and prepares for Replit deployment
"""

import os
import sys
import json
from typing import Dict, Any

def check_replit_environment() -> Dict[str, Any]:
    """Check if running in Replit environment"""
    
    replit_indicators = {
        "REPL_ID": os.getenv("REPL_ID"),
        "REPL_OWNER": os.getenv("REPL_OWNER"), 
        "REPL_SLUG": os.getenv("REPL_SLUG"),
        "REPLIT_DB_URL": os.getenv("REPLIT_DB_URL")
    }
    
    is_replit = any(replit_indicators.values())
    
    return {
        "is_replit": is_replit,
        "indicators": replit_indicators,
        "environment": "Replit" if is_replit else "Local"
    }

def validate_replit_secrets() -> Dict[str, Any]:
    """Validate required secrets are set in Replit"""
    
    required_secrets = [
        "OPENAI_API_KEY"
    ]
    
    optional_secrets = [
        "OPENAI_MODEL",
        "FLASK_SECRET_KEY",
        "FLASK_DEBUG"
    ]
    
    missing_required = []
    missing_optional = []
    
    for secret in required_secrets:
        if not os.getenv(secret):
            missing_required.append(secret)
    
    for secret in optional_secrets:
        if not os.getenv(secret):
            missing_optional.append(secret)
    
    return {
        "valid": len(missing_required) == 0,
        "missing_required": missing_required,
        "missing_optional": missing_optional,
        "configured_secrets": [s for s in required_secrets + optional_secrets if os.getenv(s)]
    }

def check_dependencies() -> Dict[str, Any]:
    """Check if all dependencies are available"""
    
    required_packages = [
        "tinytroupe",
        "openai", 
        "flask",
        "python-dotenv"
    ]
    
    available = []
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            available.append(package)
        except ImportError:
            missing.append(package)
    
    return {
        "all_available": len(missing) == 0,
        "available": available,
        "missing": missing
    }

def generate_replit_instructions() -> str:
    """Generate deployment instructions for Replit"""
    
    return """
🚀 Replit Deployment Instructions
================================

1. IMPORT REPOSITORY:
   - Go to replit.com
   - Click "Create Repl"
   - Choose "Import from GitHub" 
   - Paste your repository URL
   - Click "Import"

2. SET ENVIRONMENT VARIABLES:
   - Click on "Secrets" tab (🔒 icon in sidebar)
   - Add these secrets:
     * OPENAI_API_KEY = your_openai_api_key_here
     * FLASK_SECRET_KEY = any_random_string_here
     * OPENAI_MODEL = gpt-4 (optional, defaults to gpt-4)

3. CONFIGURE REPLIT:
   - Replit should auto-detect the configuration from .replit file
   - If not, set:
     * Language: Python
     * Run command: python main.py

4. DEPLOY:
   - Click the "Run" button
   - Replit will install dependencies automatically
   - Your app will be available at the generated URL

5. VERIFY DEPLOYMENT:
   - Check that the web interface loads
   - Test the health endpoint: /health
   - Try generating personas to verify OpenAI integration

6. TROUBLESHOOTING:
   - Check the console for error messages
   - Verify your OpenAI API key is valid and has credits
   - Ensure all secrets are set correctly
   - Check the logs in the Replit console

🎯 Your app will be live at: https://your-repl-name.your-username.repl.co
"""

def main():
    """Main deployment validation function"""
    
    print("🔍 Replit Deployment Validation")
    print("=" * 40)
    
    # Check environment
    env_check = check_replit_environment()
    print(f"📍 Environment: {env_check['environment']}")
    
    if env_check["is_replit"]:
        print("✅ Running in Replit environment")
        print(f"   Repl ID: {env_check['indicators']['REPL_ID']}")
        print(f"   Owner: {env_check['indicators']['REPL_OWNER']}")
    else:
        print("ℹ️  Not running in Replit (local development)")
    
    # Check secrets/environment variables
    print("\n🔐 Checking Environment Variables...")
    secrets_check = validate_replit_secrets()
    
    if secrets_check["valid"]:
        print("✅ All required secrets configured")
    else:
        print("❌ Missing required secrets:")
        for secret in secrets_check["missing_required"]:
            print(f"   - {secret}")
    
    if secrets_check["missing_optional"]:
        print("⚠️  Missing optional secrets (will use defaults):")
        for secret in secrets_check["missing_optional"]:
            print(f"   - {secret}")
    
    # Check dependencies
    print("\n📦 Checking Dependencies...")
    deps_check = check_dependencies()
    
    if deps_check["all_available"]:
        print("✅ All dependencies available")
    else:
        print("❌ Missing dependencies:")
        for dep in deps_check["missing"]:
            print(f"   - {dep}")
        print("Run: pip install -r requirements.txt")
    
    # Overall status
    print("\n📊 Deployment Readiness:")
    
    all_checks_passed = (
        secrets_check["valid"] and 
        deps_check["all_available"]
    )
    
    if all_checks_passed:
        print("✅ Ready for deployment!")
        
        if not env_check["is_replit"]:
            print("\n" + generate_replit_instructions())
        else:
            print("🚀 You can now run your application!")
            print("   Click the 'Run' button or execute: python main.py")
    else:
        print("❌ Not ready for deployment")
        print("   Please fix the issues above and run this script again")
    
    # Create deployment summary
    summary = {
        "timestamp": "2024-01-01T00:00:00Z",  # Will be updated in real deployment
        "environment": env_check["environment"],
        "secrets_valid": secrets_check["valid"],
        "dependencies_available": deps_check["all_available"],
        "deployment_ready": all_checks_passed,
        "missing_requirements": {
            "secrets": secrets_check["missing_required"],
            "dependencies": deps_check["missing"]
        }
    }
    
    # Save summary
    with open("deployment_check.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n💾 Deployment check saved to: deployment_check.json")
    
    return all_checks_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)