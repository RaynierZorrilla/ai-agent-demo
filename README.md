# Financial AI Agent API

A modular AI agent prototype built with FastAPI and Cohere.

---

## Features

- FastAPI backend
- Cohere LLM integration
- Tool calling
- Short-term memory
- Lightweight retrieval layer
- Structured JSON responses
- Basic logging

---

## Architecture

The system follows a modular architecture:

- API Layer: receives requests and returns structured responses
- Service Layer: orchestrates the agent workflow
- Tool Layer: executes deterministic Python functions
- Memory Layer: stores recent user interactions
- Knowledge Layer: retrieves relevant financial context

---

## Agent Flow

1. The user sends financial data
2. The agent reviews recent memory
3. The LLM decides which tools should be used
4. Python executes the selected tools
5. The system retrieves relevant financial knowledge
6. The LLM generates a structured final response

---

## Example Request

```json
{
  "user_id": "raynier",
  "income": 3000,
  "expenses": 2900,
  "debt": 12000
}
```

---

## Example Response

```json
{
  "risk_level": "high",
  "summary": "Your current financial situation indicates a high risk level due to high debt and low monthly savings.",
  "recommendation": "Focus on reducing debt and building an emergency fund."
}
```

---

## Run Locally

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Open API Docs

```text
http://127.0.0.1:8000/docs
```

---

## Environment Variables

Create a `.env` file:

```env
COHERE_API_KEY=your_cohere_api_key_here
```

---

## Future Improvements

In production, this system could be improved with:

- Persistent memory using PostgreSQL
- Vector search using embeddings
- Authentication and rate limiting
- Background queues
- Better observability and tracing
- Automated evaluation pipelines
- Unit and integration testing
- Docker deployment