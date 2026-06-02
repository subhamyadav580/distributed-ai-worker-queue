from fastapi import FastAPI, HTTPException
from schemas.request import SummarizeRequest
from tasks.summary_tasks import generate_summary_task
from config.celery_app import celery

app = FastAPI()


@app.post("/summarize")
async def create_summary(body: SummarizeRequest):
    task = generate_summary_task.delay(body.text)
    return {
        "message": "Task queued",
        "task_id": task.id
    }


@app.get("/task/{task_id}")
async def get_task_result(task_id: str):
    result = celery.AsyncResult(task_id)

    if result.state == "PENDING":
        return {"task_id": task_id, "status": "pending"}

    if result.state == "FAILURE":
        raise HTTPException(status_code=500, detail=str(result.result))

    if result.state == "SUCCESS":
        return {"task_id": task_id, "status": "success", "result": result.result}

    return {"task_id": task_id, "status": result.state}




