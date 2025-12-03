import os
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from app.config.config import settings


def get_embedder(model_name: str = None):
    model = model_name or settings.EMBED_MODEL
    # If using HF token, set env var
    if settings.HF_API_KEY:
        os.environ['HF_TOKEN'] = settings.HF_API_KEY
    # Wrap SentenceTransformer
    embedder = HuggingFaceEmbeddings(model_name=model)
    return embedder