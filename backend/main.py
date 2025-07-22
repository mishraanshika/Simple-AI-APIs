from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chat import chat_endpoint
from upload import upload_router
from ask import router as ask_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_endpoint)
app.include_router(upload_router)
app.include_router(ask_router)
