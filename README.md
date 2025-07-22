# Simple AI APIs - Anshika Mishra

## How it Works

-   **Chat:** Chat using OpenAI’s GPT model.
-   **Document Q&A:** Upload PDF or text files. The system processes them by chunking the text, creating embeddings with OpenAI, and storing them in a Qdrant vector database.
-   **Ask Your Questions:** Ask questions about your uploaded document using RAG.

---

## Components

### Backend (FastAPI)

-   **`/upload`**: Accepts PDF or TXT files, extracts text, chunks it, creates vector embeddings, and stores them in the Qdrant database.
-   **`/ask`**: Accepts a question, retrieves relevant document chunks from Qdrant, and sends a prompt to OpenAI to generate an answer.
-   **`/chat`**: A basic chat endpoint for general, non-document-based interactions with the OpenAI API.

### Frontend (React, Axios, MUI)

-   **File Upload:** A simple interface for uploading files, with Snackbar feedback on success or failure.
-   **Input boxes:**  Input boxes for the general chat and the document Q&A functionality.
-   **Loading Indicators:** Displays a "Generating..." message to inform the user that a request is in progress.

---

## Tech Stack

| Category        | Technology                                 |
| --------------- | ------------------------------------------ |
| **Frontend**    | React, Material-UI (MUI)                   |
| **Backend**     | FastAPI, OpenAI API                        |
| **Vector DB**   | Qdrant (local)                             |
| **Embeddings**  | OpenAI `text-embedding-3-small`            |
| **PDF Parsing** | PyPDF                                      |
| **Text Chunking** | Custom utility function                    |

---

## Setup Instructions

### 1. Clone the Repo

### 2. Create an Environment File
Create a file named `.env` in the backend directory. Add your OpenAI API key to this file:
```ini
OPENAI_API_KEY="Your Open AI API KEY"
```

### 3. Install Backend Dependencies
Navigate to the backend directory and install the required Python packages.
```bash
pip install -r req.txt
```

### 4. Run Qdrant Locally
```bash
docker run -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

### 5. Start the FastAPI Backend
With the dependencies installed and Qdrant running, start the backend server.
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

### 6. Start the React Frontend
Open a new terminal, navigate to the frontend directory, and start the React app.
```bash
npm install
npm start
```
The application will be accessible at `http://localhost:3000`.