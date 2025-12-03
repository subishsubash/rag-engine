import os
from langchain_community.vectorstores import FAISS
from app.utils.embeddings import get_embedder
from app.config.config import settings

# Create and Save faiss 
def create_faiss_from_texts(texts, metadatas, embed_model=None, save_path=None):
    embedder = get_embedder(embed_model)
    db = FAISS.from_texts(texts, embedding=embedder, metadatas=metadatas)
    path = save_path or settings.FAISS_PATH
    os.makedirs(path, exist_ok=True)
    db.save_local(path)
    return db

# Load faiss 
def load_faiss(save_path=None, embed_model=None):
    path = save_path or settings.FAISS_PATH
    embedder = get_embedder(embed_model)
    if not os.path.exists(path):
        raise FileNotFoundError(f"FAISS index not found at {path}")
    db = FAISS.load_local(path, embedder,  allow_dangerous_deserialization=True)
    return db