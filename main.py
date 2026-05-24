from fastapi import FastAPI, Request
from services.chat_service import generate_chat_response

app = FastAPI()


@app.get("/")
async def root(request: Request):
    ai_message = generate_chat_response("Hello, how are you?")
    return {"message": ai_message}




