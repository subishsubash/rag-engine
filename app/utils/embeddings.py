import os
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from app.config.config import settings

# Helps to embed the text chunks for faiss stores
def get_embedder(model_name: str = None):
    model = model_name or settings.EMBED_MODEL
    # If using HF token, set env var
    if settings.HF_API_KEY:
        os.environ['HF_TOKEN'] = settings.HF_API_KEY
    embedder = HuggingFaceEmbeddings(model_name=model)
    return embedder