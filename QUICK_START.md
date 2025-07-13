# Browser-Use Testing Setup

This directory contains a test setup for the `browser-use` package.

## Quick Start

### 1. Set up the environment

Run the setup script to create a virtual environment and install dependencies:

```bash
./setup.sh
```

This will:
- Create a Python virtual environment in `venv/`
- Install all required packages from `requirements.txt`
- Install Playwright browsers

### 2. Configure environment variables

Copy the template file and add your OpenAI API key:

```bash
cp env-template.txt .env
```

Then edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### 3. Activate the virtual environment

```bash
source venv/bin/activate
```

### 4. Run the agent

```bash
python main.py
```

## What the agent does

The agent provides an interactive interface for web automation tasks:
- Takes natural language input from users
- Uses OpenAI function calling to determine when to execute web tasks
- Breaks down complex tasks into manageable steps
- Executes tasks using browser-use for actual web automation
- Supports tasks like searching, shopping, booking, form filling, etc.

## Dependencies

- `browser-use` - Main automation package
- `python-dotenv` - Environment variable management
- `openai` - OpenAI API integration
- `playwright` - Browser automation backend
- `pydantic` - Data validation

## Troubleshooting

### If you get import errors:
Make sure you've activated the virtual environment:
```bash
source venv/bin/activate
```

### If you get OpenAI API errors:
Make sure your `.env` file contains a valid OpenAI API key:
```
OPENAI_API_KEY=sk-your-key-here
```

### If Playwright browsers aren't installed:
Run the playwright install command manually:
```bash
playwright install
``` 