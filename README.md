***Simple AI APIs - Anshika Mishra***

**How it works**
    ** Chat using OpenAI’s GPT model.
    ** Upload PDFs or text files, which are chunked, embedded using OpenAI embeddings, and stored in Qdrant vector DB.
    ** Ask questions about your uploaded document using RAG.

**Components**
    # Backend (FastAPI)
        ** /upload: Accepts PDF or TXT files, extracts and chunks text, creates embeddings, and stores them in Qdrant.
        ** /ask: Accepts a question, retrieves relevant chunks from Qdrant, and sends a prompt to OpenAI for an answer.
        ** /chat: A basic chat endpoint for general OpenAI-based interactions.

    # Frontend (React, Axios, MUI)
        ** File upload with Snackbar feedback.
        ** Input boxes for chat and document Q&A.
        ** Loading('Generating..') indicators during operations.

**Tech Stack**
    ** Frontend: React, MUI
    ** Backend: FastAPI, OpenAI API, Qdrant
    ** Vector DB: Qdrant (local)
    ** Embeddings: OpenAI text-embedding-3-small
    ** PDF Parsing: PyPDF
    ** Text Chunking: Custom utility function

**Setup Instructions**
    1. Clone the repo

    2. Install backend dependencies
        `pip install -r req.txt`
    
    3. Run Qdrant locally
        `docker run -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant`
    
    4. Start the FastAPI backend
        `uvicorn main:app --reload`
    
    5.Start the React frontend
        `npm install`
        `npm start`

