# web-agent-test
test repository for a web ai agent

# Goal
- Build a general-purpose browsing agent that can navigate websites and perform user requested tasks autonomously. 

- Your agent should be capable of handling common web interactions like ‘buying a basketball on amazon’, ‘booking a flight’, ‘booking a restaurant reservation’, etc. 

- The core challenge is designing a system that can reliably accomplish web-based tasks. 

- You may use any programming language and frameworks of your choice. This should be scoped to less than a day of work

# Interpretation:

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

FoundationModel CUA (Build)

Pros
- Native API support
- Custom Abstraction over the API

Cons
- Limits to Single Model Proivder
- Overhead of building the Abstraction
- Hard to make reliable

browser-use (Buy)



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


Decisions:
- Use browser-use
- Not use browser-use custom functions for this implements
    - This leaves room for us to customize our agent and not be bound to the browser-use schema
    - We want the agent to be our agent not a browser-use agent


