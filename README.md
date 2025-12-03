# RAG Engine (Llama + BAAI + FAISS + FastAPI)

## Setup
1. Create Python virtualenv and activate it.
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Place your local gguf/.bin Llama models under `models/` and set `app/config/models.json` accordingly.
4. Edit `app/config/app.env` to set EMBED_MODEL, HF_API_KEY, and other settings.

## Run
```bash
uvicorn app.main:app --reload
```

Open Swagger UI at http://127.0.0.1:8000/docs

## Endpoints
- POST /train — Accepts `sources` (list of file paths or URLs) to index.
- POST /upload — Accepts single-file upload (PDF/DOCX/TXT) and indexes it.
- POST /ask — Accepts `question` and returns an answer from LLM using retrieved context.
```

---

## What I did NOT include
- Binary Llama models (you must provide these in `models/`)
- Confluence authentication flow (basic URL fetching only)
- Production-grade error handling, logging, retries

---

## Next steps I can do for you
- Create a downloadable ZIP of this project
- Add CI / Dockerfile to containerize the app
- Add authentication for Confluence and file sources
- Add a web UI (Streamlit or React) + file uploader

---

Project generated. Open the canvas file to review and copy files into your local workspace. If you want, I can now:
- produce a ZIP file for download, or
- add Dockerfile + docker-compose, or
- add Streamlit UI.
