#!/bin/bash

echo "Setting up virtual environment for browser-use testing..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install playwright browsers
playwright install

echo "Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "source venv/bin/activate"
echo ""
echo "To run the test, make sure you have your OpenAI API key in .env file and run:"
echo "python browser-use-test.py" 