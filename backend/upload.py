from fastapi import APIRouter, HTTPException, UploadFile, File
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from utils import extract_text, embed_text, chunk_text
from uuid import uuid4

upload_router = APIRouter()

qdrant = QdrantClient(host="localhost", port=6333)
collection_name = "document_chunks"
qdrant.delete_collection(collection_name="document_chunks")  
qdrant.recreate_collection(
    collection_name="document_chunks",
    vectors_config={
        "default": VectorParams(size=1536, distance=Distance.COSINE)
    }
)

def create_collection_if_not_exists():
    if collection_name not in [c.name for c in qdrant.get_collections().collections]:
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
        

@upload_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Only .pdf or .txt allowed")

    try:
        
        qdrant.delete_collection(collection_name=collection_name)
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config={
                "default": VectorParams(size=1536, distance=Distance.COSINE)
            }
        )
        
        raw_text = extract_text(file)
        
        chunks = chunk_text(raw_text)
        points = []
        for idx, chunk in enumerate(chunks):
            vector = embed_text(chunk)
            point_id = str(uuid4())
            points.append(PointStruct(id=point_id, vector={"default": vector}, payload={"text": chunk}))

        qdrant.upsert(collection_name=collection_name, points=points)

        return {"message": f"Uploaded {len(chunks)} chunks."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
