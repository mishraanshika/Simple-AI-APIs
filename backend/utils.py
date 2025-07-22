from openai import OpenAI
from typing import List
import PyPDF2
import tiktoken
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text(file) -> str:
    if file.filename.endswith(".pdf"):
        pdf = PyPDF2.PdfReader(file.file)
        return " ".join(page.extract_text() or "" for page in pdf.pages)
    else:
        return file.file.read().decode("utf-8")


def embed_text(text: str) -> List[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small", 
        input=[text]
    )
    return response.data[0].embedding


def chunk_text(text: str, chunk_size=500, overlap=50) -> List[str]:
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    tokens = encoding.encode(text)

    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk = encoding.decode(tokens[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks
