from app.config.config import settings

# Method helps to split the text into chunks as per the chunks properties given in app.env
# This method can be improvised with availale libaries to do chunk process.
def split_text_into_chunks(text: str):
    chunk_size = settings.MAX_CHUNK_SIZE  # 500
    overlap = settings.CHUNK_OVERLAP      # 100

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # move back for overlap

    return chunks