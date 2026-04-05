# Financial Approval Agent

Autonomous AI agent that processes invoices and makes approval decisions using multi-step reasoning — no human intervention required at each step.

## What it does
- Verifies department budget availability against real ERP data
- Determines required approval level based on invoice amount
- Analyzes financial risk using LLM reasoning
- Issues final decision: Approved, Rejected, or Pending CFO Review
- Provides full traceability of every decision step

## How it works
Invoice submitted  
↓  
Node 1: Budget check ← verifies available budget  
↓  
Node 2: Approval level ← applies business rules  
↓  
Node 3: Risk analysis ← LLM evaluates risk  
↓  
Node 4: Final decision ← LLM generates recommendation  
↓  
Decision with full audit trail

## Architecture
- **LangGraph** — multi-step agent with persistent state across nodes
- **LangChain** — LLM orchestration and prompt management
- **OpenAI GPT-3.5** — language model for risk analysis and decisions
- **Streamlit** — web interface with real-time decision display

## Key difference from a RAG chatbot
A RAG assistant answers questions. This agent executes a decision workflow autonomously — each node does one thing, passes state to the next, and the final output includes full reasoning traceability.

## How to run
1. Clone the repo
2. Create virtual environment and install dependencies
3. pip install -r requirements.txt
4. Add your OpenAI API key to a `.env` file OPENAI_API_KEY=your-key-here
5. Run the agent from terminal - python agent.py
6. Or launch the web interface - streamlit run app.py

## Next steps
- Add conditional routing: skip risk analysis if budget is zero
- Connect to real D365 data via Dataverse API
- Add human-in-the-loop for CFO approval step
- Implement audit log to database

## Stack
Python · LangGraph · LangChain · OpenAI API · Streamlit
