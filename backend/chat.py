from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

chat_endpoint = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@chat_endpoint.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": req.message}]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        print("ERROR in /chat:", e)
        raise HTTPException(status_code=500, detail=str(e))

