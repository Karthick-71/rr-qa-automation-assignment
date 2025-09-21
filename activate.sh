#!/bin/bash
# Activation script for RR QA Automation Assignment

echo "🚀 Activating RR QA Automation Assignment Environment"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/pyvenv.cfg" ] || ! python -c "import pytest" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    playwright install
    echo "✅ Dependencies installed"
fi

echo "✅ Environment ready!"
echo ""
echo "Available commands:"
echo "  pytest tests/ui/ -v                    # Run UI tests"
echo "  pytest tests/api/ -v                   # Run API tests"
echo "  pytest tests/ -v                       # Run all tests"
echo "  pytest tests/ui/test_filtering.py -v   # Run specific test file"
echo "  pytest --html=reports/html/report.html --self-contained-html  # Generate HTML report"
echo ""
echo "Happy testing! 🎯"
