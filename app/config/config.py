import os
import json
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read app.env file.
ENV_PATH = os.path.join(BASE_DIR, 'config', 'app.env')
load_dotenv(ENV_PATH)

# Read models.json which contains multiple models details (LLM and Embeding) and use them in settings Object.
MODELS_JSON = os.path.join(BASE_DIR, 'config', 'models.json')
with open(MODELS_JSON, encoding='utf-8') as f:
   MODEL_PATHS = json.load(f)

class Settings:
    # Fetch LLM and Emded models from models.json
    LLM_MODEL = MODEL_PATHS["llm_models"]["llama3"]
    EMBED_MODEL = MODEL_PATHS["embedding_models"]["bge"]
    
    #Get other properties from app.env file
    HF_API_KEY = os.getenv('HF_API_KEY', '')
    LLM_MODEL_ID = os.getenv('LLM_MODEL_ID','OLLAMA')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    FAISS_PATH = os.getenv('FAISS_PATH', 'faiss_index')
    META_PATH = os.getenv('META_PATH', 'faiss_meta.pkl')
    MAX_CHUNK_SIZE = int(os.getenv('MAX_CHUNK_SIZE', 500))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 100))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.2))

settings = Settings()