#!/bin/bash

echo "Setting up browser-use web agent project..."

# Check Python version
echo "Checking Python version..."
python3 --version

# Check if Python 3.8+ is available
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    echo "❌ Error: Python 3.8 or higher is required"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt

# Install playwright browsers
echo "Installing Playwright browsers..."
playwright install

# Install patchright browsers (fixes browser compatibility issues)
echo "Installing patchright browsers for browser-use compatibility..."
python -m patchright install

# Create .env file template if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file template..."
    cat > .env << 'EOF'
# OpenAI API Key - Replace with your actual key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: OpenAI Model (defaults to gpt-4o-mini)
# OPENAI_MODEL=gpt-4o-mini
EOF
    echo "⚠️  Created .env file template - please edit it with your actual OpenAI API key"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the agent: python main.py"
echo ""
echo "🔧 Dependencies installed:"
echo "- browser-use (web automation)"
echo "- OpenAI client"
echo "- Playwright browsers"
echo "- Patchright browsers (for compatibility)"
echo ""
echo "📚 See QUICK_START.md for more detailed instructions" 