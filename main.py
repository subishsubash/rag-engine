from fastapi import FastAPI
from app.controller.rag_controller import router as rag_router

app = FastAPI(title='RAG with Llama + BAAI + FAISS')
app.include_router(rag_router, prefix='')

@app.get('/')
async def root():
    return {'status': 'ok', 'message': 'RAG API'}