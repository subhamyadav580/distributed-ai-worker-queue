from fastapi import FastAPI, Request
from services.summary_service import generate_ai_summary, generate_chat_response

app = FastAPI()


@app.get("/")
async def root(request: Request):
    ai_message = generate_ai_summary("Hello, how are you?")
    return {"message": ai_message}




