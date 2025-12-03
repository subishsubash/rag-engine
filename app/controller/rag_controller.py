from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import shutil
import os
from app.services.rag_trainer import train_from_sources
from app.services.rag_query import retrieve_and_answer
from app.config.config import settings

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    # Top K, number of retrieved chunks. It controls how much context the LLM gets.
    topk: Optional[int] = 5

# API to Train RAG model, The API accepts JSON format data. 
@router.post('/train')
async def train_endpoint(sources: List[str] = Form(...)):
    # sources may be provided as form-data key repeated or as JSON; FastAPI will parse
    try:
        result = train_from_sources(sources, save_path=settings.FAISS_PATH)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API to Train RAG model, The API accepts files - .pdf, .txt, .docx
@router.post('/train-with-file')
async def upload_file(file: UploadFile = File(...)):
    # Save uploaded file to temp and call training on it
    tmp_dir = 'tmp_uploads'
    os.makedirs(tmp_dir, exist_ok=True)
    file_path = os.path.join(tmp_dir, file.filename)
    with open(file_path, 'wb') as f:
        shutil.copyfileobj(file.file, f)
    try:
        result = train_from_sources([file_path], save_path=settings.FAISS_PATH)
        return result
    finally:
        try:
            os.remove(file_path)
        except Exception:
            pass

# API helps to query
@router.post('/ask')
async def ask_endpoint(req: AskRequest):
    try:
        resp = retrieve_and_answer(req.question, topk=req.topk)
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))