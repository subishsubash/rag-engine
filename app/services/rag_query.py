from app.utils.faiss_store import load_faiss
from app.config.config import settings
import ollama

# Service Method helps to response to the /ask calls from the trained data.
def retrieve_and_answer(question: str, topk: int = 5, temperature: float = None):
    db = load_faiss(settings.FAISS_PATH)
    docs = db.similarity_search(question, k=topk)

    context = "\n\n".join([d.page_content for d in docs])

    # Preparing prompt
    prompt = f"""
    Use only the following context to answer. If unsure say I don't know.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """

    # This implementation work with ollama with llama3.2:3b installed with in machine, where the code running.
    if settings.LLM_MODEL_ID == 'OLLAMA':
        # connect with ollama.

        result = ollama.chat(
            model=settings.LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": temperature or settings.TEMPERATURE}
        )

    # Similar implementation can be done for other models.

    return {
        "answer": result["message"]["content"],
        "chunks_used": len(docs)
    }