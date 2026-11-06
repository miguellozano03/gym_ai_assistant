# Gym AI Assistant Backend

A FastAPI backend that exposes a natural-language gym assistant. The assistant uses LangChain tools backed by in-memory repositories to answer questions about business information, opening hours, policies, trainers, products, and membership plans.

## Features

- Natural-language chat endpoint
- Repository-backed gym information
- LangChain agent with six information tools
- Provider-neutral configuration for OpenAI-compatible APIs
- BharatCode and Groq/Grok/OpenAI-compatible setup examples
- Pydantic request validation
- FastAPI dependency injection and test overrides

## Requirements

- Python 3.11 or newer
- An API key and model name from an OpenAI-compatible provider

## Installation

Create and activate a virtual environment:

```bash
cd ai_assistant/backend
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the example environment file:

```bash
cp .env.example .env
```

## Configuration

Configure the chat provider through environment variables:

```env
CHAT_PROVIDER=openai-compatible
CHAT_API_KEY=your-api-key
CHAT_MODEL=your-model-name
CHAT_API_BASE_URL=https://provider.example/v1
CHAT_TEMPERATURE=0
```

### BharatCode

```env
CHAT_PROVIDER=bharatcode
CHAT_API_KEY=bc_live_your_key_here
CHAT_MODEL=qwen-3.8-27b
CHAT_API_BASE_URL=https://bharatcode.ai/api/model/v1
CHAT_TEMPERATURE=0
```

The BharatCode adapter validates that the base URL ends with `/v1`.

### Groq

```env
CHAT_PROVIDER=openai-compatible
CHAT_API_KEY=your-groq-api-key
CHAT_MODEL=openai/gpt-oss-20b
CHAT_API_BASE_URL=https://api.groq.com/openai/v1
CHAT_TEMPERATURE=0
```

### Grok / xAI

```env
CHAT_PROVIDER=openai-compatible
CHAT_API_KEY=your-xai-api-key
CHAT_MODEL=grok-3-mini
CHAT_API_BASE_URL=https://api.x.ai/v1
CHAT_TEMPERATURE=0
```

Never commit a real API key. Keep `.env` out of version control.

## Running the API

Start the development server:

```bash
fastapi dev main.py
```

Alternative commands:

```bash
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

Interactive documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Chat Endpoint

### Request

```http
POST /chat
Content-Type: application/json
```

```json
{
  "message": "What are the opening hours on Monday?"
}
```

### Response

```json
{
  "reply": "The gym is open on Monday from 06:00 to 11:00 and from 15:00 to 20:00."
}
```

Example with `curl`:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What memberships do you offer?"}'
```

Blank messages are rejected with an HTTP 422 response.

## LangChain Tools

The agent can access the following repository-backed tools:

| Tool | Information returned |
| --- | --- |
| `get_business_information` | Gym name and description |
| `get_business_hours` | Opening hours by day |
| `get_gym_policies` | Gym rules and policies |
| `get_trainers` | Trainers, specialties, and availability |
| `get_products` | Products, prices, and availability |
| `get_membership_plans` | Membership names, prices, and durations |

The LLM is instructed to format retrieved information and not invent gym data. For the current development version, repositories store data in memory.

## Project Structure

```text
app/
├── application/       # Repository interfaces and use cases
├── core/              # Environment and application settings
├── domain/            # Business entities and domain validation
├── infrastructure/
│   ├── ai/            # LangChain agent, tools, prompt, and model adapters
│   └── persistence/   # In-memory repository implementations
└── presentation/
    ├── api/           # FastAPI routes, schemas, and dependencies
    └── main.py        # FastAPI application
main.py                # Uvicorn/FastAPI entry point
```

## Tests

Run the backend test suite:

```bash
pytest -q
```

The virtual environment can also be used directly:

```bash
./venv/bin/pytest -q
```

## Provider Selection

`app/presentation/api/dependencies.py` creates one `GymAssistantAgent` and caches it. The agent receives an injected LangChain chat model, so provider SDK selection does not affect the FastAPI route or the gym tools.

The agent requires no provider-specific code after model construction. Adding another OpenAI-compatible provider only requires updating `.env` with a valid API key, model, and base URL.
