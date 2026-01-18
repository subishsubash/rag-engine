from app.utils.faiss_store import load_faiss
from app.config.config import settings
import ollama
import logging
import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# Service Method helps to response to the /ask calls from the trained data.
def retrieve_and_answer(question: str, topk: int = 5, temperature: float = None):
    logging.info("Requested Question: %s",question)
    normalized_question = normalize_stacktrace(question)
    logging.info("Normalized Question: %s", normalized_question)
    db = load_faiss(settings.FAISS_PATH)
    docs = db.similarity_search(normalized_question, k=topk)

    context = "\n\n".join([d.page_content for d in docs])

    # Preparing prompt
    prompt = f"""
       You are a Java production support expert.

       Use ONLY the provided solution.
       Do NOT invent new fixes.

       If the solution is not clearly applicable, say:
       "I don't know."

        CONTEXT:
        {context}

        QUESTION:
        {normalized_question}

        ANSWER:
        """

    # This implementation work with ollama with llama3.2:3b installed with in machine, where the code running.
    if settings.LLM_MODEL_ID == 'OLLAMA':
        # connect with ollama.
        logging.info("Invoking LLM call to OLLAMA")
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

def normalize_stacktrace(text: str) -> str:
    lines = text.splitlines()
    cleaned = []

    for line in lines:
        line = line.strip()

        if "Exception" in line:
            cleaned.append(line.split(":")[0])

        elif line.startswith("at "):
            method = re.sub(r"\(.*?\)", "", line)
            cleaned.append(method)

        if len(cleaned) >= 4:
            break

    return "\n".join(cleaned)