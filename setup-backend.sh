#!/bin/bash

# SchoolsGate Backend Setup Script
echo "🚀 Setting up SchoolsGate Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r backend/requirements.txt

# Initialize database
echo "🗄️ Initializing database..."
python backend/run.py

echo "✅ Backend setup complete!"
echo "🎯 To start the backend server:"
echo "   source venv/bin/activate"
echo "   python backend/run.py"
echo ""
echo "📊 API will be available at: http://localhost:5000"
