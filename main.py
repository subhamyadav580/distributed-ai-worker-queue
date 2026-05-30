from fastapi import FastAPI, Request
from services.summary_service import generate_ai_summary
from tasks.summary_tasks import generate_summary_task

app = FastAPI()


@app.get("/")
async def root(request: Request):
    task = generate_summary_task.delay("Hello, how are you?")
    return {
        "message": "Task queued",
        "task_id": task.id
    }




