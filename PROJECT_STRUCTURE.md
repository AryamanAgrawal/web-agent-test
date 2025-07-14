# Browser-Use Agent Project Structure

This document explains the organization of the Browser-Use Agent codebase.

## File Structure

```
web-agent-test/
├── main.py                    # Entry point and interactive loop
├── web_agent.py              # Main WebAgent class
├── tools.py                  # Tool definitions and execution
├── config.py                 # Configuration and constants
├── __init__.py               # Package initialization
├── browser-use-test.py       # Original test script (deprecated)
├── browser-use-agent.py      # Original monolithic script (deprecated)
├── requirements.txt          # Python dependencies
├── setup.sh                  # Environment setup script
├── QUICK_START.md           # Getting started guide
├── PROJECT_STRUCTURE.md     # This file
└── venv/                    # Virtual environment
```

## Module Overview

### 1. `main.py`
- **Purpose**: Entry point for the application
- **Key Functions**:
  - `run_agent_loop()`: Main interactive loop
  - `main()`: Application entry point
- **Usage**: `python main.py`

### 2. `web_agent.py`
- **Purpose**: Core agent logic and OpenAI integration
- **Key Components**:
  - `WebAgent` class: Main orchestrator
  - `process_user_input()`: Handles OpenAI function calling
  - `get_system_message()`: Defines agent behavior
- **Dependencies**: `openai`, `tools`, `config`

### 3. `tools.py`
- **Purpose**: Tool definitions and execution logic
- **Key Components**:
  - `WebTools` class: Tool management
  - `analyze_task_requirements()`: Analyzes tasks and identifies required information
  - `execute_web_task()`: Browser automation using browser-use
  - `get_available_tools()`: OpenAI function definitions
  - `execute_tool()`: Tool dispatcher
- **Dependencies**: `browser_use`, `config`

### 4. `config.py`
- **Purpose**: Configuration settings and constants
- **Key Settings**:
  - OpenAI API configuration
  - Browser settings
  - UI messages
  - Error messages
- **Dependencies**: `python-dotenv`

### 5. `__init__.py`
- **Purpose**: Package initialization and exports
- **Exports**: Main classes and configuration constants

## Data Flow

```
User Input → main.py → WebAgent → OpenAI API → analyze_task_requirements → collect_info → execute_web_task → browser-use → Web Browser
```

1. **User Input**: User types command in terminal
2. **main.py**: Captures input and passes to WebAgent
3. **WebAgent**: Processes input using OpenAI function calling
4. **OpenAI API**: Determines which tool to use and with what parameters
5. **analyze_task_requirements**: Analyzes task and identifies required information
6. **Information Collection**: Agent requests missing information from user
7. **execute_web_task**: Executes web task with complete information
8. **browser-use**: Performs actual browser automation
9. **Web Browser**: Executes the web task

### Enhanced Workflow

The agent now follows a two-phase approach:

**Phase 1: Task Analysis**
- Analyzes user request to identify task type
- Lists required steps for completion
- Identifies information needed from user
- Asks user for missing information

**Phase 2: Task Execution**
- Executes web task with complete information
- Follows predefined steps for task completion
- Provides feedback on progress and results

## Key Design Principles

### 1. **Separation of Concerns**
- Configuration isolated in `config.py`
- Tool logic separated from agent logic
- UI/interaction logic in `main.py`

### 2. **Modular Architecture**
- Each module has a single responsibility
- Clear interfaces between modules
- Easy to extend with new tools

### 3. **Error Handling**
- Centralized error messages in config
- Graceful error handling at each layer
- User-friendly error reporting

### 4. **Type Safety**
- Type hints throughout codebase
- Proper typing for OpenAI API integration
- Clear function signatures

## Adding New Tools

To add a new tool:

1. **Define the tool** in `tools.py`:
   ```python
   async def new_tool(self, param1: str, param2: int) -> str:
       # Implementation
       pass
   ```

2. **Add to tool definitions** in `get_available_tools()`:
   ```python
   {
       "type": "function",
       "function": {
           "name": "new_tool",
           "description": "...",
           "parameters": {...}
       }
   }
   ```

3. **Add to dispatcher** in `execute_tool()`:
   ```python
   elif tool_name == "new_tool":
       return await self.new_tool(tool_args["param1"], tool_args["param2"])
   ```

## Configuration

Environment variables in `.env`:
```
OPENAI_API_KEY=your_api_key_here
```

All other configuration is in `config.py`.

## Testing

Run the agent:
```bash
source venv/bin/activate
python main.py
```

Example interactions:

**Simple Search (Direct execution):**
- User: "Search Google for Python tutorials"
- Agent: [Executes search directly]

**Complex Task (Analysis → Information gathering → Execution):**
- User: "Buy a basketball on Amazon"
- Agent: [Analyzes requirements] → "I need to know: budget, preferred brand, size, shipping address, payment method..."
- User: [Provides details]
- Agent: [Executes purchase with complete information]

**Booking Task:**
- User: "Book a flight from NYC to LA"
- Agent: [Analyzes requirements] → "I need: departure date, return date, departure time preference, number of passengers, budget, airline preference..."
- User: [Provides travel details]
- Agent: [Executes booking with complete information]

**Status Check:**
- User: "What's your status?"
- Agent: [Returns current status] 