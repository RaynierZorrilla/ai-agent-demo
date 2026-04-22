# AI Agent FastAPI

A demo [FastAPI](https://fastapi.tiangolo.com/) API that accepts a simple financial profile (income, expenses, debt) and returns a risk analysis produced by a [Cohere](https://cohere.com/) chat model.

## Requirements

- Python 3.10 or newer
- A Cohere account and an [API key](https://dashboard.cohere.com/)

## Installation

```bash
cd ai-agent-fastapi
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file at the project root (do not commit it; it is listed in `.gitignore`):

```env
COHERE_API_KEY=your_key_here
```

## Run the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Interactive docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Endpoints

| Method | Path       | Description                    |
| ------ | ---------- | ------------------------------ |
| `GET`  | `/`        | Health check.                  |
| `POST` | `/analyze` | Analyze the JSON request body. |

### `POST /analyze`

**Request body (JSON)** — all values must be greater than 0:

| Field      | Type   | Description                    |
| ---------- | ------ | ------------------------------ |
| `income`   | number | Monthly income                 |
| `expenses` | number | Monthly expenses               |
| `debt`     | number | Monthly debt payments          |

**Response** — JSON object with:

| Field            | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| `risk_level`     | Risk level (e.g. `low`, `medium`, `high`, `unknown`)     |
| `summary`        | Short summary                                              |
| `recommendation` | Concrete recommendation                                  |

If the model does not return valid JSON, the API may respond with `risk_level: "unknown"` and the raw text in `recommendation`.

**Example with `curl`:**

```bash
curl -s -X POST "http://127.0.0.1:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"income": 5000, "expenses": 3200, "debt": 400}'
```

## Project layout

```
app/
  main.py              # FastAPI routes and error handling
  schemas.py           # Pydantic models (input / output)
  services/
    analyzer.py        # Cohere call and JSON parsing
```

The model configured in code is `command-r-08-2024`; you can change it in `app/services/analyzer.py` based on what your Cohere account supports.

## Errors

- `422` responses: invalid body or values that fail schema validation.
- `500` responses: Cohere call failed, missing key, or unexpected error; details are usually in the error JSON `detail` field.
