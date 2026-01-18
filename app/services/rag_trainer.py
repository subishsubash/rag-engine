import os
import pickle
import pandas as pd

from typing import List
from app.utils.document_loader import load_input
from app.utils.splitter import split_text_into_chunks
from app.utils.faiss_store import create_faiss_from_texts
from app.config.config import settings
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
# Service method helps to store the train dataset into faiss database (vector DB)
def train_from_sources(sources: List[str], save_path: str = None, meta_path: str = None):
    texts = []
    metadatas = []

    for source in sources:
        if source.endswith(".xlsx"):
            logging.info("Recevied xlsx file to train")
            texts, metadatas = load_excel_errors(source)
        else:
            raw = load_input(source)
            chunks = split_text_into_chunks(raw)
            for i, c in enumerate(chunks):
                texts.append(c)
                metadatas.append({'source': source, 'chunk': i})

    # Save chunks in faiss
    create_faiss_from_texts(texts, metadatas, save_path=save_path)

    # Save metadata
    meta_path = meta_path or settings.META_PATH
    with open(meta_path, 'wb') as f:
        pickle.dump({'num_chunks': len(texts), 'sources': sources}, f)

    return {'status': 'Ok', 'num_chunks': len(texts), 'faiss_path': save_path or settings.FAISS_PATH, 'meta': meta_path}


def load_excel_errors(path):
    df = pd.read_excel(path)
    docs = []
    metas = []

    for _, row in df.iterrows():
        content = f"""
        ERROR:
        {row['Error']}

        SOLUTION:
        {row['Solution']}
        """
        docs.append(content)
        metas.append({"type": "java_exception"})

    return docs, metas