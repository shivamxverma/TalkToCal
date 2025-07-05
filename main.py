from fastapi import FastAPI
from pydantic import BaseModel
from agent import handle_message

app = FastAPI()

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatInput):
    reply = handle_message(req.message)
    return {"response": reply}
