#!/bin/bash

# Setup script for Agentic AI Focus Group Workflow

echo "🚀 Setting up Agentic AI Focus Group Workflow"
echo "=============================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version detected (>= 3.8 required)"
else
    echo "❌ Python $python_version detected, but >= 3.8 is required"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p cache logs exports tests

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📄 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your OpenAI API key"
else
    echo "✅ .env file already exists"
fi

# Set permissions
echo "🔐 Setting permissions..."
chmod +x scripts/*.sh
chmod +x main.py
chmod +x example_usage.py

# Run tests
echo "🧪 Running tests..."
python tests/test_workflow.py

if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "⚠️  Some tests failed, but setup continues..."
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Run: python main.py"
echo "3. Open http://localhost:5000 in your browser"
echo ""
echo "For Replit deployment:"
echo "1. Import this repository to Replit"
echo "2. Set OPENAI_API_KEY in Replit Secrets"
echo "3. Click Run!"
echo ""
echo "Happy focus grouping! 🎭"