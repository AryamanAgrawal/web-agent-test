# web-agent-test

For Project Structure: `./PROJECT_STRUCTURE.md`
For Quick Start Instructions: `QUICK_START.md`

# Input Instructions
Provide all input in one single string.

# Test Credentials for Tasks

Fake Credit Card:
`5555 5555 5555 4444; Exp: 06/27; CVV: 567`

Fake Address:
`Jamie Lee, 918 Broderick Street Apt 3B, San Francisco, CA 94115, USA, +1 (415) 555-0198`

Login:
- Gmail
- Google
- Amazon

Tested Commands:

- Go to Google Flights and Book me a flight to Amsterdam
- Go to Amazon and buy me the book: Letters to a Young Poet

# Open Questions/Follow-up Items:
- Would like to add sensitive data handling for Credentials (https://docs.browser-use.com/customize/sensitive-data)
    - We'd probably like to fetch these from a file rather than have the user input these
- Configure Browser Context
- Human in the loop element
    - Currently the application is architechted as a human-in-the-loop this human input can be replaced by interactions with another agent that is checking this agent's work
    - The human in the loop element can be architected using API endpoints supplied in functions that can prompt the user to enter further details if needed
- Add Structured Output to the browser-use output so that the next agent call can study it and verify the outcome of the call
- Memory caching to learn from previous mistakes or address edge cases
- Connections with other agents that help improvise over time
- Failure mode detection
- Structured schema for outputs with browser-use
- Custom functions with browser-use for in-depth steering
- System prompt injection browser-use


- No more human in the loop
    - Add Agents with the right context (metadata access, or user info access)
    - Guidance Agent 
        - Come up with next steps if something goes wrong
        - Validation
    - Over time data monitoring and learning from mistakes
        - Memory caching to learn from previous mistakes or address edge cases
    - Checks and Balances Agent

# Goal
- Build a general-purpose browsing agent that can navigate websites and perform user requested tasks autonomously. 

- Your agent should be capable of handling common web interactions like ‘buying a basketball on amazon’, ‘booking a flight’, ‘booking a restaurant reservation’, etc. 

- The core challenge is designing a system that can reliably accomplish web-based tasks. 

- You may use any programming language and frameworks of your choice. This should be scoped to less than a day of work

# Interpretation:

- Aiming for a demo-able POC that can serve as the building block for a productionizable web agent to be deployed at scalein out application

- Action-first web agent rather than an information-retrieval-first agent

- Should be able to navigate relatively complex tasks:
    - Go to Amazon
    - Find the best product fitting my description
    - Add the product to cart
    - Checkout
    - Ask for the information needed to order the product
    - Add payment information
    - Order the product

# Initial approach:
    - Build an agent loop that has access to tools
    - Action planning tool
    - Web Step Execution tool
    - Each tool should append state to the conversation history
    - Each task should have a finish parameter
    - Each task execution should end with a successful reply to the user


# Decisions:
- Use browser-use
- Not use browser-use custom functions for this implements
    - This leaves room for us to customize our agent and not be bound to the browser-use schema
    - We want the agent to be our agent not a browser-use agent
- Ask the user for validations or places where the browser agent gets stuck
    - For the scope of this project this is probably the best UX
    - A fully automated agent isn't that hard to achieve after this
        - It will probably need new tools to query data needed to run its tasks


# Questions to answer:
    - What Web API to use?
        - Choices: OpenAI, browser-use    
    - Do we need memory cache for state management?

# Possible Answers on Build vs Buy

- After testing the browser-use package, and reading the OpenAI computer use API documentation my leaning is towards using browser-use because our use-case is general
- OpenAI's API is arguable less reliable and we'd have to instrument more step-wise functionality
- The pros would be cost benefits, customizability, 
- Since, we're making a general-use agent, this seems like a moot effort
- If we were making an agent that was oriented towards a more specific use-case like scanning documents on Google Sheets in a very specific manner. 

## FoundationModel CUA (Build):

```
### Pros
- Native API support
- Custom Abstraction over the API

Cons
- Limits to Single Model Proivder
- Overhead of building the Abstraction
- Hard to make reliable
```

browser-use (Buy)
```
Pros
- Dedicated support and team building to enhance abstraction
- Multi-model support
- Built-in
  - Abstractions
  - Step-wise execution
  - Validation step
  - Quick setup
  - Quick deployment
- Small enterprise easy to secure better deal
- Used at scale with big enterprises: Proof of scale
- Observability
- Evals

Cons
- Cost-ineffective (likely to go down as they grow)
- Latency
- Adds a point of failure to our dependency
- Adds an additional sub-processor to user data
- Don't mention security
```
