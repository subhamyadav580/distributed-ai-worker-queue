# AI Distributed Worker Queue

A distributed AI task processing system built with **FastAPI**, **Celery**, **RabbitMQ**, and **Redis**. Offloads AI inference (summarization, embeddings) to async background workers so the API stays non-blocking.

## Architecture

```
Client
  │
  ▼
FastAPI (main.py)
  │
  │── POST /summarize ──→ Celery Task ──→ RabbitMQ (broker)
  │                                             │
  │                                             ▼
  │                                       Celery Worker
  │                                             │
  │                                       LLM via LiteLLM
  │                                       (Ollama / OpenAI)
  │                                             │
  │                                       Redis (result backend)
  │
  └── GET /task/{task_id} ──→ Redis ──→ Return result
```

## Tech Stack

| Component | Role |
|---|---|
| **FastAPI** | HTTP API layer |
| **Celery** | Distributed task queue |
| **RabbitMQ** | Message broker (task routing) |
| **Redis** | Result backend (stores task output) |
| **LiteLLM** | Unified LLM interface |
| **Ollama / OpenAI** | AI model providers |

## Project Structure

```
ai-distributed-worker/
├── main.py                  # FastAPI app, API endpoints
├── config/
│   ├── celery_app.py        # Celery configuration
│   └── settings.py          # App settings via pydantic-settings
├── tasks/
│   └── summary_tasks.py     # Celery task definitions
├── services/
│   └── summary_service.py   # Business logic
├── ai_model/
│   └── llm.py               # LiteLLM wrapper
└── schemas/
    └── request.py           # Pydantic request models
```

## API Endpoints

### POST `/summarize`
Queue a summarization task.

**Request**
```json
{ "text": "Long text to summarize..." }
```

**Response**
```json
{ "message": "Task queued", "task_id": "abc-123" }
```

### GET `/task/{task_id}`
Poll for task result.

**Response**
```json
{ "task_id": "abc-123", "status": "success", "result": "Summary text..." }
```

Status values: `pending` | `success` | `failure`

## Configuration

Set via environment variables or `.env` file:

```env
# AI Provider
PROVIDER=ollama                          # ollama or openai
MODEL_NAME=llama3                        # model to use
OLLAMA_BASE_URL=http://localhost:11434   # Ollama server URL
OPENAI_API_KEY=                          # required if using openai

# Infrastructure
RABBITMQ_URL=pyamqp://guest:guest@localhost:5672//
REDIS_URL=redis://localhost:6379/0
```

## Getting Started

**1. Start infrastructure**
```bash
docker run -d --name rabbitmq -p 5672:5672 rabbitmq:3
docker run -d --name redis -p 6379:6379 redis:7
```

**2. Start Ollama (if using local models)**
```bash
ollama pull llama3
ollama serve
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Start the Celery worker**
```bash
celery -A config.celery_app.celery worker --loglevel=info -Q summary
```

**5. Start the FastAPI server**
```bash
uvicorn main:app --reload
```

**6. Test it**
```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Artificial intelligence is transforming industries worldwide..."}'

# Use the returned task_id to poll result
curl http://localhost:8000/task/<task_id>
```

## How it works

1. Client sends text to `POST /summarize`
2. FastAPI enqueues a Celery task — returns `task_id` immediately
3. RabbitMQ routes the task to the `summary` queue
4. Celery worker picks up the task and calls the LLM
5. Result is stored in Redis
6. Client polls `GET /task/{task_id}` to retrieve the result
