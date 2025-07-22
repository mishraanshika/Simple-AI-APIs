from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from qdrant_client import QdrantClient
from openai import OpenAI
from utils import embed_text
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant = QdrantClient(host="localhost", port=6333)
collection_name = "document_chunks"


class QueryRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        
        question_embedding = embed_text(request.question)

        search_result = qdrant.search(
            collection_name=collection_name,
            query_vector=("default", question_embedding),
            limit=5  
        )

        context = "\n\n".join(hit.payload["text"] for hit in search_result)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant answering questions based on the provided context."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {request.question}"}
            ]
        )

        answer = response.choices[0].message.content
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))