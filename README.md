
# RAG API with Ollama, BAAI Embeddings, FAISS & FastAPI

This project is a **Retrieval-Augmented Generation (RAG)** backend built using **FastAPI**, **FAISS**, **BAAI (HuggingFace) embeddings**, and **Ollama** for local LLM inference.  
It allows you to **train a vector database from documents or URLs** and **ask grounded questions** over the trained data.

---

## Architecture Overview

````
Client
│
├── /train , /train-with-file
│        ↓
│   Document Loader
│        ↓
│   Text Splitter
│        ↓
│   BAAI Embeddings
│        ↓
│   FAISS Vector Store (persisted)
│
└── /ask
↓
FAISS Similarity Search
↓
Context Construction
↓
Ollama (LLM)
↓
Answer
````

---

## Features

- Train RAG using:
  - PDF
  - DOC / DOCX
  - TXT files
  - Web URLs
- Local LLM inference using **Ollama**
- Config-driven model switching
- FAISS persistence for fast retrieval
- Grounded responses (answers strictly from context)
- Clean separation of concerns (controller / service / utils)

---

## Tech Stack

- Python
- FastAPI
- FAISS
- LangChain
- HuggingFace (BAAI embeddings)
- Ollama
- PyPDF2
- python-docx
- BeautifulSoup

---

## Project Structure

````
app/
├── config/
│   ├── app.env
│   ├── config.py
│   └── models.json
│
├── controller/
│   └── rag_controller.py
│
├── services/
│   ├── rag_trainer.py
│   └── rag_query.py
│
├── utils/
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── faiss_store.py
│   └── splitter.py
│
└── main.py

````

---

## Configuration

### app.env

```env
HF_API_KEY=
OPENAI_API_KEY=
FAISS_PATH=faiss_index
META_PATH=faiss_meta.pkl
MAX_CHUNK_SIZE=500
CHUNK_OVERLAP=100
TEMPERATURE=0.2
LLM_MODEL_ID=OLLAMA
````

### models.json

```json
{
  "llm_models": {
    "llama3": "llama3.2:3b",
    "mistral7b": "mistral-7b-Q4.gguf"
  },
  "embedding_models": {
    "bge": "BAAI/bge-small-en",
    "nomic": "nomic-embed-text"
  }
}
```

---

## Prerequisites

* Python 3.9+
* Ollama installed locally
* Required LLM pulled in Ollama

```bash
ollama pull llama3.2:3b
```

---

## Installation

```bash
git clone <repo-url>
cd <repo>

python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

---

## Running the Application

```bash
uvicorn app.main:app --reloa
```
Server will be available at:

```
http://localhost:8000
```

---

## API Endpoints

### Health Check

```
GET /
```

Response:

```json
{
  "status": "ok",
  "message": "RAG API"
}
```

---

### Train Using Paths or URLs

```
POST /train
```

Form Data:

```
sources: ["file.pdf", "https://example.com"]
```

---

### Train Using File Upload

```
POST /train-with-file
```

Form Data:

```
file: <pdf | txt | docx>
```

---

### Ask a Question

```
POST /ask
```

Request Body:

```json
{
  "question": "What is RAG?",
  "topk": 5
}
```

Response:

```json
{
  "answer": "Retrieval-Augmented Generation is ...",
  "chunks_used": 5
}
```

---

## How RAG Works Here

1. Documents are loaded and cleaned
2. Text is split into overlapping chunks
3. Chunks are embedded using BAAI embeddings
4. Embeddings are stored in FAISS
5. Query retrieves top-K similar chunks
6. LLM answers strictly from retrieved context

---

## Notes

* FAISS index is stored locally and reused across restarts
* Model switching is handled via `models.json` and `app.env`
* Designed for easy extension:

   * Multiple LLM providers
   * Reranking
   * Hybrid search
   * Streaming responses

---
