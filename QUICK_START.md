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

The agent provides an intelligent interface for web automation tasks:
- Takes natural language input from users
- **Maintains browser context** across all tasks in a single session
- **Analyzes tasks** to identify required steps and information
- **Proactively requests** missing information before execution
- Uses OpenAI function calling to determine when to execute web tasks
- Breaks down complex tasks into manageable steps
- Executes tasks using browser-use for actual web automation
- Supports tasks like searching, shopping, booking, form filling, etc.

### Enhanced Workflow

The agent now follows a smart two-phase approach:

1. **Task Analysis Phase**: When you request a complex task (like booking a flight or buying something), the agent will:
   - Analyze what information is needed
   - List the steps required
   - Ask you for any missing details upfront

2. **Task Execution Phase**: Only after gathering all necessary information, the agent will:
   - Execute the web task with complete details
   - Provide progress updates
   - Handle any issues that arise

### Browser Session Management

The agent now maintains browser context throughout your session:

- **Persistent Browser Session**: All web tasks use the same browser session, maintaining:
  - Login states and cookies
  - Shopping carts and session data
  - Previously visited pages and navigation history
  - User preferences and settings

- **Session Configuration**: The browser session is configured with:
  - Stealth mode options
  - Persistent storage for cache and cookies
  - Keep-alive functionality for better performance

### Example Interaction

```
You: Book a flight to Paris
Agent: 🔍 Analyzing task requirements...

Task Analysis Complete:
📋 REQUIRED STEPS:
   1. Navigate to airline website or booking platform
   2. Enter departure and destination locations
   3. Select travel dates
   ...

❓ INFORMATION NEEDED FROM USER:
   • Departure city/airport
   • Destination city/airport
   • Departure date
   • Return date (if round trip)
   • Number of passengers
   • Budget range
   ...

Please provide the required information so I can help you complete this task.

You: I want to fly from NYC to Paris on March 15th, returning March 22nd, for 2 passengers, budget under $1000 per person
Agent: 🔧 Calling function: execute_web_task
🌐 Executing web task: Book a flight from NYC to Paris...
Perfect! Now executing your flight booking...

You: Now search for hotels in Paris for the same dates
Agent: [Uses same browser session - maintains any login state from previous booking]
🌐 Executing web task: Search for hotels in Paris...
```

### Important Notes

- The agent will **analyze complex tasks first** and ask for required information
- **Wait for the analysis to complete** before providing additional details
- For simple tasks like searches, the agent will execute directly
- If you encounter any loops or delays, try restarting the agent

### Error Handling & Recovery

The agent now handles failures intelligently:

**Authentication Errors**: If a task fails due to login issues, the agent will ask for:
- Account credentials (username/password)
- Two-factor authentication codes
- Account permissions

**Payment Errors**: If a task fails due to payment issues, the agent will ask for:
- Payment method details
- Billing address
- Payment authorization

**Task Failures**: If a task fails for other reasons, the agent will:
- Analyze the specific error
- Ask for additional information to resolve the issue
- Retry the task with the new information using `retry_web_task`

### Example Error Recovery

```
You: Buy a basketball on Amazon
Agent: [Executes task]
❌ AUTHENTICATION_ERROR: Login required to complete purchase

The agent will ask: "Please provide your Amazon login credentials to complete the purchase."

You: My username is john@email.com, password is mypassword123
Agent: [Retries task with credentials]
✅ Task retry successful! Basketball added to cart and purchase completed.
```

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